import secrets
from Crypto.Cipher import AES
import hashlib
import random
import time

def findCollision(size): 
    #i = 0
    #random_hash = secrets.randbits(size)
    #while(target != random_hash):
        #random_hash = secrets.randbits(size) #random [size] bits 
        #print("Attempt ", i , " unsuccessful")
        #i += 1
    
    #print("Attempt ", i, " successful\n")
    #random_hash = hex(random_hash)
    #return(random_hash)

    seen = {}
    while True:
        random_bytes = secrets.token_bytes(9)
        random_bytes = hashlib.sha256(random_bytes).digest()
        random_bytes = int.from_bytes(random_bytes, 'big') >> (256 - size)
        if random_bytes in seen:
            return (seen[random_bytes], random_bytes)  
        seen[random_bytes] = random_bytes


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


    for bits in range(8, 52, 2):
        start = time.time()
        findCollision(bits)  
        end = time.time()
        final_time = end - start
        print("Bit Size: " , bits, " Time took: " , final_time)




if __name__ == "__main__": 
    main()