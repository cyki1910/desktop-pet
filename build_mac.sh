#!/bin/bash
# ============================================================
# 桌宠打包脚本（在 Mac 上运行）
# 作用：把 pet.py + 图片打包成双击即用的 .app
# 用法：在终端运行  ./build_mac.sh  （或直接拖进终端）
# 产物：dist/桌宠.app  —— 双击运行，可拷给朋友
# ============================================================
set -e
cd "$(dirname "$0")"

echo "== 检查 Python =="
if ! command -v python3 >/dev/null 2>&1; then
  echo "错误：没有找到 python3，请先安装 Python3（https://www.python.org/downloads/）"
  exit 1
fi

echo "== 安装/更新依赖 =="
python3 -m pip install --user --upgrade pyinstaller PySide6

echo "== 开始打包 .app =="
python3 -m PyInstaller \
  --noconfirm --windowed \
  --name "桌宠" \
  --add-data "pet_big.png:." \
  pet.py

echo ""
echo "✅ 完成！应用在这里："
echo "   $(pwd)/dist/桌宠.app"
echo ""
echo "双击即可运行；要拷给朋友，把 桌宠.app 整个文件夹发过去即可。"
