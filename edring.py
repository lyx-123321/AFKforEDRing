# https://github.com/lyx-123321/AFKforEDRing
import ctypes
from ctypes import wintypes
import time
import threading

# API for send key board input to windows, No need to change
# Hex code for keys is on https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
# Usage: PressKey(HexCode)
#        ReleaseKey(HexCode)

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
VK_F15  = 0x7E
VK_LWIN = 0x5B
VK_Z = 0x5A
VK_ESC = 0x1B

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

#-----------------------Define the actions we may need during training----------------------------------------
#wasd上下左右默认的键位
W = 0x57
S = 0x53
A = 0x41
D = 0x44

E = 0x45 #进入赐福点
Q = 0x51 #退出赐福点
G = 0x47 #graph

Z = 0x5A #技能

def quitm():
    PressKey(Q)
    time.sleep(0.1)
    ReleaseKey(Q)

def comfirm():
    PressKey(E)
    time.sleep(0.1)
    ReleaseKey(E)

def goforward(a):
    PressKey(W)
    time.sleep(a)
    ReleaseKey(W)

def goback(a):
    PressKey(S)
    time.sleep(a)
    ReleaseKey(S)

def goleft(a):
    PressKey(A)
    time.sleep(a)
    ReleaseKey(A)

def skill():
    PressKey(Z)
    time.sleep(0.5)
    ReleaseKey(Z)

def opengraph():
    PressKey(G)
    time.sleep(0.1)
    ReleaseKey(G)
    time.sleep(1)

def shuaguai2():
    time.sleep(3)
    goforward(4)
    goleft(1)
    goforward(1)
    skill()
    time.sleep(6)
    opengraph()
    goback(0.05)
    time.sleep(1)
    comfirm()
    time.sleep(1)
    comfirm()
    time.sleep(5)

time.sleep(3)
quitm()
while(1):
    shuaguai2()
