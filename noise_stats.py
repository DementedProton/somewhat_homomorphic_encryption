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
    for i in ciphertext_vector:
        noise_bit_length = i["Noise Bitlength"]
        ciphertext = int(i["Ciphertext"])
        c_add = 0
        c_mult = 1
        n_addition =0 # count smallest n for which addition/multiplication followed by decryption fails
        n_multiplication = 0 #
        decrypted_vector[noise_bit_length] = []
        while True:
            c_add = c_add + ciphertext
            if Decrypt(secret_key, ciphertext) == 0:
                n_addition += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'xor': n_addition})
                break
        while True:
            c_mult = c_mult * ciphertext
            if Decrypt(secret_key, ciphertext) == 0:
                n_multiplication += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'and': n_multiplication})
                break
        print(decrypted_vector)
    with open('noise_stats_op.json', "r") as ofile:
        json.dump(decrypted_vector, ofile )

