import sys
import os

# We move these to the top level so they are available to all functions
_old_settings = None

if os.name == 'nt':
    import msvcrt
    
    def readchar():
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8', errors='ignore')
        return None

    def reset():
        pass

else:
    import select
    import termios
    import tty

    def readchar():
        # select.select makes it non-blocking
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None

    def reset():
        global _old_settings
        if _old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _old_settings)

def init():
    """Sets up the terminal mode."""
    if os.name != 'nt':
        global _old_settings
        _old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())