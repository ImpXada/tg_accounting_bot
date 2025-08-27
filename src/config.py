import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure OpenAI配置
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-35-turbo')
    
    # 兼容性配置（优先使用Azure）
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 其他配置
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///accounting.db')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

# 主分类和子分类映射
CATEGORIES = {
    "收入": ["薪资", "奖金", "报销入账", "理财利息/股息", "礼金收入", "其他"],
    "固定支出": ["房租", "电话费网费", "保险", "订阅", "水电费"],
    "餐饮": ["外卖", "食材", "零食饮料奶茶", "酒", "餐厅", "水果"],
    "交通&住宿": ["公交交通", "打车", "火车高铁", "共享单车", "机票", "住宿", "共享充电宝"],
    "居家&日用": ["日用品", "修理费", "家具", "家电", "五金工具"],
    "医疗&健康": ["门急诊", "牙齿健康", "药品", "医疗用品", "住院", "体检", "健身"],
    "服饰&个护": ["服饰鞋帽", "配饰", "美妆&护肤品", "美容美发"],
    "娱乐&社交": ["影音游戏", "线下娱乐", "聚餐/社交", "礼品/人情"],
    "学习&工具": ["图书", "课程", "报名费", "文具/办公用品", "软件工具"],
    "签证费及其他必要费用": ["证件签证"]
}