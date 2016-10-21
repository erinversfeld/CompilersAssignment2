import ply.lex as lex
import sys

# updated from submission for assignment 1

tokens = (
    "ID",
    "BINARY_LITERAL",
    "A",
    "S",
    "M",
    "D",
    "EQUALS",
    "OPEN_PAREN",
    "CLOSE_PAREN",
    "WHITESPACE",
    "COMMENT"
)

t_ID = r"([a-z]|_)([a-z]|_|\d)*"
t_BINARY_LITERAL = r"(\+|-)?([10])+"
t_A = r"A"
t_S = r"S"
t_M = r"M"
t_D = r"D"
t_EQUALS = r"="
t_OPEN_PAREN = r"\("
t_CLOSE_PAREN = r"\)"
t_WHITESPACE = r"(\ |\r|\t|\n)+"
t_COMMENT = r"(\/\/.*)|(\/\*(.)*?\*\/)|(\/\*(.|\n)*?\*\/)"

error = False #ensures that the value of error is correct for multiple runs


def t_error(t):
    #updated method
    global error
    error = True
    print("lexical error on line 1")
    output.write("lexical error on line 1")
    t.lexer.skip(1)


def main():
    #refactored a lot of stuff into the main method
    args = sys.argv

    filename = str(args[1])[:len(args[1]) - 3] + 'tkn'
    file = open(filename, 'r')
    lex.lex()
    lex.input(file.read())
    output = open(filename, 'w')

    for curr_token in iter(lex.token, None):
        if curr_token.type == 'COMMENT' or curr_token.type == 'WHITESPACE':
            output.write(curr_token.type + '\n')
        elif curr_token.type == 'BINARY_LITERAL' or curr_token.type == 'ID':
            output.write(curr_token.type + ',' + curr_token.value + '\n')
        else:
            output.write(curr_token.value + '\n')

    output.close()


def set_output_file(file):
    #another handy helper method
    global output
    output = file


if __name__ == "__main__":
    main()
