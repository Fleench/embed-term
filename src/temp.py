import embed_term.readchar as readchar
import embed_term.term as term
def disp(term):
    readchar.clear()
    disp_i = term.display()
    print(readchar.Keys.HOME, end='', flush=True)
    for line in disp_i[0]:
        print(line)
    print(f"\r\033[K{disp_i[1]}", end='', flush=True)
if __name__ == "__main__":
    mngr = term.TermManager()
    term1 = term.EmbedTerminal()
    mngr.add_terminal("main", term1)
    mngr.set_active_terminal("main")
    try:
        readchar.init()
        print("Type something (Ctrl-C to exit):", end='\n\n', flush=True)
        y = ""
        while True:
            active_term = mngr.get_active_terminal()
            if active_term:
                disp(active_term)
                x = mngr.tick()
                disp(active_term)
                if x:
                    active_term.output.append(active_term.prompt + active_term.read_input())
                    if active_term.read_input() == "---":
                        active_term.output.append(f"size of last input is {len(y)} chars")
                    print()  # Move to next line after the prompt
                    y = active_term.read_input()
                    active_term.clear_input()
                    disp(active_term)
                    

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        readchar.reset()
