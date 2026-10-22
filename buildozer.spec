# 知学TV · 泉州台商投资区学生专属学习软件
# 由 build_apk.py 生成 —— Kivy 官方推荐 Buildozer 打包 [1]
[app]
title = 知学TV
package.name = zhixuetv
package.domain = com.zhixuetv
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt,md
source.exclude_dirs = __pycache__,build,.git,__pycache__
version = 1.0.0

# 入口
# 单文件项目：入口为 main.py 中的 ZhiXueTVApp
# （Kivy 应用不设 main.filename，由 python-for-android 加载 main.py）


# 依赖：kivy + pillow（均为纯 Python / 已有 recipe，无 C 扩展障碍 [3]）
requirements = python3==3.11.9,kivy==2.3.1,pillow==10.4.0

# 显示与方向：大屏 / 平板 / 手机横竖屏自适应
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

# 图标
icon.filename = data/icon.png
icon.adaptive_foreground.filename = data/adaptive-icon.png
icon.adaptive_background = #2E7CF6

# 启动画面
presplash.filename = data/icon.png
presplash_color = #2E7CF6

# Android 特性
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.features = android.software.leanback
android.manifest.placeholders = leanbackLauncher=true

[buildozer]
log_level = 2
warn_on_root = 1
