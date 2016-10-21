from ply import lex
import os
import sys

tokens = ["ID", "BINARY_LITERAL", "WHITESPACE", "COMMENT"]

literals = ["A", "S", "M", "D", "=", "(", ")"]

t_BINARY_LITERAL = r'[-+]?[0-9]+'

def t_WHITESPACE(t):
    r'\s*(\p{P})?\s'
    t.lexer.lineno += t.value.count("\n") # line number tracking for exception handling
    if __name__ == "__main__":
        return t

def t_COMMENT(t):
    r'/\*(.|[\r\n])*?\*/|(//.*)'
    # regex allows for /* */ and // comments but also allows extra *s in a multiline /* */ comment
    t.lexer.lineno += t.value.count("\n") # implement line number tracking for exception handling
    if __name__ == "__main__":
        return t

def t_ID(t):
    r'[_a-z][_a-z0-9]*'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            lexer.input(infile.read())
            outfilename = os.path.splitext(infilename)[0]+".tkn"
            outfile = open(outfilename, "w")
    
            for token in lexer:
                if token.type in ["BINARY_LITERAL", "ID"]:
                    print(token.type, token.value, sep=",", file=outfile)
                    print(token.type, token.value, sep=",")
                else:
                    print(token.type, file=outfile)
                    print(token.type)
    
            outfile.close()
        else:
            print("Not a valid file, make sure the file is in testdata/lex/ and try again")
    else:
        print("Specify filename, e.g. lex_bla.ply my_program.bla")

if __name__ == "__main__":
    main()