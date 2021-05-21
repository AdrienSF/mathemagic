import random
from isbnfuncs import get_pos_entries, correct_altered
# isbn13: english book american publisher will start with 978-1 or 978-0 primarily, possibly 979
# isbn10: english book american publisher will start with 1 or 0




print('For this version, take any valid isbn10 and add a 1 digit prime to any entry')

altered = [d for d in input('Enter altered ISBN10 (no spaces): ')]
prime = int(input('Enter the prime number used: '))
all_pos = get_pos_entries(altered, prime)
# print(all_pos)
# original = correct_altered(pos, prime)

print('the original ISBN is one of the following:')
for pos in all_pos:
    og = correct_altered(pos, prime)
    if og:
        print(''.join(og))
        print(og)
        print('open this link to look up the cooresponding book:')
        if og[-1] == '10':
            og[-1] = 'x'
        print('https://isbnsearch.org/isbn/' + ''.join(og))
