from llvmlite import ir
from parse_bla import getTree
import sys

total = len(sys.argv)
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
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        if isinstance(tree[1][1], tuple):
            t_ = list(tree[1][1])
            print(t_)
            builder.store(code_gen(t_), var_dict[last_var])
        elif not isinstance(tree[1][1],list):
            print([tree[1][1]])

            list_ = tree[1][1].split(',')
            value = list_[1]
            print(value)
            print(value.isalpha())
            print(value.isnumeric())
            return(builder.load(var_dict[tree[0]]))

        elif tree[0].isnumeric():
            return(ir.Constant(ir.IntType(32), int(str(tree[0]),2)))
            builder.store(code_gen([(tree[1][1])]), var_dict[last_var])
        else:
            print(tree[1][1])
            builder.store(code_gen(tree[1][1]), var_dict[last_var])

    elif tree[0] == 'A':
        print([tree[1][0]])
        list1_ = tree[1][0].split(',')
        value1 = list1_[1]
        print(value1)
        print(value1.isalpha())
        print(value1.isnumeric())
        print([tree[1][1]])
        list2_ = tree[1][1].split(',')
        value2 = list2_[1]
        print(value2)
        print(value2.isalpha())
        print(value2.isnumeric())
        return(builder.add(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'S':
        print([tree[1][0]])
        list1_ = tree[1][0].split(',')
        value1 = list1_[1]
        print(value1)
        print(value1.isalpha())
        print(value1.isnumeric())
        print([tree[1][1]])
        list2_ = tree[1][1].split(',')
        value2 = list2_[1]
        print(value2)
        print(value2.isalpha())
        print(value2.isnumeric())
        return(builder.sub(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'M':
        print([tree[1][0]])
        list1_ = tree[1][0].split(',')
        value1 = list1_[1]
        print(value1)
        print(value1.isalpha())
        print(value1.isnumeric())
        print([tree[1][1]])
        list2_ = tree[1][1].split(',')
        value2 = list2_[1]
        print(value2)
        print(value2.isalpha())
        print(value2.isnumeric())
        return(builder.mul(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    elif tree[0] == 'D':
        print([tree[1][0]])
        list1_ = tree[1][0].split(',')
        value1 = list1_[1]
        print(value1)
        print(value1.isalpha())
        print(value1.isnumeric())
        print([tree[1][1]])
        list2_ = tree[1][1].split(',')
        value2 = list2_[1]
        print(value2)
        print(value2.isalpha())
        print(value2.isnumeric())
        return(builder.sdiv(code_gen([tree[1][0]]),code_gen([tree[1][1]])))

    else:
        list_ = tree[0].split(',')
        value = list_[1]
        if value.isalpha():
            return(builder.load(var_dict[tree[0]]))

        elif tree[0].isnumeric():
            return(ir.Constant(ir.IntType(32), int(str(tree[0]),2)))


inttyp = ir.IntType(32) # create float type
fnctyp = ir.FunctionType(inttyp, ()) # create function type to return a float
module = ir.Module(name="bla") # create module named "lang"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code

def get_module():
    filename = str(sys.argv[1])[0:len(str(sys.argv[1]))-3]+"ir"
    w = open(filename,'w')
    tree = getTree()
    print(tree)
    code_gen(tree)
    builder.ret(builder.load(var_dict[last_var]))
    w.write(str(module))
    w.close()
    return module

def main(input):
    if input == 2:
        filename = str(sys.argv[1])[0:len(str(sys.argv[1]))-3]+"ir"
        w = open(filename,'w')
        tree = getTree()
        print(tree)
        code_gen(tree)
        builder.ret(builder.load(var_dict[last_var]))
        w.write(str(module))
        w.close()
    else:
        print('Specify filename, e.g. parse_bla.ply my_program.bla')

if __name__ == "__main__":
    main(total)