import colorsys
import socket
from . import commands, structures

class Controller():
    def __init__(self, host='4.3.2.1', port=8189, attempts=3):
        self.host = host
        self.port = port

        self.attempts = attempts
        self.socket_timeout = 0.3

        try:
            self.connect()
        except OSError:
            pass

        # Default brightness level
        self.bright_level = 128

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.socket_timeout)
        self.sock.connect((self.host, self.port))

    def disconnect(self):
        self.sock.close()

    def connection(function):
        def connected_function(self, *args, **kwargs):
            attempts = self.attempts
            while attempts:
                try:
                    print('Attempt %d to run %s(%s, %s, %s)' % ((self.attempts-attempts+1), function, self, args, kwargs))
                    return function(self, *args, **kwargs)
                except BrokenPipeError:
                    print('BrokenPipeError. Attempting connect()')
                    self.connect()
                except ConnectionRefusedError as e:
                    print(e)
                    raise e
                attempts -= 1
            print('Failed to run %s(%s, %s, %s)' % (function, self, args, kwargs))
        return connected_function

    @connection
    def auto(self):
        self.sock.send(
            commands.mode_change(commands.MODE_AUTO)
        )

    def on(self, state=True):
        if not state:
            return self.brightness(0)

        self.brightness(self.bright_level)

    @connection
    def static_rgb(self, r, g, b):
        self.sock.send(
            commands.color(
                structures.RGB(r, g, b)
            )
        )
        self.sock.send(
            commands.mode_change(commands.MODE_STATIC)
        )

    @connection
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
