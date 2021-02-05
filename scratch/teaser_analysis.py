from secret_number import Performer
import itertools
import math
import statistics as stat
import csv

def get_possibilities(revealed_num: int, revealed_digits: list, total_digits: int, perf):

    # get possible digits
    possible_digits = perf.get_pos_digits(revealed_digits, total_digits)

    # get possible secret num for every possible set of digits
    possibilities = set([])
    for digits in possible_digits:
        pos = perf.get_possibilities(int(''.join([str(d) for d in digits])))
        possibilities = possibilities.union(pos)

    # remove 1 digit numbers from the possibilities
    possibilities = [pos for pos in possibilities if len(str(pos)) > 1]
    return possibilities



mult_9s = [ 9*i for i in range(2,111)]#12) ]
secret_nums = range(10,100)

results = []
for mult in mult_9s:
    print((mult/9)/11112)
    perf = Performer(mult, list(range(20)))
    total_pos = []
    for num in secret_nums:
        product = num*mult
        product_digits = [ int(d) for d in str(product) ]
        for revealed_digits in itertools.combinations(product_digits, math.ceil(len(product_digits)/2)):
            possibilities = get_possibilities(mult, list(revealed_digits), len(product_digits), perf)
            total_pos.append(len(possibilities))

    results.append([mult, max(total_pos), stat.median(total_pos), stat.mean(total_pos), stat.stdev(total_pos)])

print('sorting...')
results.sort( key = lambda x: x[1])

print('saving to teaser_results.csv...')
with open("teaser_results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['mult_9', 'max_possibilities', 'median_possibilities', 'mean_possibilities', 'stdev_possibilities'])
            writer.writerows(results)

print('done.')