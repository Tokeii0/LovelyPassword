"""
导入导出工具模块 - 用于导入导出密码数据
"""
import os
import pandas as pd
from typing import List, Dict, Any
from src.models.password import Password
from src.controllers.password_manager import PasswordManager
from PySide6.QtWidgets import QMessageBox

class ImportExportManager:
    """密码导入导出管理器"""
    
    @staticmethod
    def export_to_xlsx(passwords: List[Password], file_path: str) -> bool:
        """
        导出密码到Excel文件
        
        Args:
            passwords: 密码列表
            file_path: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        try:
            # 准备导出数据
            data = []
            for password in passwords:
                data.append({
                    "标题": password.title,
                    "用户名": password.username,
                    "密码": password.decrypted_password,  # 已解密的密码
                    "分类ID": password.category_id,
                    "备注": password.notes or "",
                    "主机": password.host or "",
                    "端口": password.port or "",
                    "连接类型": password.connection_type or "",
                    "附加参数": password.additional_params or ""
                })
            
            # 创建DataFrame并导出
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            print(f"导出失败: {str(e)}")
            return False
    
    @staticmethod
    def import_from_xlsx(file_path: str, password_manager: PasswordManager) -> tuple:
        """
        从Excel文件导入密码
        
        Args:
            file_path: 导入文件路径
            password_manager: 密码管理器实例
            
        Returns:
            tuple: (成功导入数量, 失败导入数量, 错误信息)
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # 验证必要的列是否存在
            required_columns = ["标题", "用户名", "密码"]
            for col in required_columns:
                if col not in df.columns:
                    return 0, 0, f"导入文件缺少必要的列: {col}"
            
            # 开始导入
            success_count = 0
            fail_count = 0
            errors = []
            
            for _, row in df.iterrows():
                try:
                    # 提取数据
                    title = row.get("标题", "")
                    username = row.get("用户名", "")
                    password = row.get("密码", "")
                    category_id = row.get("分类ID", 1)  # 默认使用ID为1的分类
                    notes = row.get("备注", "")
                    host = row.get("主机", None)
                    
                    # 处理端口 - 确保是整数或None
                    port = row.get("端口", None)
                    if pd.isna(port):
                        port = None
                    else:
                        try:
                            port = int(port)
                        except:
                            port = None
                    
                    connection_type = row.get("连接类型", None)
                    additional_params = row.get("附加参数", None)
                    
                    # 添加密码
                    if title and username and password:
                        password_manager.add_password(
                            title=title,
                            username=username,
                            password=password,
                            category_id=category_id,
                            notes=notes,
                            host=host,
                            port=port,
                            connection_type=connection_type,
                            additional_params=additional_params
                        )
                        success_count += 1
                    else:
                        fail_count += 1
                        errors.append(f"行 {_ + 2}: 缺少必要字段(标题/用户名/密码)")
                except Exception as e:
                    fail_count += 1
                    errors.append(f"行 {_ + 2}: {str(e)}")
            
            error_message = "\n".join(errors[:10])  # 只显示前10个错误
            if len(errors) > 10:
                error_message += f"\n... 还有 {len(errors) - 10} 个错误未显示"
                
            return success_count, fail_count, error_message
        except Exception as e:
            return 0, 0, f"导入失败: {str(e)}"
