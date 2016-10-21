from llvmlite import ir
import sys
import parse_bla as parser

#track last variable assigned
last_var = ''
#variable names associated with memory locations
var_dict = {}

def code_gen(tree):
    global last_var

    #sort out the first element
    if isinstance(tree[0], tuple):
        tree = list(tree[0])
    if tree[0] == 'Program':
        for t in tree[1]:
            code_gen(t)

    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        t = tree[1][1]
        if isinstance(t, tuple):
            t_ = list(t)
            builder.store(code_gen(t_), var_dict[last_var])
        elif not isinstance(t, list) and not isinstance(t, tuple):
            builder.store(code_gen([(t)]), var_dict[last_var])
        else:
            builder.store(code_gen(t), var_dict[last_var])

    elif tree[0] == "A":
        return(builder.add(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == "S":
        return(builder.sub(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == "M":
        return(builder.mul(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == "D":
        return(builder.sdiv(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0].isalpha():
        return(builder.load(var_dict[tree[0]]))

    elif tree[0].isnumeric():
        return(ir.Constant(ir.IntType(32), int(str(tree[0]),2)))

inttyp = ir.IntType(32) # create float type
fnctyp = ir.FunctionType(inttyp, ()) # create function type to return a float
module = ir.Module(name="bla") # create module named "lang"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code

args = sys.argv

def get_module():
    filename = str(args[1])[0:len(str(args[1]))-3]+"ir"
    w = open(filename, "w")
    tree = parser.generate_tree()
    code_gen(tree)
    builder.ret(builder.load(var_dict[last_var])) # specify return value
    w.write(str(module))
    w.close()
    return module

def main():
    filename = str(args[1])[0:len(str(args[1]))-3]+"ir"
    w = open(filename,'w')
    parser.generate_tree()
    builder.ret(builder.load(var_dict[last_var]))
    w.write(str(module))

if __name__ =="__main__":
    main()
