from shutil import copyfile
import random
import sys
import webbrowser
import numpy as np

def html_print(matrix: object):
    # put the matrix into an html file that can be easily printed
    with open('template.html', 'r') as template:
        with open('out.html', 'w') as out:
            out.writelines(template.readlines())
            for row in force_matrix:
                out.write('<p>' + str(row) + '</p>\n')
                out.write("</body>\n")
                out.write("</html>")

                # open the newly created html page
                webbrowser.open("out.html")

def get_ext_matrix(seeds: list, n: int):
    col_seeds = seeds[0:n]
    row_seeds = seeds[n:2*n]

    # sum up the seeds to produce a force matrix (exterior seeds)
    return np.array([ [col_seed + row_seed for col_seed in col_seeds] for row_seed in row_seeds ])

def get_int_matrix(seeds: list, n: int):
    col_seeds = seeds[0:n]
    row_seeds = seeds[n:2*n]
    M = np.array([ [col_seed + row_seed for col_seed in col_seeds] for row_seed in row_seeds ])

    seed_col = random.choice(range(n))
    seed_row = random.choice(range(n))
    M[:, seed_col] -= col_seeds[seed_col]
    M[seed_row, :] -= row_seeds[seed_row]

    return M

def get_positive_seeds(n: int, f: int):
    # split f into a sum of 2n integers.
    # there are f-1 choose 2n-1 ways to do this, so we will choose one randomly.

    # get random ints that split f into 2n segments
    split_points = sorted([0] + list(random.sample(range(1, f), 2*n-1)) + [f])

    # convert into a list of 2n ints that sum up to f
    seeds = [ split_points[i+1] - split_points[i] for i in range(2*n) ]
    # there could be up to 2n! ways of ordering this, so once again we will choose randomly
    random.shuffle(seeds)

    return seeds

def get_int_seeds(n: int, f: int, bound: int):
    # split f into a sum of 2n integers.
    # since the integers can be negative, we need to bound their amplitude
    # so as to avoid putting stupidly large numbers in the matrix
    init = np.array([ random.choice(range(bound)) for i in range(2*n) ])
    zero_sum = init - np.array(get_positive_seeds(n, sum(init))) # these seeds sum to 0 and each seed has an amplitude < bound

    # now add a positive seed list to it and we will get seeds that sum to f but can have negative numbers
    return zero_sum + np.array(get_positive_seeds(n, f))


def get_frac_seeds():
    pass

def get_irrational_seeds():
    pass

# shuffles the given matrix but keeps the indicated items unchanged
def get_shuffled_matrix(matrix: object, fixed_entries: list):
    n, m = np.shape(matrix)
    # fixed_entry_dicts = [ {tuple(entry): matrix[entry[0], entry[1]} for entry in fixed_entries] ]
    entries = list(np.matrix.flatten(matrix))
    # convert the entries into indices corresponding to the flattened matrix
    flattened_fixed_entries = [ n*entry[0] + entry[1] for entry in fixed_entries ]
    # print(entries)
    # reverse this so that we can remove items from entries while iterating over it
    # (effectively itterating over entries backwards)
    flattened_fixed_entries.reverse()
    fixed_entry_dict = { fixed: entries.pop(fixed) for fixed in flattened_fixed_entries }
    # print(fixed_entry_dict)
    # print(entries)
    # shuffle the entries now that the fixed entries are removed
    random.shuffle(entries)
    # return the fixed entries to their place
    for i, val in reversed(fixed_entry_dict.items()):
        entries.insert(i, val)

    # print(entries)
    # return the entries in matrix form
    return np.reshape(entries, (n, m))

# replaces a given percentage of items with random numbers, but keeps indicated
# items unchanged
def get_altered_matrix(matrix: object, fixed_entries: list, percent_change: int, bound: int):
    n, m = np.shape(matrix)
    quant_to_change = int((n*m-len(fixed_entries))*percent_change/100)
    items_to_change = random.sample([(i,j) for i in range(n) for j in range(m) if (i,j) not in fixed_entries], quant_to_change)
    # if the matrix only has positive entries, generate random positive integers only
    if (matrix > 0).all():
        interval = range(bound)
    else:
        interval = range(-1*bound, bound)
        # else allow negative integers as well

    for to_change in items_to_change:
        matrix[to_change] = random.choice(interval)

    return matrix

# input: size n of the matrix, and f the number to force.
try:
    n = int(sys.argv[1])
    f = int(sys.argv[2])
    # check that f and n are positive integers and that f > 2n
    if f <= 2*n or n < 1 or f < 1:
        raise ValueError

except Exception as e:
    print("invalid input\nusage: python3 " + str(sys.argv[0]) + " n f\nwhere n and f are positive integers, and f > 2n\n this script will only work when run from the mathimagic directory")
    print("\n")
    raise



seeds = get_int_seeds(n, f, 50)

matrix = get_ext_matrix(seeds, n)
print(matrix)
print()
fixed = [(0,0), (1,1), (2,2)]
print(get_altered_matrix(matrix, fixed, 25, 50))
