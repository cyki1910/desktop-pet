#!/bin/bash
# ============================================================
# 小熊桌宠 - Mac 一键启动
# 双击本文件即可运行；或终端执行：./启动桌宠.command
# 首次运行会自动安装 PySide6，之后秒开。
# ============================================================
cd "$(dirname "$0")"

echo "========================================"
echo "   小熊桌宠 - 一键启动"
echo "========================================"

# 找 python3
PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
  echo "[错误] 没有找到 Python3，请先安装：https://www.python.org/downloads/"
  read -r -p "按回车退出..." _
  exit 1
fi

echo "[1/3] Python: $($PY --version 2>&1)"

echo "[2/3] 检查 PySide6 依赖..."
if ! $PY -c "import PySide6" >/dev/null 2>&1; then
  echo "   未安装，正在自动安装（首次需要几分钟）..."
  $PY -m pip install --user PySide6
  if [ $? -ne 0 ]; then
    echo "[错误] PySide6 安装失败，请检查网络后重试。"
    read -r -p "按回车退出..." _
    exit 1
  fi
else
  echo "   已安装，跳过。"
fi

echo "[3/3] 启动桌宠...（右键宠物可退出）"
nohup $PY "$(pwd)/pet.py" >/dev/null 2>&1 &
echo "完成！小熊已出现在屏幕右上角。"
sleep 2
