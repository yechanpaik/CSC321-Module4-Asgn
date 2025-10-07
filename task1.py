from Crypto.Cipher import AES
import hashlib
import random
from hashlib import sha256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def main():
    input1 = input("Enter input: ")
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



if __name__ == "__main__": 
    main()