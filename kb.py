import board
from storage import getmount

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners.keypad import KeysScanner


# split side
# isRight = False
name = str(getmount('/').label)
isRight = True if name.endswith('R') else False

# GPIO to key mapping, Left
_KEY_CFG_LEFT = [
    board.GP22,  board.GP19,  board.GP11, board.GP8, board.GP5,  board.GP2,
    board.GP21,  board.GP18,  board.GP12, board.GP9, board.GP6,  board.GP3,
    board.GP20,  board.GP17,  board.GP13,board.GP10, board.GP7,  board.GP4,
                                    board.GP16, board.GP15,  board.GP14
]

# GPIO to key mapping, Left
_KEY_CFG_RIGHT = [
    board.GP19, board.GP22, board.GP11, board.GP2, board.GP8, board.GP5,
    board.GP18, board.GP21, board.GP12, board.GP3, board.GP9, board.GP6,
    board.GP17, board.GP20, board.GP13, board.GP4, board.GP10, board.GP7,
    board.GP14, board.GP15, board.GP16
]

class KMKKeyboard(_KMKKeyboard):
    def __init__(self):
        # create and register the scanner
        self.matrix = KeysScanner(
            pins = _KEY_CFG_RIGHT if isRight == True else _KEY_CFG_LEFT
        )

    # flake8: noqa
    # fmt: off
    coord_mapping = [
     0,  1,  2,  3,  4,  5,   21, 22, 23, 24, 25, 26,
     6,  7,  8,  9, 10, 11,   27, 28, 29, 30, 31, 32,
    12, 13, 14, 15, 16, 17,   33, 34, 35, 36, 37, 38,
                18, 19, 20,   39, 40, 41
    ]






