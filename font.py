def list_system_fonts():
    """打印系统中所有可用的字体"""
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QFontDatabase
    import sys
    
    app = QApplication(sys.argv)
    font_db = QFontDatabase()
    font_families = font_db.families()
    
    print("系统可用字体列表:")
    for i, family in enumerate(font_families, 1):
        print(f"{i}. {family}")
    
    return font_families

if __name__ == "__main__":
    list_system_fonts()
