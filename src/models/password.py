from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    encrypted_password = Column(String(500), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    notes = Column(String(500))
    
    # 新增字段，用于存储连接信息
    host = Column(String(255))  # 主机/IP地址
    port = Column(Integer)      # 端口
    connection_type = Column(String(50))  # 连接类型（RDP、SSH等）
    additional_params = Column(String(500))  # 额外参数
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    category = relationship("Category", back_populates="passwords")
    
    def __repr__(self):
        return f"<Password(title='{self.title}', username='{self.username}')>" 