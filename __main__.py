from secret_number import Performer
from force_matrix import MatrixHandler
import numpy as np
import json

# the script assumes the performer chooses 63 as their number and that the
# participant never chooses a zero as the digit of the product to keep secret.
revealed_num = 63
choices = list(range(2, 20)) # this is our set of possible choices to give to the participant in the second round
# We can set it to any list of integers we want, but I've set it to be all ints from 2 to 20.
# the script will remove any numbers in this list that lead to multiple
# possibilities in the second round, and present us the revised list
performer = Performer(revealed_num, choices)


# first round -------------------------------
revealed_digits = input("enter revealed digits (no sapaces): ")
digits = performer.get_digits(revealed_digits)
print("digits: " + str(digits))
possibilities1 = performer.get_possibilities(digits)
# print('possibilities1: ' + str(possibilities1))
possibilities1 = performer.crosscheck(possibilities1)
print("possibilities: ")
print(possibilities1)


if len(possibilities1) == 1:
    f = list(possibilities1)[0]

else:
    # second round ------------------------------
    print("choices to present: ")
    print(performer.filtered_choices(possibilities1)) # generate list of choices that lead to 1 possibility
    print()
    choice = int(input("enter participant's choice: "))
    revealed_digits = input("enter revealed digits (no sapaces): ")
    digits = performer.get_digits(revealed_digits)
    print("digits: " + str(digits))
    possibilities2 = performer.get_possibilities(digits, choice*revealed_num)
    print("possibilities1: " + str(possibilities1))
    print("possibilities2: " + str(possibilities2))
    intersec = [pos for pos in possibilities1 if pos in possibilities2]
    print("The participant's secret number is:")
    print(intersec)
    # in case this code has a mistake, the program will tell you it failed
    if len(intersec) != 1:
        print('Failure: unable to narrow down secret number to a single possibility')
        exit(0)
    f = intersec[0]
    print(f)



# matrix section ------------------------------
handler = MatrixHandler(f)

# a bunch of randomly generated forcing matrices of various styles and dimensions
positive_interior = []
integer_interior = []
positive_exterior = []
integer_exterior = []

for n in [4, 5, 6]:
    if f > 8*n:
        # only present positive force matrices if f is very large compared to n
        # if f is not much greater than n, the resulting positive force matrix will look wierd: too many repeat seeds
        positive_interior.append( handler.get_interior_matrix(handler.get_rand_positive_seeds(n-1, f), n) )
        positive_exterior.append( handler.get_exterior_matrix(handler.get_rand_positive_seeds(n, f), n) )

    integer_interior.append( handler.get_interior_matrix(handler.get_rand_int_seeds(n-1, f, 10*f), n) )
    integer_exterior.append( handler.get_exterior_matrix(handler.get_rand_int_seeds(n, f, 10*f), n) )

all_matrices = positive_interior + integer_interior + positive_exterior + integer_exterior

print("printing the following to " + handler.pdf_filename + '.pdf : ')
for M in all_matrices:
    print(M)

# generate pdf
handler.print_to_pdf(all_matrices)

# get participant choices
matrix_num = int(input('enter chosen matrix: ')) - 1
chosen_matrix = all_matrices[matrix_num]

again = True
while again:
    fixed_entries = handler.get_fixed_entries(chosen_matrix)


    print('original:')
    print(chosen_matrix)
    print()
    print("invariant entries:")
    print([ (n[0]+1, n[1]+1) for n in fixed_entries ])
    max_entry = np.amax(chosen_matrix)
    pseudo_matrix = handler.get_altered_matrix(handler.get_shuffled_matrix(chosen_matrix, fixed_entries), fixed_entries, max_entry)
    print()
    print('scrambled matrix:')
    print(pseudo_matrix)
    print()
    again = bool('n' in input('Correct? y/n: '))

all_matrices[matrix_num] = pseudo_matrix

input('press enter to swap matrices in ' + handler.pdf_filename + '.pdf: ')
handler.print_to_pdf(all_matrices)