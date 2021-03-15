from itertools import permutations
from datetime import datetime, timedelta
import csv

# date and divisibility constraints
def is_valid(digitstr, perf_num, is_md_order=True):

    # chek divisibility
    if not int(digitstr) % perf_num == 0:
        # print('not divisible')
        return False
    
    strpos = str(int(int(digitstr)/perf_num))
    # if it's only 3 digits add a 0 to the front
    if len(strpos) == 3:
        strpos = '0' + strpos

    # print(strpos)
    # check is a valid date
    try:
        if is_md_order:
            date = datetime(1998, int(strpos[:2]), int(strpos[2:]))
        else:
            date = datetime(1998, int(strpos[2:]), int(strpos[:2]))
    except:
        # print('not valid date')
        return False

    # check date is later than 100 years ago
    if date < datetime(1920, 1, 1):
        # print('other')
        return False

    # check date is earlier than 20 years ago
    if date > datetime(2000, 1, 1):
        # print('other')
        return False 

    # print('all good')
    return True

# filter
def yield_filtered_pos(prodstr, perf_num, is_md_order=True):
    # print('perf_num: ' + str(perf_num) + ' | product: ' + prodstr)
    # print('getting next permutation')
    for pos in set(permutations(prodstr)):
        # print('permutation to str')
        strpos = ''.join(pos)
        # print(strpos)
        # print('checking if permutation is valid')
        if is_valid(strpos, perf_num, is_md_order):
            # print('yielding possibility: ' + str(int(strpos)/perf_num))
            yield int(int(strpos)/perf_num)


def get_filtered_pos(prodstr, perf_num, is_md_order=True):
    # print('compliling possibilities')
    if is_md_order:
        return [ datetime(1, int(str(pos)[:-2]), int(str(pos)[-2:])) for pos in yield_filtered_pos(prodstr, perf_num, is_md_order) ]
    else:
        return [ datetime(1, int(str(pos)[-2:]), int(str(pos)[:-2])) for pos in yield_filtered_pos(prodstr, perf_num, is_md_order) ]

# ##### script ######

is_md_order = input("is the date order month/day? y/n: ") == 'y'


# ask the performer to select their number from a list of good options
top_choices = [ 218,  329,  413,  622,  628,  709,  712,  718,  719,
        731,  811,  821,  827,  902,  905,  908,  916,  928,
       1114, 1205, 1207, 1213, 1216, 1217, 1219, 1228, 1231 ]

for i in  range(len(top_choices)):
    print('choice ' + str(i+1) + ': ' + str(top_choices[i]))
perf_num = top_choices[int(input('enter choice num: '))-1]

print("concatenating month and day into a 4 (or 3) digit number and multiplying by the performer's chosen number results in the product that should be input into this script")
digits = input('enter product digits (no spaces): ')
res = get_filtered_pos(digits, perf_num, is_md_order=is_md_order)
# if len(res) != 1:
#     print('[WARNING]: found multiple possibilities:')
#     print(res)
#     exit(0)

# res = res[0]
print(res)
for d in res:
    print(d.strftime('%b') + ' ' + d.strftime('%d'))



'''
performer date, percent instances of 2 possibilities
[[1231.        ,    4.93150685], Psy (whose hit single "Gangnam Style" became a viral video on YouTube)
[1213.        ,    6.02739726], Taylor Swift
[1207.        ,    6.02739726], Larry Bird 
[1217.        ,    6.30136986], Pope Francis
[1216.        ,    6.30136986], Ludwig van Beethoven
[ 709.        ,    6.84931507], Tom Hanks 
[ 413.        ,    6.84931507],
[ 821.        ,    6.84931507],
[ 719.        ,    7.39726027],
[ 916.        ,    7.39726027],
[1228.        ,    8.21917808],
[ 827.        ,    8.49315068],
[1205.        ,    8.49315068],
[ 329.        ,    8.76712329],
[ 718.        ,    9.04109589],
[ 908.        ,    9.04109589],
[1219.        ,    9.04109589],
[ 811.        ,    9.31506849],
[ 622.        ,    9.5890411 ],
[ 218.        ,   10.4109589 ],
[ 905.        ,   10.95890411],
[ 628.        ,   11.23287671],
[ 712.        ,   11.78082192],
[1114.        ,   12.32876712],
[ 928.        ,   12.87671233],
[ 731.        ,   12.87671233],
[ 902.        ,   14.24657534]]
'''