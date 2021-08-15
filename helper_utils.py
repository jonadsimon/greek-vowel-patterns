from collections import defaultdict

def find_all(a_str, sub):
    '''
    Copied from https://stackoverflow.com/a/4665027/2562771
    '''
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def rec_dd():
    '''
    Copied from https://stackoverflow.com/a/19189356/2562771
    '''
    return defaultdict(rec_dd)
