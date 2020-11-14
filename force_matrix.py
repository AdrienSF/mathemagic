import random
import numpy as np
import csv


class MatrixHandler():
    # def __init__(self, f: int):
    #     self.f = f

    def get_rand_positive_seeds(self, n: int, f: int):
        # split f into a sum of 2n integers.
        # there are f-1 choose 2n-1 ways to do this, so we will choose one randomly.

        # get random ints that split f into 2n segments
        split_points = sorted([0] + list(random.sample(range(1, f), 2*n-1)) + [f])

        # convert into a list of 2n ints that sum up to f
        seeds = [ split_points[i+1] - split_points[i] for i in range(2*n) ]
        # there could be up to 2n! ways of ordering this, so once again we will choose randomly
        random.shuffle(seeds)

        return np.array(seeds)

    def get_rand_int_seeds(self, n: int, f: int, bound: int):
        # split f into a sum of 2n integers.
        # since the integers can be negative, we need to bound their amplitude
        # so as to avoid putting stupidly large numbers in the matrix
        init = np.array([ random.choice(range(bound)) for i in range(2*n) ])
        zero_sum = init - np.array(self.get_rand_positive_seeds(n, sum(init))) # these seeds sum to 0 and each seed has an amplitude < bound

        # now add a positive seed list to it and we will get seeds that sum to f but can have negative numbers
        return zero_sum + np.array(self.get_rand_positive_seeds(n, f))

    # returns a matrix where the seeds are not present. no random choices
    def get_exterior_matrix(self, seeds: list, n: int):
        col_seeds = seeds[0:n]
        row_seeds = seeds[n:2*n]

        # sum up the seeds to produce a force matrix (exterior seeds)
        return np.array([ [col_seed + row_seed for col_seed in col_seeds] for row_seed in row_seeds ])

    # returns a matrix that contains the seeds, and a 0. 
    # Where these seeds are positioned in the matrix is chosen randomly
    # requires 2 fewer seeds than for exterior matrices
    def get_interior_matrix(self, seeds: list, n: int):
        if len(seeds) != 2*(n-1):
            print("get_interior_matrix expected 2*(n-1) seeds but got: " + str(len(seeds)) + " with n=" + str(n))
            raise TypeError()
        n = n-1
        col_seeds = list(seeds[0:n])
        row_seeds = list(seeds[n:2*n])
        
        seed_col = random.choice(range(n))
        seed_row = random.choice(range(n))
        
        col_seeds.insert(seed_row, 0)
        row_seeds.insert(seed_col, 0)


        M = np.array([ [col_seed + row_seed for col_seed in col_seeds] for row_seed in row_seeds ])

        # M[:, seed_col] -= col_seeds[seed_col]
        # M[seed_row, :] -= row_seeds[seed_row]

        return M

    # shuffles the given matrix but keeps the indicated items unchanged
    def get_shuffled_matrix(self, matrix: np.array, fixed_entries: list):
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
    def get_altered_matrix(self, matrix: np.array, fixed_entries: list, percent_change: int, bound: int):
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

    def swap_matrix(self, filename: str, label: int, to_insert: np.array):
        n, m = np.shape(to_insert)
        
        with open(filename) as inf:
            rows = [ row for row in csv.reader(inf.readlines()) ]

        label_position = rows.index(['Matrix #'+str(label)])
        rows[label_position+1 : label_position+1 + n ] = list(to_insert)

        print(rows)
        with open(filename, 'w', newline='') as csvfile:
            mwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            mwriter.writerows(rows)
            
