tree = ('Program', [('=', ['ID,a', ('A', ['BINARY_LITERAL,111', 'BINARY_LITERAL,11'])])])
last_var = ''
def f(syn_tree):

    global last_var

    if syn_tree[0]== 'Program':
        for t in syn_tree[1]:
            print(t)
            f(t)

    elif syn_tree[0] == '=':
        last_var = syn_tree[1][0]
        print(syn_tree[1][1])
        f(syn_tree[1][1])

    elif syn_tree[0] == 'A':
        print(syn_tree[1][0])
        f(syn_tree[1][0])
        print(syn_tree[1][1])
        f(syn_tree[1][1])

    elif syn_tree[0] == 'S':
        print(syn_tree[1][0])
        f(syn_tree[1][0])
        print(syn_tree[1][1])
        f(syn_tree[1][1])

    elif syn_tree[0] == 'M':
        print(syn_tree[1][0])
        f(syn_tree[1][0])
        print(syn_tree[1][1])
        f(syn_tree[1][1])

    elif syn_tree[0] == 'D':
        print(syn_tree[1][0])
        f(syn_tree[1][0])
        print(syn_tree[1][1])
        f(syn_tree[1][1])

f(tree)

