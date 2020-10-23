import json
from somewhat_homomorphic_encryption import Encrypt, Decrypt

if __name__ == '__main__':
    with open('swhe-task2.json', "r") as file:
        params = json.load(file)
    ciphertext_vector = params['Ciphertext Collection']
    secret_key = int(params['SWHE']['sk'])
    decrypted_vector = []
    for i in ciphertext_vector:
        noise_bit_length = i["Noise Bitlength"]
        ciphertext = int(i["Ciphertext"])
        decrypted_vector.append(Decrypt(secret_key, ciphertext))

    print(decrypted_vector)

