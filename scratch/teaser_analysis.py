from collections import Counter
from itertools import permutations
import csv
import statistics as stat
import math

def total_differing(digits1: dict, digits2: dict):
    return sum([ abs(digits1[d] - digits2[d]) if d in digits2 else digits1[d] for d in digits1 ])


results = []
# mult_9s = [ 9*i for i in range(2,11112) ]
mult_9s = [ int("".join(perm)) for perm in permutations(['1','2','3','4','5','6','7','8','9','0']) ]
for n in mult_9s:
    possible_prod_digits = [ dict(Counter([ int(d) for d in str(n*i) ])) for i in range(10,100) ]
    pos_counts = []
    for s in range(10,100):
        prod = s*n
        actual_digits = dict(Counter([ int(d) for d in str(prod) ]))
        pos_count = len([ 1 for pos_digits in possible_prod_digits if total_differing(pos_digits, actual_digits) <= math.floor(len(actual_digits)/2) ])
        pos_counts.append(pos_count)

    res = [ n, max(pos_counts), stat.median(pos_counts), stat.mean(pos_counts), stat.stdev(pos_counts) ]
    results.append(res)
    print(res)


print('sorting...')
results.sort( key = lambda x: x[1])

print('saving to teaser_results.csv...')
with open("10_digit_teaser_results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['possibilities_upper_bound is always at least as large as the max number of possibilities, for any given mult_9'])
            writer.writerow(['mult_9', 'possibilities_upper_bound', 'median_possibilities', 'mean_possibilities', 'stdev_possibilities'])
            writer.writerows(results)

print('done.')