import numpy as np



qdict = {
    'positions of 0s?': '0'
}

bestqs = [
    'positions of 0s?'
]



def parse_ans(ans: str, q: str):
    if 'positions of ' in q:
        val = qdict[q]
        positions = ans.split(',')
        if not ans:
            return lambda pos: val not in pos
        else:
            return lambda pos: all([ pos[int(i)] == val for i in positions ])
    else:
        raise Exception('I don\'t know how to deal with this case')





def get_possible_answers(poslist: list, question):
    if not poslist and not past_qna:
        raise Warning('wtf am I supposed to do? there\'s litteraly no information.')
        return []
    if poslist:
        # do things!
        if 'positions of ' in question:
            val = qdict[question]
            if all([ val not in pos for pos in poslist ]): # the digit is not in any of the isbns at all, this question does not eliminate any posibilities
                return parse_ans([], question)
            else:
                answers = [ ','.join([i for i, x in enumerate([c for c in pos]) if x == val]) for pos in poslist ]
                return [ parse_ans(ans, question) for ans in answers ]
        else:
            raise Exception('f u I can\'t handle this')

            

    else: #can past questions narrow it down enough to store in RAM all posibilities?
        total_known_digits = 0
        known_digits = {}
        for question in past_qna:
            if 'positions of ' in question:
                val = qdict[question]

                positions = past_qna[question].split(',')
                total_known_digits += len(positions)
                for position in positions:
                    known_digits[position] = val
            else:
                raise Exception('f u I can\'t handle this')


        upper_bound = pow(10, 10-total_known_digits)
        if upper_bound < 100000: # then we can consider searching over possible isbns
            poslist = [ [c for c in str(n)] for n in range(upper_bound) ]
            for i in range(len(poslist)):
                for position in known_digits:
                    poslist[i].insert(position, known_digits[position])
                    poslist[i] = ''.join(poslist[i])
            poslist = [ pos for pos in poslist if check_isbn13(pos)]
            if not poslist:
                raise Exception('WHAT THE FUCK')
            return get_possible_answers(poslist, question)


def choose_q(mlendict: dict):
    havelens = { question: mlendict[question] for question in mlendict if mlendict[question] }
    if havelens:
        return havelens.keys()[np.argmin(havelens.values)]
    else:
        if not bestqs:
            raise Exception('well f that didn\'t work')
        return bestqs.pop(0)

def get_poslist(poslist: list, ans, q: str):
    if poslist:
        return [ pos for pos in poslist if ans(pos) ]
    else:
        return []


def get_poslists(poslist: list, question):
    posans = get_possible_answers(poslist, question)
    return { ans: get_poslist(poslist, posans, question) for ans in posans }


poslist = [None, None, None, None, None]
past_qna = {}
while len(poslist) > 1 or not poslist:
    print(len(poslist))
    # look through questions -- get every possible resulting poslist, linked to every posible question
    # policy: choose least bad, best, or average?
    # ... just choose average
    resdict = { question: get_poslists(poslist, question) for question in qdict }
    mlendict = { question: np.mean([len(l) for l in resdict[question].values()]) if resdict[question] else None for question in resdict }
    q = choose_q(mlendict)


    # ask question, load new poslist from answer
    ans_text = input(q)
    ans = parse_ans(q, ans_text)
    poslist = resdict[q][ans]
    past_qna[q] = ans_text