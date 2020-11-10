import itertools

# the script assumes the performer chooses 63 as their number and that the
# participant never chooses a zero as the digit of the product to keep secret.
revealed_num = 63
check_dict = {}
choices = list(range(2, 20)) # this is our set of possible choices to give to the participant in the second round
# We can set it to any list of intigers we want, but I've set it to be all ints from 2 to 20.
# the script will remove any numbers in this list that lead to multiple
# possibilities in the second round, and present us the revised list


def get_digits(revealed_digits: str):
    last_digit = 9 - (sum([int(d) for d in revealed_digits]) % 9)
    digits = int("".join([str(d) for d in revealed_digits] + [str(last_digit)]))

    return digits

def crosscheck(check_dict: dict, to_check: set):
    iter = sorted(list(to_check))
    for pos in iter:
        if pos in check_dict and check_dict[pos] != to_check:
            to_check.remove(pos)

    return to_check

def get_possibilities(revealed_num: int, digits: int):
    digits = [d for d in str(digits)]
    permutations = list(set([int(num) for num in ["".join(permutation) for permutation in list(itertools.permutations(digits))]]))
    possibilities1 = [int(num/revealed_num) for num in permutations if num % revealed_num == 0 and num/revealed_num < 100]

    return set(possibilities1)



# generate a "check" dictionary. This dictionary is a way to remove certain
# possibilities
for secret in range(1, 100):
    possibilities1 = get_possibilities(revealed_num, revealed_num*secret)
    possibilities1 = crosscheck(check_dict, possibilities1)
    check_dict[secret] = possibilities1

# print(check_dict)
# first round -------------------------------
revealed_digits = input("enter revealed digits (no sapaces): ")
digits = get_digits(revealed_digits)
possibilities1 = get_possibilities(revealed_num, digits)
possibilities1 = crosscheck(check_dict, possibilities1)
print("possibilities: ")
print(possibilities1)
if len(possibilities1) == 1:
    exit(0)
print()

# second round ------------------------------
# generate list of choices that lead to 1 possibility
print("choices to present: ")
for choice in choices:
    # print("if " + str(choice) + " is given as a choice")
    for pos in possibilities1:
        # print("if secret is " + str(pos))
        pos3 = get_possibilities(choice*revealed_num, choice*revealed_num*pos)
        intersec = [pos for pos in possibilities1 if pos in pos3]
        # print(str(choice) + ": " + str(intersec))
        is_presentable = (len(intersec) == 1) # present the number as a choice only if it leads to 1 possibility
        if not is_presentable:
            break # since we know we can't present this number, move on to the next
    if is_presentable:
        print(choice)


print()
choice = int(input("enter participant's choice: "))
revealed_digits = input("enter revealed digits (no sapaces): ")
digits = get_digits(revealed_digits)
possibilities2 = get_possibilities(choice*revealed_num, digits)
intersec = [pos for pos in possibilities1 if pos in possibilities2]
print("The participant's secret number is:")
print(intersec)
