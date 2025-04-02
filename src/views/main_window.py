from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTreeWidget, QTreeWidgetItem, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit,
                             QLabel, QStatusBar, QMessageBox, QToolBar, 
                             QSizePolicy, QHeaderView, QFrame, QMenu,
                             QFileDialog)
from PySide6.QtCore import Qt, QTimer, QSize, QPoint
from PySide6.QtGui import QIcon, QFont, QPixmap, QAction, QColor, QPalette, QLinearGradient, QCursor
import pyperclip
from src.controllers.password_manager import PasswordManager
from src.views.dialogs.add_password import AddPasswordDialog
from src.views.dialogs.settings import SettingsDialog
from src.views.dialogs.category import CategoryDialog
from src.models.category import Category
from src.utils.connection import ConnectionManager
from src.utils.import_export import ImportExportManager
from src.views.dialogs.password_detail import PasswordDetailDialog
from src.views.custom_titlebar import CustomTitleBar
import src.utils.resource_helper as resource_helper

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint)  # 无边框窗口
        self.password_manager = PasswordManager()
        self.password_list = []
        self.filtered_password_list = []
        self.is_filtered = False
        self.setup_ui()
        self.setup_connections()
        self.setup_auto_lock()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("LovelyPassword - 密码管理器")
        self.setMinimumSize(1200, 700)
        self.resize(1200, 700)  # 设置初始大小
        
        # 创建自定义标题栏
        self.title_bar = CustomTitleBar(self, "LovelyPassword - 密码管理器")
        self.title_bar.closeClicked.connect(self.close)
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.doubleClicked.connect(self.toggle_maximize)
        
        # 创建中央部件
        self.central_widget = QWidget()
        
        # 创建主布局（包含标题栏）
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.title_bar)
        container_layout.addWidget(self.central_widget)
        
        self.setCentralWidget(container)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        
        # 搜索栏
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("搜索:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键字搜索密码...")
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.main_layout.addLayout(self.search_layout)
        
        # 内容区域
        self.content_split_layout = QHBoxLayout()
        
        # 左侧分类树
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_label = QLabel("分类")
        self.sidebar_label.setStyleSheet("font-weight: bold; color: #666; margin: 5px 0;")
        self.sidebar_layout.addWidget(self.sidebar_label)
        
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderHidden(True)
        self.category_tree.setFixedWidth(200)
        self.category_tree.setRootIsDecorated(False)
        self.category_tree.setIndentation(10)
        
        self.sidebar_layout.addWidget(self.category_tree)
        
        # 添加类别按钮
        self.manage_category_button = QPushButton("管理类别")
        self.manage_category_button.clicked.connect(self.manage_categories)
        self.sidebar_layout.addWidget(self.manage_category_button)
        
        self.content_split_layout.addLayout(self.sidebar_layout)
        
        # 右侧密码列表区域
        self.right_layout = QVBoxLayout()
        
        # 密码表格标题
        self.passwords_label = QLabel("密码列表")
        self.passwords_label.setStyleSheet("font-weight: bold; color: #666; margin: 5px 0;")
        self.right_layout.addWidget(self.passwords_label)
        
        # 密码表格
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(6)
        self.password_table.setHorizontalHeaderLabels(["标题", "用户名", "密码", "密码类型", "连接信息", "操作"])
        self.password_table.horizontalHeader().setStretchLastSection(True)
        self.password_table.verticalHeader().setVisible(False)
        self.password_table.setAlternatingRowColors(True)
        self.password_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.password_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.right_layout.addWidget(self.password_table)
        
        # 添加密码按钮
        self.add_button = QPushButton("添加密码")
        self.add_button.setObjectName("primaryButton")
        self.add_button.setFixedHeight(36)
        self.add_button.setFixedWidth(120)
        self.add_button.clicked.connect(self.add_password)
        
        # 导入导出按钮
        self.import_export_button = QPushButton("导入/导出")
        self.import_export_button.setFixedHeight(36)
        self.import_export_button.setFixedWidth(100)
        self.import_export_button.clicked.connect(self.show_import_export_menu)
        
        # 设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.setFixedHeight(36)
        self.settings_button.setFixedWidth(80)
        self.settings_button.clicked.connect(self.show_settings)
        
        # 锁定按钮
        self.lock_button = QPushButton("锁定")
        self.lock_button.setFixedHeight(36)
        self.lock_button.setFixedWidth(80)
        self.lock_button.clicked.connect(self.lock_application)
        
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.settings_button)
        self.button_layout.addWidget(self.lock_button)
        self.button_layout.addWidget(self.import_export_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.add_button)
        self.right_layout.addLayout(self.button_layout)
        
        self.content_split_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.content_split_layout)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
    def setup_connections(self):
        """设置信号连接"""
        self.search_input.textChanged.connect(self.search_passwords)
        self.category_tree.itemClicked.connect(self.load_passwords)
        
        # 初始化加载类别
        self.load_categories()
        
    def setup_auto_lock(self):
        """设置自动锁定"""
        self.lock_timer = QTimer()
        self.lock_timer.setInterval(5 * 60 * 1000)  # 5分钟
        self.lock_timer.timeout.connect(self.lock_application)
        
    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec_()
        
    def search_passwords(self, query: str):
        """搜索密码"""
        if not query:
            # 如果搜索框为空，恢复显示当前类别的所有密码
            current_item = self.category_tree.currentItem()
            if current_item:
                self.load_passwords(current_item)
            return
            
        passwords = self.password_manager.search_passwords(query)
        self.filtered_password_list = passwords  # 保存筛选后的密码列表
        self.is_filtered = True  # 设置筛选状态
        self.update_password_table(passwords)
        
    def load_passwords(self, category_item: QTreeWidgetItem):
        """加载指定类别的密码"""
        category_id = category_item.data(0, Qt.UserRole)
        passwords = self.password_manager.get_passwords_by_category(category_id)
        self.password_list = passwords  # 保存当前加载的密码列表
        self.filtered_password_list = []  # 清空筛选列表
        self.is_filtered = False  # 重置筛选状态
        self.update_password_table(passwords)
        
    def update_password_table(self, passwords):
        """更新密码表格"""
        self.password_table.setRowCount(0)  # 清空表格
        self.password_table.setColumnCount(6)  # 增加一列用于显示密码类型
        self.password_table.setHorizontalHeaderLabels(["标题", "用户名", "密码", "密码类型", "连接信息", "操作"])
        
        # 调整列宽
        header = self.password_table.horizontalHeader()
        self.password_table.setColumnWidth(0, 150)  # 标题列固定宽度
        self.password_table.setColumnWidth(1, 120)  # 用户名列固定宽度
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # 密码列自适应内容
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 密码类型列自适应内容
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # 连接信息列自适应
        
        self.password_table.setRowCount(len(passwords))
        for row, password in enumerate(passwords):
            # 设置行高
            self.password_table.setRowHeight(row, 40)
            
            # 设置各列内容
            title_item = QTableWidgetItem(password.title)
            title_item.setData(Qt.UserRole, password.id)
            self.password_table.setItem(row, 0, title_item)
            
            username_item = QTableWidgetItem(password.username)
            self.password_table.setItem(row, 1, username_item)
            
            password_item = QTableWidgetItem("••••••••")
            password_item.setTextAlignment(Qt.AlignCenter)
            password_item.setFont(QFont("SF Pro Display", 12))
            self.password_table.setItem(row, 2, password_item)
            
            # 密码类型
            password_type = password.connection_type if password.connection_type else "普通密码"
            type_item = QTableWidgetItem(password_type)
            type_item.setTextAlignment(Qt.AlignCenter)
            self.password_table.setItem(row, 3, type_item)
            
            # 连接信息
            conn_info = ""
            if password.host:
                conn_info = f"{password.host}"
                if password.port:
                    conn_info += f":{password.port}"
            conn_info_item = QTableWidgetItem(conn_info)
            self.password_table.setItem(row, 4, conn_info_item)
            
            # 添加操作按钮
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(5)
            
            copy_btn = QPushButton("复制")
            copy_btn.setFixedSize(60, 30)
            copy_btn.clicked.connect(lambda checked=False, p=password: self.copy_password(p))
            actions_layout.addWidget(copy_btn)
            
            # 快速连接按钮
            if password.connection_type in ['RDP', 'SSH']:
                connect_btn = QPushButton("连接")
                connect_btn.setFixedSize(60, 30)
                connect_btn.clicked.connect(lambda checked=False, p=password: self.connect_to_service(p))
                actions_layout.addWidget(connect_btn)
            
            edit_btn = QPushButton("编辑")
            edit_btn.setFixedSize(60, 30)
            edit_btn.clicked.connect(lambda checked=False, p=password: self.edit_password(p))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("删除")
            delete_btn.setObjectName("dangerButton")
            delete_btn.setFixedSize(60, 30)
            delete_btn.clicked.connect(lambda checked=False, p=password: self.delete_password(p))
            actions_layout.addWidget(delete_btn)
            
            self.password_table.setCellWidget(row, 5, actions_widget)
        
        # 显示密码数量信息
        self.status_bar.showMessage(f"共 {len(passwords)} 个密码")
        
    def copy_password(self, password):
        """复制密码到剪贴板"""
        try:
            # 获取解密的密码
            decrypted_password = self.password_manager.get_password(password.id).decrypted_password
            # 复制到剪贴板
            pyperclip.copy(decrypted_password)
            self.status_bar.showMessage("密码已复制到剪贴板", 3000)
            
            # 设置自动清除剪贴板的定时器
            QTimer.singleShot(30000, lambda: pyperclip.copy(''))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"复制密码失败: {str(e)}")
        
    def edit_password(self, password):
        """编辑密码"""
        try:
            # 获取完整的密码对象，包括解密的密码
            full_password = self.password_manager.get_password(password.id)
            
            # 创建编辑对话框
            dialog = AddPasswordDialog(self, self.password_manager)
            
            # 设置对话框标题
            dialog.setWindowTitle("编辑密码")
            
            # 填充现有数据
            dialog.title_input.setText(full_password.title)
            dialog.username_input.setText(full_password.username)
            dialog.password_input.setText(full_password.decrypted_password)
            
            # 设置类别
            index = dialog.category_combo.findData(full_password.category_id)
            if index >= 0:
                dialog.category_combo.setCurrentIndex(index)
            
            # 设置备注
            if full_password.notes:
                dialog.notes_input.setText(full_password.notes)
            
            # 设置连接类型和连接参数
            if full_password.connection_type:
                index = dialog.conn_type_combo.findData(full_password.connection_type)
                if index >= 0:
                    dialog.conn_type_combo.setCurrentIndex(index)
                    dialog.update_connection_fields()  # 更新连接字段
                    
                    # 设置主机和端口
                    if full_password.host:
                        dialog.host_input.setText(full_password.host)
                    if full_password.port:
                        dialog.port_input.setValue(full_password.port)
                    if full_password.additional_params:
                        dialog.additional_params_input.setText(full_password.additional_params)
            
            # 修改保存按钮的处理函数，使用update_password替代add_password
            original_save_password = dialog.save_password
            
            def custom_save_password():
                """自定义保存函数，更新密码而非添加"""
                title = dialog.title_input.text().strip()
                username = dialog.username_input.text().strip()
                password_text = dialog.password_input.text()
                category_id = dialog.category_combo.currentData()
                notes = dialog.notes_input.toPlainText().strip()
                
                # 获取连接类型
                conn_type = dialog.conn_type_combo.currentData()
                
                if not title or not username or not password_text:
                    QMessageBox.warning(dialog, "错误", "请填写必填字段")
                    return
                
                # 如果选择了连接类型，检查主机和端口
                host = None
                port = None
                additional_params = None
                
                if conn_type:
                    host = dialog.host_input.text().strip()
                    port = dialog.port_input.value()
                    additional_params = dialog.additional_params_input.text().strip()
                    
                    if not host:
                        QMessageBox.warning(dialog, "错误", "请输入主机/IP地址")
                        return
                        
                    if port <= 0:
                        QMessageBox.warning(dialog, "错误", "请输入有效的端口号")
                        return
                
                try:
                    # 更新密码
                    self.password_manager.update_password(
                        password_id=full_password.id,
                        title=title,
                        username=username,
                        password=password_text,
                        category_id=category_id,
                        notes=notes,
                        host=host,
                        port=port,
                        connection_type=conn_type,
                        additional_params=additional_params
                    )
                    dialog.accept()
                except Exception as e:
                    QMessageBox.critical(dialog, "错误", f"更新密码失败: {str(e)}")
            
            # 替换保存函数
            dialog.save_password = custom_save_password
            
            # 显示对话框
            if dialog.exec_():
                # 重新加载密码列表
                self.load_passwords(self.category_tree.currentItem())
                self.status_bar.showMessage("密码已更新", 3000)
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"编辑密码失败: {str(e)}")
        
    def delete_password(self, password):
        """删除密码"""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除密码 '{password.title}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.password_manager.delete_password(password.id):
                self.status_bar.showMessage("密码已删除", 3000)
                self.load_passwords(self.category_tree.currentItem())
            else:
                QMessageBox.warning(self, "错误", "删除密码失败")
                
    def lock_application(self):
        """锁定应用程序"""
        # TODO: 实现应用程序锁定功能 

    def load_categories(self):
        """加载分类树"""
        self.category_tree.clear()
        
        # 添加"全部"节点
        all_item = QTreeWidgetItem(["全部"])
        all_item.setData(0, Qt.UserRole, -1)  # 使用-1表示"全部"
        self.category_tree.addTopLevelItem(all_item)
        
        # 加载数据库中的分类
        session = self.password_manager.Session()
        try:
            categories = session.query(Category).all()
            for category in categories:
                item = QTreeWidgetItem([category.name])
                item.setData(0, Qt.UserRole, category.id)
                self.category_tree.addTopLevelItem(item)
        finally:
            session.close()
        
        # 默认选中"全部"
        self.category_tree.setCurrentItem(all_item)
        
        # 只有当加密管理器已初始化时才加载密码
        if self.password_manager.encryption_manager and self.password_manager.encryption_manager.cipher_suite:
            self.load_passwords(all_item)
        
    def manage_categories(self):
        """管理分类"""
        dialog = CategoryDialog(self, self.password_manager)
        if dialog.exec_():
            # 重新加载分类
            self.load_categories()
            
    def add_password(self):
        """添加密码"""
        dialog = AddPasswordDialog(self, self.password_manager)
        if dialog.exec_():
            # 刷新显示
            self.load_passwords(self.category_tree.currentItem())

    def connect_to_service(self, password):
        """连接到服务"""
        try:
            if not password.host or not password.port:
                QMessageBox.warning(self, "错误", "缺少连接信息")
                return
                
            # 获取解密后的密码
            decrypted_password = self.password_manager.get_password(password.id).decrypted_password
            
            if password.connection_type == "RDP":
                ConnectionManager.connect_rdp(
                    host=password.host, 
                    username=password.username, 
                    password=decrypted_password, 
                    port=password.port
                )
                self.status_bar.showMessage(f"已启动RDP连接到 {password.host}:{password.port}", 3000)
                
            elif password.connection_type == "SSH":
                # SSH连接需要更多处理
                ssh = ConnectionManager.connect_ssh(
                    host=password.host, 
                    username=password.username, 
                    password=decrypted_password, 
                    port=password.port
                )
                
                if ssh:
                    self.status_bar.showMessage(f"已连接到SSH服务器 {password.host}:{password.port}", 3000)
                    # 这里可以添加更多SSH处理逻辑，如打开终端等
                    # 只有当返回的是SSH客户端对象时才关闭连接
                    if ssh is not True:  # 检查是否是布尔值True（表示MobaXterm连接）
                        ConnectionManager.close_ssh(ssh)
                else:
                    QMessageBox.warning(self, "错误", f"无法连接到SSH服务器 {password.host}:{password.port}")
            else:
                QMessageBox.information(self, "信息", f"不支持的连接类型: {password.connection_type}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"连接失败: {str(e)}")

    def show_clipboard_notification(self, message):
        """显示剪贴板通知"""
        notification = QLabel(message, self)
        notification.setAlignment(Qt.AlignCenter)
        notification.setStyleSheet("""
            background-color: #0063e1;
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)
        notification.setFixedSize(300, 50)
        
        # 居中显示
        notification.move(
            (self.width() - notification.width()) // 2,
            (self.height() - notification.height()) // 2
        )
        
        notification.show()
        
        # 3秒后隐藏
        QTimer.singleShot(3000, notification.deleteLater) 

    def toggle_maximize(self):
        """切换窗口最大化/还原状态"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def showEvent(self, event):
        """窗口显示事件处理"""
        super().showEvent(event)
        # 窗口显示时加载一次密码
        current_item = self.category_tree.currentItem()
        if current_item and self.password_manager.encryption_manager and self.password_manager.encryption_manager.cipher_suite:
            self.load_passwords(current_item)
            
    def show_import_export_menu(self):
        """显示导入导出菜单"""
        menu = QMenu(self)
        
        # 导出功能
        export_action = menu.addAction("导出密码到Excel")
        export_action.triggered.connect(self.export_passwords)
        
        # 导入功能
        import_action = menu.addAction("从Excel导入密码")
        import_action.triggered.connect(self.import_passwords)
        
        # 显示菜单
        menu.exec_(QCursor.pos())
    
    def export_passwords(self):
        """导出密码到Excel文件"""
        try:
            # 检查是否有密码可导出
            if not self.password_list and not self.filtered_password_list:
                QMessageBox.information(self, "提示", "没有可导出的密码")
                return
            
            # 选择保存文件的路径
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出密码", "", "Excel文件 (*.xlsx)"
            )
            
            if not file_path:
                return  # 用户取消了操作
                
            # 如果文件名没有.xlsx后缀，添加它
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            
            # 确定要导出的密码列表
            passwords_to_export = self.filtered_password_list if self.is_filtered else self.password_list
            
            # 执行导出
            success = ImportExportManager.export_to_xlsx(passwords_to_export, file_path)
            
            if success:
                QMessageBox.information(self, "成功", f"已成功导出 {len(passwords_to_export)} 个密码到 {file_path}")
            else:
                QMessageBox.warning(self, "失败", "导出密码失败")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出过程中发生错误: {str(e)}")
    
    def import_passwords(self):
        """从Excel文件导入密码"""
        try:
            # 选择要导入的文件
            file_path, _ = QFileDialog.getOpenFileName(
                self, "导入密码", "", "Excel文件 (*.xlsx)"
            )
            
            if not file_path:
                return  # 用户取消了操作
            
            # 确认导入
            reply = QMessageBox.question(
                self,
                "确认导入",
                "导入将添加新的密码记录，不会覆盖现有密码。确定要继续吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # 执行导入
            success_count, fail_count, error_message = ImportExportManager.import_from_xlsx(
                file_path, self.password_manager
            )
            
            # 显示导入结果
            if success_count > 0:
                # 重新加载密码列表
                current_item = self.category_tree.currentItem()
                if current_item:
                    self.load_passwords(current_item)
                
                result_message = f"导入完成:\n成功: {success_count} 条记录"
                if fail_count > 0:
                    result_message += f"\n失败: {fail_count} 条记录"
                    if error_message:
                        result_message += f"\n\n错误详情:\n{error_message}"
                
                # 根据是否有失败决定显示什么类型的消息框
                if fail_count > 0:
                    QMessageBox.warning(self, "导入结果", result_message)
                else:
                    QMessageBox.information(self, "导入成功", result_message)
            else:
                QMessageBox.critical(self, "导入失败", f"导入失败，没有成功导入任何记录。\n\n{error_message}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入过程中发生错误: {str(e)}")