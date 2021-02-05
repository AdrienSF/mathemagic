from secret_number import Performer
import statistics as stat

def get_possibilities(revealed_digits: list, revealed_num: int):
    # the computation will be monstrous, so I gave up on running this simulation




results = []
for revealed_num in range(100000):
    print(revealed_num/100000)
    total_pos = []
    for secret_num in range(10, 100):
        product = revealed_num*secret_num
        product_digits = [ int(d) for d in str(product) ]
        for secret_digit in range(0,len(product_digits)):
            product_digits.pop(secret_digit)
            possibilities = get_possibilities(product_digits, revealed_num)
            total_pos.append(len(possibilities))
    
    results.append([ revealed_num, max(total_pos), stat.median(total_pos), stat.mean(total_pos), stat.stdev(total_pos) ])


print('sorting...')
results.sort( key = lambda x: x[1])

print('saving to teaser_results.csv...')
with open("teaser_results.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['revealed_num', 'max_possibilities', 'median_possibilities', 'mean_possibilities', 'stdev_possibilities'])
            writer.writerows(results)

print('done.')