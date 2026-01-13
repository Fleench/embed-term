'''
A basic module to embed a terminal-like input in Python applications.
'''
import readchar
import sys

INPUT = []
LOC = 0

def init_terminal():
    readchar.init()

def reset_terminal():
    readchar.reset()

def read_input():
    return "".join(INPUT)

def display_input(type="sl"):
    prompt = "> "
    content = "".join(INPUT)
    
    if type == "nl":
        print("\n" + prompt + content, end='', flush=True)
    elif type == "sl":
        # \r: Go to start of line
        # \033[K: Clear everything currently on the line
        print(f"\r\033[K{prompt}{content}", end='', flush=True)
        
        # Calculate how far to move cursor back from the end
        back_steps = len(INPUT) - LOC
        if back_steps > 0:
            # \033[ND: Move cursor left N times
            print(f"\033[{back_steps}D", end='', flush=True)
            
    elif type == "er":
        print("\r\033[K", end='', flush=True)
    elif type == "cl":
        print("\033c", end='', flush=True)
        display_input(type="sl")

def clear_input():
    global INPUT, LOC
    INPUT = []
    LOC = 0

def tick():
    global INPUT, LOC
    ch = readchar.readchar()
    
    if ch == readchar.Keys.CTRL_C:
        raise KeyboardInterrupt
    
    elif ch == readchar.Keys.BACKSPACE:
        if INPUT and LOC > 0:
            INPUT.pop(LOC - 1)
            LOC -= 1
            
    elif ch == readchar.Keys.ENTER:
        # Returning True to signal the main loop that a command was submitted
        return True
        
    elif ch == readchar.Keys.RIGHT:
        if LOC < len(INPUT):
            LOC += 1
            
    elif ch == readchar.Keys.LEFT:
        if LOC > 0:
            LOC -= 1
    elif ch == readchar.Keys.DELETE:
        if LOC < len(INPUT):
            INPUT.pop(LOC)
            # Note: LOC doesn't change because the string shifts left into the cursor
    elif ch == readchar.Keys.HOME:
        LOC = 0
    elif ch == readchar.Keys.END:
        LOC = len(INPUT)
    elif ch is not None:
        # Handle regular character insertion
        if LOC == len(INPUT):
            INPUT.append(ch)
        else:
            INPUT.insert(LOC, ch)
        LOC += 1
    return False

if __name__ == "__main__":
    try:
        init_terminal()
        print("Type something (Ctrl-C to exit):")
        display_input(type="nl")
        
        while True:
            submitted = tick()
            
            if submitted:
                current_text = read_input()
                print()  # Move to next line after the prompt
                if "quit" in current_text:
                    break
                print(f"Submitting: {current_text}")
                clear_input()
                display_input(type="nl")
            else:
                display_input(type="sl")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        reset_terminal()