from my_parse_bla import get_tree
import sys


def error_check(output, tree, sym_table, line_num):
    for t in tree[1]:
        if isinstance(t, tuple):
            error_check(output, t, sym_table, line_num + 1)
        else:
            line_num + 1
            t_ = t.split(',')

            #LHS
            if t_[0] == 'ID':
                #error
                if str(t_[1]) in sym_table:
                    output.write('semantic error on line ' + str(line_num + 1))
                    break
                else:
                    sym_table.append(t_[1])

            #RHS
            elif t_[0] == 'ID_RHS':
                #error
                if t_[1] not in sym_table:
                    output.write('semantic error on line ' + str(line_num))
                    print('semantic error on line ' + str(line_num))
                    break


def main():
    args = sys.argv
    filename = str(args[1])[:len(args[1]) - 3] + '.err'
    output = open(filename, 'w')

    tree = get_tree(output)

    if tree:
        error_check(output, tree, sym_table=[], line_num=0)

    output.close()


if __name__ == "__main__":
    main()
