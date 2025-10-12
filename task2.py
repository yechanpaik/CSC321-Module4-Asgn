import argparse
import bcrypt
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Event, Manager
from typing import List, Tuple

def load_shadow_file(path: str) -> List[Tuple[str, str]]:
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            user, full_hash = line.split(':', 1)
            entries.append((user.strip(), full_hash.strip()))
    return entries

def build_wordlist_nltk(min_len=6, max_len=10) -> List[str]:
    import nltk
    from nltk.corpus import words
    raw = words.words()
    wl = set()
    for w in raw:
        if w.isalpha():
            wl_w = w.lower()
            if min_len <= len(wl_w) <= max_len:
                wl.add(wl_w)
    return sorted(wl)

def load_wordlist_file(path: str, min_len=6, max_len=10) -> List[str]:
    wl = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            w = line.strip()
            if not w: 
                continue
            if w.isalpha():
                w_low = w.lower()
                if min_len <= len(w_low) <= max_len:
                    wl.append(w_low)
    return sorted(set(wl))

def chunkify(lst: List[str], chunk_size: int) -> List[List[str]]:
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def worker_check_chunk(args):
    chunk, full_hash, stop_event = args
    attempts = 0
    full_hash_b = full_hash.encode('utf-8')
    for w in chunk:
        if stop_event.is_set():
            return (None, attempts)
        attempts += 1
        if bcrypt.checkpw(w.encode('utf-8'), full_hash_b):
            stop_event.set()
            return (w, attempts)
    return (None, attempts)

def crack_user_parallel(full_hash: str, wordlist: List[str], workers: int, chunk_size: int = 1000):
    chunks = chunkify(wordlist, chunk_size)
    manager = Manager()
    stop_event = manager.Event() 

    attempts_total = 0
    found_password = None

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as exe:
        args_iter = ((chunks[i], full_hash, stop_event) for i in range(len(chunks)))
        futures = [exe.submit(worker_check_chunk, args) for args in args_iter]

        for fut in as_completed(futures):
            try:
                pw, attempts = fut.result()
            except Exception as e:
                pw, attempts = (None, 0)
            attempts_total += attempts
            if pw:
                found_password = pw
    elapsed = time.perf_counter() - start
    return found_password, attempts_total, elapsed

def main():
    parser = argparse.ArgumentParser(description="Parallel bcrypt cracker using nltk wordlist (6-10 letters).")
    parser.add_argument('shadow_file', help='Path to shadow file (User:$2b$.. per line)')
    parser.add_argument('--workers', '-w', type=int, default=(os.cpu_count() or 4), help='Number of worker processes (default = CPU cores)')
    parser.add_argument('--wordlist', '-l', type=str, default=None, help='Optional path to a custom wordlist (one word per line)')
    parser.add_argument('--chunk', '-c', type=int, default=200, help='Chunk size (words per task). Smaller => earlier stopping, more overhead. Default 200.')
    args = parser.parse_args()

    if not os.path.exists(args.shadow_file):
        print("Shadow file not found:", args.shadow_file)
        return

    entries = load_shadow_file(args.shadow_file)
    if not entries:
        print("No valid entries in shadow file.")
        return

    if args.wordlist:
        print("Loading wordlist from file:", args.wordlist)
        wordlist = load_wordlist_file(args.wordlist)
    else:
        print("Loading wordlist from nltk corpus (words). Make sure you've downloaded it.")
        wordlist = build_wordlist_nltk()

    print(f"Candidate list size (6-10 letters): {len(wordlist)}")
    print(f"Using {args.workers} worker processes, chunk size {args.chunk}.\n")

    results = []
    for username, full_hash in entries:
        print(f"Cracking user: {username}  (hash prefix: {full_hash[:29]}... )")
        pw, attempts, elapsed = crack_user_parallel(full_hash, wordlist, args.workers, chunk_size=args.chunk)
        if pw:
            print(f"  -> Found password: {pw}")
        else:
            print("  -> Password not found in candidate list")
        print(f"     Attempts: {attempts}, Time: {elapsed:.2f} s\n")
        results.append((username, pw, attempts, elapsed))

    with open('crack_results.txt', 'w', encoding='utf-8') as out:
        out.write("username\tpassword\tattempts\ttime_s\n")
        for u, p, a, t in results:
            out.write(f"{u}\t{p}\t{a}\t{t:.2f}\n")
    print("Done. Results written to crack_results.txt")

if __name__ == '__main__':
    main()

