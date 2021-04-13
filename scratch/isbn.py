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
    return ''.join([str(d) for d in front + [last]])


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


def weighted_sum(pos: str, isbn13=False):
    if isbn13:
        return sum([ ( 2*(i%2)+1 )*int(pos[i]) for i in range(len(pos))])
    else:
        return sum([ (10-i)*int(pos[i]) for i in range(len(pos)) ])


def get_factor(altered: str, prime: int):
    res = weighted_sum(altered) % 11
    # print(res)
    for i in range(1,11):
        if (i*prime % 11) == res:
            return i
    print('[WARNING]: no solution to i*'+str(prime)+ ' %11 == ' + str(res) + ' for i in range(1,11)')


def correct_altered(altered: str, prime: int):
    altered_pos = 10 - get_factor(altered, prime)
    return altered[:altered_pos] + str(int(altered[altered_pos]) - prime) + altered[altered_pos + 1:]


print('this version expects a 10 digit ISBN (last entry cannot be 10 or X)')
print('for this version, take any valid isbn10 and add a prime to any entry such that the entry remains a single digit')

altered = input('Enter altered ISBN10 (no spaces): ')
prime = int(input('Enter the prime number used: '))
original = correct_altered(altered, prime)

print('the original ISBN is:')
print(original)