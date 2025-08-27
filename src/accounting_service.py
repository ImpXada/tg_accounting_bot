from models import AccountingRecord, SessionLocal
from ai_service import AIParsingService


class AccountingService:
    """记账服务核心类"""
    
    def __init__(self):
        self.ai_service = AIParsingService()
    
    def parse_and_save(self, user_input: str) -> dict:
        """
        解析用户输入并保存到数据库
        
        Args:
            user_input: 用户的自然语言输入
            
        Returns:
            dict: 包含结果状态和数据的字典
        """
        try:
            # AI解析
            result = self.ai_service.parse_text(user_input)
            
            if result['return_code'] != 0:
                return result
            
            # 存储到数据库
            db = SessionLocal()
            try:
                record = AccountingRecord(
                    account=result.get('account', '钱包'),
                    currency=result.get('currency', 'CNY'),
                    record_type=result['record_type'],
                    main_category=result['main_category'],
                    sub_category=result['sub_category'],
                    amount=result['amount'],
                    name=result['name'],
                    merchant=result.get('merchant', ''),
                    date=result['date'],
                    time=result['time'],
                    project=result.get('project', ''),
                    description=result.get('description', '')
                )
                
                db.add(record)
                db.commit()
                db.refresh(record)
                
                return {
                    "return_code": 0,
                    "return_msg": "记录成功",
                    "record_id": record.id,
                    "data": result
                }
                
            except Exception as e:
                db.rollback()
                return {
                    "return_code": -1,
                    "return_msg": f"数据库错误：{str(e)}"
                }
            finally:
                db.close()
                
        except Exception as e:
            return {
                "return_code": -1,
                "return_msg": f"服务器错误：{str(e)}"
            }
    
    def health_check(self) -> dict:
        """健康检查"""
        try:
            # 检查AI服务
            ai_status = "正常" if self.ai_service else "异常"
            
            # 检查数据库连接
            db = SessionLocal()
            try:
                db.execute("SELECT 1")
                db_status = "正常"
            except:
                db_status = "异常"
            finally:
                db.close()
            
            return {
                "return_code": 0,
                "return_msg": "服务正常",
                "service": "OnlineAccounting",
                "ai_service": ai_status,
                "database": db_status
            }
        except Exception as e:
            return {
                "return_code": -1,
                "return_msg": f"健康检查失败：{str(e)}"
            }


# 创建全局实例
accounting_service = AccountingService()