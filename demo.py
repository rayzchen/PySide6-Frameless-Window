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
        self.setWindowTitle("PyQt Frameless Window")

        self.statusBar().showMessage("Hello World!")

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction("Open")
        fileMenu.addAction("Save")
        workMenu = menuBar.addMenu("Work")
        workMenu.addAction("Work something")
        analysisMenu = menuBar.addMenu("Analysis")
        analysisMenu.addAction("Analize action")

        self.titleBar.raise_()

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
