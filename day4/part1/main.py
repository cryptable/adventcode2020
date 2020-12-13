obligatory_entries = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def processPassport(data):
    fields = data.split(' ')
    entries = {}
    for field in fields:
        entry = field.split(':')
        entries[ entry[0] ] = entry[1]
    for obligatory_entry in obligatory_entries:
        if not (obligatory_entry in entries.keys()):
            return False
    print(data)
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    valid = 0
    with open("./input.txt", "r") as infile:
        passport_data = ''
        for line in infile:
            if line == '\n':
                if processPassport(passport_data.strip()):
                    valid += 1
                passport_data = ''
            passport_data = passport_data + ' ' + line.rstrip('\n')
        if passport_data != '':
            if processPassport(passport_data.strip()):
                valid += 1
    print(valid)