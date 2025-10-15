from multiprocessing import Pool
import bcrypt
import nltk
from nltk.corpus import words
import os
from collections import namedtuple
import threading
import concurrent.futures
import time

# run the following in terminal once
# python -c "import nltk; nltk.download('words')"

FILTERED_CORPUS = [word.lower() for word in words.words() if 6 <= len(word) <= 10]

def load_shadow_file(file_path) -> list[str]:
    entry = []
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Shadow not found in ", file_path)
    with open(file_path, 'r') as f:
        # “User:$Algorithm$Workfactor$SaltHash”
        for lines in f: 
            entry.append(lines.strip())    
    return entry 

def notify():
    while True:
        time.sleep(60 )
        print(".", end="", flush=True)
    

def guess(data_split, entry, split_num):
    # entry = b"$2b$10$L.z8uq99JkFAvX/Q1jGRI.TzrHIIxWMoRi/VzO1sj/UvVFPgW8dW."
    # word = "secretword"

    entry = entry.split(":")
    username = entry[0]
    entry = entry[1]
    entry = entry.encode("utf-8")

    notifier_thread = threading.Thread(target=notify, daemon=True)
    notifier_thread.start()

    print(f"Entry: {username} | {entry} | Split#{split_num}")
    
    for word in data_split:
        if bcrypt.checkpw(word.encode("utf-8"), entry):
            print(f"match found: {username} {word}")
            return word
    
    print("not found")
    return ("not found")

    
def crack_password(entry):
    
    NUM_THREADS = 10
    
    # data_splits[10] = split the corpus into 10 pieces evenly
    # the ith thread spawned will process the ith data_split
    split_size = len(FILTERED_CORPUS) // NUM_THREADS
    data_splits = [FILTERED_CORPUS[i:i+split_size] for i in range(0, len(FILTERED_CORPUS), split_size)]
    
    username = entry.split(":")[0]
        
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as master:
        threads = []
        for i in range(0, NUM_THREADS):
            # results[i] = master.map(guess, data_splits[i], entry.Workfactor, entry.SaltHash)
            threads.append(master.submit(guess, data_splits[i], entry, i))
            print(f"({username}) Thread {i} spawned.")
        
        # if match_found_flag.wait(): #if all complete with 'fucked':
        #     #doesnt handle case where threads complete and not found
        #     for thread in threads:
        #         thread.join()
        #         results.append(thread.result)
        
        # for thread in concurrent.futures.as_completed(threads):
        #     results.append(thread.result())
            
        # print(f"Results ({username}): ", results)
                
        #results: a list of results such that the ith index is the ith users's password


def task_2_main():    
    shadow_entries = load_shadow_file("shadow(sean2).txt")

    print("Starting password cracking...")

    with Pool() as pool:
        
        print(f"SHADOW ENTRIES ({type(shadow_entries)})): ", shadow_entries)
        results = pool.map(crack_password, shadow_entries)

    # print("Password cracking completed. Results:")
    # for result in results:
    #     user, password, duration = result
    #     if password:
    #         print(f"Cracked password for {user}: {password} in {    duration:.2f} seconds")
    #     else:
    #         print(f"Failed to crack password for {user} in {duration:.2f} seconds.")

if __name__ == '__main__':
   task_2_main()