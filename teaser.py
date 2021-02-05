from secret_number import Performer

def get_possibilities(revealed_num, revealed_digits, total_digits):
    perf = Performer(revealed_num, list(range(20)))




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


# ask the performer to select their number from a list of good options
top_choices = [10161, 15678, 16101, 16839, 17172, 18531, 19611, 20205, 5202, 4041, 729, 63]

for i in  range(len(top_choices)):
    print('choice ' + str(i+1) + ': ' + str(top_choices[i]))
revealed_num = top_choices[int(input('enter choice: '))-1]
# input digits
revealed_digits = [ int(d) for d in input('enter revealed digits(no spaces): ') ]
total_digits = int(input('enter total number of digits: '))
possibilities = get_possibilities(revealed_num, revealed_digits, total_digits)

print('possible secret numbers: ')
print(possibilities)
