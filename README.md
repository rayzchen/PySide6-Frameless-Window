# PySide6-Frameless-Window

Based off https://github.com/zhiyiYo/PyQt-Frameless-Window but migrated to PySide6.

New features:
- Merged MenuBar and TitleBar (hidden by default)
- Added centered title label, set with `Window.setWindowTitle`

# Original README:

## Features
* Move
* Stretching
* Window animation
* Window shadow
* Win10 acrylic blur
* Win11 mica blur
* Win7 Aero blur
* MacOS blur

## Install
To install use pip:
```shell
pip install PySide6-Frameless-Window
```
Or clone the repo:
```shell
git clone https://github.com/rayzchen/PySide6-Frameless-Window
python setup.py install
```

## Requirements

| Platform | Requirement |
| :------: | :---------: |
|  Win32   |   pywin32   |
|  Linux   |   xcffib    |
|  MacOS   |   pyobjc    |


## Usage
To use the frameless window, you only need to inherit `FramelessWindow`. Here is a minimal example:
```python
import sys

from PySide6.QtWidgets import QApplication
from qframelesswindow import FramelessWindow


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PyQt-Frameless-Window")
        self.titleBar.raise_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())
```
For more complex requirements, you can refer to the [demo.py](./demo.py).

## Examples
* Normal frameless window
![Normal Frameless Window](screenshot/normal_frameless_window.gif)
* Acrylic frameless window
![Acrylic Frameless Window](screenshot/Acrylic_window.gif)



## Notes
1. `FramelessWindow` provides a default custom title bar. If you don't like it, just rewrite it as [demo.py](./demo.py) does.

2. Moving the acrylic window on Win10 may get stuck. At present, there is no good solution. Maybe you can disable the acrylic effect when moving the window, but I haven't done this in the source code.

3. If you encounter this problem on Windows:
   > ImportError: DLL load failed while importing win32api

   see my answer on [stackoverflow](https://stackoverflow.com/questions/58612306/how-to-fix-importerror-dll-load-failed-while-importing-win32api/72488468#72488468) or my [blog](https://www.cnblogs.com/zhiyiYo/p/16340429.html) for the solution.

4. If you are using PySide2 or PyQt6, you can download the code in [PySide2](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/Pyside2) or [PyQt6](https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PyQt6) branch, but they only support Win32 and macOS at present.

## See Also
Here are some projects that use PyQt-Frameless-Window:
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)
* [**tonquer/picacg-qt**: PicACG PC Client ](https://github.com/tonquer/picacg-qt)

## Reference
* [**wangwenx190/framelesshelper**: Frameless windows for Qt Widgets and Qt Quick applications. Support Win32, X11, Wayland and macOS](https://github.com/wangwenx190/framelesshelper)
* [**libxcb**: Basic Graphics Programming With The XCB Library](https://github.com/zhaiyuhan/HAODA)

## License
```
MIT License

Copyright (c) 2021 Zhengzhi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
>>>>>>> upstream/master
