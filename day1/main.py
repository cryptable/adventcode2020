
if __name__ == '__main__':
    input = open("./input.txt", "r")
    values = []
    value = input.readline(5)
    while value != '':
        values.append(int(value))
        value = input.readline(5)

    input.close()
    for i in range(len(values)):
        for j in range(i, len(values)):
            sum = values[i] + values[j]
            if sum == 2020:
                mul = values[i] * values[j]
                print('Result: {} * {} = {}'.format(values[i], values[j], mul))

