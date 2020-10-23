import json
import random


def Encrypt(params: dict, plaintext_m: int) -> int:
    """
    Encrypt(pk,m)  for a plaintext bit m∈{0,1} sample a random subsetS⊆{1,τ} and a
    random integer r ← (−2^(2ρ),2^(2ρ)) and output c = (m+ 2r+ 2∑xi, i∈S) mod x0
    :param params: Dictionary of public paramters
    :param plaintext_m: plaintext m
    :return: ciphertext c
    """
    eta = int(params['SWHE']['Public Parameters']['eta'])  # bit length of secret key
    gammma = int(params['SWHE']['Public Parameters']['gamma']) # bit length of integers in public key
    rho = int(params['SWHE']['Public Parameters']['rho'])  # bit length of noise
    tau = int(params['SWHE']['Public Parameters']['tau']) # number of elements in public key
    public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]
    # Random subset S calculated from {1, τ}
    random_subset_S = [_ for _ in range(1, tau+1) if bool(round(random.random()))] # 0 to 10, 11 elements totally
    random_integer_r = random.randint(-(2**rho), (2**rho)) # random r←(−2^(2ρ),2^(2ρ))
    # c=(m+ 2r+ 2∑xi, i∈S ) mod x0
    ciphertext_c = plaintext_m + 2 * random_integer_r + 2 * sum(public_key[_] for _ in random_subset_S) % public_key[0]
    return ciphertext_c


def Decrypt(secret_key: int, ciphertext_c: int) -> int:
    """
    Dec(sk,c)  Calculate and output (c mod p)  mod 2
    :param secret_key: sk Secret key integer
    :param ciphertext_c: ciphertext c integer
    :return: plaintext_m integer
    """
    plaintext_m = (ciphertext_c % secret_key) % 2
    return plaintext_m


if __name__ == '__main__':
    with open('swhe-task1.json', "r") as file:
        params = json.load(file)
    vector = params['Plaintext Vector']
    secret_key = int(params['SWHE']['sk'])
    encrypted_vector = []
    decrypted_vector = []
    for i in vector:
        encrypted_vector.append(Encrypt(params, i))
    for i in encrypted_vector:
        decrypted_vector.append(Decrypt(secret_key, i))
    params['Encrypted Vector'] = [str(_) for _ in encrypted_vector]
    with open('swhe-task1_vector.json', "w") as file:
        json.dump(params, file)

        # print(encrypted_vector)
        # print(vector)
        # print(decrypted_vector)

