#!/usr/bin/env python3
"""
在线记账系统主入口
启动Telegram机器人
"""
from telegram_bot import TelegramBot

if __name__ == '__main__':
    print("🤖 启动AI记账机器人...")
    bot = TelegramBot()
    bot.run()