# coding:utf-8
import sys
import warnings
from ctypes import POINTER, byref, c_bool, c_int, cdll, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID
from platform import platform

from win32 import win32api
from win32 import win32gui
from win32.lib import win32con

from .c_structures import (ACCENT_POLICY, ACCENT_STATE, DWMNCRENDERINGPOLICY,
                           DWMWINDOWATTRIBUTE, MARGINS,
                           WINDOWCOMPOSITIONATTRIB,
                           WINDOWCOMPOSITIONATTRIBDATA)


class WindowsWindowEffect:
    """ Windows window effect """

    def __init__(self, window):
        self.window = window

        # Declare the function signature of the API
        self.user32 = cdll.LoadLibrary("user32")
        self.dwmapi = cdll.LoadLibrary("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute
        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]

        # Initialize structure
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    def setAcrylicEffect(self, hWnd, gradientColor="F2F2F299", enableShadow=True, animationId=0):
        """ Add the acrylic effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        gradientColor: str
            Hexadecimal acrylic mixed color, corresponding to four RGBA channels

        isEnableShadow: bool
            Enable window shadows

        animationId: int
            Turn on matte animation
        """
        if "Windows-7" in platform():
            warnings.warn("The acrylic effect is only available on Win10+")
            return

        hWnd = int(hWnd)
        gradientColor = "".join(gradientColor[i:i+2] for i in range(6, -1, -2))
        gradientColor = DWORD(int(gradientColor, base=16))
        animationId = DWORD(animationId)
        accentFlags = DWORD(0x20 | 0x40 | 0x80 | 0x100) if enableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def setMicaEffect(self, hWnd, isDarkMode=False):
        """ Add the mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        isDarkMode: bool
            whether to use dark mode mica effect
        """
        if sys.getwindowsversion().build < 22000:
            warnings.warn("The mica effect is only available on Win11")
            return

        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

        if isDarkMode:
            self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_USEDARKMODECOLORS.value
            self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

        if sys.getwindowsversion().build < 22523:
            self.DwmSetWindowAttribute(hWnd, 1029, byref(c_int(1)), 4)
        else:
            self.DwmSetWindowAttribute(hWnd, 38, byref(c_int(2)), 4)

    def setAeroEffect(self, hWnd):
        """ Add the aero effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def removeBackgroundEffect(self, hWnd):
        """ Remove background effect

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    @staticmethod
    def moveWindow(hWnd):
        """ Move the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            hWnd, win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0
        )

    def addShadowEffect(self, hWnd):
        """ Add DWM shadow to window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def addMenuShadowEffect(self, hWnd):
        """ Add DWM shadow to menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED.value)),
            4,
        )
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def removeShadowEffect(self, hWnd):
        """ Remove DWM shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    @staticmethod
    def removeMenuShadowEffect(hWnd):
        """ Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetClassLong(hWnd, win32con.GCL_STYLE)
        style &= ~0x00020000  # CS_DROPSHADOW
        win32api.SetClassLong(hWnd, win32con.GCL_STYLE, style)

    @staticmethod
    def addWindowAnimation(hWnd):
        """ Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )
