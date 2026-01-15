# embed-term

A basic module to embed a terminal-like input in Python applications.

## Features

- Terminal-like input handling with cursor control
- Cross-platform support (Windows, Linux, macOS)
- ANSI escape code support for text formatting
- Raw character input processing

## Installation

```bash
pip install embed-term
```

## Usage

```python
from embed_term import EmbedTerminal

# Create a terminal instance
terminal = EmbedTerminal()

# Initialize the terminal
terminal.init_terminal()

# Read user input
terminal.tick()

# Display input
terminal.display_input()

# Reset terminal
terminal.reset_terminal()
```

## API

### EmbedTerminal

Main class for handling terminal-like input.

#### Methods

- `init_terminal()` - Initialize the terminal for raw input
- `reset_terminal()` - Reset the terminal to normal mode
- `read_input()` - Get the current input as a string
- `display_input(type="sl")` - Display input with prompt
  - `"sl"` - Single line display (default)
  - `"nl"` - New line display
  - `"er"` - Erase display
  - `"cl"` - Clear and redisplay
- `clear_input()` - Clear the input buffer
- `tick()` - Process one character of input

## License

MIT

## Author

Glenn Sutherland
