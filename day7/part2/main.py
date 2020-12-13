# bag-rule: <bag-kind> contains <bags>(,<bags>)*.
# bag-kind: <color-tone> <color> bag(s)?
# color-tone: <word>
# color: <word>
# bags: (<number> <bag-kind>) | no other bags

class Token:

    def __init__(self, token, value):
        self.token = token
        self.value = value

    def __str__(self):
        return str('[kind:{},value:{}]'.format(self.token, self.value))


class BagKind:

    def __init__(self, colorTone, color):
        self.colorTone = colorTone
        self.color = color

    def __eq__(self, other):
        return self.colorTone == other.colorTone and \
            self.color == other.color

    def __str__(self):
        return str('[colortone:{},color:{}]'.format(self.colorTone, self.color))


class NbrBagKind:

    def __init__(self, number, bagKind):
        self.nbr = number
        self.bagKind = bagKind

    def __eq__(self, other):
        return self.colorTone == other.colorTone and \
            self.color == other.color


class BagRule:

    def __init__(self, bagKind, nbrAndBagKinds):
        self.bagKind = bagKind
        self.nbrAndBagKinds = nbrAndBagKinds


def processToken(token, line, i):
    if token == 'contain':
        return (i, Token('contain', ''))
    if token == 'no':
        i += len("other bags ")
        return (i, Token('no other bags', ''))
    if token == 'bag' or token == 'bags':
        return (i, Token('bag', ''))
    if token.isnumeric():
        return (i, Token('number', int(token)))
    return (i, Token('word', token))


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
        elif line[i] == ',':
            i += 1
            if len(token) > 0:
                (i, tkn) = processToken(token, line, i)
                tokens.append(tkn)
            tokens.append(Token('comma', ','))
            token = ''
        elif line[i] == '.':
            (i, tkn) = processToken(token, line, i)
            tokens.append(tkn)
        elif line[i] == '\n':
            break
        else:
            token += line[i]
            i += 1
    return tokens


def processKindOfBag(tokens, idx):
    if tokens[idx].token != 'word':
        raise Exception('KindOfBag: Invalid token')
    colortone = tokens[idx].value
    idx += 1
    if tokens[idx].token != 'word':
        raise Exception('KindOfBag: Invalid token')
    color = tokens[idx].value
    idx += 1
    if tokens[idx].token != 'bag':
        raise Exception('KindOfBag: Invalid token (not bag)')
    idx += 1
    return (idx, BagKind(colortone, color))


def processNumber(tokens, idx):
    if tokens[idx].token != 'number':
        raise Exception('Number: Invalid token')
    nbr = tokens[idx].value
    idx += 1
    return (idx, nbr)


def processBags(tokens, idx):
    bags = []
    i = idx
    while i < len(tokens):
        if tokens[i].token == 'comma':
            i += 1
        elif tokens[i].token == 'no other bags':
            i += 1
            return []
        else:
            (i, number) = processNumber(tokens, i)
            (i, bagKind) = processKindOfBag(tokens, i)
            bags.append(NbrBagKind(number, bagKind))
    return bags


def printTokens(tokens):

    for token in tokens:
        print(token)


def pass2_parser(tokens):
    idx = 0
    (idx, bagKind) = processKindOfBag(tokens, idx)
    if tokens[idx].token != 'contain':
        printTokens(tokens)
        raise Exception('Contains: Invalid token')
    idx += 1
    bags = processBags(tokens, idx)
    return BagRule(bagKind, bags)


def isBagInBagRule(bag, nbrAndBagKinds):
    if nbrAndBagKinds == None:
        return False
    for nbrBagKind in nbrAndBagKinds:
        if bag == nbrBagKind.bagKind:
            return True
    return False


def findBagsCanContain(bagRules, bag):
    print("--- begin: {} ---".format(bag))
    nbrBags = 0
    for bagRule in bagrules:
        if bagRule.bagKind == bag:
            for nbrAndBagKind in bagRule.nbrAndBagKinds:
                print(nbrAndBagKind.nbr)
                nbrBags += nbrAndBagKind.nbr
                nbrBags += nbrAndBagKind.nbr * findBagsCanContain(bagRules, nbrAndBagKind.bagKind)
                print("nbr bags: {}".format(nbrBags))


    print("--- end: {} ---".format(bag))

    return nbrBags


if __name__ == '__main__':
    bagrules = []
    with open('input.txt', 'r') as infile:
        for line in infile:
            tokens = pass1_lex(line)
            bagrules.append(pass2_parser(tokens))
        infile.close()

    bag = BagKind("shiny", "gold")
    nbrBags = findBagsCanContain(bagrules, bag)

    print(len(bagrules))
    print(nbrBags)
