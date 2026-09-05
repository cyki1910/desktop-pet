#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桌宠 —— 简笔画小熊
Python + PySide6 实现的极简桌面宠物，纯本地、无需 API。

功能：
  - 透明、无边框、置顶悬浮在桌面
  - 按住左键拖动到任意位置
  - 点一下会弹跳（squash & stretch）作为反馈
  - 待机时每隔几秒轻微上下晃动
  - 右键菜单：退出
  - Qt.Tool 窗口，不占 Dock、不抢焦点

打包成 .app（在 Mac 上执行）：
  pip3 install pyinstaller PySide6
  pyinstaller --noconfirm --windowed --name 桌宠 \
      --add-data "pet_big.png:." pet.py
  完成后 .app 在 dist/桌宠.app，双击即用，可拷给朋友。
"""
import os
import sys

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPointF, QRectF
from PySide6.QtGui import QPixmap, QAction, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QMenu


def resource_path(name: str) -> str:
    """兼容 PyInstaller 打包后的资源路径。"""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


TARGET_HEIGHT = 180          # 桌宠显示高度（px），可调
FLOAT_RANGE = 8              # 待机晃动的幅度
FLOAT_INTERVAL_MS = 3000     # 每隔多久晃一次


class Pet(QWidget):
    def __init__(self, image_name="pet_big.png"):
        super().__init__()

        # 加载图片并缩放到目标高度
        self._pix = QPixmap(resource_path(image_name))
        if self._pix.isNull():
            raise FileNotFoundError(f"找不到图片: {resource_path(image_name)}")
        scale = TARGET_HEIGHT / self._pix.height()
        self._pix = self._pix.scaled(
            int(self._pix.width() * scale),
            TARGET_HEIGHT,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.resize(self._pix.size())

        # 窗口：透明 + 无边框 + 置顶 + 工具窗
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # 初始位置：屏幕右上角附近
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.right() - self.width() - 80, screen.top() + 80)

        # 交互状态
        self._drag_offset = None      # 拖动偏移
        self._base_pos = self.pos()   # 待机晃动基准位置
        self._float_anim = None

        # 右键菜单
        self._build_menu()

        # 待机晃动定时器
        self._float_timer = QTimer(self)
        self._float_timer.timeout.connect(self._idle_float)
        self._float_timer.start(FLOAT_INTERVAL_MS)

    # ---------- 绘制 ----------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._pix)

    # ---------- 鼠标交互 ----------
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_offset = e.globalPosition().toPoint() - self.pos()
            self._bounce()          # 点一下 = 弹一下
            e.accept()
        elif e.button() == Qt.RightButton:
            self._menu.exec(e.globalPosition().toPoint())
            e.accept()

    def mouseMoveEvent(self, e):
        if self._drag_offset is not None and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_offset)
            self._base_pos = self.pos()   # 拖动后重新锚定晃动基准
            e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_offset = None
            e.accept()

    # ---------- 弹跳动画（squash & stretch） ----------
    def _bounce(self):
        r = QRectF(self.rect())
        cx, cy = r.center().x(), r.center().y()
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(260)
        anim.setEasingCurve(QEasingCurve.OutBack)
        anim.setKeyValueAt(0.0, self.geometry())
        anim.setKeyValueAt(0.45, QRectF(
            cx - r.width() * 0.88 / 2, cy - r.height() * 1.10 / 2,
            r.width() * 0.88, r.height() * 1.10,
        ).toRect())
        anim.setKeyValueAt(1.0, self.geometry())
        anim.start(QPropertyAnimation.DeleteWhenStopped)

    # ---------- 待机晃动 ----------
    def _idle_float(self):
        base = self._base_pos
        dy = FLOAT_RANGE
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(700)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.setKeyValueAt(0.0, self.pos())
        anim.setKeyValueAt(0.5, QPointF(base.x(), base.y() - dy))
        anim.setKeyValueAt(1.0, QPointF(base.x(), base.y()))
        anim.start(QPropertyAnimation.DeleteWhenStopped)

    # ---------- 右键菜单 ----------
    def _build_menu(self):
        self._menu = QMenu()
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(QApplication.quit)
        self._menu.addAction(quit_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    pet = Pet()
    pet.show()
    sys.exit(app.exec())
