import json
from somewhat_homomorphic_encryption import Decrypt, Encrypt, keygen
from math import log, ceil, floor
from itertools import combinations
from functools import reduce
from gmpy2 import mul, add, t_mod, f_mod, c_mod
import time


def hw_add(a, b, x0):
    """
    Adding 2 ciphertexts a and b and then performing modulo reduction with x0
    :param a: c1
    :param b: c2
    :param x0: public key x0
    :return: (a + b) mod x0
    """
    ans = (a + b) % x0
    return ans


def hw_mul(a, b, x0):
    """
    Multiplying 2 ciphertexts a and b and then performing modulo reduction with x0
    :param a: c1
    :param b: c2
    :param x0: public key x0
    :return: (a * b) mod x0
    """
    ans = (a * b) % x0
    return ans


def calc_hamming_weight(hamming_distance: list, x0: int) -> list:
    """
    Calculate the hamming weight of the given vector
    :param hamming_distance: hamming distance vector, v whose hamming weight needs to be computed
    :param x0: public key
    :return: Hamming Weight vector (binary encoded form of hamming distance)
    """
    hw_size = int(ceil(log(len(hamming_distance) + 1, 2)))
    hw = [None] * hw_size
    for i in range(0, hw_size):
        print("Calculating bit %d of hamming weight" % i)
        xor_operations = []
        no_of_combination_bits = 2 ** i
        # calculating all the 2^i combinations
        and_operations = [list(comb) for comb in combinations(hamming_distance, no_of_combination_bits)]
        if (len(and_operations)) > 100:
            print("Hold on... a lot of combinations here, better get some coffee...")
        for j in and_operations:
            if no_of_combination_bits > 1:
                xor_operations.append(reduce(lambda x, y: hw_mul(x, y, x0), j))
            else:
                xor_operations.append(j[0])
        hw[hw_size - 1 - i] = reduce(lambda x, y: hw_add(x, y, x0), xor_operations)
    return hw


if __name__ == '__main__':
    # ACTUAL THING STARTS HERE....
    start_time = time.time()
    with open('swhe-task3_v2.json', "r") as file:
        params = json.load(file)

    v1 = params['Ciphertext Collection']['Encrypted V1']
    v2 = params['Ciphertext Collection']['Encrypted V2']

    public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]
    rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    tau = int(params['SWHE']['Public Parameters']['tau'])  # number of elements in public key

    print("XORing 2 vectors...")
    hamming_distance = list(map(lambda x, y: (int(x) + int(y)) % public_key[0], v1, v2))

    print("Done... Calculting the hamming weight of the result...")
    hamming_weight = calc_hamming_weight(hamming_distance, public_key[0])

    params['Encrypted Hamming Distance'] = hamming_weight
    # print(time.time() - start_time)
    with open('swhe-task3_v2.json', "w") as file:
        json.dump(params, file)


    # DEBUGGING...
    # with open('swhe-task3_v2.json', "r") as file:
    #     params = json.load(file)
    # # with open('swhe-task1.json', "r") as file:
    # #     params = json.load(file)
    # eta = int(params['SWHE']['Public Parameters']['eta'])  # bit length of secret key
    # gammma = int(params['SWHE']['Public Parameters']['gamma'])  # bit length of integers in public key
    # rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    # tau = int(params['SWHE']['Public Parameters']['tau'])  # number of elements in public key
    #
    # secret_key, public_key = keygen(eta, gammma, rho, tau)
    #
    # v1 = [1, 0, 1, 1, 0]
    # v2 = [0, 1, 1, 0, 0]
    #
    # encrypted_v1 = []
    # encrypted_v2 = []
    # decrypted_v1 = []
    # decrypted_v2 = []
    # decrypted_hamming = []
    #
    # for i in v1:
    #     encrypted_v1.append(Encrypt(public_key, tau, rho, i))
    # for j in v2:
    #     encrypted_v2.append(Encrypt(public_key, tau, rho, j))
    #
    # for i in encrypted_v1:
    #     decrypted_v1.append(Decrypt(secret_key, i))
    # for j in encrypted_v2:
    #     decrypted_v2.append(Decrypt(secret_key, j))
    #
    #
    # start_time = time.time()
    # print("XORing 2 vectors...")
    # hamming_distance = [0] * len(encrypted_v1)
    # for i in range(len(hamming_distance)):
    #     hamming_distance[i] = int(t_mod(add(encrypted_v1[i], encrypted_v2[i]), public_key[0]))
    #
    # print("Done... Calculating the hamming weight of the result...")
    # for i in hamming_distance:
    #     decrypted_hamming.append(Decrypt(secret_key, i))
    #
    # hamming_weight = calc_hamming_weight(hamming_distance, public_key[0])
    # decrypted_vector = []
    # for k in hamming_weight:
    #     decrypted_vector.append(Decrypt(secret_key, k))
    # print(decrypted_v1)
    # print(decrypted_v2)
    # print(decrypted_hamming)
    # print(decrypted_vector)
    # end_time = time.time()
    # print("Time taken: ", end_time - start_time)



