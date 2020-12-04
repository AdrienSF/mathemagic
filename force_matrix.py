import random
import numpy as np
from pylatex import Document, Math, Matrix, Subsection, NoEscape, Tabular
import csv

class MatrixHandler():
    def __init__(self, f=None, 
                pdf_filename='matrices', 
                csv_filename='select_entries.csv', 
                percent_change=20,
                perm_fixed_entries=[(0,0)]):

        self.f = f
        self.pdf_filename = pdf_filename
        self.csv_filename = csv_filename
        self.percent_change = percent_change
        self.perm_fixed_entries = perm_fixed_entries
 

    def get_rand_positive_seeds(self, n: int, f=None):
        if f == None:
            f = self.f
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
        if f == None:
            f = self.f
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
        # reverse sorted order so that we can remove items from entries while iterating over it
        # (effectively itterating over entries backwards)
        flattened_fixed_entries.sort(reverse=True)
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
    def get_altered_matrix(self, matrix: np.array, fixed_entries: list, bound: int, percent_change=None):
        if percent_change == None:
            percent_change = self.percent_change

        n, m = np.shape(matrix)
        quant_to_change = int((n*m-len(fixed_entries))*percent_change/100)
        items_to_change = random.sample([(i,j) for i in range(n) for j in range(m) if (i,j) not in fixed_entries], quant_to_change)
        # if the matrix only has positive entries, generate random positive integers only
        if (matrix >= 0).all():
            interval = list(range(1, bound))
        else:
            interval = list(range(-1*bound, -1)) + list(range(1, bound))
            # else allow negative integers as well

        for to_change in items_to_change:
            matrix[to_change] = random.choice(interval)

        return matrix

    def print_to_pdf(self, matrices: list, filename=None, add_borders=True):
        if filename == None:
            filename = self.pdf_filename

        doc = Document()
        doc.append(NoEscape('\setcounter{secnumdepth}{0}'))
        doc.append(NoEscape('\pagenumbering{gobble}'))
        for i in range(len(matrices)):
            M = matrices[i]
            # set the specs for the table that holds the matrix entries
            if add_borders:
                table_spec = "|" + "|".join(['c' for t in M[0]]) + "|"
            else:
                table_spec = "".join(['c' for t in M[0]])
            

            with doc.create(Subsection('Option #' + str(i+1))):
                with doc.create(Tabular(table_spec)) as table:
                    if add_borders:
                        table.add_hline()
                    for row in M:
                        # if there are negative entries, put a + in front of positives
                        if (M < 0).any():
                            row = [ '+' + str(num) if num >= 0 else '–' + str(-1*num) for num in row ]
                            if "+0" in row:
                                row[row.index("+0")] = '0'

                        table.add_row(row)
                        if add_borders:
                            table.add_hline()
        
        doc.generate_pdf(filename, clean_tex=False)


    def get_fixed_entries(self, matrix: np.array, filename=None):
        if filename == None:
            filename = self.csv_filename

        # make sure some key entries are fixed, for example if there is a 0 entry
        perm_fixed_entries = [ tuple(ntry) for ntry in self.perm_fixed_entries ]
        if (matrix == 0).any():
            coord0 = np.where(matrix == 0)
            perm_fixed_entries.append((int(coord0[0]), int(coord0[1])))
        perm_fixed_entries = list(set(perm_fixed_entries))

        # convert ndarray to vanilla python
        matrix = [ [item for item in row] for row in matrix ]
        # mark fixed entries with *
        for entry in perm_fixed_entries:
            matrix[entry[0]][entry[1]] = '[' + str(matrix[entry[0]][entry[1]]) + ']'

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(matrix)

        print('generated \'select_entries.csv\'')
        print('add a \'*\' to the entries of \'select_entries.csv\' that should remain invariant')
        print('some entries have already been marked as invariant with brackets: []')
        input('press enter to save invariant entries: ')

        fixed_entries = []
        rows = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                rows.append(row)

            for i in range(len(rows)):
                for j in range(len(rows[0])):
                    if '*' in rows[i][j] or '[' in rows[i][j]:
                        fixed_entries.append((i, j))
        
        return list(set(fixed_entries))
            
