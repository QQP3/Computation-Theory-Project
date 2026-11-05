
<div align="center">

# 🧠 Computation Theory Project

### DFA Simulator — Part 1

An interactive, crash-proof Deterministic Finite Automaton simulator written in pure Python.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![No Dependencies](https://img.shields.io/badge/Dependencies-none-brightgreen.svg)](#-requirements)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Quick Start](#-quick-start)
- [Input Format](#-input-format)
- [Output & Interaction](#-output--interaction)
- [Worked Example](#-worked-example)
- [Error Handling](#-error-handling)
- [Behavior Notes](#-behavior-notes)
- [Troubleshooting](#-troubleshooting)
- [Development Notes (LLM-Assisted)](#-development-notes-llm-assisted)
- [License](#-license)

---

## 🔎 Overview

This project implements an **interactive Deterministic Finite Automaton (DFA) simulator**.

You describe a DFA by answering a series of prompts (states, alphabet, start state,
accept states, and transitions). The program then repeatedly asks for an input
string and tells you whether the DFA **accepts** or **rejects** it.

The simulator is designed to **never crash on bad input**. Every invalid entry
produces a descriptive, colored error message and re-prompts for the *same*
field, so you can fix the mistake without restarting.

There are two implementations side by side:

| Folder | Description |
|---|---|
| `Original/` | The reference implementation |
| `LLM-Badassified/` | An LLM-improved variant of the same program |

Both behave identically from the user's point of view.

---

## 🌳 Project Structure

```
Computation-Theory-Project/
├── README.md
└── DFA-Part-1/
    ├── LLM-Badassified/
    │   ├── DFA_Project-Part-1_llm.py
    │   └── globalvar_llm.py
    └── Original/
        ├── DFA_Project-Part-1.py
        └── globalvar.py
```

> ⚠️ **Important — import path**
> Each main script imports its helper as `from globalvar import ...`.
> Python adds the *script's own directory* to the import path, so this works
> automatically **only if the helper file is named `globalvar.py` and sits next
> to the main script.**
>
> - In `Original/` the files are already named correctly — just run it.
> - In `LLM-Badassified/` the helper is named `globalvar_llm.py`. Either:
>   - rename it to `globalvar.py`, **or**
>   - edit the first line of `DFA_Project-Part-1_llm.py` to
>     `from globalvar_llm import ...`.

---

## ⚙️ Requirements

- **Python 3.6 or newer**
- **No third-party packages** — everything uses the standard library.
- A terminal that supports ANSI colors (optional; colors auto-disable otherwise).

---

## 🚀 Quick Start

```bash
# 1. Clone / download the project
cd Computation-Theory-Project/DFA-Part-1/Original

# 2. Run the simulator
python DFA_Project-Part-1.py
```

Or, from the project root:

```bash
python DFA-Part-1/Original/DFA_Project-Part-1.py
```

To run the LLM variant (after renaming the helper as noted above):

```bash
python DFA-Part-1/LLM-Badassified/DFA_Project-Part-1_llm.py
```

---

## 📝 Input Format

The program prompts you line by line. On each line, **tokens are separated by
spaces**. Multi-character state names and multi-character alphabet symbols are
both supported.

### 1. `STATES:`

All state names, space-separated. State names may be any non-space token.
**Cannot be empty.**

```
STATES: q0 q1 q2 q3
```

### 2. `ALPHABET:`

All input symbols (Σ), space-separated. Symbols may be multiple characters,
but each symbol is a single space-separated token.
**Cannot be empty.**

```
ALPHABET: 0 1
```

### 3. `START:`

Exactly **one** state — the start state. Must appear in `STATES`.

```
START: q0
```

### 4. `ACCEPT:`

One or more accept states, space-separated. Every state listed must appear in
`STATES`. **Cannot be empty.**

```
ACCEPT: q3
```

### 5. `NUMBER OF TRANSITIONS:`

A **non-negative integer** (digits only, no spaces). Tells the program how many
transition lines follow. `0` is allowed and skips the transition section.

```
NUMBER OF TRANSITIONS: 8
```

### 6. Transition lines — `<from_state> <symbol> <to_state>`

Exactly **three** space-separated tokens per line:

| Token | Meaning | Rule |
|---|---|---|
| 1 | Source state | must be in `STATES` |
| 2 | Input symbol | must be in `ALPHABET` |
| 3 | Destination state | must be in `STATES` |

A DFA allows **at most one** transition per `(state, symbol)` pair; a duplicate
is rejected with an error.

```
1) q0 0 q1
2) q0 1 q0
3) q1 0 q2
4) q1 1 q0
5) q2 0 q3
6) q2 1 q2
7) q3 0 q3
8) q3 1 q3
```

### 7. `DFS INPUT:`

The string to test, as space-separated symbols. Each token must be in
`ALPHABET`. **An empty line is valid** — it tests the empty string (ε), and a
warning is printed to confirm.

```
DFS INPUT: 0 1 0 1
```

> 💡 The prompt says "DFS INPUT" (not "DFA") to match the assignment wording.
> It refers to the **input string**, not the machine.

---

## 🖥 Output & Interaction

After simulating, the program prints a colored result card:

```
┌─ RESULT ───────────────────────────────────────────────────────────────┐
│  ✔ ACCEPTED                                                           │
│  The given DFA accepts the input.  GOOD JOB ;)                        │
└───────────────────────────────────────────────────────────────────────┘
```

or

```
┌─ RESULT ───────────────────────────────────────────────────────────────┐
│  ✖ REJECTED                                                           │
│  The given DFA rejects the input.  :(                                 │
└───────────────────────────────────────────────────────────────────────┘
```

For the empty string the word `empty` replaces `the`:

```
The given DFA accepts empty input.  GOOD JOB ;)
```

It then asks:

```
  Proceed with another input? [y/N]:
```

- Type **`y`** + Enter → enter another `DFS INPUT:` for the **same** DFA.
- Type anything else (or just Enter) → exit cleanly.

When the input is non-empty, a **trace** is printed before the verdict so you
can see the path taken:

```
  Trace: q0 --0--> q1 --1--> q0 --0--> q1 --0--> q2
```

If a transition is missing, the trace shows `⊥` (dead end):

```
  Trace: q0 --1--> q0 --1--> q0 --1--> ⊥
```

---

## 🧪 Worked Example

A DFA over `{0, 1}` that accepts exactly the strings containing `000`.

**Definition:**

```
STATES: q0 q1 q2 q3
ALPHABET: 0 1
START: q0
ACCEPT: q3
NUMBER OF TRANSITIONS: 8
```

**Transitions:**

| From | Symbol | To |
|------|--------|----|
| q0 | 0 | q1 |
| q0 | 1 | q0 |
| q1 | 0 | q2 |
| q1 | 1 | q0 |
| q2 | 0 | q3 |
| q2 | 1 | q2 |
| q3 | 0 | q3 |
| q3 | 1 | q3 |

**Sample session:**

```
STATES: q0 q1 q2 q3
ALPHABET: 0 1
START: q0
ACCEPT: q3
NUMBER OF TRANSITIONS: 8
1) q0 0 q1
2) q0 1 q0
3) q1 0 q2
4) q1 1 q0
5) q2 0 q3
6) q2 1 q2
7) q3 0 q3
8) q3 1 q3
DFS INPUT: 0 0 0
  Trace: q0 --0--> q1 --0--> q2 --0--> q3
  ✔ ACCEPTED
  Proceed with another input? [y/N]: y
DFS INPUT: 1 1
  Trace: q0 --1--> q0 --1--> q0
  ✖ REJECTED
  Proceed with another input? [y/N]: n
  Goodbye!  👋
```

---

## 🛡 Error Handling

Every field is validated **before** it is used. On an invalid entry, the
program prints a red error message and **re-prompts for the same field** —
without restarting and without crashing.

| Situation | What you see |
|---|---|
| Empty `STATES` | `✖ ERROR: STATES cannot be empty. Enter at least one state name.` |
| Empty `ALPHABET` | `✖ ERROR: ALPHABET cannot be empty. Enter at least one symbol.` |
| Empty / multi-token `START` | `✖ ERROR: START must be a single state ...` |
| `START` not in `STATES` | `✖ ERROR: Start state 'q9' is not in STATES. ...` |
| Empty `ACCEPT` | `✖ ERROR: ACCEPT cannot be empty. List at least one accept state.` |
| `ACCEPT` state not in `STATES` | `✖ ERROR: Accept state 'q7' is not in STATES. ...` |
| Non-integer transition count | `✖ ERROR: NUMBER OF TRANSITIONS must be a non-negative integer ...` |
| Transition with ≠ 3 tokens | `✖ ERROR: Insufficient tokens. Expected: <from_state> <symbol> <to_state>.` |
| Unknown state in transition | `✖ ERROR: Source state 'qX' is not in STATES.` |
| Symbol not in alphabet | `✖ ERROR: Symbol '2' is not in ALPHABET.` |
| Duplicate transition | `✖ ERROR: A transition from 'q0' on '0' already exists ...` |
| DFS input symbol not in alphabet | `✖ ERROR: Symbol '2' at position 3 is not in ALPHABET.` |
| Empty DFS input | `⚠ WARNING: DFS INPUT is empty — simulating the empty string.` |

The program **never raises an unhandled exception** for any of the above.

---

## 📌 Behavior Notes

- **Partial DFAs are allowed.** A state need not define a transition for every
  symbol. If the simulation reaches a state with no transition on the next
  symbol, the input is **rejected** (no crash). Missing transitions appear as
  `⊥` in the trace.
- **Multi-character symbols** are supported. An alphabet of `ab cd` means two
  symbols, `ab` and `cd` — type them as space-separated tokens in `DFS INPUT:`.
- **Empty string** — press Enter on an empty `DFS INPUT:` line to test ε.
- **Colors auto-disable** when `NO_COLOR` is set, when stdout is piped/redirected,
  or on a Windows terminal without ANSI support. The program remains fully
  usable in all cases.
- **No files are read or written** — everything is interactive.

---

## 🔧 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'globalvar'` | Helper file is not named `globalvar.py` or is in a different folder | Rename `globalvar_llm.py` → `globalvar.py`, **or** change the import in the main script to `from globalvar_llm import ...` |
| `ModuleNotFoundError: No module named 'globalvar_llm'` | Same, reversed | Run from the folder that contains the helper, or fix the import |
| Boxes look misaligned | Terminal font not monospaced, or a very long title | Use a monospaced font; keep section titles short |
| No colors | Output is piped, `NO_COLOR` is set, or old terminal | Run in an interactive terminal; unset `NO_COLOR` |
| `python: command not found` | Python not installed / not on `PATH` | Install Python 3.8+ and use `python3` on macOS/Linux |

---

## 🤖 Development Notes (LLM-Assisted)

Parts of this project — the input-format design, the validation logic, and the
UI polish — were developed with the help of a large language model, iteratively.
The full conversation, including the review rounds where bugs were found and
fixed, is preserved publicly so anyone can follow the reasoning and see how the
code evolved:

> 📎 **Full LLM conversation & review history:**
> https://chat.deepseek.com/share/atp0szyad2sy3rjpez

### How the process went

1. **Design.** We discussed the input format for a DFA (sectioned text file vs.
   interactive prompts, how to handle multi-character symbols, how to validate
   determinism, etc.) and settled on an **interactive prompt-based format**
   with one field per line and space-separated tokens.
2. **First implementation.** The original script was written by hand. The
   `SPECIAL_ERROR_RISE` / `dfs_accept_reject` helpers were extracted into
   `globalvar.py` so the main driver could stay readable.
3. **Review rounds.** The code was reviewed several times against the stated
   format spec. Each round found a real bug — for example:
   - `accept = SPECIAL_ERROR_RISE(...)[0]` was truncating the accept set to a
     single string, so `set(accept)` produced a set of *characters*;
   - `transactions[(from, sym)]` in the validator raised `KeyError` on the
     first non-duplicate transition;
   - the empty-input path re-prompted forever because the validator returned a
     truthy tuple instead of `None`;
   - a later `empty` flag was referenced before assignment, causing a
     `NameError` on the first non-empty run.
   Each fix was verified before moving on. The final `Original/` version
   reflects the last verified state.
4. **Polish.** A second pass — the `LLM-Badassified/` variant — added the
   banner, colored prompts, boxed result card, and a per-run trace, without
   changing any simulation logic.

### Why keep the chat public

- **Transparency** — reviewers can see exactly which parts were LLM-assisted
  and which were written by hand.
- **Reproducibility** — the bug-fix trail shows *why* each guard exists, which
  is useful for anyone extending the project (e.g. adding NFAs or ε-transitions).
- **Learning** — it's a concrete example of using an LLM as a *reviewer*
  rather than a *generator*: the model was most useful when it pushed back on
  the code, not when it wrote it.

### Scope of LLM involvement

| Area | Written by | Reviewed by LLM |
|---|---|---|
| Input format spec | Hand | ✅ |
| `SPECIAL_ERROR_RISE` | Hand | ✅ |
| Field validators | Hand | ✅ |
| Simulation loop | Hand | ✅ |
| `globalvar_llm.py` UI helpers | LLM | ✅ |
| `LLM-Badassified/` variant | LLM | ✅ |
| This README | Hand + LLM | ✅ |

> 💡 If you fork this project, feel free to replace the link above with your
> own conversation and keep the table accurate to your own process.

---

## 📜 License

MIT License — free to use, modify, and distribute for academic and personal
purposes.

---

<div align="center">

**Made with 🐍 and a lot of `:)` / `:(`**

</div>
