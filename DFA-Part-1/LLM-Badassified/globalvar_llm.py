"""
globalvar.py
Shared helpers for the DFA project (Part 1).

Provides:
    SPECIAL_ERROR_RISE  - prompt/validate/retry loop
    dfs_accept_reject   - print the verdict and ask whether to continue
    Colors, box drawing, and small UI helpers used by the main script.
"""

import os
import sys


# ---------------------------------------------------------------------------
# Terminal UI helpers
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        # Enable ANSI on modern Windows terminals.
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True


_USE_COLOR = _supports_color()


class C:
    """ANSI color codes. All are no-ops when color is disabled."""
    RESET   = "\033[0m"   if _USE_COLOR else ""
    BOLD    = "\033[1m"   if _USE_COLOR else ""
    DIM     = "\033[2m"   if _USE_COLOR else ""
    RED     = "\033[31m"  if _USE_COLOR else ""
    GREEN   = "\033[32m"  if _USE_COLOR else ""
    YELLOW  = "\033[33m"  if _USE_COLOR else ""
    BLUE    = "\033[34m"  if _USE_COLOR else ""
    MAGENTA = "\033[35m"  if _USE_COLOR else ""
    CYAN    = "\033[36m"  if _USE_COLOR else ""
    WHITE   = "\033[37m"  if _USE_COLOR else ""


WIDTH = 64  # inner width of boxes


def _vis_len(text: str) -> int:
    """Length of a string ignoring ANSI escape sequences."""
    out = 0
    i = 0
    while i < len(text):
        if text[i] == "\033":
            # Skip until 'm'
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
        else:
            out += 1
            i += 1
    return out


def _pad(text: str, width: int = WIDTH) -> str:
    """Right-pad a possibly-colored string to `width` visible characters."""
    return text + " " * max(0, width - _vis_len(text))


def box_top(title: str = "", color: str = C.CYAN) -> None:
    if title:
        line = f"┌─ {title} "
        line += "─" * max(0, WIDTH - _vis_len(line) + 1) + "┐"
    else:
        line = "┌" + "─" * (WIDTH + 1) + "┐"
    print(color + C.BOLD + line + C.RESET)


def box_bottom(color: str = C.CYAN) -> None:
    print(color + C.BOLD + "└" + "─" * (WIDTH + 1) + "┘" + C.RESET)


def box_line(text: str = "", color: str = C.CYAN, indent: int = 2) -> None:
    inner = " " * indent + text
    print(color + "│" + C.RESET + " " + _pad(inner) + " " + color + "│" + C.RESET)


def banner() -> None:
    """Print the project banner."""
    top    = "╔" + "═" * (WIDTH + 1) + "╗"
    mid1   = "║" + "  D F A   S I M U L A T O R  ".center(WIDTH + 1) + "║"
    mid2   = "║" + "  Computation Theory - Part 1  ".center(WIDTH + 1) + "║"
    bottom = "╚" + "═" * (WIDTH + 1) + "╝"
    print()
    print(C.CYAN + C.BOLD + top    + C.RESET)
    print(C.CYAN + C.BOLD + mid1   + C.RESET)
    print(C.CYAN + C.DIM  + mid2   + C.RESET)
    print(C.CYAN + C.BOLD + bottom + C.RESET)
    print()


def section(title: str) -> None:
    """Print a section header box."""
    box_top(title, C.BLUE)
    box_bottom(C.BLUE)
    print()


def prompt(label: str) -> str:
    """Colored input prompt."""
    return C.CYAN + C.BOLD + label + C.RESET + C.CYAN + " " + C.RESET


def err(msg: str) -> None:
    print(C.RED + C.BOLD + "  ✖ ERROR:" + C.RESET + C.RED + " " + msg + C.RESET)


def warn(msg: str) -> None:
    print(C.YELLOW + C.BOLD + "  ⚠ WARNING:" + C.RESET + C.YELLOW + " " + msg + C.RESET)


def ok(msg: str) -> None:
    print(C.GREEN + C.BOLD + "  ✔ " + C.RESET + C.GREEN + msg + C.RESET)


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def SPECIAL_ERROR_RISE(try_function, error_function, *,
                       try_internal_inputs=None,
                       error_internal_inputs=None,
                       initial_function=None):
    """
    Repeatedly call `try_function` and validate its result with
    `error_function` until the validator returns None (meaning "no error").

    Returns the validated value.
    """
    if initial_function is not None:
        initial_function()

    def _attempt():
        value = (try_function() if try_internal_inputs is None
                 else try_function(try_internal_inputs))
        problem = (error_function(value) if error_internal_inputs is None
                   else error_function(value, error_internal_inputs))
        return value, problem

    value, problem = _attempt()
    while problem is not None:
        value, problem = _attempt()

    return value


def dfs_accept_reject(is_accepted: bool, ifexit: bool = False, empty: bool = False) -> None:
    """
    Print the accept/reject verdict, then ask whether to continue.

    Pressing 'y' returns (caller loops for another input string).
    Anything else exits the program.
    """
    arg = "empty" if empty else "the"

    print()
    box_top("RESULT", C.GREEN if is_accepted else C.RED)
    if is_accepted:
        box_line(C.GREEN + C.BOLD + "✔ ACCEPTED" + C.RESET)
        box_line(f"The given DFA accepts {arg} input.  GOOD JOB ;)")
    else:
        box_line(C.RED + C.BOLD + "✖ REJECTED" + C.RESET)
        box_line(f"The given DFA rejects {arg} input.  :(")
    box_bottom(C.GREEN if is_accepted else C.RED)
    print()

    proceed = input(prompt("  Proceed with another input? [y/N]:")).strip().lower()
    if proceed != "y":
        print()
        print(C.CYAN + C.BOLD + "  Goodbye!  👋" + C.RESET)
        print()
        sys.exit(0)
    print()