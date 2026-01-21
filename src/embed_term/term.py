'''
A basic module to embed a terminal-like input in Python applications.
'''
#from . import readchar
from . import readchar
import sys
import os
import math
'''
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
'''
class EmbedTerminal:
    '''
    A basic class to embed a terminal-like input in Python applications.
    '''
    
    def __init__(self):
        self.input = []
        self.loc = 0
        self.prompt = ">"
        self.output = []
    def display(self):
        width = os.get_terminal_size().columns
        lines_to_go_up = math.ceil(len(self.prompt+ "".join(self.input))/width)-1
        up = readchar.Codes.up(lines_to_go_up)
        if lines_to_go_up == 0:
            up = ""
        input_line = f"{up}{self.prompt}{"".join(self.input)}{readchar.Codes.set_col(1 + len(self.prompt.encode() + "".join(self.input)[:self.loc].encode()))}"
        return self.output, input_line
    def add_char(self, ch):
        self.input.insert(self.loc, ch)
        self.loc += len(ch)
    def remove_char(self):
        if self.loc > 0:
            x = self.input.pop(self.loc - 1)
            self.loc -= len(x)
    def clear_input(self):
        self.input = []
        self.loc = 0
    def read_input(self):
        return "".join(self.input)
class TermManager:
    '''
    An upgraded terminal manager to handle multiple EmbedTerminal instances.
    '''
    def __init__(self):
        self.terminals = {}
        self.active_terminal = None

    def add_terminal(self, name, term):
        self.terminals[name] = term

    def remove_terminal(self, name):
        self.terminals.pop(name, None)

    def set_active_terminal(self, name):
        self.active_terminal = self.terminals.get(name, None)

    def get_active_terminal(self):
        return self.active_terminal

    def tick(self):
        '''
        Processes input and returns True if a command was submitted (Enter),
        otherwise returns False.
        '''
        if not self.active_terminal:
            return False

        x = readchar.readchar()
        if not x:
            return False

        match x:
            case readchar.Keys.CTRL_C:
                raise KeyboardInterrupt
            
            case readchar.Keys.BACKSPACE:
                self.active_terminal.remove_char()
                
            case readchar.Keys.ENTER:
                return True
                
            case readchar.Keys.LEFT:
                if self.active_terminal.loc > 0:
                    # Decrement location based on the size of the previous character
                    self.active_terminal.loc -= 1 
                    
            case readchar.Keys.RIGHT:
                if self.active_terminal.loc < len(self.active_terminal.input):
                    self.active_terminal.loc += 1
            
            case readchar.Keys.DELETE:
                # Remove the character at the current cursor position
                if self.active_terminal.loc < len(self.active_terminal.input):
                    self.active_terminal.input.pop(self.active_terminal.loc)
            
            case readchar.Keys.HOME:
                self.active_terminal.loc = 0
                
            case readchar.Keys.END:
                self.active_terminal.loc = len(self.active_terminal.input)
                
            case _:
                # Ignore UP/DOWN arrows if not implemented
                if x in (readchar.Keys.UP, readchar.Keys.DOWN):
                    return False
                # Insert regular characters at current location
                self.active_terminal.add_char(x)
        
        return False
