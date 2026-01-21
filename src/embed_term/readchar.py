import sys
import os
# We move these to the top level so they are available to all functions
_old_settings = None

if os.name == 'nt':
    import msvcrt # pylint: disable=import-error

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
    UP = '\x1b[A'
    DOWN = '\x1b[B'
class Codes:
    # Base Control Sequence Introducer
    CSI = "\033["

    @staticmethod
    def pos(row, col):
        """Sets the cursor to a specific row and column."""
        return f"{Codes.CSI}{row};{col}H"

    @staticmethod
    def up(n=1):
        """Moves the cursor up n lines."""
        return f"{Codes.CSI}{n}A"

    @staticmethod
    def down(n=1):
        """Moves the cursor down n lines."""
        return f"{Codes.CSI}{n}B"

    @staticmethod
    def right(n=1):
        """Moves the cursor forward (right) n columns."""
        return f"{Codes.CSI}{n}C"

    @staticmethod
    def left(n=1):
        """Moves the cursor backward (left) n columns."""
        return f"{Codes.CSI}{n}D"

    @staticmethod
    def clear_screen():
        """Clears the entire screen and moves cursor to home."""
        return f"{Codes.CSI}2J{Codes.CSI}H"

    @staticmethod
    def clear_line():
        """Clears the line from the cursor position to the end."""
        return f"{Codes.CSI}K"

    @staticmethod
    def hide_cursor():
        return f"{Codes.CSI}?25l"

    @staticmethod
    def show_cursor():
        return f"{Codes.CSI}?25h"
    @staticmethod
    def set_col(n):
        return f"{Codes.CSI}{n}G"
    @staticmethod
    def set_row(n):
        return f"{Codes.CSI}{n}d"