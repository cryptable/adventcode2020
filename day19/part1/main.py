


READ_RULES = 0
READ_VALUE = 1


class AlphaRuleNode:

    def __init__(self, rule_value):
        self.rule = rule_value

    def create_node(self, rules):
        return self

    def print(self):
        print("a:{}".format(self.rule))

    def print_tree(self, level):
        print("a-{}:{}".format(level, rule.rule))

    def create_values(self):
        return rule.rule

class OrRuleNode:

    def __init__(self, rule_value1, rule_value2):
        self.rule1 = ConcatRuleNode(rule_value1)
        self.rule2 = ConcatRuleNode(rule_value2)
        self.children = []

    def create_node(self, rules):
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

    def __init__(self, rule_value):
        self.rule = [int(x) for x in rule_value.split(" ")]
        self.children = []

    def create_node(self, rules):
        for val in self.rule:
            self.children.append(rules[val].create_node(rules))
        return self

    def print(self):
        print("c:{}".format(self.rule))

    def print_tree(self, level):
        for val in self.children:
            print("c-{}:".format(level), end='')
            val.print_tree(level+1)


def create_rule_node(rule_value):
    or_values = rule_value.split(" | ")
    if len(or_values) == 2:
        return OrRuleNode(or_values[0], or_values[1])
    str_value = rule_value.strip('"')
    if str_value.isalpha():
        return AlphaRuleNode(str_value)
    return ConcatRuleNode(rule_value)


def processRule(rule_line):
    values = rule_line.split(": ")
    return (int(values[0]), create_rule_node(values[1]))


def create_rule_tree(rules, start_node):
    return rules[start_node].create_node(rules)


def print_tree(ruleTree):
    ruleTree.print_tree(0)


if __name__ == '__main__':
    state = READ_RULES
    rules = {}
    result = 0
    with open("input_test1.txt", "r") as inFile:
        for line in inFile:
            if line == '\n':
                state = READ_VALUE
                for rule in rules.values():
                    print('t')
                    rule.print()
                createTree = create_rule_tree(rules, 0)
#                print_tree(createTree)
                break
            if state == READ_RULES:
                (key, rule) = processRule(line.rstrip('\n'))
                rules[key] = rule
#                print("{}: {}".format(key,line))
            if state == READ_VALUE:
                result += rules[0].validate(rules, line.rstrip('\n'))

        inFile.close()
#        print(result)