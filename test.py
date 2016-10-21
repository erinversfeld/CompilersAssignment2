('Program', [])
('=', [])
['ID,a', ('A', ['BINARY_LITERAL,111', 'BINARY_LITERAL,11'])]
last_var = ""
var_dict = {}

def code_gen(tree):
    global last_var

    if isinstance(tree[0], tuple):
        tree = list(tree[0])

    if tree[0] == 'Program':
        for t in tree[1][0:]:
            code_gen(t)
    elif tree[0] == '=':
        last_var = tree[1][0] A
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        if isinstance(tree[1][1], tuple):
            t_ = list(tree[1][1])
            builder.store(code_gen(t_), var_dict[last_var])
        else:
            if not isinstance(tree[1][1],list) and not isinstance(tree[1][1], tuple):
                builder.store(code_gen([(tree[1][1])]), var_dict[last_var])
            else:
                builder.store(code_gen(tree[1][1]), var_dict[last_var])

    elif tree[0] == 'A':
        return(builder.add(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'S':
        return(builder.sub(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'M':
        return(builder.mul(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'D':
        return(builder.sdiv(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0].isalpha():
        return(builder.load(var_dict[tree[0]]))

    elif tree[0].isnumeric():
        return(ir.Constant(ir.IntType(32), int(str(tree[0]),2)))
