from secret_number import Performer
from force_matrix import MatrixHandler
import numpy as np
import json
import webbrowser
from color_matrix import ColorMatrix
import random

# the script assumes that the participant never chooses a zero as the digit of the product to keep secret.

# initialization -------------------------------
# generates a pdf of feigned downloaded random matrices
dummy = MatrixHandler()
f = 73
positive_interior = []
integer_interior = []
positive_exterior = []
integer_exterior = []
for n in [4, 5, 6]:
    if f > 8*n:
        # only present positive force matrices if f is very large compared to n
        # if f is not much greater than n, the resulting positive force matrix will look wierd: too many repeat seeds
        positive_interior.append( dummy.get_interior_matrix(dummy.get_rand_positive_seeds(n-1, f), n) )
        positive_exterior.append( dummy.get_exterior_matrix(dummy.get_rand_positive_seeds(n, f), n) )

    integer_interior.append( dummy.get_interior_matrix(dummy.get_rand_int_seeds(n-1, f, 10*f), n) )
    integer_exterior.append( dummy.get_exterior_matrix(dummy.get_rand_int_seeds(n, f, 10*f), n) )

all_matrices = positive_interior + integer_interior + positive_exterior + integer_exterior

# generate coresponding color matrices
color_handler = ColorMatrix()
color_matrices = [ color_handler.get_color_matrix(len(M), len(M[0])) for M in all_matrices ]

# scramble all matrices
for i in range(len(all_matrices)):
    all_matrices[i] = dummy.get_altered_matrix(dummy.get_shuffled_matrix(all_matrices[i], constrain_digits=False), np.amax(all_matrices[i]), constrain_digits=False)
# duplicate to 99 options
i = 0
duped_mats = []
duped_colors = []
while len(duped_mats) < 99:
    i += 1
    duped_mats.append(all_matrices[i % len(all_matrices)])
    duped_colors.append(color_matrices[i % len(all_matrices)])

rand_order = list(range(99))
random.shuffle(rand_order)
duped_mats[:] = [ duped_mats[i] for i in rand_order]
duped_colors[:] = [ duped_colors[i] for i in rand_order]

dummy.print_to_pdf(duped_mats, duped_colors)


# ask the performer to select their number from a list of good options
top_choices = [10161, 15678, 16101, 16839, 17172, 18531, 19611, 20205, 5202, 4041, 729, 63]


for i in  range(len(top_choices)):
    print('choice ' + str(i+1) + ': ' + str(top_choices[i]))
revealed_num = top_choices[int(input('enter choice: '))-1]
choices = list(range(2, 20)) # this is our set of possible choices to give to the participant in the second round
# We can set it to any list of integers we want, but I've set it to be all ints from 2 to 20.
# the script will remove any numbers in this list that lead to multiple
# possibilities in the second round, and present us the revised list
performer = Performer(revealed_num, choices)


# first round -------------------------------
revealed_digits = input("enter revealed digits (no spaces): ")
digits = performer.get_digits(revealed_digits)
print("digits: " + str(digits))
possibilities1 = performer.get_possibilities(digits)
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
    revealed_digits = input("enter revealed digits (no spaces): ")
    digits = performer.get_digits(revealed_digits)
    print("digits: " + str(digits))
    possibilities2 = performer.get_possibilities(digits, choice*revealed_num)
    intersec = [pos for pos in possibilities1 if pos in possibilities2]
    # in case this code has a mistake, the program will tell you it failed
    if len(intersec) != 1:
        print('Failure: unable to narrow down secret number to a single possibility')
        exit(0)
    print("The participant's secret number is:")
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

    # bound = min([])
    integer_interior.append( handler.get_interior_matrix(handler.get_rand_int_seeds(n-1, f, 10*f), n) )
    integer_exterior.append( handler.get_exterior_matrix(handler.get_rand_int_seeds(n, f, 10*f), n) )

all_matrices = positive_interior + integer_interior + positive_exterior + integer_exterior

# print("printing the following to " + handler.pdf_filename + '.pdf : ')
# for M in all_matrices:
#     print(M)


# duplicate to 99 options
i = 0
duped_mats = []
duped_colors = []
while len(duped_mats) < 99:
    i += 1
    duped_mats.append(all_matrices[i % len(all_matrices)])
    duped_colors.append(color_matrices[i % len(all_matrices)])

rand_order = list(range(99))
random.shuffle(rand_order)
duped_mats[:] = [ duped_mats[i] for i in rand_order]
duped_colors[:] = [ duped_colors[i] for i in rand_order]


# generate pdf
handler.print_to_pdf(duped_mats, duped_colors)

# get participant choices
matrix_num = int(input('enter chosen matrix: ')) - 1
chosen_matrix = duped_mats[matrix_num]


# ###### too verbose:
# again = True
# while again:
#     fixed_entries, coord_dict = handler.get_fixed_entries(chosen_matrix)


#     print('original:')
#     print(chosen_matrix)
#     print()
#     print("invariant entries:")
#     print([ (n[0]+1, n[1]+1) for n in fixed_entries ])
#     max_entry = np.amax(chosen_matrix)
#     pseudo_matrix = handler.get_altered_matrix(handler.get_shuffled_matrix(chosen_matrix, fixed_entries=fixed_entries), max_entry, fixed_entries=fixed_entries)
#     print()
#     print('scrambled matrix:')
#     print(pseudo_matrix)
#     print()
#     again = bool('n' in input('Correct? y/n: '))

fixed_entries, coord_dict = handler.get_fixed_entries(chosen_matrix)
max_entry = np.amax(chosen_matrix)
pseudo_matrix = handler.get_altered_matrix(handler.get_shuffled_matrix(chosen_matrix, fixed_entries=fixed_entries), max_entry, fixed_entries=fixed_entries)


# shuffle all matrices
for i in range(len(duped_mats)):
    duped_mats[i] = handler.get_altered_matrix(handler.get_shuffled_matrix(duped_mats[i], constrain_digits=False), np.amax(duped_mats[i]), constrain_digits=False)

# replace the chosen matrix with a specially shuffled matrix
duped_mats[matrix_num] = pseudo_matrix
# replace it's cooresponing color matrix with a octored one
duped_colors[matrix_num] = color_handler.get_doctored_matrix(duped_colors[matrix_num], coord_dict)

# set the option whose number is the secret number to the same matrix as the chosen matrix
duped_mats[f-1] = pseudo_matrix

input('press enter to swap matrices in ' + handler.pdf_filename + '.pdf: ')
handler.print_to_pdf(duped_mats, duped_colors)

