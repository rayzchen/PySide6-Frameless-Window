# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel
from qframelesswindow import FramelessWindow


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setPixmap(QPixmap("screenshot/shoko.png"))
        self.setStyleSheet("background-color: white")
        self.setWindowTitle("PyQt Frameless Window")
        self.statusBar().showMessage("Hello World!")
        self.customizeTitleBar()

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        workMenu = menuBar.addMenu("Work")
        workMenu.addAction("Work something")
        analysisMenu = menuBar.addMenu("Analysis")
        analysisMenu.addAction("Analize action")

        self.titleBar.raise_()

    def customizeTitleBar(self):
        normalDarkStyle = {
            "normal": {
                "color": (255, 255, 255, 255),
                "background": (0, 0, 0, 0)
            },
            "hover": {
                "color": (255, 255, 255),
                "background": (0, 100, 182)
            },
            "pressed": {
                "color": (255, 255, 255),
                "background": (89, 94, 107)
            },
        }        
        closeDarkStyle = {
            "normal": {
                "background": (0, 0, 0, 0),
                "icon": ":/framelesswindow/close_white.svg"
            },
            "hover": {
                "background": (232, 17, 35),
                "icon": ":/framelesswindow/close_white.svg"
            },
            "pressed": {
                "background": (241, 112, 122),
                "icon": ":/framelesswindow/close_white.svg"
            },
        }
        self.titleBar.minBtn.updateStyle(normalDarkStyle)
        self.titleBar.maxBtn.updateStyle(normalDarkStyle)
        self.titleBar.closeBtn.updateStyle(closeDarkStyle)
        self.titleBar.setStyleSheet("background-color: #363941; color: white")

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(
            self.width() // 2 - length // 2,
            self.height() // 2 - length // 2
        )
        self.label.lower()


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
