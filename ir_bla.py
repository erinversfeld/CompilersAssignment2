from llvmlite import ir
import sys
import parse_bla as parser

def code_gen(tree):
    global last_var

    if tree[0] == 'Program':
        for t in tree[1]:
            code_gen(t)

    elif tree[0] == '=':
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        builder.store(code_gen(tree[1][1]), var_dict[last_var])

    elif tree[0] == 'A':
        str_1 = tree[1][0]
        str_2 = tree[1][1]

        num_1 = [str_1.split(',')[1]]
        num_2 = [str_2.split(',')[1]]
        return(builder.add(code_gen(num_1),code_gen(num_2)))

    elif tree[0] == 'S':
        str_1 = tree[1][0]
        str_2 = tree[1][1]

        num_1 = [str_1.split(',')[1]]
        num_2 = [str_2.split(',')[1]]
        return(builder.sub(code_gen(num_1),code_gen(num_2)))

    elif tree[0] == 'M':
        str_1 = tree[1][0]
        str_2 = tree[1][1]

        num_1 = [str_1.split(',')[1]]
        num_2 = [str_2.split(',')[1]]
        return(builder.mul(code_gen(num_1),code_gen(num_2)))

    elif tree[0] == 'D':
        str_1 = tree[1][0]
        str_2 = tree[1][1]

        num_1 = [str_1.split(',')[1]]
        num_2 = [str_2.split(',')[1]]
        return(builder.div(code_gen(num_1),code_gen(num_2)))

    elif tree[0].isnumeric():
        return(ir.Constant(ir.IntType(32), int(tree[0], 2)))

args = sys.argv

#get the compact AST
r = open(args[1], 'r')
tree = parser.generate_tree(r.read())

#track last variable assigned
last_var = ''

#variable names associated with memory locations
var_dict = {}

inttyp = ir.IntType(32) # create float type
fnctyp = ir.FunctionType(inttyp, ()) # create function type to return a float
module = ir.Module(name="bla") # create module named "lang"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code
code_gen(tree) # call code_gen() to traverse tree & generate code
builder.ret(builder.load(var_dict[last_var])) # specify return value

filename = str(args[1])[0:len(str(args[1]))-3]+"ir"
w = open(filename,'w')
w.write(str(module))
w.close()
