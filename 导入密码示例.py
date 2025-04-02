"""
创建密码导入示例文件
"""
import pandas as pd

# 创建示例数据
data = [
    {
        "标题": "示例Gmail账号",
        "用户名": "example@gmail.com",
        "密码": "Gmailpassword123!",
        "分类ID": 1,
        "备注": "这是一个Gmail账号示例",
        "主机": "",
        "端口": "",
        "连接类型": "",
        "附加参数": ""
    },
    {
        "标题": "示例SSH服务器",
        "用户名": "admin",
        "密码": "Secure@Server2025",
        "分类ID": 1,
        "备注": "开发服务器SSH登录",
        "主机": "192.168.1.100",
        "端口": 22,
        "连接类型": "SSH",
        "附加参数": ""
    },
    {
        "标题": "示例数据库账号",
        "用户名": "dbadmin",
        "密码": "Database@2025",
        "分类ID": 1,
        "备注": "MySQL数据库登录信息",
        "主机": "db.example.com",
        "端口": 3306,
        "连接类型": "",
        "附加参数": "数据库名称: example_db"
    },
    {
        "标题": "示例远程桌面",
        "用户名": "administrator",
        "密码": "RemoteDesktop!2025",
        "分类ID": 1,
        "备注": "Windows服务器远程桌面",
        "主机": "192.168.1.200",
        "端口": 3389,
        "连接类型": "RDP",
        "附加参数": ""
    },
    {
        "标题": "示例网站账号",
        "用户名": "user123",
        "密码": "WebsiteLogin!456",
        "分类ID": 1,
        "备注": "某购物网站账号",
        "主机": "",
        "端口": "",
        "连接类型": "",
        "附加参数": ""
    }
]

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel文件
df.to_excel("密码导入示例.xlsx", index=False, engine='openpyxl')

print("密码导入示例文件已创建: 密码导入示例.xlsx")
