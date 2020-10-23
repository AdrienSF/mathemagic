from shutil import copyfile
import random
import sys
import webbrowser

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



# split f into a sum of 2n integers.
# there are f-1 choose 2n-1 ways to do this, so we will choose one randomly.

# get random ints that split f into 2n segments
split_points = sorted([0] + list(random.sample(range(1, f), 2*n-1)) + [f])

# convert into a list of 2n ints that sum up to f
seeds = [ split_points[i+1] - split_points[i] for i in range(2*n) ]
# there could be up to 2n! ways of ordering this, so once again we will choose randomly
random.shuffle(seeds)
print(seeds)
print()
col_seeds = seeds[0:n]
row_seeds = seeds[n:2*n]

# sum up the seeds to produce the force matrix
force_matrix = [ [col_seed + row_seed for col_seed in col_seeds] for row_seed in row_seeds ]

# display the matrix on terminal
for row in force_matrix:
    print(row)

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
