import itertools
import copy

def get_possibilities(mult_9: int, secret: int):
    digits1 = [d for d in str(mult_9*secret)]
    permutations = list(set([int(num) for num in ["".join(permutation) for permutation in list(itertools.permutations(digits1))]]))
    possibilities1 = [int(num/mult_9) for num in permutations if num % mult_9 == 0 and num/mult_9 < 100]

    return set(possibilities1)

def crosscheck(check_dict: dict, to_check: set):
    iter = sorted(list(to_check))
    for pos in iter:
        if pos in check_dict and check_dict[pos] != to_check:
            to_check.remove(pos)

    return to_check

mult_9 = [63, 8]
pos_dict = {}
pos_dict2 = {}


for secret in range(1, 100):
    # print("secret: " + str(secret))
    possibilities1 = get_possibilities(mult_9[0], secret)
    # print(possibilities1)
    possibilities1 = crosscheck(pos_dict, possibilities1)

    # print(possibilities1)
    pos_dict[secret] = possibilities1

    # ===================
    # if len(possibilities1) > 1:
    #     for c2 in range(2, 20):
    #         pos3 = get_possibilities(c2*mult_9[0], secret)
    #         intersec2 = [pos for pos in possibilities1 if pos in pos3]
    #         if len(intersec2) < 2:
    #             print(c2)
            # print(str(c2) + ": " + str(intersec2))
            # print(str(c2) + ": " + str(len(intersec2)))
    # ===================


    # possibilities2 = get_possibilities(mult_9[0]*mult_9[1], secret)
    # possibilities2 = crosscheck(pos_dict2, possibilities2)
    # pos_dict2[secret] = possibilities2

    # intersec = [pos for pos in possibilities1 if pos in possibilities2]
    # print(intersec)
    # print(len(intersec))

for secret in pos_dict:
    print("secret: " + str(secret) + " => possibilities: " + str(pos_dict[secret]) + "<br>")