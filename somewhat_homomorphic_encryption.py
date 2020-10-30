import json
import random
from math import ceil, floor
from gmpy2 import f_div, mul, f_mod, c_mod, sub, t_mod, div, c_div, add


def keygen(eta: int, gamma: int, rho: int, tau: int) -> tuple:
    """
    Key generation function
    :return: secret key and public key list
    """
    p = 0
    while p % 2 == 0:
        p = random.randint(2 ** (eta - 1), (2 ** eta) - 1)
    q0 = random.randint(0, f_div(2 ** gamma, p))
    # q0 = random.randint(0, (2 ** gamma) / p - 1)
    x0 = p * q0
    pk = [0] * (tau + 1)
    pk[0] = int(x0)
    for i in range(1, tau):
        flag = 0
        while flag == 0:
            q = random.randint(0, f_div(2 ** gamma, p))
            r = random.randint(-(2 ** rho) + 1, (2 ** rho) - 1)
            pk[i] = int(p * q + r)
            if x0 > pk[i]:
                flag = 1
    return int(p), pk


def Encrypt(public_key: list, tau: int, rho: int, plaintext_m: int) -> int:
    """
    Encrypt(pk,m)  for a plaintext bit m∈{0,1} sample a random subsetS⊆{1,τ} and a
    random integer r ← (−2^(2ρ),2^(2ρ)) and output c = (m+ 2r+ 2∑xi, i∈S) mod x0
    :param public_key: given Public key
    :param rho: Rho parameter given for random variable r
    :param tau: Tau variable given for creating random Subset of zeros
    :param plaintext_m: plaintext m
    :return: ciphertext c
    """
    # Random subset S calculated from {1, τ}
    random_subset_S = [_ for _ in range(1, tau + 1) if bool(round(random.random()))]  # 0 to 10, 11 elements totally
    random_integer_r = random.randint(-(2 ** (2 * rho)) + 1, (2 ** (2 * rho)) - 1)  # random r←(−2^(2ρ),2^(2ρ))
    ciphertext_c = (plaintext_m + 2 * random_integer_r + 2 * sum(public_key[_] for _ in random_subset_S))  # % public_key[0]
    quotient = ciphertext_c / public_key[0]
    ciphertext_c = ciphertext_c - int(public_key[0] * quotient)
    return ciphertext_c


def Decrypt(secret_key: int, ciphertext_c: int) -> int:
    """
    Dec(sk,c)  Calculate and output (c mod p)  mod 2
    :param secret_key: sk Secret key integer
    :param ciphertext_c: ciphertext c integer
    :return: plaintext_m integer
    """
    # m = [c % 2 + ⌊c/p⌉] % 2
    quotient = ciphertext_c / secret_key
    if quotient - floor(quotient) < 0.5:
        quotient = floor(quotient)
    else:
        quotient = ceil(quotient)
    plaintext_m = (ciphertext_c % 2 + quotient % 2) % 2
    return plaintext_m


if __name__ == '__main__':
    with open('swhe-task1.json', "r") as file:
        params = json.load(file)

    vector = params['Plaintext Vector']
    secret_key = int(params['SWHE']['sk'])
    eta = int(params['SWHE']['Public Parameters']['eta'])  # bit length of secret key
    gamma = int(params['SWHE']['Public Parameters']['gamma']) # bit length of integers in public key
    rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    tau = int(params['SWHE']['Public Parameters']['tau'])  # number of elements in public key
    public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]

    encrypted_vector = []
    decrypted_vector = []
    for i in vector:
        encrypted_vector.append(Encrypt(public_key, tau, rho, i))
    for i in encrypted_vector:
        decrypted_vector.append(Decrypt(secret_key, i))

    params['Encrypted Vector'] = encrypted_vector
    with open('swhe-task1.json', "w") as file:
        json.dump(params, file)
    # print("Encrypted Vector: ", encrypted_vector)

    print("Encrypted Vector written to the JSON file.")
    print("Plaintext Vector:", vector)
    print("Decrypted Vector:", decrypted_vector)
