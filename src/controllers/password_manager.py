from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from src.models.password import Password, Base
from src.models.category import Category
from src.utils.encryption import EncryptionManager

class PasswordManager:
    def __init__(self, db_url: str = "sqlite:///passwords.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.encryption_manager = EncryptionManager()
        
        # 初始化数据库表
        Base.metadata.create_all(self.engine)
    
    def initialize(self, master_password: str):
        """初始化密码管理器"""
        key, salt = self.encryption_manager.generate_key_from_password(master_password)
        self.encryption_manager.initialize(key)
        return salt
    
    def add_password(self, title: str, username: str, password: str, 
                    category_id: int, notes: str = "", host: str = None,
                    port: int = None, connection_type: str = None,
                    additional_params: str = None) -> Password:
        """添加新密码"""
        session = self.Session()
        try:
            encrypted_password = self.encryption_manager.encrypt(password)
            new_password = Password(
                title=title,
                username=username,
                encrypted_password=encrypted_password,
                category_id=category_id,
                notes=notes,
                host=host,
                port=port,
                connection_type=connection_type,
                additional_params=additional_params
            )
            session.add(new_password)
            session.commit()
            return new_password
        finally:
            session.close()
    
    def get_password(self, password_id: int) -> Optional[Password]:
        """获取密码"""
        session = self.Session()
        try:
            password = session.query(Password).filter_by(id=password_id).first()
            if password:
                password.decrypted_password = self.encryption_manager.decrypt(password.encrypted_password)
            return password
        finally:
            session.close()
    
    def update_password(self, password_id: int, title: str = None, 
                       username: str = None, password: str = None,
                       category_id: int = None, notes: str = None,
                       host: str = None, port: int = None,
                       connection_type: str = None, additional_params: str = None) -> Optional[Password]:
        """更新密码"""
        session = self.Session()
        try:
            db_password = session.query(Password).filter_by(id=password_id).first()
            if not db_password:
                return None
            
            if title:
                db_password.title = title
            if username:
                db_password.username = username
            if password:
                db_password.encrypted_password = self.encryption_manager.encrypt(password)
            if category_id:
                db_password.category_id = category_id
            if notes is not None:
                db_password.notes = notes
            
            # 更新连接信息
            if host is not None:
                db_password.host = host
            if port is not None:
                db_password.port = port
            if connection_type is not None:
                db_password.connection_type = connection_type
            if additional_params is not None:
                db_password.additional_params = additional_params
            
            session.commit()
            return db_password
        finally:
            session.close()
    
    def delete_password(self, password_id: int) -> bool:
        """删除密码"""
        session = self.Session()
        try:
            password = session.query(Password).filter_by(id=password_id).first()
            if password:
                session.delete(password)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_passwords_by_category(self, category_id: int) -> List[Password]:
        """获取指定类别的所有密码"""
        session = self.Session()
        try:
            # 如果category_id为-1，表示"全部"类别，返回所有密码
            if category_id == -1:
                passwords = session.query(Password).all()
            else:
                passwords = session.query(Password).filter_by(category_id=category_id).all()
                
            for password in passwords:
                password.decrypted_password = self.encryption_manager.decrypt(password.encrypted_password)
            return passwords
        finally:
            session.close()
    
    def search_passwords(self, query: str) -> List[Password]:
        """搜索密码"""
        session = self.Session()
        try:
            passwords = session.query(Password).filter(
                (Password.title.ilike(f"%{query}%")) |
                (Password.username.ilike(f"%{query}%")) |
                (Password.notes.ilike(f"%{query}%"))
            ).all()
            for password in passwords:
                password.decrypted_password = self.encryption_manager.decrypt(password.encrypted_password)
            return passwords
        finally:
            session.close() 