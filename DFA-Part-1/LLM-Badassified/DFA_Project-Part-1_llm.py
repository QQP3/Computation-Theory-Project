"""
DFA_Project-Part-1.py
Interactive DFA simulator.

Reads a DFA definition from the user, then repeatedly runs input strings
through it and reports ACCEPT / REJECT.

Run:
    python DFA_Project-Part-1.py
"""

from globalvar_llm import (
    SPECIAL_ERROR_RISE, dfs_accept_reject,
    banner, section, prompt, err, warn, ok,
    C,
)


# ---------------------------------------------------------------------------
# 1. STATES
# ---------------------------------------------------------------------------

state_input_function = lambda: input(prompt("  STATES:")).split()
state_error_function = lambda val: (
    err("STATES cannot be empty. Enter at least one state name."), 1
) if val == [] else None

banner()
section("1 · STATES")
states = SPECIAL_ERROR_RISE(state_input_function, state_error_function)
states = set(states)
ok(f"Loaded {len(states)} state(s): {', '.join(sorted(states))}")
print()


# ---------------------------------------------------------------------------
# 2. ALPHABET
# ---------------------------------------------------------------------------

alphabet_input_function = lambda: input(prompt("  ALPHABET:")).split()
alphabet_error_function = lambda val: (
    err("ALPHABET cannot be empty. Enter at least one symbol."), 1
) if val == [] else None

section("2 · ALPHABET (Σ)")
alphabet = SPECIAL_ERROR_RISE(alphabet_input_function, alphabet_error_function)
alphabet = set(alphabet)
ok(f"Loaded {len(alphabet)} symbol(s): {', '.join(sorted(alphabet))}")
print()


# ---------------------------------------------------------------------------
# 3. START
# ---------------------------------------------------------------------------

start_input_function = lambda: input(prompt("  START:")).split()

def start_error_function(val):
    if len(val) == 0:
        err("START cannot be empty. Enter exactly one state name.")
        return 1
    if len(val) > 1:
        err("START must be a single state (no spaces between letters).")
        return 2
    if val[0] not in states:
        err(f"Start state '{val[0]}' is not in STATES. "
            f"Add it to STATES or fix the typo.")
        return 3
    return None

section("3 · START STATE")
start = SPECIAL_ERROR_RISE(start_input_function, start_error_function)[0]
ok(f"Start state: {start}")
print()


# ---------------------------------------------------------------------------
# 4. ACCEPT
# ---------------------------------------------------------------------------

accept_input_function = lambda: input(prompt("  ACCEPT:")).split()

def accept_error_function(val):
    if len(val) == 0:
        err("ACCEPT cannot be empty. List at least one accept state.")
        return 1
    for temp in val:
        if temp not in states:
            err(f"Accept state '{temp}' is not in STATES. "
                f"Add it to STATES or remove it from ACCEPT.")
            return 3
    return None

section("4 · ACCEPT STATES")
accept = SPECIAL_ERROR_RISE(accept_input_function, accept_error_function)
accept = set(accept)
ok(f"Accept state(s): {', '.join(sorted(accept))}")
print()


# ---------------------------------------------------------------------------
# 5. NUMBER OF TRANSITIONS
# ---------------------------------------------------------------------------

transition_num_input_function = lambda: input(prompt("  NUMBER OF TRANSITIONS:")).split()

def transition_num_error_function(val):
    if len(val) == 0:
        err("NUMBER OF TRANSITIONS cannot be empty. Enter a non-negative integer.")
        return 1
    if len(val) > 1:
        err("Enter a single integer, with no spaces between the digits.")
        return 2
    if not val[0].isdigit():
        err("NUMBER OF TRANSITIONS must be a non-negative integer (digits only).")
        return 3
    return None

section("5 · TRANSITIONS")
transition_num = int(
    SPECIAL_ERROR_RISE(transition_num_input_function, transition_num_error_function)[0]
)
print()


# ---------------------------------------------------------------------------
# 6. TRANSITIONS
# ---------------------------------------------------------------------------

each_transitions_input_function = lambda i: input(
    C.CYAN + C.BOLD + f"  {i:>3}) " + C.RESET
).split()

def each_transitions_error_function(val, transactions):
    if len(val) < 3:
        err("Insufficient tokens. Expected: <from_state> <symbol> <to_state>.")
        return 1
    if len(val) > 3:
        err("Too many tokens. Expected exactly: <from_state> <symbol> <to_state>.")
        return 2
    if val[0] not in states:
        err(f"Source state '{val[0]}' is not in STATES.")
        return 3
    if val[1] not in alphabet:
        err(f"Symbol '{val[1]}' is not in ALPHABET.")
        return 4
    if val[2] not in states:
        err(f"Destination state '{val[2]}' is not in STATES.")
        return 5
    existing = transactions.get((val[0], val[1]))
    if existing is not None:
        err(f"A transition from '{val[0]}' on '{val[1]}' already exists "
            f"(→ '{existing}'). A DFA allows at most one.")
        return 6
    return None

if transition_num == 0:
    ok("No transitions to enter.")
    transactions = {}
else:
    ok(f"Enter {transition_num} transition(s), each as: <from> <symbol> <to>")
    print()
    transactions = {}
    for i in range(1, transition_num + 1):
        cnd = SPECIAL_ERROR_RISE(
            each_transitions_input_function,
            each_transitions_error_function,
            try_internal_inputs=i,
            error_internal_inputs=transactions,
        )
        transactions[(cnd[0], cnd[1])] = cnd[2]

print()
ok(f"Loaded {len(transactions)} transition(s).")
print()


# ---------------------------------------------------------------------------
# 7. RUN LOOP
# ---------------------------------------------------------------------------

def dfa_input_input_function():
    return input(prompt("  DFS INPUT:")).split()

def dfa_input_error_function(val):
    if len(val) == 0:
        warn("DFS INPUT is empty — simulating the empty string.")
        return None
    for temp in val:
        if temp not in alphabet:
            err(f"Symbol '{temp}' at position {val.index(temp) + 1} "
                f"is not in ALPHABET.")
            return 3
    return None


section("7 · RUN")
print(C.DIM + "  Enter the input string as space-separated symbols."
      + C.RESET)
print(C.DIM + "  Press Enter on an empty line to test the empty string."
      + C.RESET)
print()

while True:
    dfa_input = SPECIAL_ERROR_RISE(dfa_input_input_function, dfa_input_error_function)

    # Simulate
    is_accept = True
    current_state = start
    for symbol in dfa_input:
        next_state = transactions.get((current_state, symbol))
        if next_state is not None:
            current_state = next_state
        else:
            is_accept = False
            break

    empty = (dfa_input == [])
    verdict = is_accept and (current_state in accept)

    # Trace (helpful for debugging)
    if dfa_input:
        trace = start
        state = start
        for sym in dfa_input:
            nxt = transactions.get((state, sym))
            if nxt is None:
                trace += f" --{sym}--> ⊥"
                break
            trace += f" --{sym}--> {nxt}"
            state = nxt
        print(C.DIM + "  Trace: " + trace + C.RESET)

    dfs_accept_reject(verdict, empty=empty)
