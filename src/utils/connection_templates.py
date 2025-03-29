class ConnectionTemplates:
    """预定义的连接模板"""
    
    @staticmethod
    def get_common_ports():
        """获取常见的端口列表"""
        return {
            # 数据库端口
            "MySQL": 3306,
            "PostgreSQL": 5432,
            "SQLServer": 1433,
            "Oracle": 1521,
            "MongoDB": 27017,
            "Redis": 6379,
            "Elasticsearch": 9200,
            "Cassandra": 9042,
            # 远程连接端口
            "SSH": 22,
            "RDP": 3389,
            "FTP": 21,
            "SFTP": 22,
            "Telnet": 23,
            # Web服务端口
            "HTTP": 80,
            "HTTPS": 443,
        }
    
    @staticmethod
    def get_templates():
        """获取所有模板列表"""
        common_ports = ConnectionTemplates.get_common_ports()
        
        return [
            {
                "name": "RDP连接",
                "connection_type": "RDP",
                "port": common_ports["RDP"],
                "fields": [
                    {"name": "host", "label": "主机/IP地址", "required": True},
                    {"name": "port", "label": "端口", "default": common_ports["RDP"], "required": True},
                    {"name": "username", "label": "用户名", "required": True},
                    {"name": "password", "label": "密码", "required": True},
                    {"name": "domain", "label": "域", "required": False},
                    {"name": "additional_params", "label": "其他参数", "required": False},
                ]
            },
            {
                "name": "SSH连接",
                "connection_type": "SSH",
                "port": common_ports["SSH"],
                "fields": [
                    {"name": "host", "label": "主机/IP地址", "required": True},
                    {"name": "port", "label": "端口", "default": common_ports["SSH"], "required": True},
                    {"name": "username", "label": "用户名", "required": True},
                    {"name": "password", "label": "密码", "required": True},
                    {"name": "key_file", "label": "密钥文件", "required": False},
                    {"name": "additional_params", "label": "其他参数", "required": False},
                ]
            },
            {
                "name": "数据库连接",
                "connection_type": "DATABASE",
                "port": common_ports["MySQL"],  # MySQL默认端口
                "fields": [
                    {"name": "host", "label": "主机/IP地址", "required": True},
                    {"name": "port", "label": "端口", "default": common_ports["MySQL"], "required": True},
                    {"name": "username", "label": "用户名", "required": True},
                    {"name": "password", "label": "密码", "required": True},
                    {"name": "database", "label": "数据库名", "required": False},
                    {"name": "db_type", "label": "数据库类型", "required": False},
                    {"name": "additional_params", "label": "其他参数", "required": False},
                ]
            },
            {
                "name": "FTP连接",
                "connection_type": "FTP",
                "port": common_ports["FTP"],
                "fields": [
                    {"name": "host", "label": "主机/IP地址", "required": True},
                    {"name": "port", "label": "端口", "default": common_ports["FTP"], "required": True},
                    {"name": "username", "label": "用户名", "required": True},
                    {"name": "password", "label": "密码", "required": True},
                    {"name": "additional_params", "label": "其他参数", "required": False},
                ]
            }
        ]
    
    @staticmethod
    def get_template(connection_type):
        """获取指定类型的模板"""
        templates = ConnectionTemplates.get_templates()
        for template in templates:
            if template["connection_type"] == connection_type:
                return template
        return None