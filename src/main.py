import sys
import os
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from src.views.main_window import MainWindow
from src.views.dialogs.login import LoginDialog
import src.utils.resource_helper as resource_helper
from src.utils.font_helper import set_application_font, optimize_font_rendering

# 全局过滤 TripleDES 警告
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning, 
                      message="TripleDES has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.TripleDES")

def main():
    # 在导入任何其他模块前设置环境变量，禁用 cryptography 的废弃警告
    os.environ['CRYPTOGRAPHY_SUPPRESS_DEPRECATION_WARNINGS'] = '1'
    
    # 禁用Qt的显示器接口警告消息
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'
    
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setApplicationName("LovelyPassword")
    app.setWindowIcon(QIcon("resources/icons/app_icon.png"))
    
    # 设置高DPI缩放
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    
    # 加载并设置高质量字体
    selected_font = set_application_font()
    if selected_font:
        print(f"使用字体: {selected_font}")
    
    # 优化字体渲染
    optimize_font_rendering()
    
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