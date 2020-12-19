

STATE_RULES = 1
STATE_MYTICKET = 2
STATE_NEARTICKETS = 3


def sort_func(val):
    return len(val[1])


class Rules:

    def __init__(self):
        self.rules = {}

    def add(self, rule):
        data = rule.split(': ')
        or_ranges = data[1].rstrip('\n').split(' or ')
        valid_ranges1 = [int(x) for x in or_ranges[0].split('-')]
        valid_ranges2 = [int(x) for x in or_ranges[1].split('-')]
        self.rules[data[0]] = (valid_ranges1, valid_ranges2)

    def _verify(self, val):
        result = False
        for ranges in self.rules.values():
            if (ranges[0][0] <= val and val <= ranges[0][1]) or (ranges[1][0] <= val and val <= ranges[1][1]):
                result = True
        return result

    def invalid_numbers(self, line):
        nbrs = []
        for tst in line:
            if not self._verify(tst):
                nbrs.append(tst)
        return nbrs

    def _verify_ranges(self, low1, high1, low2, high2, column, tickets):
        for ticket in tickets:
#            print("l1:{} h1:{} l2:{} h2:{} t:{}".format(low1, high1, low2, high2, ticket[column]))
            if not ((low1 <= ticket[column] <= high1) or (low2 <= ticket[column] <= high2)):
                return False
        return True

    def _verify_column(self, column, tickets):
        fields = []
        for key in self.rules.keys():
            range1 = self.rules[key][0]
            range2 = self.rules[key][1]
            if self._verify_ranges(range1[0], range1[1], range2[0], range2[1], column, tickets):
                fields.append(key)
        return fields

    def guess_fields(self, valid_tickets):
        fields = []
        columns = len(valid_tickets[0])

        for column in range(columns):
            fields.append((column, self._verify_column(column, validtickets)))

        fields.sort(key=sort_func)
        print(fields)

        for i in range(len(fields)):
            for j in range(i+1, len(fields)):
                key = fields[i][1]
                if key[0] in fields[j][1]:
                    fields[j][1].remove(key[0])
        return fields


if __name__ == '__main__':
    with open("input.txt", "r") as inFile:
        state = STATE_RULES
        rules = Rules()

        validtickets = []
        myticket = []
        for line in inFile:
            if line == 'your ticket:\n':
                state = STATE_MYTICKET
            elif line == 'nearby tickets:\n':
                state = STATE_NEARTICKETS
            elif line == '\n':
                continue
            else:
                if state == STATE_RULES:
                    rules.add(line)
                if state == STATE_MYTICKET:
                    myticket = [ int(x.rstrip('\n')) for x in line.split(',') ]
                if state == STATE_NEARTICKETS:
                    invalidNumbersLine = rules.invalid_numbers([ int(x.rstrip('\n')) for x in line.split(',') ])
                    if len(invalidNumbersLine) == 0:
                        validtickets.append([ int(x.rstrip('\n')) for x in line.split(',') ])

        validtickets.append(myticket)
        column_defs = rules.guess_fields(validtickets)
        result = 1
        print(myticket)
        print(column_defs)
        for idx in range(len(column_defs)):
            val = column_defs[idx][1][0]
            if val.startswith('departure'):
                print("{}: {}".format(val, myticket[column_defs[idx][0]]))
                result *= myticket[column_defs[idx][0]]

        print(result)