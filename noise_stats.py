import json
from somewhat_homomorphic_encryption import Decrypt
import pdb


# xor - addition mod 2 - here
#and - mulitplication
#
#
if __name__ == '__main__':
    with open('swhe-task2.json', "r") as file:
        params = json.load(file)
    ciphertext_vector = params['Ciphertext Collection']
    secret_key = int(params['SWHE']['sk'])
    decrypted_vector = {}
    public_key = [int(_) for _ in params['SWHE']['Public Parameters']['pk']]
    x0 = public_key[0]
    for i in ciphertext_vector:
        noise_bit_length = i["Noise Bitlength"]
        ciphertext = int(i["Ciphertext"])
        c_add = 0
        c_mult = 1
        n_addition = 0  # count smallest n for which addition/multiplication followed by decryption fails
        n_multiplication = 0
        decrypted_vector[noise_bit_length] = []
        while True:
            c_add = c_add + ciphertext
            # find c_add mod x0
            # quotient = c_add / x0
            # c_add = c_add - int(quotient * x0)
            c_add = c_add % x0
            if Decrypt(secret_key, c_add) == 0:
                n_addition += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'xor': n_addition})
                break
        while True:
            c_mult = c_mult * ciphertext
            # find c_mult mod x0
            # quotient = c_mult / x0
            # c_mult = c_mult - int(quotient * x0)
            c_mult = c_mult % x0
            if Decrypt(secret_key, c_mult) == 0:
                n_multiplication += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'and': n_multiplication})
                break
        print(decrypted_vector)
    with open('noise_stats_op.json', "w") as ofile:
        json.dump(decrypted_vector, ofile )

