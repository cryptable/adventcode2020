import math


def search_trees(tree_map, shift_right, shift_down):
    trees = 0
    shift_idx = 0
    line_idx = shift_down
    len_line = len(tree_map[0].rstrip('\n')) # <enter> sign at the end
    print("Line length {}".format(len_line))
    while line_idx < len(tree_map):
        shift_idx = (shift_idx + shift_right) % len_line  # modulo to go to extend the map
        if shift_idx >= len_line:
            print("Error: Reach right end")
            return trees
        if tree_map[line_idx][shift_idx] == '#':
            trees += 1
        line_idx += shift_down
    return trees


if __name__ == '__main__':
    input_file = open("./input.txt", "r")
    tree_map = []
    value = input_file.readline()
    while value != '':
        tree_map.append(value)
        value = input_file.readline()
    input_file.close()
    trees_slope1 = search_trees(tree_map, 1, 1)
    print("Number of trees slope 1 {}".format(trees_slope1))
    trees_slope2 = search_trees(tree_map, 3, 1)
    print("Number of trees slope 2 {}".format(trees_slope2))
    trees_slope3 = search_trees(tree_map, 5, 1)
    print("Number of trees slope 3 {}".format(trees_slope3))
    trees_slope4 = search_trees(tree_map, 7, 1)
    print("Number of trees slope 4 {}".format(trees_slope4))
    trees_slope5 = search_trees(tree_map, 1, 2)
    print("Number of trees slope 5 {}".format(trees_slope5))

    mul_trees = trees_slope1 * trees_slope2 * trees_slope3 * trees_slope4 * trees_slope5
    print("Number of trees {}".format(mul_trees))