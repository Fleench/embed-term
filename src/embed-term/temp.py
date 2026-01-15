import readchar
import sys

def init_terminal():
    readchar.init()

def reset_terminal():
    readchar.reset()

if __name__ == "__main__":
    try:
        init_terminal()
        print("Press HOME and END keys (Ctrl-C to exit):")
        
        while True:
            ch = readchar.readchar()
            
            if ch == readchar.Keys.CTRL_C:
                break
            
            # Print the raw bytes and escape representation
            print(f"Key pressed: {repr(ch)}", flush=True)
                
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        reset_terminal()