from run_bla import get_module, get_target, main as run
import sys

def main():
    args = sys.argv
    filename = str(args[1])[:len(args[1])-3]+'asm'
    output = open(filename,'w')
    
    run()
    asm = get_target().emit_assembly(get_module())

    output.write(asm)

if(__name__ == "__main__"):
    main()