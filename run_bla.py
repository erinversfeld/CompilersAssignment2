import llvmlite.binding as llvm
import sys

from ctypes import CFUNCTYPE, c_int
import ir_bla

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ""
target_machine = ""
engine = ""

def compile_ir(engine, irModule):
    module = llvm.parse_assembly(str(irModule))
    module.verify()
    engine.add_module(module)
    engine.finalize_object()
    return module

def create_exec_engine():
    global target_machine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def main(): 
    global engine,module
    
    fileName = str(sys.argv[1])       
    output = open(fileName[:len(fileName)-3]+'run','w')
    engine = create_exec_engine()
    module = compile_ir(engine, str(ir_bla.get_module()))
    func_ptr = engine.get_function_address("main")
    cfunc = CFUNCTYPE(c_int)(func_ptr)
    formatted = "{0:b}".format(cfunc()) #dec -> bin
    output.write(formatted)
    output.close()

def get_module():
    return module

def get_target():
    return target_machine

if(__name__ == "__main__"):
    main()
