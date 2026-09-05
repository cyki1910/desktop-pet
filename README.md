# 简笔画小熊 · Mac 桌宠

一只会弹跳、会晃动、可拖动的桌面小宠物，做成 `.app` 双击即用。

## 交付内容（在 `桌宠/` 目录）

| 文件 | 说明 |
|---|---|
| `pet.py` | 桌宠主程序（Python + PySide6） |
| `pet_big.png` | 你的简笔画小熊（已抠成透明背景、放大 2 倍） |
| `pet_transparent.png` | 抠图后的原始尺寸版 |
| `process_img.py` / `verify_alpha.py` | 抠图与透明校验脚本（已跑完） |
| `启动桌宠.bat` | **Windows 一键启动**（双击即用，自动装依赖） |
| `启动桌宠.command` | **Mac 一键启动**（双击即用，自动装依赖） |
| `build_mac.sh` | **Mac 一键打包成 .app** |

## 桌宠功能

- 透明、无边框、**置顶**悬浮在桌面
- **点一下**会弹跳（squash & stretch 缩放反馈）
- **按住左键**可拖动到任意位置
- **待机时**每隔几秒轻微上下晃动，更生动
- **右键菜单**：退出
- 工具窗口设计：不占 Dock、不抢焦点，不挡干活

## 怎么用

### 方式一：一键启动（最快，直接看效果）

| 平台 | 操作 |
|---|---|
| **Windows**（你现在开发的环境） | 双击 **`启动桌宠.bat`**，自动装好依赖并弹出一只小熊 |
| **Mac**（给朋友） | 双击 **`启动桌宠.command`**（首次需 `右键 → 打开` 放行），同样自动装依赖并启动 |

两者都会：检测 Python → 缺 PySide6 就自动安装 → 启动桌宠。桌宠出现在**屏幕右上角**，右键可退出。

### 方式二：打包成 .app（正式分发给朋友，需在 Mac 上跑一次）

> ⚠️ PyInstaller 不能跨平台打包，Windows 上打不出 Mac 的 .app，
> 所以打包必须在 Mac 环境执行。有两种办法：**云端自动打包（推荐，无需装任何东西）** 或 **Mac 本地手动打包**。

#### 方案 A：GitHub Actions 云端自动打包（推荐，Mac 朋友零安装）

完全不用在 Mac 上装 Python / PyInstaller，云端自动搞定：

1. 把整个 `桌宠/` 文件夹推到 GitHub 仓库（作为仓库根目录，`pet.py` 在根下）
   ```
   git init
   git add .
   git commit -m "桌宠"
   git branch -M main
   git remote add origin <你的仓库地址>
   git push -u origin main
   ```
2. 到仓库的 **Actions** 页，点 **Run workflow**（或打个 tag `git tag v1.0 && git push --tags`）
3. 云端用 Mac 环境自动：装 Python → 装 PyInstaller → 打出 `桌宠.app`
4. 运行完成后，在本次运行的底部 **Artifacts** 里下载 `desktop-pet-macos`，解压得到 `桌宠.app`
5. 把 `桌宠.app` 发给朋友，**双击即用，对方什么都不用装**

配置已写好：`.github/workflows/build-macos.yml`，推上去即可用。

#### 方案 B：Mac 本地手动打包（需要朋友装一次 Python）

1. 把整个 `桌宠/` 文件夹发给 Mac 朋友
2. 打开「终端」，拖入脚本：
   ```bash
   cd ~/Downloads/桌宠
   ./build_mac.sh
   ```
   如果提示没有权限，先执行 `chmod +x build_mac.sh`
3. 完成后应用在 `桌宠/dist/桌宠.app`，双击即用，可无限复制

> 该脚本会自动装依赖，但**前提是 Mac 上已有 Python3**。若没有：
> - 最快：到 https://www.python.org/downloads/ 装官方最新版
> - 或终端：`brew install python`（已装 Homebrew 的话）

## 高级：窗口默认放在右上角，想改？

打开 `pet.py`，改这几行即可：

- `TARGET_HEIGHT = 180` → 桌宠显示大小
- `FLOAT_RANGE = 8` / `FLOAT_INTERVAL_MS = 3000` → 待机晃动幅度与频率
- `screen.right() - self.width() - 80, screen.top() + 80` → 初始位置
