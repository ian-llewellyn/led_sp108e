import colorsys
import socket
from . import commands, structures


class Controller():
    def __init__(self, host='4.3.2.1', port=8189):
        self.host = host
        self.port = port
        self.connect()

        self.bright_level = 128

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def auto(self):
        self.sock.send(
            commands.mode_change(commands.MODE_AUTO)
        )

    def on(self, state=True):
        print('on():', type(state), state)
        if not state:
            return self.brightness(0)

        self.brightness(self.bright_level)

    def static_rgb(self, r, g, b):
        self.sock.send(
            commands.color(
                structures.RGB(r, g, b)
            )
        )
        self.sock.send(
            commands.mode_change(commands.MODE_STATIC)
        )

    def brightness(self, brightness):
        self.sock.send(
            commands.brightness(brightness)
        )
        if brightness:
            self.bright_level = brightness

    def static_hsv(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r, g, b = [int(r), int(g), int(b)]
        self.static_rgb(r, g, b)
