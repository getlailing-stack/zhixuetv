"""知学TV · 一键准备 APK 打包工程。

本脚本不依赖 Android SDK / NDK，纯本地完成：
1. 生成 buildozer.spec（Kivy 官方推荐方式，见 [1]）
2. 生成应用图标（自适应图标 / 桌面图标 / 启动画面）
3. 生成 GitHub Actions 工作流（buildozer-action@v1，官方推荐 CI 方式 [2]）
4. 输出可直接照搬的本地打包命令

[1] https://kivy.org/doc/stable/guide/packaging-android.html
[2] https://github.com/kivy/buildozer
"""
import os
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
PKG = "com.zhixuetv.app"


def sh(text):
    print(text)


sh("=" * 64)
sh("知学TV · APK 打包工程生成器")
sh("=" * 64)

# ---------------- 图标 ----------------
ICON = ROOT / "data" / "icon.png"
ADAPTIVE = ROOT / "data" / "adaptive-icon.png"
PRIMARY = ROOT / "data" / "primary-color.txt"
os.makedirs(ROOT / "data", exist_ok=True)
PRIMARY.write_text("#2E7CF6\n", encoding="utf-8")
try:
    from PIL import Image, ImageDraw, ImageFont

    def font(sz):
        for p in [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc",
        ]:
            if os.path.exists(p):
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()

    def round_rect(d, box, r, fill):
        d.rounded_rectangle(box, radius=r, fill=fill)

    # 圆形应用图标 432x432
    s = 432
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    round_rect(d, [0, 0, s, s], 96, (46, 124, 246, 255))
    # 顶部 TV 屏框
    d.rounded_rectangle([86, 70, 346, 250], radius=26, fill=(255, 255, 255, 255))
    d.rounded_rectangle([110, 96, 322, 224], radius=14, fill=(46, 124, 246, 255))
    for i, c in enumerate([(255, 255, 255, 230), (120, 200, 255, 220), (60, 150, 255, 200)]):
        d.rounded_rectangle([132 + i * 46, 196, 164 + i * 46, 212], radius=6, fill=c)
    # TV 支架
    d.rounded_rectangle([186, 250, 246, 290], radius=8, fill=(255, 255, 255, 220))
    d.rounded_rectangle([96, 284, 336, 304], radius=10, fill=(255, 255, 255, 220))
    # 学段圆点
    for i, c in enumerate([(255, 196, 0, 255), (46, 204, 113, 255), (231, 76, 60, 255)]):
        cx, cy = 122 + i * 94, 340
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=c)
    img.save(ICON, "PNG")
    sh(f"✓ 应用图标 -> {ICON}")

    # 自适应图标 432，留安全边距（中心 66%）
    simg = Image.new("RGBA", (s, s), (46, 124, 246, 255))
    sd = ImageDraw.Draw(simg)
    for i, c in enumerate([(255, 255, 255, 240), (180, 220, 255, 220), (90, 170, 255, 220)]):
        sd.rounded_rectangle([158, 130 + i * 52, 274, 162 + i * 52], radius=16, fill=c)
    simg.save(ADAPTIVE, "PNG")
    sh(f"✓ 自适应图标 -> {ADAPTIVE}")
except Exception as e:
    sh(f"! 图标生成跳过（{e}），将使用纯色占位")

# ---------------- buildozer.spec ----------------
spec = f"""# 知学TV · 泉州台商投资区学生专属学习软件
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
main.filename = main
package.entry = main:ZhiXueTVApp

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
"""

(ROOT / "buildozer.spec").write_text(spec, encoding="utf-8")
sh("✓ buildozer.spec")

# ---------------- GitHub Actions ----------------
wf_dir = ROOT / ".github" / "workflows"
wf_dir.mkdir(parents=True, exist_ok=True)
wf = """name: Build 知学TV APK
on:
  push:
    branches: [main, master]
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build APK
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          workdir: .
          buildozer_version: stable
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: zhixuetv-apk
          path: ${{ steps.buildozer.outputs.filename }}
"""
(wf_dir / "build-apk.yml").write_text(wf, encoding="utf-8")
sh("✓ GitHub Actions 工作流 .github/workflows/build-apk.yml")

# ---------------- 本地打包脚本 ----------------
sh_script = """#!/usr/bin/env bash
# 知学TV 本地 APK 打包（一键脚本）
# 需要 Linux / macOS / WSL2 + Python 3.8+
set -e
echo "==> [1/4] 安装系统依赖（Ubuntu/Debian）"
sudo apt-get update -qq
sudo apt-get install -y -qq git zip unzip openjdk-17-jdk python3-pip \\
  python3-venv autoconf libtool pkg-config zlib1g-dev libffi-dev \\
  libssl-dev cmake 2>/dev/null || echo "（非 Debian 系请自行安装对应依赖）"

echo "==> [2/4] 建立虚拟环境"
python3 -m venv .venv
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q buildozer cython==0.29.34

echo "==> [3/4] 初始化 buildozer（如已有 spec 会跳过）"
buildozer init >/dev/null 2>&1 || true

echo "==> [4/4] 开始构建 Debug APK（首次约 15-30 分钟，会下载 SDK/NDK）"
buildozer -v android debug
echo ""
echo "✅ APK 已生成，路径："
ls -lh bin/*.apk 2>/dev/null || true
"""
(ROOT / "build_apk.sh").write_text(sh_script, encoding="utf-8")
os.chmod(ROOT / "build_apk.sh", 0o755)
sh("✓ 本地打包脚本 build_apk.sh")

# ---------------- README 增补 ----------------
readme_add = """

---

## 📦 APK 打包指南（Android）

本项目由 Python + Kivy 编写。Kivy 官方推荐用 **Buildozer** 将其打包为 APK/AAB，
它负责自动下载 Android SDK/NDK、交叉编译 Python 解释器并打包你的代码 [1]。

### 方案一：一键脚本（本地 Linux / WSL2 / macOS）

```bash
chmod +x build_apk.sh
./build_apk.sh
```

完成后 APK 位于 `bin/知学TV-1.0.0-debug.apk`。

### 方案二：手动步骤

```bash
pip install buildozer cython==0.29.34
buildozer init            # 已生成 buildozer.spec，可跳过
buildozer -v android debug
buildozer android debug deploy run   # 构建 + 安装到已连接设备
```

### 方案三：GitHub Actions（推荐，零本地环境）

push 到 GitHub 后，Actions 会自动构建并在 Artifacts 产出 APK：
`build-apk.yml` 已配置好（使用 `ArtemSBulgakov/buildozer-action@v1`）。

### 发布正式版（签名 AAB）

```bash
buildozer android release
# 首次会生成未签名 AAB，用以下命令签名：
buildozer android sign release
```

签名密钥配置在 `buildozer.spec` 的 `[buildozer]` 段 `android.release_*` 项。

### 已配置说明

| 项 | 值 |
|---|---|
| 包名 | com.zhixuetv.app |
| 最低 API | 21（Android 5.0） |
| 目标 API | 33 |
| Python | 3.11.9 |
| 依赖 | kivy 2.3.1 + pillow 10.4.0（纯 Python，无 C 扩展障碍） |

> 依赖选择说明：本项目只用了 Kivy + Pillow，二者在 python-for-android 中均有现成
> recipe，不会出现 "Chaquopy cannot compile native code" 类错误。若后续接入 NumPy
> 等带 C 扩展的库，需确认该库在 Android 上已有二进制 wheel [3]。

### 引用来源

[1] https://kivy.org/doc/stable/guide/packaging-android.html
> "For new users, we recommend using Buildozer as the easiest way to make a full APK or AAB."

[2] https://github.com/kivy/buildozer
> "Buildozer is a development tool for turning Python applications into binary packages
> ready for installation on any of a number of platforms, including mobile devices."

[3] https://briefcase.beeware.org/en/v0.3.12/background/faq.html
> "If the package is pure-Python... that's all you need to do."
"""
readme = (ROOT / "README.md").read_text(encoding="utf-8")
if "APK 打包指南" not in readme:
    (ROOT / "README.md").write_text(readme + readme_add, encoding="utf-8")
    sh("✓ README.md 增补打包指南")
else:
    sh("✓ README.md 已含打包指南（跳过）")

sh("")
sh("=" * 64)
sh("完成。工程结构：")
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and "__pycache__" not in str(p) and ".git" not in str(p):
        print(f"  {p.relative_to(ROOT)}")
sh("=" * 64)
sh("下一步：运行 ./build_apk.sh 或推送到 GitHub 触发 Actions")
