# Vocabularia
# statement : '(' <mul-expression> ')' | <number>
# mul-expression : plus-expression ('*' plus-expression)*
# plus-expression : statement ('+' statement)*
# <operand> : '+' | '*'
# <number> : [1-9][0-9]*

class Token:

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return str('[kind:{},value:{}]'.format(self.token, self.value))


class ASTNode:

    def __init__(self, operand_token, left, right):
        self.token = operand_token
        self.left = left
        self.right = right


class AST:

    def __init__(self, ast_node):
        self.root = ast_node

    def traverse(self, node):

        if node.token.token == 'number':
            return node.token.value
        if node.token.token == 'operand':
            if node.token.value == '+':
                return self.traverse(node.left) + self.traverse(node.right)
            if node.token.value == '*':
                return self.traverse(node.left) * self.traverse(node.right)

    def walk(self):
        return self.traverse(self.root)

    def _print_tree(self, node, level):
        slevel = "-" * level
        if node.token.token == 'number':
            print("{}: '{}' ".format(slevel,node.token.value))
        if node.token.token == 'operand':
            if node.token.value == '+':
                self._print_tree(node.left, level+1)
                print("{}: {}".format(slevel, node.token.value))
                self._print_tree(node.right, level+1)
            if node.token.value == '*':
                self._print_tree(node.left, level+1)
                print("{}: {}".format(slevel, node.token.value))
                self._print_tree(node.right, level+1)

    def print(self):
        self._print_tree(self.root, 0)


def processToken(token, line, i):
    if token == '(':
        return (i, Token('(', ''))
    if token == ')':
        return (i, Token(')', ''))
    if token == '+':
        return (i, Token('operand', '+'))
    if token == '*':
        return (i, Token('operand', '*'))
    if token.isnumeric():
        return (i, Token('number', int(token)))
    raise Exception("unknown token {}:{} \"{}\"".format(line.rstrip('\n'), i, token))


def pass1_lex(line):
    tokens = []
    token = ''
    for i in range(0, len(line)):
        if line[i] == ' ':
            i += 1
            if len(token) > 0:
                (i, tkn) = processToken(token, line, i)
                tokens.append(tkn)
            token = ''
        elif line[i] == '(':
            (i, tkn) = processToken(line[i], line, i)
            tokens.append(tkn)
            token = ''
        elif line[i] == ')':
            if len(token) > 0:
                (i, tkn) = processToken(token, line, i)
                tokens.append(tkn)
            (i, tkn) = processToken(line[i], line, i)
            tokens.append(tkn)
            token = ''
        elif line[i] == '\n':
            if len(token) > 0:
                (i, tkn) = processToken(token, line, i)
                tokens.append(tkn)
                token = ''
            break
        else:
            token += line[i]
            i += 1
    # last token no '\n'
    if len(token) > 0:
        (i, tkn) = processToken(token, line, i)
        tokens.append(tkn)
    return tokens


def processPlusExpression(tokens, idx):

    (idx, value1) = processStatement(tokens, idx)
    ast = value1
#    print("p1: {}".format(idx))
    while idx < len(tokens) and tokens[idx].token != ')' and tokens[idx].value != '*':
        if tokens[idx].token != 'operand' or tokens[idx].value != '+':
            raise Exception('Illegal expression')
        operand = tokens[idx]
        idx += 1
        (idx, value2) = processStatement(tokens, idx)
        ast = ASTNode(operand, ast, value2)
#        print("p2: {}".format(idx))

    return (idx, ast)


def processMulExpression(tokens, idx):

    (idx, value1) = processPlusExpression(tokens, idx)
    ast = value1

#    print("m1: {}".format(idx))
    while idx < len(tokens) and tokens[idx].token != ')' and tokens[idx].value != '+':
        if tokens[idx].token != 'operand' or tokens[idx].value != '*':
            raise Exception('Illegal mul expression {}: {}'.format(tokens[idx].token, tokens[idx].value))
        operand = tokens[idx]
        idx += 1
        (idx, value2) = processPlusExpression(tokens, idx)
        ast = ASTNode(operand, ast, value2)
#        print("m2: {}".format(idx))

    return (idx, ast)


def processStatement(tokens, idx):

    # <number>
#    print("s1: {}".format(idx))
    if tokens[idx].token == 'number':
        number_node = ASTNode(tokens[idx], None, None)
        idx += 1
        return (idx, number_node)
    elif tokens[idx].token == '(':
        idx += 1
        if idx >= len(tokens):
            raise Exception("Unbalanced braces")
        (idx, parenthese_node) = processMulExpression(tokens, idx)
        if tokens[idx].token != ')':
            raise Exception("Unbalanced braces")
        idx += 1
        return (idx, parenthese_node)
    else:
        raise Exception("Unexpected token {}".format(tokens[idx].token))

    return (0, None)


def printTokens(tokens):
    for token in tokens:
        print(token)


def pass2_parser(tokens):
    idx = 0
    (idx, val) = processMulExpression(tokens, idx)
    if idx != len(tokens):
        raise Exception("Unused Tokens {} vs {}".format(idx, len(tokens)))

    return val


if __name__ == '__main__':
    sum = 0
    with open('input.txt', 'r') as infile:
        for line in infile:
            tokens = pass1_lex(line)
 #           for token in tokens:
 #               print(token, end=',')
 #           print()
            value = pass2_parser(tokens)
            astTree = AST(value)
#            astTree.print()
            print(astTree.walk())
            sum += astTree.walk()
        infile.close()
        print(sum)
