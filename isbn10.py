import random
# isbn13: english book american publisher will start with 978-1 or 978-0 primarily, possibly 979
# isbn10: english book american publisher will start with 1 or 0



def splitint(thing: int):
    return [int(c) for c in str(thing)]


def get_rand_isbn10(exclude10=True):
    front = [ random.choice(range(10)) for _ in range(9)]
    last = (11 - (sum([ (10-i)*front[i] for i in range(len(front)) ]) % 11)) % 11
    if exclude10:
        if last == 10:
            return get_rand_isbn10(True)
    return [d for d in front + [last]]


def check_isbn10(pos):
    pos = str(pos)
    return sum([ (11-i)*int(pos[i]) for i in range(len(pos)) ]) % 11 == 0
    


def get_rand_isbn13(usenglish=True):
    front = [ random.choice(range(10)) for _ in range(12)]
    if usenglish:
        front = [978] + [random.choice([0,1])] + [ random.choice(range(10)) for _ in range(8)]
    last = (10 - (sum([ ( 2*(i%2)+1 )*front[1] for i in range(len(front)) ]) % 10)) % 10

    return int(''.join([str(d) for d in front + [last]]))


def check_isbn13(pos):
    pos = str(pos)

    return sum([ ( 2*(i%2)+1 )*int(pos[i]) for i in range(len(pos))]) % 10 == 0


def weighted_sum(pos: list, isbn13=False):
    if isbn13:
        return sum([ ( 2*(i%2)+1 )*int(pos[i]) for i in range(len(pos))])
    else:
        return sum([ (10-i)*int(pos[i]) for i in range(len(pos)) ])


def get_factor(altered: list, prime: int):
    res = weighted_sum(altered) % 11
    # print(res)
    for i in range(1,11):
        if (i*prime % 11) == res:
            return i
    # print('[WARNING]: no solution to i*'+str(prime)+ ' %11 == ' + str(res) + ' for i in range(1,11)')
    return False


def correct_altered(altered: list, prime: int):
    assert len(altered) == 10
     
    factor = get_factor(altered, prime)

    if factor:
        altered_pos = 10 - factor
        corrected = altered[:altered_pos] + [str(int(altered[altered_pos]) - prime)] + altered[altered_pos + 1:]
        double = [ e for e in corrected if len(e) == 2 ]
        if int(altered[altered_pos]) < prime:
            return False
        if len(double) == 0 or (corrected[-1] == '10' and len(double) == 1 and double[0] == '10'):
            return corrected
    
    return False


def is_pos(pos: list, prime: int):
    double = [ e for e in pos if len(e) == 2 ][0]
    if pos[-1] == double:
        return int(double) <= prime + 10 and int(double) >= prime and int(double) >= 10
    else:
        return int(double) <= prime + 9 and int(double) >= prime and int(double) >= 10


def get_pos_entries(altered: str, prime: int):
    assert len(altered) <= 12 and len(altered) >= 10
    digits = [d for d in altered]

    if len(altered) == 10:
        return [[d for d in altered]]
    elif len(altered) == 11:
        if altered[-2:] == '10':
            return [[d for d in altered][:-2] + ['10']]
        else:
            # then either 10 start, 11 with prime or
            # 11 start, prime added to last entry.
            # in any case
            pos_entries = [ digits[:i] + [''.join(digits[i:i+2])] + digits[i+2:] for i in range(len(digits)-1) ]
            return [ pos for pos in pos_entries if is_pos(pos, prime) ]
    elif len(altered) == 12:
        # then 11 start (last entry MUST be 10) + prime to give 12
        assert altered[-2:] == '10'
        pos_entries = [ digits[:i] + [''.join(digits[i:i+2])] + digits[i+2:-2] + [''.join(digits[-2:])] for i in range(len(digits)-3) ]
        # print(pos_entries)
        return [ pos for pos in pos_entries if is_pos(pos, prime) ]









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
