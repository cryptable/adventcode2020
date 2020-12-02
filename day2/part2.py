
if __name__ == '__main__':
    input = open("./input-2.txt", "r")
    values = []
    value = input.readline()
    total = 0
    while value != '':
        policy, *password = value.split(": ")
        firstsecond, *kar = policy.split()
        sfirst, *ssecond = firstsecond.split("-")
        first = int(sfirst)
        second = int(ssecond[0])
        first_kar = password[0][first-1]
        second_kar = password[0][second-1]
        if ((first_kar == kar[0]) and (second_kar != kar[0])) or ((first_kar != kar[0]) and (second_kar == kar[0])):
            total += 1
        value = input.readline()

    print('Total correct passwords = {}'.format(total))
    input.close()

