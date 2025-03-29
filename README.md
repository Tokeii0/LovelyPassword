# LovelyPassword - 密码管理器

一个使用PySide6开发的现代化密码管理应用。

## 最新功能

- **密码类型显示**：在密码表格中直观显示密码类型（RDP、SSH或普通密码）
- **MobaXterm集成**：支持通过MobaXterm连接SSH服务器，提供更好的终端体验
- **智能端口选择**：内置常见数据库和服务的端口选项，同时支持自定义端口
- **优化界面布局**：调整表格列宽，提供更合理的显示效果
- **自动加载密码**：窗口显示时自动加载密码列表，提升用户体验

## 项目结构
```
LovelyPassword/
├── src/
│   ├── __init__.py
│   ├── main.py              # 应用程序入口
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── password.py      # 密码数据模型
│   │   └── category.py      # 分类数据模型
│   ├── views/               # 视图组件
│   │   ├── __init__.py
│   │   ├── main_window.py   # 主窗口
│   │   ├── password_list.py # 密码列表视图
│   │   └── dialogs/         # 对话框
│   │       ├── __init__.py
│   │       ├── add_password.py
│   │       └── settings.py
│   ├── controllers/         # 控制器
│   │   ├── __init__.py
│   │   └── password_manager.py
│   └── utils/              # 工具函数
│       ├── __init__.py
│       ├── encryption.py    # 加密相关
│       ├── connection.py    # 连接工具
│       └── connection_templates.py # 连接模板
├── resources/              # 资源文件
│   ├── icons/
│   └── styles/
├── tests/                 # 测试文件
├── requirements.txt       # 依赖项
└── README.md             # 项目文档
```

## 核心功能模块

### 1. 数据模型
- Password: 密码条目模型
  - 标题
  - 用户名
  - 密码
  - 类别
  - 备注
  - 主机/IP地址
  - 端口
  - 连接类型
  - 额外参数
  - 创建时间
  - 最后修改时间

- Category: 分类模型
  - 名称
  - 描述
  - 图标

### 2. 加密模块
- 使用 Fernet (对称加密)
- 主密码哈希存储
- 密码数据加密存储

### 3. 用户界面
- 主窗口布局
  - 左侧分类导航
  - 右侧密码列表
  - 顶部搜索栏
  - 底部状态栏

- 密码列表视图
  - 表格显示（标题、用户名、密码、密码类型、连接信息）
  - 右键菜单
  - 密码强度指示器
  - 快速连接按钮

### 4. 连接功能
- RDP连接
- SSH连接（支持MobaXterm和paramiko）
- 数据库连接模板
- 常见端口预设
- 连接历史记录

## 技术栈
- Python 3.8+
- PySide6
- SQLite (数据存储)
- cryptography (加密)
- paramiko (SSH连接)
- MobaXterm (高级SSH终端)

## 安全特性
- 主密码验证
- 自动锁定
- 密码强度检查
- 加密存储
- 安全剪贴板处理

## 使用说明

### 首次使用
1. 运行应用程序，设置主密码
2. 创建密码分类
3. 添加您的第一个密码

### 连接到远程服务器
1. 选择带有连接信息的密码条目
2. 点击"连接"按钮
3. 对于SSH连接，将优先使用MobaXterm（如果已安装）
4. 对于RDP连接，将使用内置的RDP客户端

### 管理数据库连接
1. 添加新密码时选择"数据库连接"类型
2. 从下拉菜单选择常见的数据库端口，或输入自定义端口
3. 填写必要的连接信息