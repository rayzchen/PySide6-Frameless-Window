# coding:utf-8
import sys

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont, QPainter
from PySide6.QtWidgets import QHBoxLayout, QWidget, QMenuBar, QLabel, QStyleOption, QStyle

if sys.platform == "win32":
    from win32.lib import win32con
    from win32.win32api import SendMessage
    from win32.win32gui import ReleaseCapture
else:
    from ..utils.linux_utils import LinuxMoveResize

from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton


class TitleBarBase(QWidget):
    """ Title bar base class """

    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.resize(200, 32)
        self.setFixedHeight(32)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.menuBar = QMenuBar(self.window())
        self.menuBar.resize(200, 32)
        self.menuBar.setFixedHeight(32)
        self.menuBar.setFont(QFont("Segoe UI", 11))
        self.menuBar.setStyleSheet("QMenuBar{padding-top: 2px; background-color: rgba(0, 0, 0, 0);}")
        self.hBoxLayout.addWidget(self.menuBar, 0)

        self.label = QLabel(self)
        self.label.setFont(QFont("Segoe UI", 11))
        self.label.setStyleSheet("QLabel{padding-bottom: 2px;}")
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.lower()
        self.hBoxLayout.addWidget(self.label, 1)

        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)

        # add buttons to layout
        self.hBoxLayout.addWidget(self.minBtn, 0)
        self.hBoxLayout.addWidget(self.maxBtn, 0)
        self.hBoxLayout.addWidget(self.closeBtn, 0)

        # connect signal to slot
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def paintEvent(self, event):
        self.label.move(self.width() // 2 - self.label.width() // 2, 0)
        super(TitleBarBase, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        s = self.style()
        s.drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton:
            return

        self.__toggleMaxState()

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the pressed point belongs to the area where dragging is allowed """
        return self.menuBar.width() < pos.x() < self.width() - 46 * 3


class WindowsTitleBar(TitleBarBase):
    """ Title bar for Windows system """

    def mouseMoveEvent(self, event):
        if not self._isDragRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE | win32con.HTCAPTION, 0)
        event.ignore()


class UnixTitleBar(TitleBarBase):
    """ Title bar for Unix system """

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDragRegion(event.pos()):
            return

        pos = event.globalPos()
        LinuxMoveResize.startSystemMove(self.window(), pos)


TitleBar = WindowsTitleBar if sys.platform == "win32" else UnixTitleBar