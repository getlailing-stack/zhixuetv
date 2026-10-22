#!/usr/bin/env bash
# 知学TV 本地 APK 打包（一键脚本）
# 需要 Linux / macOS / WSL2 + Python 3.8+
set -e
echo "==> [1/4] 安装系统依赖（Ubuntu/Debian）"
sudo apt-get update -qq
sudo apt-get install -y -qq git zip unzip openjdk-17-jdk python3-pip \
  python3-venv autoconf libtool pkg-config zlib1g-dev libffi-dev \
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
