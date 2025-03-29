from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QFormLayout, QMessageBox,
    QSpinBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class PasswordDetailDialog(QDialog):
    """密码详情对话框"""
    
    def __init__(self, parent=None, password=None):
        super().__init__(parent)
        self.password = password
        self.is_deleted = False
        self.is_updated = False
        
        self.setup_ui()
        self.load_password_data()
        
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("密码详情")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # 标题
        self.title_label = QLabel("标题:")
        self.title_value = QLabel()
        self.title_value.setFont(QFont("SF Pro Display", 12, QFont.Bold))
        form_layout.addRow(self.title_label, self.title_value)
        
        # 用户名
        self.username_label = QLabel("用户名:")
        self.username_value = QLabel()
        self.username_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        form_layout.addRow(self.username_label, self.username_value)
        
        # 密码
        self.password_label = QLabel("密码:")
        self.password_value = QLineEdit()
        self.password_value.setEchoMode(QLineEdit.Password)
        self.password_value.setReadOnly(True)
        self.toggle_password_btn = QPushButton("显示")
        self.toggle_password_btn.setFixedWidth(60)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_value)
        password_layout.addWidget(self.toggle_password_btn)
        form_layout.addRow(self.password_label, password_layout)
        
        # 复制密码按钮
        self.copy_password_btn = QPushButton("复制密码")
        self.copy_password_btn.clicked.connect(self.copy_password)
        self.copy_password_btn.setObjectName("primaryButton")
        
        # 复制用户名按钮
        self.copy_username_btn = QPushButton("复制用户名")
        self.copy_username_btn.clicked.connect(self.copy_username)
        
        # 类别
        self.category_label = QLabel("类别:")
        self.category_value = QLabel()
        form_layout.addRow(self.category_label, self.category_value)
        
        # 连接信息
        self.connection_label = QLabel("连接信息:")
        self.connection_value = QLabel()
        form_layout.addRow(self.connection_label, self.connection_value)
        
        # 添加时间
        self.created_at_label = QLabel("创建时间:")
        self.created_at_value = QLabel()
        form_layout.addRow(self.created_at_label, self.created_at_value)
        
        # 修改时间
        self.updated_at_label = QLabel("更新时间:")
        self.updated_at_value = QLabel()
        form_layout.addRow(self.updated_at_label, self.updated_at_value)
        
        # 备注
        self.notes_label = QLabel("备注:")
        self.notes_value = QTextEdit()
        self.notes_value.setReadOnly(True)
        self.notes_value.setMaximumHeight(100)
        form_layout.addRow(self.notes_label, self.notes_value)
        
        main_layout.addLayout(form_layout)
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # 复制按钮区域
        copy_buttons_layout = QHBoxLayout()
        copy_buttons_layout.addWidget(self.copy_username_btn)
        copy_buttons_layout.addWidget(self.copy_password_btn)
        buttons_layout.addLayout(copy_buttons_layout)
        
        buttons_layout.addStretch()
        
        # 编辑按钮
        self.edit_btn = QPushButton("编辑")
        self.edit_btn.clicked.connect(self.edit_password)
        buttons_layout.addWidget(self.edit_btn)
        
        # 删除按钮
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self.delete_password)
        buttons_layout.addWidget(self.delete_btn)
        
        # 关闭按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(buttons_layout)
        
    def load_password_data(self):
        """加载密码数据"""
        if not self.password:
            return
            
        self.title_value.setText(self.password.get('title', ''))
        self.username_value.setText(self.password.get('username', ''))
        self.password_value.setText(self.password.get('password', ''))
        
        category = self.password.get('category', '')
        self.category_value.setText(category if category else '无')
        
        # 连接信息
        conn_info = ""
        host = self.password.get('host', '')
        port = self.password.get('port', '')
        if host:
            conn_info = f"{host}"
            if port:
                conn_info += f":{port}"
        self.connection_value.setText(conn_info if conn_info else '无')
        
        # 时间信息
        self.created_at_value.setText(self.password.get('created_at', ''))
        self.updated_at_value.setText(self.password.get('updated_at', ''))
        
        # 备注
        notes = self.password.get('notes', '')
        self.notes_value.setText(notes if notes else '无')
        
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.password_value.echoMode() == QLineEdit.Password:
            self.password_value.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("隐藏")
        else:
            self.password_value.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("显示")
    
    def copy_password(self):
        """复制密码到剪贴板"""
        import pyperclip
        pyperclip.copy(self.password_value.text())
        
        # 显示通知
        QMessageBox.information(self, "复制成功", "密码已复制到剪贴板")
    
    def copy_username(self):
        """复制用户名到剪贴板"""
        import pyperclip
        pyperclip.copy(self.username_value.text())
        
        # 显示通知
        QMessageBox.information(self, "复制成功", "用户名已复制到剪贴板")
    
    def edit_password(self):
        """编辑密码"""
        # 这里只是标记密码已更新，实际编辑功能会在主窗口实现
        QMessageBox.information(self, "编辑", "请在主窗口实现编辑功能")
        self.is_updated = True
        self.accept()
    
    def delete_password(self):
        """删除密码"""
        # 确认对话框
        reply = QMessageBox.question(
            self, "确认删除", 
            "确定要删除这个密码吗？此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 这里只是标记密码已删除，实际删除功能会在主窗口实现
            self.is_deleted = True
            self.accept() 