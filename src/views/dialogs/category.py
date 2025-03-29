from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QListWidget,
                             QListWidgetItem)
from PySide6.QtCore import Qt
from src.controllers.password_manager import PasswordManager
from src.models.category import Category
from sqlalchemy.orm import Session

class CategoryDialog(QDialog):
    def __init__(self, parent=None, password_manager=None):
        super().__init__(parent)
        self.password_manager = password_manager
        self.setup_ui()
        self.load_categories()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("管理类别")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 类别列表
        self.category_list = QListWidget()
        layout.addWidget(self.category_list)
        
        # 添加类别
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("类别名称")
        add_button = QPushButton("添加")
        add_button.clicked.connect(self.add_category)
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)
        
        # 删除按钮
        delete_button = QPushButton("删除所选")
        delete_button.clicked.connect(self.delete_category)
        layout.addWidget(delete_button)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
    def load_categories(self):
        """加载类别列表"""
        self.category_list.clear()
        
        session = self.password_manager.Session()
        try:
            categories = session.query(Category).all()
            for category in categories:
                item = QListWidgetItem(category.name)
                item.setData(Qt.UserRole, category.id)
                self.category_list.addItem(item)
        finally:
            session.close()
            
    def add_category(self):
        """添加新类别"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "错误", "请输入类别名称")
            return
            
        session = self.password_manager.Session()
        try:
            # 检查是否已存在同名类别
            existing = session.query(Category).filter_by(name=name).first()
            if existing:
                QMessageBox.warning(self, "错误", "已存在同名类别")
                return
                
            # 添加新类别
            category = Category(name=name)
            session.add(category)
            session.commit()
            
            # 更新列表
            item = QListWidgetItem(category.name)
            item.setData(Qt.UserRole, category.id)
            self.category_list.addItem(item)
            
            # 清空输入框
            self.name_input.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"添加类别失败: {str(e)}")
        finally:
            session.close()
            
    def delete_category(self):
        """删除所选类别"""
        current_item = self.category_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "错误", "请选择要删除的类别")
            return
            
        category_id = current_item.data(Qt.UserRole)
        category_name = current_item.text()
        
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除类别 '{category_name}' 吗？\n这将同时删除该类别下的所有密码记录！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
            
        session = self.password_manager.Session()
        try:
            # 查找类别
            category = session.query(Category).filter_by(id=category_id).first()
            if not category:
                QMessageBox.warning(self, "错误", "类别不存在")
                return
                
            # 删除类别
            session.delete(category)
            session.commit()
            
            # 更新列表
            self.category_list.takeItem(self.category_list.row(current_item))
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除类别失败: {str(e)}")
        finally:
            session.close() 