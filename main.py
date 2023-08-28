import board

from kb import KMKKeyboard, isRight; keyboard = KMKKeyboard()
from kmk.modules.split import Split, SplitSide, SplitType
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap; keyboard.modules.append(HoldTap())
from kmk.modules.combos import Combos, Chord, Sequence; keyboard.modules.append(Combos())
from kmk.modules.mouse_keys import MouseKeys; keyboard.modules.append(MouseKeys())
#from kmk.modules.power import Power; keyboard.modules.append(Power())
#from kmk.modules.tapdance import TapDance; keyboard.modules.append(TapDance())
from kmk.extensions.media_keys import MediaKeys; keyboard.extensions.append(MediaKeys())
#from kmk.modules.capsword import CapsWord; keyboard.modules.append(CapsWord())

keyboard.debug_enabled = True
is_USB_Left = False # Defines where usb is connected. Pimaroni trackball can only be used on the same side as the usb connected pico

combo_layers = {
  (1, 2): 3, # Activate layer 3 when pressing layer 1 and 2
}

if isRight:
    from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection
    import busio as io
    from kmk.modules.layers import Layers as _Layers;
    i2c = io.I2C(scl=board.GP27, sda=board.GP26)
    trackball = Trackball(i2c,angle_offset=90,)

    keyboard.modules.append(trackball)
    trackball.set_red(100)

    class Layers(_Layers):
        last_top_layer = 0

        def after_hid_send(self, keyboard):
            if keyboard.active_layers[0] != self.last_top_layer:
                self.last_top_layer = keyboard.active_layers[0]
                trackball.set_rgbw(0, 0, 0, 0) # Reset leds
                if self.last_top_layer == 0: trackball.set_green(100)
                elif self.last_top_layer == 1: trackball.set_white(100)
                elif self.last_top_layer == 2: trackball.set_blue(100)
                else: trackball.set_red(100)

else:
    from kmk.modules.layers import Layers;

keyboard.modules.append(Layers(combo_layers))

split_side = SplitSide.RIGHT if isRight else SplitSide.LEFT

data_pin = board.GP1 if split_side == SplitSide.LEFT else board.GP0
data_pin2 = board.GP0 if split_side == SplitSide.LEFT else board.GP1

split = Split(
    split_side=split_side,
    split_type=SplitType.UART,
    split_target_left=is_USB_Left,
    split_flip=False,
    data_pin=data_pin if is_USB_Left else data_pin2,
    data_pin2=data_pin2 if is_USB_Left else data_pin
)
keyboard.modules.append(split)

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1) # momentarily activate while pressed
RAISE = KC.MO(2) # momentarily activate while pressed
ADJUST = KC.SPC
# ADJUST = KC.LT(3, KC.SPC)
LGUI = KC.HT(KC.LALT, KC.LGUI,  prefer_hold=False) # mainly for alt tab, if held it's gui
INS_PASTE = Sequence(KC.LSFT, KC.INSERT)


keyboard.keymap = [
    [  #QWERTY
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,                         KC.Y,    KC.U,    KC.I,    KC.O,   KC.P,  KC.BSPC,\
        KC.LCTL,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,                         KC.H,    KC.J,    KC.K,    KC.L, KC.SCLN, KC.QUOT,\
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,                         KC.N,    KC.M, KC.COMM,  KC.DOT, KC.SLSH, KC.RSFT,\
                                                LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #LOWER
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                         KC.N6,   KC.N7,  KC.N8,   KC.N9,   KC.N0, KC.BSPC,\
        KC.LCTL, XXXXXXX, XXXXXXX, XXXXXXX,  KC.DEL, KC.INSERT,                      KC.LEFT, KC.DOWN, KC.UP,   KC.RIGHT, XXXXXXX, XXXXXXX,\
        KC.LSFT, XXXXXXX, KC.MB_LMB, KC.MB_RMB, XXXXXXX, XXXXXXX,                    KC.HOME, KC.PGDOWN, KC.PGUP, KC.END, XXXXXXX, XXXXXXX,\
                                                LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #RAISE
        KC.ESC, KC.EXLM,   KC.AT, KC.HASH,  KC.DLR, KC.PERC,                         KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.BSPC,\
        KC.LCTL, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        KC.MINS,  KC.EQL, KC.LCBR, KC.RCBR, KC.PIPE,  KC.GRV,\
        KC.LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                        KC.UNDS, KC.PLUS, KC.LBRC, KC.RBRC, KC.BSLS, KC.TILD,\
                                                LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #COMBO LAYER
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                         XXXXXXX, KC.MEDIA_PREV_TRACK, KC.MEDIA_PLAY_PAUSE, KC.MEDIA_NEXT_TRACK, XXXXXXX, XXXXXXX,\
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                         KC.AUDIO_MUTE, KC.AUDIO_VOL_DOWN, KC.AUDIO_VOL_UP, XXXXXXX, XXXXXXX, XXXXXXX,\
        XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,                         KC.DF(0), KC.DF(4), XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
                                                LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],
    [  #GAMING (ESO)
        KC.TAB,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,                         KC.N6,   KC.N7,  KC.N8,   KC.N9,   KC.N0, KC.BSPC,\
        KC.LCTL,   KC.Q,   KC.LEFT, KC.UP, KC.RIGHT,   KC.E,                         XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
        KC.LSFT,XXXXXXX, XXXXXXX, KC.DOWN, XXXXXXX, XXXXXXX,                         XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,\
                                                LGUI,   LOWER,  ADJUST,     KC.ENT,   RAISE,  KC.RALT,
    ],

]


if __name__ == '__main__':
     print('starting Piantor KMK')
     keyboard.go()
# Write your code here :-)
