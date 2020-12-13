import re

obligatory_entries = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def validate_birth_year(year):
    year_int = int(year)
    return (1920 <= year_int) and (year_int <= 2002)


def validate_issue_year(year):
    year_int = int(year)
    return (2010 <= year_int) and (year_int <= 2020)


def validate_expiration_year(year):
    year_int = int(year)
    return (2020 <= year_int) and (year_int <= 2030)


re_hgh = re.compile(r'^(\d+)(\w*)')


def validate_height(height):
    res = re_hgh.match(height).groups()

    height_int = int(res[0])
    if res[1] == 'cm':
        return (150 <= height_int) and (height_int <= 193)
    if res[1] == 'in':
        return (59 <= height_int) and (height_int <= 76)

    return False


re_hair = re.compile(r'^#[0-9a-f]{6}$')


def validate_hair_color(hair):
    res = re_hair.match(hair)
    if res is None:
        return False
    return True


eye_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def validate_eye_color(eye):
    return eye in eye_colors


re_pid = re.compile(r'^\d{9}$')


def validate_pid(pid):
    res = re_pid.match(pid)
    if res is None:
        return False
    return True


def processPassport(data):
    fields = data.split(' ')
    entries = {}
    for field in fields:
        entry = field.split(':')
        entries[ entry[0] ] = entry[1]
    for obligatory_entry in obligatory_entries:
        if not (obligatory_entry in entries.keys()):
            return False
    if not validate_birth_year(entries['byr']):
        print('Invalid birth year')
        return False
    if not validate_issue_year(entries['iyr']):
        print('Invalid Issue year')
        return False
    if not validate_expiration_year(entries['eyr']):
        print('Invalid Expiration year')
        return False
    if not validate_height(entries['hgt']):
        print('Invalid height')
        return False
    if not validate_hair_color(entries['hcl']):
        print('Invalid hair color')
        return False
    if not validate_eye_color(entries['ecl']):
        print('Invalid eye color')
        return False
    if not validate_pid(entries['pid']):
        print('Invalid pid')
        return False
    print(data)
    return True


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