from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QCheckBox, QPushButton,
                             QMessageBox)
from PySide6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("设置")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 自动锁定设置
        lock_layout = QHBoxLayout()
        lock_label = QLabel("自动锁定时间(分钟):")
        self.lock_time = QSpinBox()
        self.lock_time.setRange(1, 60)
        self.lock_time.setValue(5)
        lock_layout.addWidget(lock_label)
        lock_layout.addWidget(self.lock_time)
        layout.addLayout(lock_layout)
        
        # 密码生成器设置
        generator_layout = QVBoxLayout()
        generator_label = QLabel("密码生成器设置")
        generator_layout.addWidget(generator_label)
        
        # 密码长度
        length_layout = QHBoxLayout()
        length_label = QLabel("默认密码长度:")
        self.password_length = QSpinBox()
        self.password_length.setRange(8, 32)
        self.password_length.setValue(16)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.password_length)
        generator_layout.addLayout(length_layout)
        
        # 密码选项
        self.use_uppercase = QCheckBox("使用大写字母")
        self.use_uppercase.setChecked(True)
        generator_layout.addWidget(self.use_uppercase)
        
        self.use_lowercase = QCheckBox("使用小写字母")
        self.use_lowercase.setChecked(True)
        generator_layout.addWidget(self.use_lowercase)
        
        self.use_numbers = QCheckBox("使用数字")
        self.use_numbers.setChecked(True)
        generator_layout.addWidget(self.use_numbers)
        
        self.use_special = QCheckBox("使用特殊字符")
        self.use_special.setChecked(True)
        generator_layout.addWidget(self.use_special)
        
        layout.addLayout(generator_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def load_settings(self):
        """加载设置"""
        # TODO: 从配置文件加载设置
        
    def save_settings(self):
        """保存设置"""
        settings = {
            'auto_lock_time': self.lock_time.value(),
            'password_length': self.password_length.value(),
            'use_uppercase': self.use_uppercase.isChecked(),
            'use_lowercase': self.use_lowercase.isChecked(),
            'use_numbers': self.use_numbers.isChecked(),
            'use_special': self.use_special.isChecked()
        }
        
        # TODO: 保存设置到配置文件
        
        QMessageBox.information(self, "成功", "设置已保存")
        self.accept() 