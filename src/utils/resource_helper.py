import os
import sys

def get_resource_path(relative_path):
    """获取资源文件的绝对路径
    
    用于处理PyInstaller打包后的资源文件路径
    
    Args:
        relative_path: 相对于resources目录的路径
    
    Returns:
        资源文件的绝对路径
    """
    # 确定应用程序是否被打包
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的路径
        base_path = sys._MEIPASS
    else:
        # 开发环境路径
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 构建资源路径
    resource_path = os.path.join(base_path, 'resources', relative_path)
    
    return resource_path

def load_stylesheet(name):
    """加载样式表
    
    Args:
        name: 样式表名称，不包含扩展名和路径
    
    Returns:
        样式表内容
    """
    stylesheet_path = get_resource_path(f'styles/{name}.qss')
    
    try:
        with open(stylesheet_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"加载样式表出错: {e}")
        return ""

def get_icon_path(icon_name):
    """获取图标路径
    
    Args:
        icon_name: 图标名称，包含扩展名但不包含路径
    
    Returns:
        图标的绝对路径
    """
    return get_resource_path(f'icons/{icon_name}') 