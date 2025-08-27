from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import Config

Base = declarative_base()

class AccountingRecord(Base):
    __tablename__ = 'accounting_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account = Column(String(50), nullable=False, default='钱包')
    currency = Column(String(10), nullable=False, default='CNY')
    record_type = Column(String(10), nullable=False)  # 收入 or 支出
    main_category = Column(String(50), nullable=False)
    sub_category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    name = Column(String(100), nullable=False)
    merchant = Column(String(100), default='')
    date = Column(String(20), nullable=False)  # yyyy/MM/dd
    time = Column(String(10), nullable=False)  # HH:mm
    project = Column(String(100), default='')
    description = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'account': self.account,
            'currency': self.currency,
            'record_type': self.record_type,
            'main_category': self.main_category,
            'sub_category': self.sub_category,
            'amount': self.amount,
            'name': self.name,
            'merchant': self.merchant,
            'date': self.date,
            'time': self.time,
            'project': self.project,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 数据库连接
engine = create_engine(Config.DATABASE_URL, echo=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)