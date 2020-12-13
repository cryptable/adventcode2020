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
    nbr_answers = 0
    with open("./input.txt", "r") as infile:
        question_data = ''
        for line in infile:
            if line == '\n':
                nbr_answers += processAnsweers(question_data.strip())
                question_data = ''
            question_data = question_data + line
        if question_data != '':
            nbr_answers += processAnsweers(question_data.strip())

        infile.close()

    print(nbr_answers)