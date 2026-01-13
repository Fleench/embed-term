'''
A basic module to embed a terminal-like input in Python applications.
'''
import readchar
INPUT = []
LOC = 0
def init_terminal():
    readchar.init()
def reset_terminal():
    readchar.reset()
def read_input():
    return "".join(INPUT)
def display_input(type = "nl"):
    if type == "nl":
        print("\n> " + "".join(INPUT), end='', flush=True)
    elif type == "sl":
        print("\r> " + "".join(INPUT), end='', flush=True)
    elif type == "er":
        print("\r" + " " * (len(INPUT) + 2) + "\r", end='', flush=True)
    elif type == "cl":
        print("\033c", end='', flush=True)
        print("> " + "".join(INPUT), end='', flush=True)
def clear_input():
    global INPUT
    INPUT = []
    loc = -1
def tick():
    global INPUT
    global LOC
    ch = readchar.readchar()
    if ch == readchar.Keys.CTRL_C:
        raise KeyboardInterrupt
    elif ch == readchar.Keys.BACKSPACE:
        if INPUT:
            INPUT.pop(LOC - 1)
            LOC -= 1
    elif ch == readchar.Keys.ENTER:
        #TODO: raise a flag instead
        clear_input()
    elif ch == readchar.Keys.RIGHT:
        if LOC < len(INPUT):
            LOC += 1
    elif ch == readchar.Keys.LEFT:
        if LOC > 0:
            LOC -= 1
    elif ch is not None:
        if LOC == -1 or LOC == len(INPUT):
            INPUT.append(ch)
            LOC += 1
        else:
            INPUT.insert(LOC, ch)
            LOC += 1
    if LOC < 0:
        LOC = len(INPUT)
        
if __name__ == "__main__":
    try:
        init_terminal()
        print("Type something (Ctrl-C to exit):")
        display_input(type="cl")
        while True:
            tick()
            print( "\n" + str(LOC))
            display_input(type="cl")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        reset_terminal()