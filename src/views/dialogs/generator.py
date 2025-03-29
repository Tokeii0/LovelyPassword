from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QCheckBox, QPushButton,
                             QProgressBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pyperclip
from src.utils.password_generator import PasswordGenerator

class PasswordGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_generator = PasswordGenerator()
        self.setup_ui()
        self.generate_new_password()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("密码生成器")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 生成的密码显示
        password_layout = QHBoxLayout()
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        font = QFont("Courier New", 12)
        self.password_display.setFont(font)
        copy_button = QPushButton("复制")
        copy_button.clicked.connect(self.copy_password)
        password_layout.addWidget(self.password_display)
        password_layout.addWidget(copy_button)
        layout.addLayout(password_layout)
        
        # 密码强度
        strength_label = QLabel("密码强度:")
        layout.addWidget(strength_label)
        
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setTextVisible(True)
        layout.addWidget(self.strength_bar)
        
        # 设置
        settings_layout = QVBoxLayout()
        
        # 密码长度
        length_layout = QHBoxLayout()
        length_label = QLabel("密码长度:")
        self.length_spinner = QSpinBox()
        self.length_spinner.setRange(6, 64)
        self.length_spinner.setValue(16)
        self.length_spinner.valueChanged.connect(self.generate_new_password)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spinner)
        settings_layout.addLayout(length_layout)
        
        # 字符选项
        self.uppercase_check = QCheckBox("包含大写字母 (A-Z)")
        self.uppercase_check.setChecked(True)
        self.uppercase_check.stateChanged.connect(self.generate_new_password)
        settings_layout.addWidget(self.uppercase_check)
        
        self.lowercase_check = QCheckBox("包含小写字母 (a-z)")
        self.lowercase_check.setChecked(True)
        self.lowercase_check.stateChanged.connect(self.generate_new_password)
        settings_layout.addWidget(self.lowercase_check)
        
        self.numbers_check = QCheckBox("包含数字 (0-9)")
        self.numbers_check.setChecked(True)
        self.numbers_check.stateChanged.connect(self.generate_new_password)
        settings_layout.addWidget(self.numbers_check)
        
        self.special_check = QCheckBox("包含特殊字符 (!@#$%^&*)")
        self.special_check.setChecked(True)
        self.special_check.stateChanged.connect(self.generate_new_password)
        settings_layout.addWidget(self.special_check)
        
        layout.addLayout(settings_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        generate_button = QPushButton("生成新密码")
        generate_button.clicked.connect(self.generate_new_password)
        button_layout.addWidget(generate_button)
        
        use_button = QPushButton("使用此密码")
        use_button.clicked.connect(self.accept)
        button_layout.addWidget(use_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
    def generate_new_password(self):
        """生成新密码"""
        # 确保至少选择了一种字符类型
        if not (self.uppercase_check.isChecked() or 
                self.lowercase_check.isChecked() or 
                self.numbers_check.isChecked() or 
                self.special_check.isChecked()):
            QMessageBox.warning(self, "警告", "请至少选择一种字符类型")
            self.lowercase_check.setChecked(True)
            return
        
        # 生成密码
        password = self.password_generator.generate_password(
            length=self.length_spinner.value(),
            use_uppercase=self.uppercase_check.isChecked(),
            use_lowercase=self.lowercase_check.isChecked(),
            use_numbers=self.numbers_check.isChecked(),
            use_special=self.special_check.isChecked()
        )
        
        # 显示密码
        self.password_display.setText(password)
        
        # 计算并显示密码强度
        strength = self.password_generator.check_password_strength(password)
        self.strength_bar.setValue(strength)
        
        # 根据强度设置颜色
        if strength < 40:
            self.strength_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        elif strength < 70:
            self.strength_bar.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")
        else:
            self.strength_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
    
    def copy_password(self):
        """复制密码到剪贴板"""
        pyperclip.copy(self.password_display.text())
    
    def get_password(self):
        """获取生成的密码"""
        return self.password_display.text() 