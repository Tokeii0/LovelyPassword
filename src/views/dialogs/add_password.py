from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QComboBox, QPushButton,
                             QMessageBox, QSpinBox, QGroupBox, QTabWidget,
                             QWidget, QFormLayout, QCheckBox)
from PySide6.QtCore import Qt
from src.controllers.password_manager import PasswordManager
from src.models.category import Category
from src.views.dialogs.generator import PasswordGeneratorDialog
from src.utils.connection_templates import ConnectionTemplates

class AddPasswordDialog(QDialog):
    def __init__(self, parent=None, password_manager: PasswordManager = None):
        super().__init__(parent)
        self.password_manager = password_manager
        self.templates = ConnectionTemplates.get_templates()
        self.setup_ui()
        self.load_categories()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("添加密码")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout(self)
        
        # 使用选项卡组织界面
        self.tab_widget = QTabWidget()
        
        # 基本信息选项卡
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        
        # 标题
        title_layout = QHBoxLayout()
        title_label = QLabel("标题:")
        self.title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        basic_layout.addLayout(title_layout)
        
        # 类别
        category_layout = QHBoxLayout()
        category_label = QLabel("类别:")
        self.category_combo = QComboBox()
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        basic_layout.addLayout(category_layout)
        
        # 连接类型
        conn_type_layout = QHBoxLayout()
        conn_type_label = QLabel("连接类型:")
        self.conn_type_combo = QComboBox()
        self.conn_type_combo.addItem("普通密码", "")
        for template in self.templates:
            self.conn_type_combo.addItem(template["name"], template["connection_type"])
        self.conn_type_combo.currentIndexChanged.connect(self.update_connection_fields)
        conn_type_layout.addWidget(conn_type_label)
        conn_type_layout.addWidget(self.conn_type_combo)
        basic_layout.addLayout(conn_type_layout)
        
        # 用户名密码组
        credentials_group = QGroupBox("登录凭据")
        credentials_layout = QFormLayout(credentials_group)
        
        # 用户名
        self.username_input = QLineEdit()
        credentials_layout.addRow("用户名:", self.username_input)
        
        # 密码
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        generate_button = QPushButton("生成")
        generate_button.clicked.connect(self.generate_password)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(generate_button)
        credentials_layout.addRow("密码:", password_layout)
        
        basic_layout.addWidget(credentials_group)
        
        # 备注
        notes_label = QLabel("备注:")
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        basic_layout.addWidget(notes_label)
        basic_layout.addWidget(self.notes_input)
        
        self.tab_widget.addTab(basic_tab, "基本信息")
        
        # 连接详情选项卡
        self.connection_tab = QWidget()
        self.connection_layout = QFormLayout(self.connection_tab)
        
        # 主机/IP地址
        self.host_input = QLineEdit()
        self.connection_layout.addRow("主机/IP地址:", self.host_input)
        
        # 端口 - 使用组合框和输入框的组合
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.port_combo.addItem("自定义", 0)
        # 添加常见端口
        common_ports = ConnectionTemplates.get_common_ports()
        for name, port in common_ports.items():
            self.port_combo.addItem(f"{name} ({port})", port)
        self.port_combo.currentIndexChanged.connect(self.update_port_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(0)
        
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.port_input)
        self.connection_layout.addRow("端口:", port_layout)
        
        # 额外参数
        self.additional_params_input = QLineEdit()
        self.connection_layout.addRow("其他参数:", self.additional_params_input)
        
        # 自定义字段容器
        self.custom_fields_container = QWidget()
        self.custom_fields_layout = QFormLayout(self.custom_fields_container)
        self.connection_layout.addRow(self.custom_fields_container)
        
        self.tab_widget.addTab(self.connection_tab, "连接详情")
        
        # 初始隐藏连接选项卡
        self.tab_widget.setTabVisible(1, False)
        
        layout.addWidget(self.tab_widget)
        
        # 按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        save_button.clicked.connect(self.save_password)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def update_port_input(self):
        """更新端口输入框值"""
        port = self.port_combo.currentData()
        if port > 0:  # 非自定义端口
            self.port_input.setValue(port)
            
    def update_connection_fields(self):
        """根据连接类型更新字段"""
        conn_type = self.conn_type_combo.currentData()
        
        if not conn_type:
            # 普通密码，隐藏连接选项卡
            self.tab_widget.setTabVisible(1, False)
            return
            
        # 显示连接选项卡
        self.tab_widget.setTabVisible(1, True)
        
        # 清除自定义字段
        for i in reversed(range(self.custom_fields_layout.count())):
            item = self.custom_fields_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # 获取选中的模板
        template = ConnectionTemplates.get_template(conn_type)
        if template:
            # 设置默认端口
            default_port = template.get("port", 0)
            
            # 查找并选择对应的端口
            found = False
            for i in range(self.port_combo.count()):
                if self.port_combo.itemData(i) == default_port:
                    self.port_combo.setCurrentIndex(i)
                    found = True
                    break
            
            # 如果没找到匹配的端口，设置为自定义并填入值
            if not found and default_port > 0:
                self.port_combo.setCurrentIndex(0)  # 自定义选项
                self.port_input.setValue(default_port)
            
            # 添加自定义字段
            for field in template["fields"]:
                if field["name"] in ["host", "port", "username", "password"]:
                    continue  # 这些字段已经有了
                    
                if field["name"] == "additional_params":
                    continue  # 额外参数已经有了
                    
                field_label = QLabel(field["label"])
                field_input = QLineEdit()
                if "default" in field:
                    field_input.setText(str(field["default"]))
                
                setattr(self, f"{field['name']}_input", field_input)
                self.custom_fields_layout.addRow(field_label, field_input)
        
    def load_categories(self):
        """加载类别列表"""
        self.category_combo.clear()
        
        session = self.password_manager.Session()
        try:
            categories = session.query(Category).all()
            if not categories:
                QMessageBox.warning(self, "警告", "没有可用的密码类别，请先创建类别")
                self.reject()
                return
                
            for category in categories:
                self.category_combo.addItem(category.name, category.id)
        finally:
            session.close()
        
    def generate_password(self):
        """打开密码生成器对话框"""
        dialog = PasswordGeneratorDialog(self)
        if dialog.exec_():
            self.password_input.setText(dialog.get_password())
    
    def save_password(self):
        """保存密码"""
        title = self.title_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        category_id = self.category_combo.currentData()
        notes = self.notes_input.toPlainText().strip()
        
        # 获取连接类型
        conn_type = self.conn_type_combo.currentData()
        
        if not title or not username or not password:
            QMessageBox.warning(self, "错误", "请填写必填字段")
            return
        
        # 如果选择了连接类型，检查主机和端口
        host = None
        port = None
        additional_params = None
        
        if conn_type:
            host = self.host_input.text().strip()
            
            # 获取端口 - 从下拉框或输入框
            selected_port = self.port_combo.currentData()
            if selected_port > 0:  # 预定义端口
                port = selected_port
            else:  # 自定义端口
                port = self.port_input.value()
            
            additional_params = self.additional_params_input.text().strip()
            
            if not host:
                QMessageBox.warning(self, "错误", "请输入主机/IP地址")
                return
                
            if port <= 0:
                QMessageBox.warning(self, "错误", "请输入有效的端口号")
                return
        
        try:
            self.password_manager.add_password(
                title=title,
                username=username,
                password=password,
                category_id=category_id,
                notes=notes,
                host=host,
                port=port,
                connection_type=conn_type,
                additional_params=additional_params
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存密码失败: {str(e)}") 