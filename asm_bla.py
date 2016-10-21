from run_bla import get_module, get_target, main as the_other_main
import sys

def main():
    file = sys.argv[1]
    input_file = open(file, 'r').read()
    print(input_file)

    file_name = str(file)[:len(file)-3]+'asm'
    output_file = open(file_name,"w")
    
    the_other_main(len(sys.argv))
    asm = get_target().emit_assembly(get_module())

    output_file.write(asm)

if(__name__ == "__main__"):
    main()