import itertools

class Performer():
    def __init__(self, revealed_num, choices):
        self.revealed_num = revealed_num
        self.choices = choices
        self.check_dict = self.get_check_dict()

    # given all but one non-zero digit, find the last digit and return all the digits
    def get_digits(self, revealed_digits: str):
        revealed_digits = sorted([ int(d) for d in revealed_digits], reverse=True)
        last_digit = 9 - (sum(revealed_digits) % 9)
        if last_digit == 9:
            print('warning: hidden digit could be 0 OR 9. Continuing with the assumption that it is 9')
        digits = int("".join([str(last_digit)] + [str(d) for d in revealed_digits]))

        return digits


    # given some digits and the total number of digits, return the possible digits
    def get_pos_digits(self, revealed_digits: list, total_digits: int):
        total_last_digits = total_digits - len(revealed_digits)
        digit_set = set(range(pow(10, total_last_digits-1), pow(10, total_last_digits)))
        last_digits_pos = [ revealed_digits + [int(d) for d in str(pos)] for pos in digit_set if sum(revealed_digits + [int(d) for d in str(pos)]) % 9 == 0 ]

        return last_digits_pos


    # this is a way of eliminating further possibilities
    def crosscheck(self, to_check: set, check_dict=None):
        if check_dict == None:
            check_dict = self.check_dict
        iter = sorted(list(to_check))
        for pos in iter:
            if pos in check_dict and check_dict[pos] != to_check:
                to_check.remove(pos)

        return to_check

    # given the product digits in some order, returns possible secret numbers
    def get_possibilities(self, digits: int, revealed_num=None, r=100):
        if not revealed_num:
            revealed_num = self.revealed_num

        digits = [d for d in str(digits)]
        permutations = list(set([int(num) for num in ["".join(permutation) for permutation in list(itertools.permutations(digits))]]))
        possibilities1 = [int(num/revealed_num) for num in permutations if num % revealed_num == 0 and num/revealed_num < r]

        return set(possibilities1)

    # this generates the dictionary used for crosscheck()
    def get_check_dict(self, revealed_num=None, r=100):
        check_dict = {}
        if not revealed_num:
            revealed_num = self.revealed_num
        for secret in range(1, r):
            possibilities1 = self.get_possibilities(revealed_num*secret, revealed_num, r)
            possibilities1 = self.crosscheck(possibilities1, check_dict)
            check_dict[secret] = possibilities1

        return check_dict

    # returns choices that will lead to just one possibility in the second round
    def filtered_choices(self, possibilities1: list, revealed_num=None, choices=None):
        if not revealed_num:
            revealed_num = self.revealed_num
        if not choices:
            choices = self.choices
        presentables = []
        for choice in choices:
            for pos in possibilities1:
                pos3 = self.get_possibilities(choice*revealed_num*pos, choice*revealed_num)
                intersec = [pos for pos in possibilities1 if pos in pos3]
                is_presentable = (len(intersec) == 1) # present the number as a choice only if it leads to 1 possibility
                if not is_presentable:
                    break # since we know we can't present this number, move on to the next
            if is_presentable:
                presentables.append(choice)

        return presentables