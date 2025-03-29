from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
import os
from src.controllers.password_manager import PasswordManager
from src.utils.encryption import EncryptionManager
from src.views.custom_titlebar import CustomTitleBar
import json
import warnings


# 无边框登录对话框
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint)  # 无边框窗口
        self.password_manager = PasswordManager()
        self.encryption_manager = EncryptionManager()
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("LovelyPassword - 登录")
        self.setMinimumWidth(380)
        self.setMinimumHeight(250)  # 进一步减小窗口高度
        self.setFixedSize(380, 200)  # 固定窗口大小，增加高度以适应标题栏
        
        # 创建自定义标题栏
        self.title_bar = CustomTitleBar(self, "LovelyPassword - 登录")
        self.title_bar.closeClicked.connect(self.reject)
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        # 登录对话框不需要最大化按钮，隐藏它
        self.title_bar.maximize_button.hide()
        
        # 创建内容区域
        content_widget = QWidget()
        
        # 创建主布局（包含标题栏和内容）
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.title_bar)
        container_layout.addWidget(content_widget)
        
        # 内容布局
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # 添加提示标签
        info_label = QLabel("请输入主密码以访问您的密码库")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; margin-bottom: 3px;")
        layout.addWidget(info_label)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("主密码")
        self.password_input.setMinimumHeight(28)  
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dadada;
                border-radius: 4px;
                padding: 3px 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
            }
        """)
        layout.addWidget(self.password_input)
        
        # 按钮
        login_buttons_layout = QHBoxLayout()
        login_buttons_layout.setSpacing(10)  
        
        create_button = QPushButton("创建新密码库")
        create_button.setFixedHeight(28)  
        create_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #dadada;
                border-radius: 4px;
                background-color: #f5f5f5;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
            }
            QPushButton:pressed {
                background-color: #d8d8d8;
            }
        """)
        create_button.clicked.connect(self.create_new_vault)
        login_buttons_layout.addWidget(create_button)
        
        login_button = QPushButton("登录")
        login_button.setFixedHeight(28)  
        login_button.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 4px;
                background-color: #0078d7;
                color: white;
                font-weight: bold;
                padding: 3px 10px;
            }
            QPushButton:hover {
                background-color: #006cc1;
            }
            QPushButton:pressed {
                background-color: #005ba1;
            }
        """)
        login_button.clicked.connect(self.verify_password)
        login_buttons_layout.addWidget(login_button)
        
        layout.addLayout(login_buttons_layout)
        
        # 添加额外提示信息
        hint_label = QLabel("首次使用请创建新密码库")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet("color: #999; font-size: 9px; margin-top: 5px;")  
        layout.addWidget(hint_label)
        
        # 设置回车键触发登录
        self.password_input.returnPressed.connect(self.verify_password)
        
    def verify_password(self):
        """验证主密码"""
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "错误", "请输入主密码")
            return
        
        # 检查配置文件是否存在
        if not os.path.exists("config.json"):
            QMessageBox.warning(self, "错误", "密码库不存在")
            return
        
        # 读取配置文件
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            
            # 验证密码
            stored_key = config.get("key")
            salt = bytes.fromhex(config.get("salt"))
            
            key, _ = self.encryption_manager.generate_key_from_password(password, salt)
            
            if key.decode() == stored_key:
                # 初始化密码管理器
                self.password_manager.encryption_manager.initialize(key)
                self.accept()
            else:
                QMessageBox.warning(self, "错误", "主密码不正确")
                self.password_input.clear()
                self.password_input.setFocus()
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"验证密码失败: {str(e)}")
    
    def create_new_vault(self):
        """创建新的密码库"""
        # 检查是否已经存在密码库
        if os.path.exists("config.json"):
            reply = QMessageBox.question(
                self,
                "确认",
                "已存在密码库，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "错误", "请输入主密码")
            return
        
        try:
            # 生成密钥
            key, salt = self.encryption_manager.generate_key_from_password(password)
            
            # 保存配置
            config = {
                "key": key.decode(),
                "salt": salt.hex()
            }
            
            with open("config.json", "w") as f:
                json.dump(config, f)
            
            # 初始化密码管理器
            self.password_manager.encryption_manager.initialize(key)
            
            QMessageBox.information(self, "成功", "密码库创建成功")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建密码库失败: {str(e)}") 