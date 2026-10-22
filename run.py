#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知学 TV 启动脚本"""
import os
import sys

# 确保以脚本所在目录为工作目录，方便加载 progress.json
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
sys.path.insert(0, BASE)

from main import ZhiXueTVApp

if __name__ == "__main__":
    ZhiXueTVApp().run()
