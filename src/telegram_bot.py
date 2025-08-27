import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from accounting_service import accounting_service

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """发送欢迎消息"""
        welcome_text = """
🤖 AI记账机器人

直接发送消息描述你的消费：
• "今天买了一杯奶茶15元"
• "昨天吃了火锅花了120"
• "本月工资到账8000"
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """帮助命令"""
        await self.start(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理普通消息"""
        user_text = update.message.text
        user_id = update.effective_user.id
        username = update.effective_user.username or "未知用户"
        
        logger.info(f"收到用户 {username} (ID: {user_id}) 的消息: {user_text}")
        
        # 显示处理中消息
        processing_msg = await update.message.reply_text("🤔 正在解析...")
        
        try:
            # 直接调用记账服务
            result = accounting_service.parse_and_save(user_text)
            
            if result['return_code'] == 0:
                # 解析成功
                data = result['data']
                success_text = f"""✅ 记录成功
金额: {data['amount']} {data['currency']}
分类: {data['main_category']} → {data['sub_category']}"""
                await processing_msg.edit_text(success_text)
            else:
                # 解析或存储失败
                error_text = f"❌ {result['return_msg']}"
                await processing_msg.edit_text(error_text)
                
        except Exception as e:
            logger.error(f"处理消息时出错: {e}")
            await processing_msg.edit_text("❌ 处理消息时出错，请稍后重试")
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """全局错误处理"""
        logger.error(f"更新 {update} 引起异常", exc_info=context.error)
    
    def run(self):
        """运行机器人"""
        if not self.token:
            logger.error("未设置 TELEGRAM_BOT_TOKEN")
            return
        
        # 创建应用
        application = Application.builder().token(self.token).build()
        
        # 添加处理器
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # 添加错误处理器
        application.add_error_handler(self.error_handler)
        
        # 运行机器人
        logger.info("Telegram机器人启动中...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()