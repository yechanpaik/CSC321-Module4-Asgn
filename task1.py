import secrets
#from Crypto.Cipher import AES
import hashlib
import random
import time
import matplotlib.pyplot as plt

def findCollision(size):
    #approach 1 to finding collisions 
    seen = {}
    count = 0
    
    while True:
        random_bytes = secrets.token_bytes(9)
        random_bytes = hashlib.sha256(random_bytes).digest()
        random_bytes = int.from_bytes(random_bytes, 'big') >> (256 - size)
        count += 1
        if random_bytes in seen:
            # return (seen[random_bytes], random_bytes)
            return count  
        seen[random_bytes] = random_bytes

def main():
    # a
    input1 = input("Enter input: ")
    print()
    print("Task 1 & 2")
    input1 = input1.encode()

    #bit flipping //b
    for i in range(0, 4):
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

    bit_sizes = []
    times = []
    counts = []
    
    for bit_size in range(8, 52, 2):
        start = time.time()
        count = findCollision(bit_size)  
        end = time.time()
        final_time = end - start
        print("Bit Size: " , bit_size, " Time took: " , final_time, " Tries: " , count)
        bit_sizes.append(bit_size)
        counts.append(count)
        times.append(final_time)
        
    #Graph 1 bit_size x final_time??
    fig1, ax1 = plt.subplots()
    ax1.plot(bit_sizes, times)
    ax1.set_xlabel("Digest Size")
    ax1.set_ylabel("Collision Time")
    
    # Graph 2: bit_size vs count
    fig2, ax2 = plt.subplots()
    ax2.plot(bit_sizes, counts)
    ax2.set_xlabel("Digest Size")
    ax2.set_ylabel("Number of Inputs")
    
    plt.show()
    

if __name__ == "__main__": 
    main()