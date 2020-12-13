def intersection(set1, set2):
    intersec = []
    for el1 in set1:
        for el2 in set2:
            if (el1 == el2):
                intersec.append(el1)
    return intersec


def processAnsweers(answers):
    answers_list = list(answers)
    unique_list = []
    for answer in answers_list:
        if not answer in unique_list:
            unique_list.append(answer)

    print("group answers {}".format(len(unique_list)))

    return len(unique_list)


if __name__ == '__main__':
    with open("./input.txt", "r") as infile:
        nbr_answers = 0
        intset=[]
        first = True
        for line in infile:
            if line == '\n':
                print(intset)
                print(len(intset))
                nbr_answers += len(intset)
                intset = []
                first = True
            elif first:
                intset = list(line.strip('\n'))
                first = False
            else:
                intset = intersection(intset, list(line.strip('\n')))
        if len(intset) > 0:
            print(intset)
            print(len(intset))
            nbr_answers += len(intset)

        infile.close()

    print(nbr_answers)