from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.password import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    icon = Column(String(50))  # 图标文件名
    
    # 关系
    passwords = relationship("Password", back_populates="category")
    
    def __repr__(self):
        return f"<Category(name='{self.name}')>" 