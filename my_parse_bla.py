import os

import ply.yacc as yacc
import my_lex_bla
import sys

# conditional lexing stuff, generate tokens
my_lex_bla.t_WHITESPACE = r"$a"
my_lex_bla.t_COMMENT = r"$a"
my_lex_bla.t_ignore_WHITESPACE = r"(\ |\r|\t|\n)+"
my_lex_bla.t_ignore_COMMENT = r"(\/\/.*)|(\/\*(.)*?\*\/)|(\/\*(.|\n)*?\*\/)"
my_lex_bla.main()

from my_lex_bla import tokens  # stuff breaks without this according to 6.1 here http://www.dabeaz.com/ply/ply.html

line_num = 1
p = yacc.yacc()
args = sys.argv


def p_program(p):
    '''program : program statement
               | empty'''
    p[0] = []
    for i in range(1, len(p)):
        if p[i]:
            p[0].append(p[i])
    p[0] = list(p[0])


def p_empty(p):
    'empty :'
    pass


def p_whitespace(p):
    'statement : WHITESPACE'
    p[0] = ""


def p_comment(p):
    'statement : COMMENT'
    p[0] = ""


def p_statement(p):
    'statement : ID EQUALS expression'
    p[0] = [p[2], "ID," + p[1], p[3]]


def p_statements(p):#forgot this last time
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_expression_plus(p):
    'expression : expression A term'
    p[0] = [p[2], p[1], p[3]]


def p_expression_minus(p):
    'expression : expression S term'
    p[0] = [p[2], p[1], p[3]]


def p_expression_times(p):
    'expression : term M factor'
    p[0] = [p[2], p[1], p[3]]


def p_expression_div(p):
    'expression : term D factor'
    p[0] = [p[2], p[1], p[3]]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : BINARY_LITERAL'
    p[0] = "BINARY_LITERAL," + p[1]


def p_factor_expr(p):
    'factor : OPEN_PAREN expression CLOSE_PAREN'
    p[0] = p[2]


def p_factor_id(p):
    'factor : ID'
    p[0] = "ID," + p[1]


def p_error(p):
    # updated for this assignment
    if my_lex_bla.error is False:
        output.write('parse error on line ' + str(line_num))
    else:
        pass


def populate_output_file(output, tree, depth):
    #did a major refactor here
    output.write("\t" * depth + str(tree[0]) + '\n')

    for item in tree[1]:
        if isinstance(item, tuple):
            populate_output_file(output, item, depth + 1)
        else:
            output.write("\t" * (depth + 1) + str(item) + '\n')


def print_tree(tuple_tree):
    print(tuple_tree)


def generate_tree(src):
    return p.parse(src)

def main():
    if len(args) == 2:
        if os.path.isfile(args[1]):
            input_file = open(args[1], 'r')
            global tree
            tree = generate_tree(input_file.read())

            filename = str(args[1])[:len(args[1]) - 3] + 'ast'
            with open(filename, 'w') as output:
                output.write('Program\n')
                populate_output_file(output, tree, 1)
        else:
            print('Not a valid file')
    else:
        print('Specify filename, e.g. parse_bla.ply my_program.bla')

def get_tree(out):
    global output
    output = out
    my_lex_bla.set_output_file(output)

    file = open(str(sys.argv[1]), 'r')
    return p.parse(file.read())

def get_ast_tree(out):
    filename = str(args[1])

if __name__ == "__main__":
    main()
