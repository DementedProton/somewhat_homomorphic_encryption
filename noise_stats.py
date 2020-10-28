import json
from somewhat_homomorphic_encryption import Encrypt, Decrypt



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
        n_addition =0 # count smallest n for which addition/multiplication followed by decryption fails
        n_multiplication = 0 #
        decrypted_vector[noise_bit_length] = []
        while True:
            ciphertext = ciphertext + ciphertext
            if Decrypt(secret_key, ciphertext) == 0:
                n_addition += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'xor': n_addition})
                print(decrypted_vector)
                break
        ciphertext = int(i["Ciphertext"])
        while True:
            ciphertext = ciphertext * ciphertext
            if Decrypt(secret_key, ciphertext) == 0:
                n_multiplication += 1
                continue
            else:
                decrypted_vector[noise_bit_length].append({'and': n_multiplication})
                print(decrypted_vector)
                break

    print(decrypted_vector)

