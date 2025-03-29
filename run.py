#!/usr/bin/env python
"""
LovelyPassword 启动脚本
"""
import sys
import os
import warnings

# 在导入任何其他模块前设置环境变量，禁用 cryptography 的废弃警告
os.environ['CRYPTOGRAPHY_SUPPRESS_DEPRECATION_WARNINGS'] = '1'

# 完全忽略所有警告
warnings.filterwarnings("ignore")

from src.main import main

if __name__ == "__main__":
    main()