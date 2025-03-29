import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.views.main_window import MainWindow
from src.views.dialogs.login import LoginDialog
import src.utils.resource_helper as resource_helper

# 全局过滤 TripleDES 警告
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning, 
                      message="TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES")

def main():
    """应用程序主入口"""
    app = QApplication(sys.argv)
    
    # 设置应用程序图标
    app.setWindowIcon(QIcon("resources/icons/app_icon.png"))
    
    # 使用系统原生风格
    
    # 加载并应用macOS风格样式表
    stylesheet = resource_helper.load_stylesheet("macos_style")
    app.setStyleSheet(stylesheet)
    
    # 先显示登录对话框
    login_dialog = LoginDialog()
    if login_dialog.exec():
        # 登录成功，显示主窗口
        window = MainWindow()
        # 传递加密管理器
        window.password_manager.encryption_manager = login_dialog.password_manager.encryption_manager
        window.show()
        
        sys.exit(app.exec())
    else:
        # 登录取消，退出应用
        sys.exit(0)

if __name__ == "__main__":
    main()