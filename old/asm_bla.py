from run_bla import get_module, get_target, main as run
import sys
import os

def main():
    fileName = str(sys.argv[1])
    outFile = open(fileName[:len(fileName)-4]+".asm","w")

    run()
    asm = get_target().emit_assembly(get_module())

    print(asm)	#Print to console
    outFile.write(asm)	#Write to file

if(__name__ == "__main__"):
    main()
