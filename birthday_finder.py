from itertools import permutations
from datetime import datetime, timedelta
import csv

# date and divisibility constraints
def is_valid(digitstr, perf_num):

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
        date = datetime(1998, int(strpos[:2]), int(strpos[2:]))
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
def yield_filtered_pos(prodstr, perf_num):
    # print('perf_num: ' + str(perf_num) + ' | product: ' + prodstr)
    # print('getting next permutation')
    for pos in set(permutations(prodstr)):
        # print('permutation to str')
        strpos = ''.join(pos)
        # print(strpos)
        # print('checking if permutation is valid')
        if is_valid(strpos, perf_num):
            # print('yielding possibility: ' + str(int(strpos)/perf_num))
            yield int(int(strpos)/perf_num)


def get_filtered_pos(prodstr, perf_num):
    # print('compliling possibilities')
    return [ datetime(1, int(str(pos)[:-2]), int(str(pos)[-2:])) for pos in yield_filtered_pos(prodstr, perf_num) ]

# ##### script ######
# perf_nums = [1049, 1064, 1073, 1082, 1085, 1097, 1163, 1172, 1190, 1199, 1208, 1214, 1217, 1229, 
# 1236, 1239, 1247, 1262, 1272, 1289, 1292, 1344, 1388, 1391, 1439, 1529, 1532, 1550, 1556, 1583]



# ask the performer to select their number from a list of good options
top_choices = [1049, 1064, 1073, 1082, 1085, 1097, 1163, 1172, 1190, 1199, 1208, 1214]

for i in  range(len(top_choices)):
    print('choice ' + str(i+1) + ': ' + str(top_choices[i]))
perf_num = top_choices[int(input('enter choice num: '))-1]


digits = input('enter product digits (no spaces): ')
res = get_filtered_pos(digits, perf_num)
# if len(res) != 1:
#     print('[WARNING]: found multiple possibilities:')
#     print(res)
#     exit(0)

# res = res[0]
for d in res:
    print(d.strftime('%b') + ' ' + d.strftime('%d'))
