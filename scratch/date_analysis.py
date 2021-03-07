from itertools import permutations
from datetime import datetime, timedelta
import csv
import random

# given date constraints and choice of a 2 digit number, 
# how much information do you need about the product to find the date?


# first premise: we know all digits in any order



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
    return list(yield_filtered_pos(prodstr, perf_num))


#######ANALYSIS
def pos_dates(date):
    # yield a random date once
    # yield datetime(random.choice(range(1920, 2000)), random.choice(range(1,13)), random.choice(range(1,28)))

    # if date > datetime(2000, 1, 1) or date < datetime(1920, 1, 1):
    #     return

    # yield date

    # for yielded in pos_dates(date + timedelta(days=1)):
    #     yield yielded
    # >>>>>> RecursionError: maximum recursion depth exceeded while calling a Python object
    # nooo python why!?
    # print('getting next date')
    while date <= datetime(1998, 12, 31) and date >= datetime(1920, 1, 1):
        yield date 
        date += timedelta(days=1)


for perf_num in range(1000, 10000):
    for date in pos_dates(datetime(1998, 1, 1)):
        date_int = int(date.strftime("%m") + date.strftime("%d"))

        prodstr = str(date_int*perf_num)
        # print('getting possibilities...')
        res  = len(get_filtered_pos(prodstr, perf_num))
        # print(str([ perf_num, date_int, res ]))
        # check if there are more than 30 possibilities. if so skip this perf num
        # if res > 100:
        #     print(str(perf_num) + ': trying nex perf num')
        #     break

        # if date >= datetime(1998, 12, 31):
        #     print('succes!-----------------------------------------')
        #     print(str([ perf_num, date_int, res ]))

        # # print('writing possibilities...')
        with open('4digit_possibillity_counts.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow([ perf_num, date_int, res ])

        assert res != 0