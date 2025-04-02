"""
字体助手模块 - 用于加载和设置高质量字体
"""
import os
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

def load_custom_fonts():
    """加载自定义字体"""
    # 获取资源目录中的字体路径
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fonts_dir = os.path.join(base_dir, "resources", "fonts")
    
    # 字体文件列表
    font_files = [
        "LXGWWenKai-Regular.ttf",
        "LXGWWenKai-Light.ttf",
        "LXGWWenKai-Medium.ttf"
    ]
    
    # 加载每个字体
    for font_file in font_files:
        font_path = os.path.join(fonts_dir, font_file)
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id < 0:
                print(f"无法加载字体: {font_file}")

def set_application_font():
    """设置应用程序默认字体"""
    # 加载自定义字体
    load_custom_fonts()
    
    # 获取字体系列名称
    font_families = QFontDatabase.families()
    
    # 优先使用思源字体，如果没有则使用系统默认字体
    preferred_fonts = ["LXGW WenKai", "Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei"]
    
    selected_font = None
    for font_name in preferred_fonts:
        for family in font_families:
            if font_name.lower() in family.lower():
                selected_font = family
                break
        if selected_font:
            break
    
    # 如果找到了合适的字体，设置为应用程序默认字体
    if selected_font:
        app_font = QFont(selected_font, 10)  # 10pt 大小
        QApplication.setFont(app_font)
        
        # 返回所选字体名称，用于调试
        return selected_font
    
    return None

def optimize_font_rendering():
    """优化字体渲染，减少锯齿"""
    # 获取应用程序实例
    app = QApplication.instance()
    if app:
        # 启用字体抗锯齿
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        
        # 设置字体渲染提示
        hint_style = QFont.PreferAntialias  # 优先使用抗锯齿
        default_font = app.font()
        default_font.setHintingPreference(QFont.PreferFullHinting)  # 完全微调
        default_font.setStyleStrategy(QFont.PreferAntialias)  # 优先抗锯齿
        app.setFont(default_font)
