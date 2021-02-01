import random
import numpy as np
from pylatex import Document, Math, Matrix, Subsection, NoEscape, Tabular, Section, Package
import csv
from datetime import date
from color_matrix import ColorMatrix

class MatrixHandler():
    def __init__(self, f=None, 
                pdf_filename='matrices', 
                csv_filename='select_entries.csv', 
                percent_change=20,
                perm_fixed_entries=[(0,0)],
                constrain_digits=True):

        self.f = f
        self.pdf_filename = pdf_filename
        self.csv_filename = csv_filename
        self.percent_change = percent_change
        self.perm_fixed_entries = perm_fixed_entries
        self.constrain_digits = constrain_digits
 

    def get_rand_positive_seeds(self, n: int, f=None):
        total_samples = 2*n-1
        if f == None:
            f = self.f
        if n == 1:
            return [f]
        if f-1 < total_samples:
            zeros = [ 0 for i in range(total_samples - f + 1) ]
        else:
            zeros = []

            # 2*n-1 - f
        # split f into a sum of 2n integers.
        # there are f-1 choose 2n-1 ways to do this, so we will choose one randomly.

        # get random ints that split f into 2n segments
        split_points = sorted([0] + list(random.sample(zeros + list(range(1, f)), total_samples)) + [f])

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
    def get_shuffled_matrix(self, matrix: np.array, fixed_entries=[], constrain_digits=None):
        if constrain_digits == None:
            constrain_digits = self.constrain_digits
        if constrain_digits:
            for i in range(len(str(np.amax(matrix)))):
                curr_fixed = [ (j, k) for j in range(len(matrix)) for k in range(len(matrix[0])) if not (abs(matrix[j][k]) >= pow(10, i) and abs(matrix[j][k]) < pow(10, (i+1)) )] + list(fixed_entries)
                curr_fixed = list(set(curr_fixed))
                matrix = self.shuffle_helper(matrix, curr_fixed)
            return matrix
        else:
            return self.shuffle_helper(matrix, fixed_entries)

    def shuffle_helper(self, matrix: np.array, fixed_entries=[]):
        n, m = np.shape(matrix)
        entries = list(np.matrix.flatten(matrix))
        # convert the entries into indices corresponding to the flattened matrix
        flattened_fixed_entries = [ n*entry[0] + entry[1] for entry in fixed_entries ]
        # reverse sorted order so that we can remove items from entries while iterating over it
        # (effectively itterating over entries backwards)
        flattened_fixed_entries.sort(reverse=True)
        fixed_entry_dict = { fixed: entries.pop(fixed) for fixed in flattened_fixed_entries }
        # shuffle the entries now that the fixed entries are removed
        random.shuffle(entries)
        # return the fixed entries to their place
        for i, val in reversed(list(fixed_entry_dict.items())):
            entries.insert(i, val)

        # return the entries in matrix form
        return np.reshape(entries, (n, m))

    # replaces a given percentage of items with random numbers, but keeps indicated
    # items unchanged
    def get_altered_matrix(self, matrix: np.array, bound: int, fixed_entries=[], percent_change=None, constrain_digits=None):
        if constrain_digits == None:
            constrain_digits = self.constrain_digits
        if percent_change == None:
            percent_change = self.percent_change

        n, m = np.shape(matrix)
        quant_to_change = int((n*m-len(fixed_entries))*percent_change/100)
        items_to_change = random.sample([(i,j) for i in range(n) for j in range(m) if (i,j) not in fixed_entries], quant_to_change)
        # if the matrix only has positive entries, generate random positive integers only
        if (matrix >= 0).all():
            interval = list(range(1, bound))
            pos_signs = [1]
        else:
            interval = list(range(-1*bound, -1)) + list(range(1, bound))
            pos_signs = [1, -1]
            # else allow negative integers as well
        
        if constrain_digits:
            for to_change in items_to_change:
                digits = str(abs(matrix[to_change]))
                matrix[to_change] = random.choice(pos_signs) * int(''.join([str(random.choice(list(range(1*int(digits.index(d) == 0), 10)))) for d in digits]))
                                    # random sign               ranomize each digit from 0 through 9, except first digit never 0
        else:

            for to_change in items_to_change:
                matrix[to_change] = random.choice(interval)

        return matrix

    def print_to_pdf(self, matrices: list, color_matrices: list, filename=None, add_borders=True):
        if filename == None:
            filename = self.pdf_filename

        doc = Document()
        doc.packages.append(Package('xcolor', options='table'))
        doc.packages.append(Package('transparent'))
        # doc.packages.append(Package('geometry', options='margin=0.5in'))
        doc.append(NoEscape('\setcounter{secnumdepth}{0}'))
        doc.append(NoEscape('\pagenumbering{gobble}'))
        doc.append(NoEscape('\setlength{\\arrayrulewidth}{1pt}'))
        # define colors from color dict
        colors = ColorMatrix()
        for color in colors.strDict:
            doc.append(NoEscape(colors.strDict[color]))
            
        


        today = date.today()
        with doc.create(Section(NoEscape('{\\fontsize{20pt}{15pt}\selectfont' + ' Randomly generated numbers collected on ' + str(today) + ' and adapted from:}'))):
            doc.append(NoEscape('{\\fontsize{14pt}{12pt}\selectfont' + ' https://onlinemathtools.com/generate-random-matrix}'))

        with doc.create(Section(NoEscape('{\\fontsize{20pt}{15pt}\selectfont' + ' Zoom color palette shuffled with and adapted from:}'))):
            doc.append(NoEscape('{\\fontsize{14pt}{12pt}\selectfont' + ' https://onlinerandomtools.com/shuffle-words}'))
            doc.append(NoEscape("\\newpage"))
            
        for i in range(len(matrices)):
            M = matrices[i]
            C = color_matrices[i]
            # set the specs for the table that holds the matrix entries
            if add_borders:
                border = '|'
            else:
                border = ''
            
            with doc.create(Subsection('Option #' + str(i+1))):
                ############ create number table
                with doc.create(Tabular(border + border.join(['c' for t in M[0]]) + border)) as table:
                    if add_borders:
                        table.add_hline()
                    for row in M:
                        # if there are negative entries, put a + in front of positives
                        if (M < 0).any():
                            row = [ '+' + str(num) if num >= 0 else '–' + str(-1*num) for num in row ]
                            if "+0" in row:
                                row[row.index("+0")] = '0'
                                # NoEscape('\cellcolor{green}0')

                        table.add_row(row)
                        if add_borders:
                            table.add_hline()

                # doc.append(NoEscape("\hfill")) # same line right side
                doc.append(NoEscape("\\break")) # new line
                doc.append(NoEscape("\\vspace{1cm}")) # new line
                # doc.append('.') # new line
                doc.append(NoEscape("\\break")) # new line
                ############ create color table
                # fin correct table width
                if (M < 0).any():
                    if (M > 1000).any():
                        spacer = '23.2'
                    else:
                        spacer = '23.1'
                else:
                    spacer = '10'
                    
                with doc.create(Tabular(border + border.join(['m{' + spacer + 'px}' for t in C[0]]) + border)) as table:
                    if add_borders:
                        table.add_hline()
                    for row in C:
                        table.add_row([ NoEscape('\cellcolor{'+ color + '}') for color in row])
                        if add_borders:
                            table.add_hline()


        
        doc.generate_pdf(filename, clean_tex=False)



    def get_fixed_entries(self, matrix: np.array, filename=None):
        input_matrix = matrix
        if filename == None:
            filename = self.csv_filename

        # make sure some key entries are fixed, for example if there is a 0 entry
        perm_fixed_entries = [ tuple(ntry) for ntry in self.perm_fixed_entries ]
        if (matrix == 0).any():
            coord0 = np.where(matrix == 0)
            try:
                perm_fixed_entries.append((int(coord0[0]), int(coord0[1])))
            except:
                coord0 = np.transpose(coord0)
                for coords in coord0:
                    perm_fixed_entries.append((int(coords[0]), int(coords[1])))

        

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
            # add color choice columns
            color_handler = ColorMatrix()
            # color_choices = np.transpose(np.array([ list(color_handler.strDict.keys()) for i in matrix ]))
            # # convert ndarray to vanilla python
            # color_choices = [ [item for item in row] for row in color_choices ] #just one line
            # writer.writerows(color_choices)

            writer.writerow(list(color_handler.strDict.keys()))


        print('generated \'select_entries.csv\'')
        # print('add a \'x\' to the number entries of \'select_entries.csv\' that should remain invariant')
        # print('some entries have already been marked as invariant with brackets: []')
        print('add coordinates (comma seperated) to the color entries to select the color of the invariant entry said coordinates (ex: white1,2')
        input('press enter to save invariant entries and their colors: ')

        # fixed_entries = []
        # chosen_entries = []
        rows = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                rows.append(row)

            # collect selected number entries
            # for i in range(len(matrix)):
            #     for j in range(len(matrix[0])):
            #         if 'x' in rows[i][j]:
            #             chosen_entries.append((i, j))
            #         if 'x' in rows[i][j] or '[' in rows[i][j]:
            #             fixed_entries.append((i, j))

            # # sanity check
            # if len(chosen_entries) != len(matrix):
            #     print('the matrix is of size ' + str(len(matrix)) + ' but ' + str(len(chosen_entries)) + ' entries were selected')
            #     print('retrying selection: ')
            #     print()
            #     return self.get_fixed_entries(np.array(input_matrix))
                
            # collect selected color entries
            # coord_dict = {}
            # for i in range(len(rows[0]), len(rows)):
            #     for j in range(len(rows[0])):
            #         if 'x' in rows[i][j]:
            #             color = list(color_handler.strDict.keys())[i-len(rows[0])]
            #             matching_coords = [ coords for coords in chosen_entries if coords[1] == j ]
            #             if len(matching_coords) > 1:
            #                 print("Warning: expected one item but found: " + len(coords))
            #                 print("Using first item.")
            #             coords = matching_coords.pop()

            #             coord_dict[coords] = color
            color_row = rows[-1]
            # turn color row into list of coords
            coord_list = [ item for item in color_row if ',' in item ] # get entries that have commas
            coord_list = [ [d for d in item if d.isdigit() or d == ','] for item in coord_list ] # extract only the numbers and commas from the entry
            coord_list = [ "".join(item) for item in coord_list ] # join the coords into a single string
            coord_list = [ item.split(',') for item in coord_list ] # split the string around the comma
            coord_list = [ [int(n)-1 for n in item] for item in coord_list ] # convert to int and subtract 1 to get 0 indexed column and row numbers
            coord_list = [ tuple(item) for item in coord_list ] # turn the coordinate list of list into list of tuples
            # sanity check
            if len(coord_list) != len(matrix):
                print('the matrix is of size ' + str(len(matrix)) + ' but ' + str(len(coord_list)) + ' colors were selected')
                print('retrying selection: ')
                print()
                return self.get_fixed_entries(np.array(input_matrix))

            # turn list of coords into a color dict of coords
            color_names = list(color_handler.strDict.keys())
            coord_dict = { coord_list[i]: color_names[i] for i in range(len(coord_list))}


        
        return list(coord_dict.keys()), coord_dict
            
