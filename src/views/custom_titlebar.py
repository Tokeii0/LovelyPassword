from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QIcon, QFont, QCursor

class CustomTitleBar(QWidget):
    """自定义 macOS 风格标题栏"""
    
    # 定义信号
    closeClicked = Signal()
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    doubleClicked = Signal()
    
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.parent = parent
        self.title = title
        self.is_pressed = False
        self.start_pos = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        self.setObjectName("titleBar")
        self.setFixedHeight(28)  # macOS 标题栏高度
        
        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)
        
        # macOS 风格按钮容器（左侧靠顶部）
        button_container = QWidget()
        button_container.setObjectName("macButtonContainer")
        button_container.setFixedWidth(70)
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(8)
        
        # 创建窗口控制按钮（红、黄、绿）
        self.close_button = QPushButton()
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(12, 12)
        self.close_button.setToolTip("关闭")
        self.close_button.clicked.connect(self.closeClicked.emit)
        
        self.minimize_button = QPushButton()
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.setFixedSize(12, 12)
        self.minimize_button.setToolTip("最小化")
        self.minimize_button.clicked.connect(self.minimizeClicked.emit)
        
        self.maximize_button = QPushButton()
        self.maximize_button.setObjectName("maximizeButton")
        self.maximize_button.setFixedSize(12, 12)
        self.maximize_button.setToolTip("最大化")
        self.maximize_button.clicked.connect(self.maximizeClicked.emit)
        
        # 添加按钮到布局
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.maximize_button)
        
        # 将按钮容器添加到主布局
        layout.addWidget(button_container)
        
        # 添加标题标签（居中）
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # 添加标题到布局
        layout.addWidget(self.title_label)
        
        # 添加一个空白区域保持对称
        spacer = QWidget()
        spacer.setFixedWidth(70)  # 与左侧按钮区域相同的宽度
        layout.addWidget(spacer)
        
        self.setLayout(layout)
        
    def set_title(self, title):
        """设置标题"""
        self.title = title
        self.title_label.setText(title)
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.start_pos = event.globalPosition().toPoint() - self.parent.pos()
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_pressed:
            if self.parent.isMaximized():
                # 如果窗口已最大化，则先恢复正常大小
                self.parent.showNormal()
                # 调整起始位置，使鼠标保持在相对位置
                ratio = event.position().x() / self.width()
                self.start_pos = QPoint(int(self.parent.width() * ratio), 0)
            
            # 移动窗口
            self.parent.move(event.globalPosition().toPoint() - self.start_pos)
        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.is_pressed = False
        super().mouseReleaseEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)
