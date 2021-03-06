#provided courtesy of UCT CS department angels
from ply import yacc
from lex_bla import tokens
import os
import sys


start = "Program"


def p_program_statements(p):
    """Program : Statements"""
    p[0] = ("Program", p[1])


def p_statements(p):
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """Statement : ID '=' expression"""
    p[0] = ("=", ["ID," + p[1], p[3]])


def p_expression_plus(p):
    """expression : expression 'A' term"""
    p[0] = ("A", [p[1], p[3]])


def p_expression_minus(p):
    """expression : expression 'S' term"""
    p[0] = ("S", [p[1], p[3]])


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_multiply(p):
    """term : term 'M' factor"""
    p[0] = ("M", [p[1], p[3]])


def p_term_divide(p):
    """term : term 'D' factor"""
    p[0] = ("D", [p[1], p[3]])


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_expression(p):
    """factor : '(' expression ')'"""
    p[0] = p[2]


def p_factor_binary(p):
    """factor : BINARY_LITERAL"""
    p[0] = "BINARY_LITERAL," + p[1]


def p_factor_id(p):
    """factor : ID"""
    p[0] = "ID," + p[1]

#endrules


def p_error(p):
    pass

def print_tree(outfile, tupletree, depth=0):
    print("\t"*depth, tupletree[0], sep="", file=outfile)
    print("\t"*depth, tupletree[0])
    for item in tupletree[1]:
        if isinstance(item, tuple):
            print_tree(outfile, item, depth + 1)
        else:
            print("\t"*(depth+1), item, sep="", file=outfile)
            print("\t"*(depth+1), item)


def generate_tree(source):
    result = parser.parse(source)
    return result


parser = yacc.yacc()


def main():
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            syntree = generate_tree(infile.read())
            outfilename = os.path.splitext(infilename)[0]+".ast"
            with open(outfilename, "w") as outfile:
                print_tree(outfile, syntree)
        else:
            print("Not a valid file")
    else:
        print("Specify filename, e.g. parse_bla.ply my_program.bla")

def getTree():
    #custom helper method
    filename = str(sys.argv[1])
    text = open(filename, 'r').read()
    return parser.parse(text);

def output_tree(source):
    result = parser.parse(source,tracking=True)
    return result

def get_output_tree(args):
    #custom helper method
    if len(args) == 2:
        file = args[1]
        if os.path.isfile(file):
            f = open(file, 'r').read()
            tree = generate_tree(f)
            return output_tree(f)
    else:
        print('Specify filename, e.g. parse_bla.ply my_program.bla')


if __name__ == "__main__":
    main()
