import paramiko
import subprocess
import os
import tempfile
from typing import Optional

class ConnectionManager:
    @staticmethod
    def connect_rdp(host: str, username: str, password: str, port: int = 3389, domain: str = "", additional_params: str = "") -> None:
        """连接到RDP服务器
        
        使用Windows内置的远程桌面客户端(mstsc.exe)连接到远程服务器。
        """
        # Windows上RDP连接的基本命令
        cmd = f'mstsc.exe /v:{host}'
        
        # 如果指定了非默认端口，添加端口号
        if port != 3389:
            cmd = f'mstsc.exe /v:{host}:{port}'
            
        # 创建临时的RDP文件以包含用户名等信息
        temp_dir = tempfile.gettempdir()
        rdp_file = os.path.join(temp_dir, f"{host}_{port}.rdp")
        
        with open(rdp_file, 'w') as f:
            # 基本连接设置
            f.write(f"full address:s:{host}:{port}\n")
            f.write(f"username:s:{username}\n")
            
            # 如果有域，添加域信息
            if domain:
                f.write(f"domain:s:{domain}\n")
                
            # 添加其他常用设置
            f.write("screen mode id:i:1\n")  # 在窗口中打开
            f.write("use multimon:i:0\n")    # 不使用多显示器
            f.write("desktopwidth:i:1280\n") # 默认宽度
            f.write("desktopheight:i:800\n") # 默认高度
            f.write("session bpp:i:32\n")    # 色彩深度
            f.write("winposstr:s:0,1,0,0,1280,800\n") # 窗口位置和大小
            f.write("compression:i:1\n")     # 使用压缩
            f.write("keyboardhook:i:2\n")    # 键盘钩子
            f.write("audiocapturemode:i:0\n") # 不捕获音频
            f.write("videoplaybackmode:i:1\n") # 视频播放模式
            f.write("connection type:i:7\n") # 连接类型 (7=AUTO)
            f.write("networkautodetect:i:1\n") # 自动检测网络
            f.write("bandwidthautodetect:i:1\n") # 自动检测带宽
            f.write("enableworkspacereconnect:i:0\n") # 禁用工作区重连
            f.write("disable wallpaper:i:0\n") # 不禁用壁纸
            f.write("allow font smoothing:i:1\n") # 允许字体平滑
            f.write("allow desktop composition:i:1\n") # 允许桌面组合
            f.write("redirectprinters:i:1\n") # 重定向打印机
            f.write("redirectcomports:i:0\n") # 不重定向串口
            f.write("redirectsmartcards:i:1\n") # 重定向智能卡
            f.write("redirectclipboard:i:1\n") # 重定向剪贴板
            f.write("redirectposdevices:i:0\n") # 不重定向POS设备
            f.write("autoreconnection enabled:i:1\n") # 启用自动重连
            f.write("authentication level:i:2\n") # 身份验证级别
            f.write("prompt for credentials:i:0\n") # 不提示凭据
            f.write("negotiate security layer:i:1\n") # 协商安全层
            f.write("remoteapplicationmode:i:0\n") # 非远程应用模式
            f.write("alternate shell:s:\n") # 无备用shell
            f.write("shell working directory:s:\n") # 无shell工作目录
            f.write("gatewayhostname:s:\n") # 无网关
            f.write("gatewayusagemethod:i:4\n") # 网关使用方法
            f.write("prompt for credentials on client:i:0\n") # 客户端不提示凭据
            
            # 添加额外的自定义参数
            if additional_params:
                for param in additional_params.split(';'):
                    if param.strip():
                        f.write(f"{param.strip()}\n")
        
        # 使用创建的RDP文件启动连接
        subprocess.Popen(f'mstsc.exe "{rdp_file}"', shell=True)
    
    @staticmethod
    def connect_ssh(host: str, username: str, password: str = None, port: int = 22, 
                   key_file: str = None, additional_params: str = None) -> Optional[paramiko.SSHClient]:
        """连接到SSH服务器
        
        支持两种连接方式：
        1. 使用MobaXterm进行SSH连接（默认）
        2. 使用paramiko库进行SSH连接，如果MobaXterm路径不存在
        
        当使用MobaXterm连接时，返回一个特殊值True表示连接已启动
        当使用paramiko连接时，返回SSHClient对象
        连接失败则返回None
        """
        # MobaXterm路径
        mobaxterm_path = r"C:\Program Files (x86)\Mobatek\MobaXterm\MobaXterm.exe"
        
        # 检查MobaXterm是否存在
        if os.path.exists(mobaxterm_path):
            try:
                # 构建MobaXterm命令行参数
                # 基本命令格式：MobaXterm.exe -newtab "ssh username@host -P port"
                ssh_command = f'ssh {username}@{host} -p {port}'
                
                # 如果提供了密钥文件
                if key_file and os.path.exists(key_file):
                    ssh_command += f' -i "{key_file}"'
                
                # 如果有额外参数
                if additional_params:
                    ssh_command += f' {additional_params}'
                
                # 启动MobaXterm
                subprocess.Popen(f'"{mobaxterm_path}" -newtab "{ssh_command}"', shell=True)
                
                # 返回特殊值True表示MobaXterm连接已启动
                return True
            except Exception as e:
                print(f"启动MobaXterm失败: {str(e)}")
                # 如果MobaXterm启动失败，尝试使用paramiko作为后备选项
        
        # 作为后备，使用paramiko库连接
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 准备连接参数
            connect_kwargs = {
                'hostname': host,
                'port': port,
                'username': username,
                'timeout': 10  # 超时设置
            }
            
            # 如果提供了密码
            if password:
                connect_kwargs['password'] = password
            
            # 如果提供了密钥文件
            if key_file and os.path.exists(key_file):
                key = paramiko.RSAKey.from_private_key_file(key_file)
                connect_kwargs['pkey'] = key
            
            # 建立连接
            ssh.connect(**connect_kwargs)
            
            return ssh
        except Exception as e:
            print(f"SSH连接失败: {str(e)}")
            return None
    
    @staticmethod
    def execute_ssh_command(ssh: paramiko.SSHClient, command: str) -> tuple:
        """执行SSH命令"""
        if not ssh:
            return ("", "SSH客户端未连接")
            
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            return ("", f"命令执行失败: {str(e)}")
    
    @staticmethod
    def close_ssh(ssh: paramiko.SSHClient) -> None:
        """关闭SSH连接"""
        if ssh:
            ssh.close() 