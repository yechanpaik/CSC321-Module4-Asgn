import secrets
from Crypto.Cipher import AES
import hashlib
import random
from hashlib import sha256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def main():
    input1 = input("Enter input: ")
    print()
    print("Task 1 & 2")
    input1 = input1.encode()

    #bit flipping
    array = bytearray(input1)
    pos = random.randrange(len(input1)*8) #choose random position to bitflip
    byte_pos = pos//8
    bit_pos = pos%8
    array[byte_pos] ^= (1 << bit_pos)
    input1_bitflipped = bytes(array)


    input_hash = hashlib.sha256(input1).digest()
    print("Input hashed: " , input_hash)
    input_bitflipped_hash = hashlib.sha256(input1_bitflipped).digest()
    print("Input bitflipped hashed: " , input_bitflipped_hash)
    print('\n\n')

    input_hash_truncated = input_hash[:1]
    random_hash = input_bitflipped_hash[:1]

    i = 0
    while(input_hash_truncated != random_hash):
        random_hash = secrets.token_bytes(1) #random 1 byte string
        print("Attempt ", i , " unsuccessful")
        i += 1

    print("Attempt ", i, " successful\n")
    
    random_hash = random_hash.hex()
    print("Word is: ", random_hash)





if __name__ == "__main__": 
    main()