'''
A basic module to embed a terminal-like input in Python applications.
'''
from . import readchar
import sys
class EmbedTerminal:

    def __init__(self):
        self.INPUT = []
        self.LOC = 0
    def init_terminal(self):
        readchar.init()

    def reset_terminal(self):
        readchar.reset()

    def read_input(self):
        return "".join(self.INPUT)

    def display_input(self,type="sl"):
        prompt = "> "
        content = "".join(self.INPUT)
        
        if type == "nl":
            print("\n" + prompt + content, end='', flush=True)
        elif type == "sl":
            # \r: Go to start of line
            # \033[K: Clear everything currently on the line
            print(f"\r\033[K{prompt}{content}", end='', flush=True)
            
            # Calculate how far to move cursor back from the end
            back_steps = len(self.INPUT) - self.LOC
            if back_steps > 0:
                # \033[ND: Move cursor left N times
                print(f"\033[{back_steps}D", end='', flush=True)
                
        elif type == "er":
            print("\r\033[K", end='', flush=True)
        elif type == "cl":
            print("\033c", end='', flush=True)
            self.display_input(type="sl")

    def clear_input(self):
        self.INPUT = []
        self.LOC = 0

    def tick(self):
        ch = readchar.readchar()
        
        if ch == readchar.Keys.CTRL_C:
            raise KeyboardInterrupt
        
        elif ch == readchar.Keys.BACKSPACE:
            if self.INPUT and self.LOC > 0:
                self.INPUT.pop(self.LOC - 1)
                self.LOC -= 1
                
        elif ch == readchar.Keys.ENTER:
            # Returning True to signal the main loop that a command was submitted
            return True
            
        elif ch == readchar.Keys.RIGHT:
            if self.LOC < len(self.INPUT):
                self.LOC += 1
                
        elif ch == readchar.Keys.LEFT:
            if self.LOC > 0:
                self.LOC -= 1
        elif ch == readchar.Keys.UP or ch == readchar.Keys.DOWN:
            return False
        elif ch == readchar.Keys.DELETE:
            if self.LOC < len(self.INPUT):
                self.INPUT.pop(self.LOC)
                # Note: LOC doesn't change because the string shifts left into the cursor
        elif ch == readchar.Keys.HOME:
            self.LOC = 0
        elif ch == readchar.Keys.END:
            self.LOC = len(self.INPUT)
        elif ch is not None:
            # Handle regular character insertion
            if self.LOC == len(self.INPUT):
                self.INPUT.append(ch)
            else:
                self.INPUT.insert(self.LOC, ch)
            self.LOC += 1
        return False

if __name__ == "__main__":
    term = EmbedTerminal()
    try:
        term.init_terminal()
        print("Type something (Ctrl-C to exit):")
        term.display_input(type="nl")
        
        while True:
            submitted = term.tick()
            
            if submitted:
                current_text = term.read_input()
                print()  # Move to next line after the prompt
                if "quit" in current_text:
                    break
                print(f"Submitting: {current_text}")
                term.clear_input()
                term.display_input(type="nl")
            else:
                term.display_input(type="sl")
                
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        term.reset_terminal()
