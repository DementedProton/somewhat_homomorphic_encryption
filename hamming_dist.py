import json
from somewhat_homomorphic_encryption import Decrypt, Encrypt
from math import log, ceil
from itertools import combinations
from functools import reduce
import time


def calc_hamming_weight(hamming_distance: list, x0: int) -> list:
    hw_size = ceil(log(len(hamming_distance)+1,2))
    hw = [None] * hw_size
    for i in range(0, hw_size):
        print("Calculating bit %d of hamming weight" % i)
        xor_operations = []
        no_of_combination_bits = 2 ** i
        c_add = 0
        c_mult = 1
        and_operations = [list(map(int, comb)) for comb in combinations(hamming_distance, no_of_combination_bits)]
        if (len(and_operations)) > 100:
            print("Hold on... a lot of combinations here, better get some coffee...")
        # for j in and_operations:
        #     if no_of_combination_bits > 1:
        #         xor_operations.append(reduce(lambda x, y: x * y % x0, j))
        #     else:
        #         xor_operations.append(j[0])
        # # for k in and_combinations:
        # hw[hw_size - 1 - i] = reduce(lambda x,y : x+y % x0, xor_operations)
        for j in and_operations:
            for k in j:
                c_mult = c_mult * k
                c_mult = c_mult % x0
            xor_operations.append(c_mult)
        for m in xor_operations:
            c_add = c_add + m
            c_add = c_add % x0
        hw[hw_size - 1 - i] = c_add


    return hw


if __name__ == '__main__':
    with open('swhe-task3_v2.json', "r") as file:
        params = json.load(file)
    v1 = params['Ciphertext Collection']['Encrypted V1']
    v2 = params['Ciphertext Collection']['Encrypted V2']
    public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]
    start_time = time.time()
    print("XORing 2 vectors...")
    hamming_distance = list(map(lambda x, y: (int(x) + int(y)) % public_key[0], v1, v2))
    print("Done... Calculting the hamming weight of the result...")
    hamming_weight = calc_hamming_weight(hamming_distance, public_key[0])
    end_time = time.time()
    print("Time taken: ", end_time - start_time)
    # print(params['Ciphertext Collection'])
