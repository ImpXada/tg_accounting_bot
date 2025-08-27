import json
from datetime import datetime
from config import Config, CATEGORIES
from openai import OpenAI, AzureOpenAI

class AIParsingService:
    def __init__(self):
        # 优先使用Azure OpenAI，如果没有配置则使用原版OpenAI
        if Config.AZURE_OPENAI_API_KEY and Config.AZURE_OPENAI_ENDPOINT:
            # 配置Azure OpenAI
            self.client = AzureOpenAI(
                api_key=Config.AZURE_OPENAI_API_KEY,
                api_version=Config.AZURE_OPENAI_API_VERSION,
                azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
            )
            self.deployment_name = Config.AZURE_OPENAI_DEPLOYMENT_NAME
            self.use_azure = True
        elif Config.OPENAI_API_KEY:
            # 使用原版OpenAI
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.use_azure = False
        else:
            raise ValueError("必须配置 AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT 或 OPENAI_API_KEY")
        self.prompt_template = """你是一个记账助手
要求：
0. [非常重要]所有<>中的内容，均为解释，你只需要理解里面的内容即可，不需要处理其逻辑，或者输出给用户
1. 对于传入的话语你要识别金额，货币类型(默认CNY)，主分类，子分类，记录类型(收入或支出)，名称，商家(默认为空)，日期(没传入自动获取当前时间)，时间(没传入自动获取当前时间)，描述(默认为空)，项目(默认为空)，账户(默认为钱包)

2. 主分类，前面带序号，命名时需要去掉序号，子分类跟随每个主分类后面
[极度重要]主分类子分类名称必须从下面的分类中选择，不能自定义！！！
01 收入 薪资、奖金、报销入账、理财利息/股息、礼金收入、其他
02 固定支出 房租、电话费网费、保险、订阅、水电费
03 餐饮 外卖、食材、零食饮料奶茶、酒、餐厅、水果
04 交通&住宿 公交交通、打车、火车高铁、共享单车、机票、住宿、共享充电宝
05 居家&日用 日用品、修理费、家具、家电、五金工具
06 医疗&健康 门急诊、牙齿健康、药品、医疗用品、住院、体检、健身
07 服饰&个护 服饰鞋帽、配饰、美妆&护肤品、美容美发
08 娱乐&社交 影音游戏、线下娱乐、聚餐/社交、礼品/人情
09 学习&工具 图书、课程、报名费、文具/办公用品、软件工具
10 签证费及其他必要费用 证件签证

3. [非常重要]输出为json格式
示例：
输入：今天(2025/08/24 19:34)买了一只信必可吸入剂
输出：{{
    "return_code": 0,
    "return_msg": "success",
    "account": "钱包",
    "currency": "CNY",
    "record_type": "支出",
    "main_category": "医疗&健康",
    "sub_category": "药品",
    "amount": -77.8,
    "name": "药品",
    "merchant": "",
    "date": "2025/08/25",
    "time": "19:34",
    "project": "",
    "description": "信必可"
}}
示例：
输入：信必可 77.8元 <这是只有物品名称和价格的简单输入，你应该根据物品名称来判断主分类和子分类，同时补全其他信息>
输出：{{
    "return_code": 0,
    "return_msg": "success",
    "account": "钱包",
    "currency": "CNY",
    "record_type": "支出",
    "main_category": "医疗&健康",
    "sub_category": "药品",
    "amount": -77.8,
    "name": "药品",
    "merchant": "",
    "date": "2025/08/25",
    "time": "19:34",
    "project": "",
    "description": "信必可"
}}
示例：
输入：信必可 77.8 <这是只有物品名称和价格但是没有单位的简单输入，你应该根据物品名称来判断主分类和子分类，同时补全其他信息，价格单位默认为CNY>
输出：{{
    "return_code": 0,
    "return_msg": "success",
    "account": "钱包",
    "currency": "CNY",
    "record_type": "支出",
    "main_category": "医疗&健康",
    "sub_category": "药品",
    "amount": -77.8,
    "name": "药品",
    "merchant": "",
    "date": "2025/08/25",
    "time": "19:34",
    "project": "",
    "description": "信必可"
}}
4. [非常重要]每一项必须有准确的主分类及其对应的子分类，如果无法分类，请输出失败原因，及改正建议
示例：今天买了只火箭
输出：
{{
    "return_code": -1,
    "return_msg": "无法识别主分类及子分类，请提供更具体的描述"
}}

5. [重要]金额必须为数字，且支出为负数，收入为正数
6. [重要]时间格式必须为yyyy/MM/dd及HH:mm
7. [非常重要]你不应该输出除了json的任何内容

当前时间：{current_time}
请解析以下文本：{user_input}"""

    def parse_text(self, user_input: str) -> dict:
        try:
            current_time = datetime.now().strftime("%Y/%m/%d %H:%M")
            
            prompt = self.prompt_template.format(
                current_time=current_time,
                user_input=user_input
            )
            
            if self.use_azure:
                # Azure OpenAI调用 - 使用新版本客户端库
                response = self.client.chat.completions.create(
                    model=self.deployment_name,  # 新版本Azure客户端使用model参数
                    messages=[
                        {"role": "system", "content": "你是一个专业的记账助手，严格按照要求输出JSON格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
            else:
                # 原版OpenAI调用 - 使用新版本客户端库
                response = self.client.chat.completions.create(
                    model="gpt-5-mini",
                    messages=[
                        {"role": "system", "content": "你是一个专业的记账助手，严格按照要求输出JSON格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
            
            result_text = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            try:
                result = json.loads(result_text)
                return self._validate_result(result)
            except json.JSONDecodeError:
                return {
                    "return_code": -1,
                    "return_msg": "AI返回格式错误，请重试"
                }
                
        except Exception as e:
            return {
                "return_code": -1,
                "return_msg": f"AI服务异常：{str(e)}"
            }
    
    def _validate_result(self, result: dict) -> dict:
        """验证AI返回结果的格式和内容"""
        if result.get("return_code") != 0:
            return result
            
        # 验证必需字段
        required_fields = [
            "account", "currency", "record_type", "main_category", 
            "sub_category", "amount", "name", "date", "time"
        ]
        
        for field in required_fields:
            if field not in result:
                return {
                    "return_code": -1,
                    "return_msg": f"缺少必需字段：{field}"
                }
        
        # 验证分类是否有效
        main_cat = result["main_category"]
        sub_cat = result["sub_category"]
        
        if main_cat not in CATEGORIES:
            return {
                "return_code": -1,
                "return_msg": f"无效的主分类：{main_cat}"
            }
            
        if sub_cat not in CATEGORIES[main_cat]:
            return {
                "return_code": -1,
                "return_msg": f"子分类'{sub_cat}'不属于主分类'{main_cat}'"
            }
        
        # 验证金额
        try:
            amount = float(result["amount"])
            if result["record_type"] == "支出" and amount > 0:
                result["amount"] = -amount
            elif result["record_type"] == "收入" and amount < 0:
                result["amount"] = abs(amount)
        except (ValueError, TypeError):
            return {
                "return_code": -1,
                "return_msg": "金额格式错误"
            }
        
        return result