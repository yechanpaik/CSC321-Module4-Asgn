from multiprocessing import Pool
import hashlib
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
    """
    Minimal-change version that times the search for this entry,
    prints the elapsed time as soon as a password is found, and
    returns (username, found_password_or_None, elapsed_seconds).
    """
    NUM_THREADS = 10

    # split the corpus into NUM_THREADS chunks
    split_size = len(FILTERED_CORPUS) // NUM_THREADS
    data_splits = [FILTERED_CORPUS[i:i+split_size] for i in range(0, len(FILTERED_CORPUS), split_size)]

    username = entry.split(":")[0]

    t_start = time.perf_counter()

    found_password = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as master:
        futures = []
        for i in range(0, NUM_THREADS):
            futures.append(master.submit(guess, data_splits[i], entry, i))
            print(f"({username}) Thread {i} spawned.")

        # process results as they complete; stop when we find the first match
        for fut in concurrent.futures.as_completed(futures):
            try:
                res = fut.result()   # res is the string returned by guess()
            except Exception:
                res = None

            if res and res != "not found":
                found_password = res
                elapsed = time.perf_counter() - t_start
                print(f"[{username}] Password found: {found_password} (time: {elapsed:.2f} s)")
                # best-effort: cancel any futures that haven't started
                for f in futures:
                    if not f.done():
                        f.cancel()
                break

        # optional: allow running threads to exit; we don't block long here
        # collect remaining results to avoid dangling exceptions and to be tidy
        for f in futures:
            if not f.done():
                try:
                    f.result(timeout=0.1)
                except Exception:
                    pass

    # If nothing found, print elapsed and indicate not found
    if not found_password:
        elapsed = time.perf_counter() - t_start
        print(f"[{username}] Password not found (time: {elapsed:.2f} s)")

    return (username, found_password, elapsed)



def task_2_main():    
    shadow_entries = load_shadow_file("shadow.txt")

    print("Starting password cracking...")

    t0 = time.perf_counter()

    with Pool() as pool:
        
        print(f"SHADOW ENTRIES ({type(shadow_entries)})): ", shadow_entries)
        results = pool.map(crack_password, shadow_entries)
    
    t1 = time.perf_counter()

    total_elapsed = t1 - t0
    print(f"\nTotal time for cracking job: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)\n")

    # print("Password cracking completed. Results:")
    # for result in results:
    #     user, password, duration = result
    #     if password:
    #         print(f"Cracked password for {user}: {password} in {    duration:.2f} seconds")
    #     else:
    #         print(f"Failed to crack password for {user} in {duration:.2f} seconds.")

if __name__ == '__main__':
   task_2_main()
