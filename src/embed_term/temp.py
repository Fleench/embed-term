import embed_term.readchar #pylint: disable=import-error
from embed_term.term import * #pylint: disable=import-error
if __name__ == "__main__":
    mngr = TermManager()
    term1 = EmbedTerminal()
    mngr.add_terminal("main", term1)
    mngr.set_active_terminal("main")
    try:
        readchar.init()
        print("Type something (Ctrl-C to exit):")
        while True:
            x = mngr.tick()
            active_term = mngr.get_active_terminal()
            if active_term:
                print(f"\r\033[K{active_term.display()}", end='', flush=True)
                if x:
                    print()  # Move to next line after the prompt
                    pass
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        readchar.reset()
