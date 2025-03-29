import os
import sqlite3
from src.models.category import Category
from src.models.password import Base, Password
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def recreate_database():
    """删除并重新创建数据库"""
    
    # 如果有应用程序正在使用数据库，需要首先关闭它
    print("请先关闭所有正在使用数据库的应用程序，然后按任意键继续...")
    input()
    
    # 尝试删除数据库文件
    try:
        if os.path.exists("passwords.db"):
            os.remove("passwords.db")
            print("已删除旧数据库文件")
    except Exception as e:
        print(f"删除数据库文件失败: {str(e)}")
        print("请手动关闭使用该文件的程序，然后重新运行此脚本")
        return
    
    # 创建新的数据库和表
    try:
        # 创建引擎和会话
        engine = create_engine("sqlite:///passwords.db")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # 创建所有表
        Base.metadata.create_all(engine)
        print("已创建数据库表")
        
        # 添加默认分类
        default_category = Category(name="默认", description="默认分类")
        session.add(default_category)
        session.commit()
        print("已创建默认分类")
        
        session.close()
        print("数据库重建完成！")
    except Exception as e:
        print(f"创建数据库失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_database() 