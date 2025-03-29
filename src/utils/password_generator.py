import random
import string

class PasswordGenerator:
    @staticmethod
    def generate_password(length=16, use_uppercase=True, use_lowercase=True, 
                         use_numbers=True, use_special=True):
        """生成随机密码"""
        chars = ''
        
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation
            
        if not chars:
            # 如果没有选择任何字符集，默认使用小写字母
            chars = string.ascii_lowercase
            
        # 确保每种字符类型至少有一个
        password = []
        if use_uppercase:
            password.append(random.choice(string.ascii_uppercase))
        if use_lowercase:
            password.append(random.choice(string.ascii_lowercase))
        if use_numbers:
            password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice(string.punctuation))
            
        # 填充剩余长度
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(random.choice(chars) for _ in range(remaining_length))
            
        # 打乱顺序
        random.shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def check_password_strength(password):
        """检查密码强度，返回0-100的得分"""
        score = 0
        
        # 长度得分 (最多40分)
        length = len(password)
        if length >= 16:
            score += 40
        elif length >= 12:
            score += 30
        elif length >= 8:
            score += 20
        elif length >= 6:
            score += 10
            
        # 复杂性得分 (最多60分)
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        # 每种字符类型15分
        if has_uppercase:
            score += 15
        if has_lowercase:
            score += 15
        if has_numbers:
            score += 15
        if has_special:
            score += 15
            
        return score 