from multiprocessing import Pool
import hashlib
import bcrypt
import nltk
from nltk.corpus import words
import os
from collections import namedtuple
import threading
from concurrent.futures import ThreadPoolExecutor

#creates a Datatype called 'EntryFormat' s.t. 
# var = EntryFormat(...)
# var.User = ...
# var.Algorithm = ...
# and stuff can be accessed more easily
EntryFormat = namedtuple('User','Algorthim','Workfactor','SaltHash')

FILTERED_CORPUS = [word.lower() for word in words.words() if 6 <= len(word) <= 10]

# Download the necessary NLTK corpus (only once)
nltk.download('words')

def load_wordlist():
    print("placeholder")
    
def load_shadow_file(file_path) -> EntryFormat:
    entry: EntryFormat
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Shadow not found in ", file_path)
    with open(file_path, 'r') as f:
        # “User:$Algorithm$Workfactor$SaltHash”
        for lines in f: 
            parts = lines.strip().split('$')
            if(parts):
                entry = parts
    return entry 

def guess(word):
    #if     

    

def crack_password(entry: EntryFormat):
    # entry.User = <username>
    # entry.Algorthim = <algorthim>
    # entry.Workfactor = <workfactor>
    # entry.SaltHash = <salt + hash>
    NUM_THREADS = 10
    
    # datasets [10] = split the corpus into 10 pieces evenly
    # the ith thread spawned will process the ith dataset
    

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as master:
        # master.submit(<function name>, param1, param2,)

        #for word in FILTERED_CORPUS: 
            #master.map(guess, word, entry.SaltHash[22:])

        
        #results = master.map(guess, )

    print("placeholder")

def task_2_main():
    # Use os.path.join for cross-platform compatibility
    # shadow_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'shadow.txt')
    
    shadow_entries = load_shadow_file("shadow.txt")

    print("Starting password cracking...")

    with Pool() as pool:
        
        print(f"SHADOW ENTRIES ({type(shadow_entries)})): ", shadow_entries)
        #results = pool.map(crack_password, shadow_entries)

    # print("Password cracking completed. Results:")
    # for result in results:
    #     user, password, duration = result
    #     if password:
    #         print(f"Cracked password for {user}: {password} in {    duration:.2f} seconds")
    #     else:
    #         print(f"Failed to crack password for {user} in {duration:.2f} seconds.")
if __name__ == '__main__':
   task_2_main()