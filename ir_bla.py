from llvmlite import ir
from parse_bla import generate_tree
import sys

last_var = ""
var_dict = {}
args = sys.argv


def code_gen(tree):
    global last_var
    first = tree[1][0]
    second = tree[1][1]

    if isinstance(tree[0], tuple):
        tree = list(tree[0])
    if tree[0] == 'Program':
        for t in tree[1][0:]:
            code_gen(t)

    elif tree[0] == '=':
        last_var = first
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        if isinstance(second, tuple):
            t_ = list(second)
            builder.store(code_gen(t_), var_dict[last_var])
        elif not isinstance(second, list) and not isinstance(second, tuple):
            builder.store(code_gen([(second)]), var_dict[last_var])
        else:
            builder.store(code_gen(second), var_dict[last_var])

    elif tree[0] == 'A':
        return (builder.add(code_gen([first]), code_gen([second])))

    elif tree[0] == 'S':
        return (builder.sub(code_gen([first]), code_gen([second])))

    elif tree[0] == 'M':
        return (builder.mul(code_gen([first]), code_gen([second])))

    elif tree[0] == 'D':
        return (builder.sdiv(code_gen([first]), code_gen([second])))

    elif tree[0].isalpha():
        return (builder.load(var_dict[tree[0]]))

    elif tree[0].isnumeric():
        return (ir.Constant(ir.IntType(32), int(str(tree[0]), 2)))


inttyp = ir.IntType(32)
fnctyp = ir.FunctionType(inttyp, ())
module = ir.Module(name="bla")
func = ir.Function(module, fnctyp, name="main")
block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)


def get_module():
    inputfile = open(args[1], 'r').read()
    filename = str(args[1])[:len(args[1]) - 3] + 'ir'
    output = open(filename, 'w')
    tree = generate_tree(inputfile)

    code_gen(tree)
    builder.ret(builder.load(var_dict[last_var]))  # Specifies the return value
    output.write(str(module))
    return module


def main():
    inputfile = open(args[1], 'r').read()
    filename = str(sys.argv[1])
    output = open(filename[:len(filename) - 3] + 'ir', 'w')
    tree = generate_tree(inputfile)

    builder.ret(builder.load(var_dict[last_var]))
    output.write(str(module))


if __name__ == "__main__":
    main()
