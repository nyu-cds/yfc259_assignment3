'''
Assignment 5, part 2:
Write a program that takes two arguments n and k and prints all binary strings of length n that contain k zero bits, one per line.
Yu-Fen Chiu (yfc259)
'''
from itertools import permutations
from itertools import repeat
def zbits(n, k):
    """
    :param n: length of string
    :param k: number of zero bits
    :return: all binary strings of length n that contain k zero bits
    """
    # create an empty set to store the results
    result = set()
    # combine two lists: one contains (n-k) one bits, and another contains k zero bits
    item = list(repeat("1",(n-k))) + list(repeat("0",k))
    # loop over the iterator
    for thing in permutations(item,n):
        result.add(''.join(thing))
    return result

if __name__ == '__main__':
    assert zbits(4, 3) == {'0100', '0001', '0010', '1000'}
    assert zbits(4, 1) == {'0111', '1011', '1101', '1110'}
    assert zbits(5, 4) == {'00001', '00100', '01000', '10000', '00010'}