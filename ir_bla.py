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
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "+":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0].isnumeric():
        return(ir.Constant(ir.FloatType(), float(tree[0])))

args = sys.argv

#get the compact AST
r = open(args[1], 'r')
tree = parser.generate_tree(r.read())

#track last variable assigned
last_var = ''

#variable names associated with memory locations
var_dict = {}

flttyp = ir.FloatType() # create float type
fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
module = ir.Module(name="lang") # create module named "lang"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code
code_gen(tree) # call code_gen() to traverse tree & generate code
builder.ret(builder.load(var_dict[last_var])) # specify return value
print(module)
