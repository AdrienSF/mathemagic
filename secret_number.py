import random
import itertools

input("choose a secret number between 1 and 100, and I will choose one as well")

# revealed_num = 9 * random.choice([1, 2, 3, 5, 7, 9, 11])
revealed_num = 45
# restrict to prime numbers, so as to diminish the number of divisors of the
# secret product, and hence narrow down the possibilities.

input("the number I chose was " + str(revealed_num))
print("now calculate the product of our two numbers")
some_digits = input("keep any one of the digits of this number secret, and enter the others in any order (no spaces): ")
last_digit = 9 - (sum([int(d) for d in some_digits]) % 9) # if the mod is 0, the last digit could be 9 or 0
digits = [str(d) for d in some_digits] + [str(last_digit)]
permutations = list(set([int(num) for num in [ "".join(permutation) for permutation in list(itertools.permutations(digits)) ] ]))
print(permutations)
possibilities = [ num for num in permutations if num % revealed_num == 0 and num > 10*len(digits) ]
print(possibilities)
print([ pos/revealed_num for pos in possibilities ])
possible_secret_nums = sorted([ int(pos/revealed_num) for pos in possibilities if pos/revealed_num < 100 ])
print(possible_secret_nums)
if len(possible_secret_nums) == 1:
    print("your secret number is: " + str(possible_secret_nums[0]))
    exit(0)

# if the program hasn't terminated it means there are multiple possibilities.
# the question is, how to narrow it down from here?
# idea: determine which number it is through a simple >= question
# midpoint = int((possible_secret_nums[0] + possible_secret_nums[1])/2)
# if input("is your number greater than " + str(midpoint) + "? (y/n):") == "y":
#     print("secret number is: " + str(possible_secret_nums[1]))
# else:
#     print("secret number is: " + str(possible_secret_nums[0]))



# mult_9 = [ 9*i for i in range(1,12) ]
# random.shuffle(mult_9)
# possible_secret_nums = set(range(1, 100))
#
# while mult_9:
#     revealed_num = mult_9.pop(0)
#     input("the number I chose was " + str(revealed_num))
#     print("now calculate the product of our two numbers")
#     some_digits = input("keep any one of the digits of this number secret, and enter the others in any order (no spaces): ")
#     last_digit = 9 - (sum([int(d) for d in some_digits]) % 9)
#     digits = [str(d) for d in some_digits] + [str(last_digit)]
#     permutations = list(set([int(num) for num in [ "".join(permutation) for permutation in list(itertools.permutations(digits)) ] ]))
#     print(permutations)
#     possibilities = [ num for num in permutations if num % revealed_num == 0 ]
#     print(possibilities)
#     print([ pos/revealed_num for pos in possibilities ])
#     possible_secret_nums = set([ pos/revealed_num for pos in possibilities ]) & possible_secret_nums
#     print(possible_secret_nums)
#     if len(possible_secret_nums) == 1:
#         print("your secret number is: " + str(int(possible_secret_nums.pop())))
#         break

# how many possibilities / how to reverse engineer to 100%
# plug into force_matrix.py <<(later?make more complex force matrices to choose from)
# push secret num to webpage <<(+scrambled force matrix)
