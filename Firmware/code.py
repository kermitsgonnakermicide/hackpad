import board
import digitalio
import adafruit_displayio_ssd1306
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.modules.oled import OLED, OledDisplayMode
from kmk.extensions.media_keys import MediaKeys

keyboard = KMKKeyboard()

key_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4]
encoder_pins = ((board.GP26, board.GP27, board.GP28),)

from kmk.scanners import MatrixScanner
#no diodes yeay
keyboard.matrix = MatrixScanner(
    cols=key_pins,
    rows=[],
    diode_orientation=DiodeOrientation.COL2ROW
)

keyboard.keymap = [
    [
        KC.A, KC.B, KC.C, KC.D, KC.E
    ]
]

encoder = EncoderHandler()
encoder.pins = encoder_pins
encoder.map = [
    ((KC.VOLD, KC.VOLU),)
]
#encoder will handle volume, pause and play
keyboard.modules.append(encoder)

keyboard.extensions.append(MediaKeys())

encoder_btn = digitalio.DigitalInOut(board.GP28)
encoder_btn.switch_to_input(pull=digitalio.Pull.UP)

oled = OLED(
    i2c=board.I2C(),
    display_mode=OledDisplayMode.MASTER,
    flip=True,
    width=128,
    height=32,
)

keyboard.modules.append(oled)

media_playing = False
last_button_state = True
current_track = "no track"

def update_oled():
    oled.clear()
    oled.display_text(f"Track: {current_track}", 0, 0)
    status = "▶" if media_playing else "❚❚"
    oled.display_text(f"Status: {status}", 0, 16)

def check_encoder_switch():
    global media_playing, last_button_state

    current_state = encoder_btn.value
    if not current_state and last_button_state:
        media_playing = not media_playing
        keyboard.tap_key(KC.MPLY)
        update_oled()
    last_button_state = current_state

keyboard.after_scan = check_encoder_switch

update_oled()

if __name__ == '__main__':
    keyboard.go()
