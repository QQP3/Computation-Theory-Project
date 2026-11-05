from globalvar import *

state_input_function = lambda : input("STATES: ").split()
state_error_function = lambda val: (print("ERROR: STATE CANNOT BE EMPTY!"), 1) if val == [] else None

states = SPECIAL_ERROR_RISE(state_input_function, state_error_function)
states = set(states)



alphabet_input_function = lambda : input("ALPHABET: ").split()
alphabet_error_function = lambda val: (print("ERROR: ALPHABET CANNOT BE EMPTY!"), 1) if val == [] else None

alphabet = SPECIAL_ERROR_RISE(alphabet_input_function, alphabet_error_function)
alphabet = set(alphabet)



start_input_function = lambda : input("START: ").split()
start_error_function = lambda val: (print("ERROR: START CANNOT BE EMPTY!"), 1) if len(val) == 0 else (print("ERROR: THE INTPUT CANNOT CONTAIN SPACE INBETWEEN THE LETERS!"), 2) if len(val) > 1 else (print("ERROR: START STATE MUST BE IN THE STATES!"), 3) if val[0] not in states else None 

start = SPECIAL_ERROR_RISE(start_input_function, start_error_function)[0]



accept_input_function = lambda : input("ACCEPT: ").split()
def accept_error_function(val):
    if len(val) == 0:
        return (print("ERROR: ACCEPT CANNOT BE EMPTY!"), 1)

    for temp in val:
        if temp not in states:
            return (print(f"ERROR {temp}: ACCEPT STATE MUST BE IN THE STATES!"), 3)

    return None

accept = SPECIAL_ERROR_RISE(accept_input_function, accept_error_function)
accept = set(accept)


transition_num_input_function = lambda : input("NUMBER OF TRANSITIONS: ").split()
transition_num_error_function = lambda val: (print("ERROR: NUMBER OF TRANSITIONS CANNOT BE EMPTY!"), 1) if len(val) == 0 else (print("ERROR: THE INTPUT CANNOT CONTAIN SPACE INBETWEEN THE DIGITS!"), 2) if len(val) > 1 else (print("ERROR: NUMBER OF TRANSITIONS MUST BE A DIGIT!"), 3) if not val[0].isdigit() else None 

transition_num = int(SPECIAL_ERROR_RISE(transition_num_input_function, transition_num_error_function)[0])



each_transitions_input_function = lambda i: input(f"{i}) ").split()
def  each_transitions_error_function(val, transactions):
    if len(val) < 3:
        return(print("ERROR: INSUFFICIENT NUMBER OF VARIABLES!"), 1)

    if len(val) > 3:
        return(print("ERROR: TOO MENY VARIABLES!"), 2)

    if val[0] not in states:
        return (print(f"ERROR: VARIABLE {val[0]} IS NOT IN STATES!"), 3)

    if val[1] not in alphabet:
        return (print(f"ERROR: THE LETTER {val[1]} IS NOT IN ALPHABET"), 4)

    if val[2] not in states:
        return (print(f"ERROR: THE VARIABLE {val[2]} IS NOT IN STATES!"), 5)

    temp = transactions.get((val[0], val[1]))
    if temp != None:
        return (print(f"ERROR: A PATH FROM STATE {val[0]} VIA LETTER {val[1]} TO STATE {temp} ALLREADY EXITS! "), 6)
    return None

transactions = {}

print("TRANSITIONS: ")
for i in range(1, transition_num + 1):
    cnd = SPECIAL_ERROR_RISE(each_transitions_input_function, each_transitions_error_function, try_internal_inputs = i, error_internal_inputs = transactions)
    transactions[(cnd[0], cnd[1])] = cnd[2]


dfa_input_input_function = lambda : input("DFS INPUT: ").split()
def dfa_input_error_function(val):
    if len(val) == 0:
        print("WARNING: DFS INPUT IS EMPTY!")
        #return (dfs_accept_reject(start in accept, empty = True), 1)
        return None

    #if len(val) > 1:
    #    (print("ERROR: THE INTPUT CANNOT CONTAIN SPACE INBETWEEN THE LETERS!"), 2)

    for temp in val:
        if temp not in alphabet:
            return (print(f"ERROR: THE LETER {temp} IS NOT IN ALPHABET!"), 3)
        
    return None

while True:
    dfa_input = SPECIAL_ERROR_RISE(dfa_input_input_function, dfa_input_error_function)

    is_accept = True
    current_state = start
    for cnd in dfa_input:
        next_state = transactions.get((current_state, cnd))
        if next_state:
            current_state = next_state
        else:
            is_accept = False
            break
    
    empty = False
    if dfa_input == []:
        empty = True

    dfs_accept_reject(is_accept and current_state in accept, empty = empty)