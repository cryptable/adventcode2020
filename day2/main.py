
if __name__ == '__main__':
    input = open("./input-2.txt", "r")
    values = []
    value = input.readline()
    total = 0
    while value != '':
        policy, *password = value.split(": ")
        minmax, *kar = policy.split()
        smin, *smax = minmax.split("-")
        min = int(smin)
        max = int(smax[0])
        occurence = password[0].count(kar[0])
        if (min <= occurence) and (occurence <= max):
            total += 1
        value = input.readline()

    print('Total correct passwords = {}'.format(total))
    input.close()

