from parse_bla import generate_tree
import lex_bla
import sys

def error_checks(output, tree, sym_table, line_num):

    for t in tree[1]:
        if isinstance(t, tuple):
            error_checks(output, t, sym_table, line_num + 1)
        else:
            line_num + 1
            t_ = t.split(',')

            if t_[0] == "ID":
                if str(t_[1]) in sym_table:
                    print("semantic error on line " + str(line_num + 1))
                    output.write("semantic error on line " + str(line_num + 1))
                    break
                else:
                    sym_table.append(t_[1])

            elif t_[0] == "ID_RHS":
                if t_[1] not in sym_table:
                    output.write("semantic error on line " + str(line_num))
                    print("semantic error on line " + str(line_num))
                    break

def main():
    args = sys.argv
    filename = str(args[1])[:len(args[1])-3]+"err"
    w = open(filename,"w")
    lex_bla.set_output_file(w)
    tree = generate_tree()
    if tree:
        error_checks(w, tree, sym_table= [], line_num= 0)
    w.close()

if __name__ == "__main__":
    main()

