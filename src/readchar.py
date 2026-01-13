import sys
import os

# We move these to the top level so they are available to all functions
_old_settings = None

if os.name == 'nt':
    import msvcrt

    _WIN_ARROW_MAP = {
        b'H': '\x1b[A',  # Up
        b'P': '\x1b[B',  # Down
        b'M': '\x1b[C',  # Right
        b'K': '\x1b[D',  # Left
    }

    def readchar():
        # Blocking read on Windows; msvcrt.getch() blocks until a key is pressed
        ch = msvcrt.getch()
        # Special keys are indicated by a prefix 0x00 or 0xe0 followed by a code
        if ch in (b'\x00', b'\xe0'):
            nxt = msvcrt.getch()
            return _WIN_ARROW_MAP.get(nxt, (ch + nxt).decode('utf-8', errors='ignore'))
        s = ch.decode('utf-8', errors='ignore')
        # Normalize Ctrl-H (backspace) -> DEL
        if s == '\x08':
            return '\x7f'
        return s

    def reset():
        pass

else:
    import select
    import termios
    import tty

    def readchar():
        fd = sys.stdin.fileno()
        # Block until at least one byte is available
        select.select([fd], [], [], None)
        b = os.read(fd, 1)
        if not b:
            return None
        ch = b.decode('utf-8', errors='ignore')
        # If an escape was read, try to read the rest of the sequence within a short timeout
        if ch == '\x1b':
            seq = []
            while True:
                dr, _, _ = select.select([fd], [], [], 0.01)
                if dr:
                    more = os.read(fd, 1)
                    if not more:
                        break
                    seq.append(more.decode('utf-8', errors='ignore'))
                else:
                    break
            return ch + ''.join(seq)
        # Normalize Ctrl-H (backspace) -> DEL
        if ch == '\x08':
            return '\x7f'
        return ch

    def reset():
        global _old_settings
        if _old_settings:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _old_settings) 

def init():
    """Sets up the terminal mode."""
    if os.name != 'nt':
        # Only configure the terminal if stdin is a TTY
        if not sys.stdin.isatty():
            return
        global _old_settings
        _old_settings = termios.tcgetattr(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())

class Keys:
    ENTER = '\n'
    BACKSPACE = '\x7f'
    CTRL_C = '\x03'
    LEFT = '\x1b[D'
    RIGHT = '\x1b[C'
    HOME = '\x1b[H'
    END = '\x1b[F'
    DELETE = '\x1b[3~'