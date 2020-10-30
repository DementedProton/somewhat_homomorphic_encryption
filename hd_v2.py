import json
from somewhat_homomorphic_encryption import Decrypt, Encrypt, keygen
from math import log, ceil, floor
from itertools import combinations
from functools import reduce
from gmpy2 import mul, add, t_mod, f_mod, c_mod
import time


def hw_add(a, b, x0):
    ans = (a + b) % x0
    return ans


def hw_mul(a, b, x0):
    ans = (a * b) % x0
    return ans


def half_adder(a, b, x0):
    s = hw_add(a, b, x0)
    c = hw_mul(a, b, x0)
    return s, c


def full_adder(a, b, c_in, x0):
    s0 = hw_add(a, b, x0)
    s = hw_add(s0, c_in, x0)
    t1 = hw_mul(c_in, a, x0)
    t2 = hw_mul(c_in, b, x0)
    t3 = hw_mul(t1, b, x0)
    t4 = hw_mul(t2, a, x0)
    c_out = hw_mul(a, b, x0)
    c_out = hw_add(c_out, t1, x0)
    c_out = hw_add(c_out, t2, x0)
    c_out = hw_add(c_out, t3, x0)
    c_out = hw_add(c_out, t4, x0)
    return s, c_out


def calc_hamming_weight(hamming_distance: list, pk: list, tau: int, rho: int) -> list:
    x0 = pk[0]
    hamming_distance.reverse()
    s, c = half_adder(hamming_distance[0], hamming_distance[1], x0)
    hw = [s]
    index = 1
    while index < len(hamming_distance):
        temp = []
        temp.append(hamming_distance[index])
        for k in range(1, len(hw)):
            temp.append(Encrypt(pk, tau, rho, 0))
        if len(hw) > 1:
            s, c = half_adder(hw[0], temp[0], x0)
            res = [s]
            for j in range(1, len(hw)):
                s, c = full_adder(hw[j], temp[j], c, x0)
                res.append(s)
            res.append(c)
            hw = res
        index += 1
        print(len(hw))

        if len(hw) == 1:
            hw.append(c)
    hw.reverse()
    return hw


if __name__ == '__main__':
    with open('swhe-task3_v2.json', "r") as file:
        params = json.load(file)
    # with open('swhe-task1.json', "r") as file:
    #     params = json.load(file)
    eta = int(params['SWHE']['Public Parameters']['eta'])  # bit length of secret key
    gammma = int(params['SWHE']['Public Parameters']['gamma'])  # bit length of integers in public key
    rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    tau = int(params['SWHE']['Public Parameters']['tau'])  # number of elements in public key

    secret_key, public_key = keygen(eta, gammma, rho, tau)

    v1 = [1, 0, 1, 1, 0]
    v2 = [0, 1, 1, 0, 0]

    encrypted_v1 = []
    encrypted_v2 = []
    decrypted_v1 = []
    decrypted_v2 = []
    decrypted_hamming = []

    for i in v1:
        encrypted_v1.append(Encrypt(public_key, tau, rho, i))
    for j in v2:
        encrypted_v2.append(Encrypt(public_key, tau, rho, j))

    for i in encrypted_v1:
        decrypted_v1.append(Decrypt(secret_key, i))
    for j in encrypted_v2:
        decrypted_v2.append(Decrypt(secret_key, j))

    start_time = time.time()
    print("XORing 2 vectors...")
    hamming_distance = [0] * len(encrypted_v1)
    for i in range(len(hamming_distance)):
        hamming_distance[i] = int(t_mod(add(encrypted_v1[i], encrypted_v2[i]), public_key[0]))

    print("Done... Calculting the hamming weight of the result...")
    for i in hamming_distance:
        decrypted_hamming.append(Decrypt(secret_key, i))

    hamming_weight = calc_hamming_weight(hamming_distance, public_key, tau, rho)
    decrypted_vector = []
    for k in hamming_weight:
        decrypted_vector.append(Decrypt(secret_key, k))
    print(decrypted_v1)
    print(decrypted_v2)
    print(decrypted_hamming)
    print(decrypted_vector)
    end_time = time.time()
    print("Time taken: ", end_time - start_time)



    # ACTUAL THING STARTS HERE....
    # start_time = time.time()
    # with open('swhe-task3_v2.json', "r") as file:
    #     params = json.load(file)
    # v1 = params['Ciphertext Collection']['Encrypted V1']
    # v2 = params['Ciphertext Collection']['Encrypted V2']
    # public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]
    # rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    # tau = int(params['SWHE']['Public Parameters']['tau'])  # number of elements in public key
    # print("XORing 2 vectors...")
    # # print(public_key.index(max(public_key)))
    # hamming_distance = list(map(lambda x, y: (int(x) + int(y)) % public_key[0], v1, v2))
    # print("Done... Calculting the hamming weight of the result...")
    # hamming_weight = calc_hamming_weight(hamming_distance, public_key, tau, rho)
    # print(time.time() - start_time)

