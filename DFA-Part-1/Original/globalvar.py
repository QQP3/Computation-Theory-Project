def SPECIAL_ERROR_RISE(try_function, error_function, *, try_internal_inputs = None, error_internal_inputs = None, initial_function = None):
    if initial_function != None:
        initial_function()

    #init_input_not_none = lambda func, val: func(val) if val is not None else func()
    
    try_value = try_function() if try_internal_inputs is None else try_function(try_internal_inputs)
    error_rise = error_function(try_value) if error_internal_inputs is None else error_function(try_value, error_internal_inputs)
    while(error_rise != None):
        try_value = try_function() if try_internal_inputs is None else try_function(try_internal_inputs)
        error_rise = error_function(try_value) if error_internal_inputs is None else error_function(try_value, error_internal_inputs)
    
    return try_value


def dfs_accept_reject(is_accepted, ifexit = False, empty = False):
    arg = "empty" if empty else "the"

    if is_accepted:
        print(f"The given dfs accepts {arg} input, GOOD JOB ;)")
    else:
        print(f"OH NOOO, the given dfs rejects {arg} input :(")

    proceed = input("if you wish to proceed press y and Enter if not press any key and Enter: ")

    if proceed != 'y':
        exit()

    return None