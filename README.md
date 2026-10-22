# 知学 TV · 泉州台商投资区 —— 大屏学习应用

面向**泉州台商投资区在读学生**的本地化大屏学习应用：从幼儿园到高中全学段、全学科，12 大 AI 辅导场景，并内置本地升学政策、中考政策专区、闽南文化课堂。

> 原型版本，桌面可直接运行演示；亦可参照 `main.py` 的交互与内容结构迁移到 Android TV（Leanback）。

## 为什么是「泉州台商区专属」

| 模块 | 本地化内容 |
|---|---|
| 本地升学政策 | 2026 台商区义务教育招生、中考中招政策、招考办咨询电话 |
| 身边好学校 | 师院附小台商区分校、泉州五中台商区分校、惠南中学、实验高中、第十七中学 |
| 中考政策专区 | 福建新中考 800 分制全解析、6月21-23日统考日程 |
| 闽南文化课堂 | 海丝起点、洛阳桥、南音、闽南语、侨乡下南洋 |
| 家乡地理 | 洛阳江与泉州湾、海岸线与滩涂、福建地形气候 |

数据来源：台商区 2025 教育事业发展统计公报（在校生 75073 人、公办小学 42 所、中学 11 所）、2026 泉州市中考中招方案、2025 高中录取分数线。

## 运行

```bash
pip install -r requirements.txt
python run.py
```

操作：方向键移动焦点（高亮+边框放大），回车确认，ESC 返回。

## 迁移到 Android TV

- `FocusCard` → Leanback `BaseCardView`（焦点态用 `onFocusChanged` + Elevation）
- 学段/学科/课时三级页 → `BrowseSupportFragment` + `RowsSupportFragment`
- 播放页 → `VideoSupportFragment` / ExoPlayer
- 随堂测验 → `GuidedStepSupportFragment`
- 建议 Kotlin + Leanback 1.2，适配 1080p/4K TV

## 界面预览

`screenshots/overview.png`（12 大界面总览），单张截图见 `screenshots/` 目录。


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
