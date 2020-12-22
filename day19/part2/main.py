


READ_RULES = 0
READ_VALUE = 1


class AlphaRuleNode:

    def __init__(self, key, rule_value):
        self.rule = rule_value
        self.type = "alpha"
        self.key = key

    def create_node(self, rules):
        return self

    def print(self):
        print("a:{}".format(self.rule))

    def print_tree(self, level):
        print("a-{}:{}".format(level, rule.rule))

    def create_values(self):
        return rule.rule


class OrRuleNode:

    def __init__(self, key, rule_value1, rule_value2):
        self.rule1 = ConcatRuleNode(key, rule_value1)
        self.rule2 = ConcatRuleNode(key, rule_value2)
        self.children = []
        self.type = "or"
        self.key = key

    def create_node(self, rules):
        if len(self.children) == 0:
            self.children.append(self.rule1.create_node(rules))
            self.children.append(self.rule2.create_node(rules))
        return self

    def print(self):
        print("o0:", end='')
        self.rule1.print()
        print("o1:", end='')
        self.rule2.print()

    def print_tree(self, level):
        print("o0-{}:".format(level), end='')
        self.children[0].print_tree(level+1)
        print("o1-{}:".format(level), end='')
        self.children[1].print_tree(level+1)

    def create_values(self):
        return [self.children[0].create_values(), self.children[1].create_values()]


class ConcatRuleNode:

    def __init__(self, key, rule_value):
        self.rule = [int(x) for x in rule_value.split(" ")]
        self.children = []
        self.type = "concat"
        self.key = key

    def create_node(self, rules):
        if len(self.children) == 0:
            for val in self.rule:
                self.children.append(rules[val].create_node(rules))
        return self

    def print(self):
        print("c:{}".format(self.rule))

    def print_tree(self, level):
        for val in self.children:
            print("c-{}:".format(level), end='')
            val.print_tree(level+1)


def verify_alpha(node, list_idx, value):
    result = []
    for idx in list_idx:
        print("{}: {} =? {}".format(node.key, node.rule, value[idx]))
        if node.rule == value[idx]:
            result.append(idx+1)
    return result


def verify_concat(node, list_idx, value):
    for child in node.children:
        list_idx = traverse_tree(child, list_idx, value)
        if not list_idx:
            print("concat: NOK")
            return []
    print("concat: OK")
    return list_idx


def verify_or(node, list_idx, value):
    print("or {}: children: {}".format(node.key, len(node.children)))
    list_ridx1 = traverse_tree(node.children[0], list_idx, value)
    list_ridx2 = traverse_tree(node.children[1], list_idx, value)

    if list_ridx1 and list_ridx2:
        print("or:OK")
        return list_ridx1 + list_ridx2
    if list_ridx1:
        print("or1:OK")
        return list_ridx1
    if list_ridx2:
        print("or2:OK")
        return list_ridx2

    print("or: NOK")
    return []


def traverse_tree(node, list_idx, value):
    new_list_idx = []
    for idx in list_idx:
        if idx < len(value):
            print("p:{}-{} -> {}:{}".format(node.key, node.type, idx, value[idx]))
            new_list_idx.append(idx)
    if not list_idx:
        print("p:{}-{}: overrun".format(node.key, node.type))
        []
    if node.type == "alpha":
        return verify_alpha(node, new_list_idx, value)
    if node.type == "concat":
        return verify_concat(node, new_list_idx, value)
    if node.type == "or":
        return verify_or(node, new_list_idx, value)
    return []


def create_rule_node(key, rule_value):
    or_values = rule_value.split(" | ")
    if len(or_values) == 2:
        return OrRuleNode(key, or_values[0], or_values[1])
    str_value = rule_value.strip('"')
    if str_value.isalpha():
        return AlphaRuleNode(key, str_value)
    return ConcatRuleNode(key, rule_value)


def processRule(rule_line):
    values = rule_line.split(": ")
    return (int(values[0]), create_rule_node(values[0], values[1]))


def create_rule_tree(rules, start_node):
    return rules[start_node].create_node(rules)


def print_tree(ruleTree):
    ruleTree.print_tree(0)


if __name__ == '__main__':
    state = READ_RULES
    rules = {}
    result = 0
    results=[]
    tree = None
    with open("input.txt", "r") as inFile:
        for line in inFile:
            if line == '\n':
                state = READ_VALUE
                tree = create_rule_tree(rules, 0)
                continue
            if state == READ_RULES:
                (key, rule) = processRule(line.rstrip('\n'))
                rules[key] = rule
#                print("{}: {}".format(key,line))
            if state == READ_VALUE:
                print("read: {}".format(line.rstrip('\n')))
                list_idx = traverse_tree(tree, [0], line.rstrip('\n'))
                if list_idx:
                    for idx in list_idx:
                        if idx == len(line.rstrip('\n')):
                            results.append(line.rstrip('\n'))
                            result += 1
                            break

        inFile.close()
        print("Result: {}".format(result))
        print(results)