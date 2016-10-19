import re
import sys
import parse_bla as parser
import exceptions_bla as exceptions


def main():

    args = sys.argv

    try:
        filename = str(args[1])[0:len(str(args[1]))-3]+"err"
        w = open(filename,'w')
        text = parser.main()

    #Parse errors
    except TypeError as error:
        print(error)
        error_message = 'parse error on line '
        line_num = str(1)
        w.write(error_message+line_num)

    #Lex errors
    except exceptions.LexicalException as error:
        error_message = 'lexical error on line '
        line_num = str(error.args[0])
        w.write(error_message+line_num)

    if not text:
        error_message = 'semantic error on line '
        line_num = str(2)
        w.write(error_message+line_num)

    w.close()

if __name__=="__main__":
    main()
