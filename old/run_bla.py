import llvmlite.binding as llvm
import sys

from ctypes import CFUNCTYPE, c_int
import ir_bla

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

module = ""
tMachine = ""
eng = ""

def compileIR(engine,irModule):
    module = llvm.parse_assembly(str(irModule))
    module.verify()
    engine.add_module(module)
    engine.finalize_object()
    return module

def buildEngine():
    global tMachine
    t = llvm.Target.from_default_triple()
    tMachine = t.create_target_machine()
    backMod = llvm.parse_assembly("")
    eng = llvm.create_mcjit_compiler(backMod, tMachine)
    return eng


def main():
    global eng,module
    args = sys.argv

    fileName = str(args[1])
    w = open(fileName[:len(fileName)-4]+".run","w")
    eng = buildEngine()
    module = compileIR(eng, str(ir_bla.get_module()))
    func_ptr = eng.get_function_address("main")
    cfunc = CFUNCTYPE(c_int)(func_ptr)
    formatted = "{0:b}".format(cfunc()) #Conversion of decimal to Binary.
    w.write(formatted)
    w.close()

def get_module():
    return module

def get_target():
    return tMachine

if(__name__ == "__main__"):
    main()

