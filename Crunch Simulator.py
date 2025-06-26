
import itertools
import os
import gzip
import bz2
import lzma
import shutil

def print_banner():
    WHITE = '\033[97m'
    GREEN = "\033[92m"
    simon=(GREEN + r"""
   MADE WITH..._____  _____ __  __  ____  _   _ 
              / ____| _   _|  \/  |/ __ \| \ | |
              | (___   | | | \  / | |  | |  \| |
               \___ \  | | | |\/| | |  | | . ` |
               ____) |_| |_| |  | | |__| | |\  |
              |_____/|_____|_|  |_|\____/|_| \_|""")

    print(simon)

print_banner()
def validate_pattern(pattern, charset_lower, charset_upper, charset_numbers, charset_symbols):
    """Validate the pattern and assign character sets to each position"""
    charsets = {
        '@': charset_lower,
        ',': charset_upper,
        '%': charset_numbers,
        '^': charset_symbols
    }
    result = []
    for char in pattern:
        if char in charsets and charsets[char]:
            result.append(charsets[char])
        else:
            result.append([char])
    return result

def apply_duplicate_limit(word, limit_lower, limit_upper, limit_numbers, limit_symbols, pattern):
    """Apply duplicate character limit (-d)"""
    charsets = {
        '@': charset_lower,
        ',': charset_upper,
        '%': charset_numbers,
        '^': charset_symbols
    }
    limits = {'@': limit_lower, ',': limit_upper, '%': limit_numbers, '^': limit_symbols}
    for char_type, limit in limits.items():
        if limit > 0:
            count = 1
            for i in range(1, len(word)):
                if pattern[i] == char_type and pattern[i-1] == char_type and word[i] == word[i-1]:
                    count += 1
                    if count > limit:
                        return False
                else:
                    count = 1
    return True

def convert_size_to_bytes(size_str):
    """Convert file size to bytes"""
    size_str = size_str.lower()
    units = {'kb': 1000, 'mb': 1000**2, 'gb': 1000**3, 'kib': 1024, 'mib': 1024**2, 'gib': 1024**3}
    for unit in units:
        if size_str.endswith(unit):
            return int(float(size_str[:-len(unit)]) * units[unit])
    return int(size_str)

def generate_permutations(words):
    """Generate all permutations of specific words (-p)"""
    return [''.join(perm) for perm in itertools.permutations(words)]

print("*** Crunch Simulator ***")
use_permutation = input("Do you want to generate permutations of specific words (-p)? (yes/no): ").lower() == "yes"

words = []
if use_permutation:
    words = input("Enter words (separated by spaces, e.g., dog cat bird): ").split()
    words = generate_permutations(words)
else:
    min_len = int(input("Enter minimum word length: "))
    max_len = int(input("Enter maximum word length: "))
    charset_lower = input("Enter lowercase charset (e.g., abc, empty for default): ") or "abcdefghijklmnopqrstuvwxyz"
    charset_upper = input("Enter uppercase charset (e.g., ABC, empty for default or +): ") or "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    charset_numbers = input("Enter numbers charset (e.g., 123, empty for default): ") or "0123456789"
    charset_symbols = input("Enter symbols charset (e.g., !@#, empty for default): ") or "!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?/ "
    
    use_pattern = input("Do you want to specify a pattern (-t)? (yes/no): ").lower() == "yes"
    pattern = input("Enter pattern (e.g., @@%% for two lowercase + two numbers, empty for none): ") if use_pattern else ""
    
    use_limit = input("Do you want to apply duplicate limits (-d)? (yes/no): ").lower() == "yes"
    limit_lower = limit_upper = limit_numbers = limit_symbols = 0
    if use_limit:
        limit_lower = int(input("Max consecutive lowercase characters (0 for no limit): "))
        limit_upper = int(input("Max consecutive uppercase characters (0 for no limit): "))
        limit_numbers = int(input("Max consecutive numbers (0 for no limit): "))
        limit_symbols = int(input("Max consecutive symbols (0 for no limit): "))
    
    use_start = input("Do you want to start from a specific word (-s)? (yes/no): ").lower() == "yes"
    start_word = input("Enter start word (e.g., aaaa): ") if use_start else ""
    use_end = input("Do you want to stop at a specific word (-e)? (yes/no): ").lower() == "yes"
    end_word = input("Enter end word (e.g., zzzz): ") if use_end else ""

save_to_file = input("Do you want to save output to a file (-o)? (yes/no): ").lower() == "yes"
output_file = input("Enter output file name (e.g., wordlist.txt, empty to print): ") if save_to_file else ""
use_split = input("Do you want to split output files (-b)? (yes/no): ").lower() == "yes" if save_to_file else False
split_size = input("Enter file size (e.g., 10mb or 20kib): ") if use_split else ""
use_compress = input("Do you want to compress output (-z)? (yes/no): ").lower() == "yes" if save_to_file else False
compress_type = input("Enter compression type (gzip, bzip2, lzma): ").lower() if use_compress else ""

if not use_permutation:
    charsets = {
        '@': charset_lower,
        ',': charset_upper,
        '%': charset_numbers,
        '^': charset_symbols
    }
    for length in range(min_len, max_len + 1):
        if use_pattern and len(pattern) != length:
            print(f"Error: Pattern length ({len(pattern)}) must match word length ({length})!")
            continue
        if use_pattern:
            charset_per_position = validate_pattern(pattern, charset_lower, charset_upper, charset_numbers, charset_symbols)
            if not charset_per_position:
                continue
            combinations = itertools.product(*charset_per_position)
        else:
            all_chars = charset_lower + charset_upper + charset_numbers + charset_symbols
            combinations = itertools.product(all_chars, repeat=length)
        
        start_found = not use_start
        for combo in combinations:
            word = ''.join(combo)
            if use_start and not start_found:
                if word == start_word:
                    start_found = True
                continue
            if use_limit and use_pattern:
                if not apply_duplicate_limit(word, limit_lower, limit_upper, limit_numbers, limit_symbols, pattern):
                    continue
            words.append(word)
            if use_end and word == end_word:
                break

if save_to_file:
    if use_split:
        split_bytes = convert_size_to_bytes(split_size)
        current_file = 1
        current_size = 0
        file_words = []
        file_start = words[0] if words else ""
        
        for word in words:
            word_size = len(word.encode('utf-8')) + 1 
            if current_size + word_size > split_bytes and file_words:
                file_name = f"{file_start}-{file_words[-1]}.txt"
                with open(file_name, 'w', encoding='utf-8') as f:
                    for w in file_words:
                        f.write(w + '\n')
                if use_compress:
                    if compress_type == "gzip":
                        with open(file_name, 'rb') as f_in:
                            with gzip.open(file_name + '.gz', 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(file_name)
                    elif compress_type == "bzip2":
                        with open(file_name, 'rb') as f_in:
                            with bz2.BZ2File(file_name + '.bz2', 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(file_name)
                    elif compress_type == "lzma":
                        with open(file_name, 'rb') as f_in:
                            with lzma.open(file_name + '.xz', 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(file_name)
                file_words = []
                current_size = 0
                file_start = word
            file_words.append(word)
            current_size += word_size
        
        if file_words:
            file_name = f"{file_start}-{file_words[-1]}.txt"
            with open(file_name, 'w', encoding='utf-8') as f:
                for w in file_words:
                    f.write(w + '\n')
            if use_compress:
                if compress_type == "gzip":
                    with open(file_name, 'rb') as f_in:
                        with gzip.open(file_name + '.gz', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(file_name)
                elif compress_type == "bzip2":
                    with open(file_name, 'rb') as f_in:
                        with bz2.BZ2File(file_name + '.bz2', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(file_name)
                elif compress_type == "lzma":
                    with open(file_name, 'rb') as f_in:
                        with lzma.open(file_name + '.xz', 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(file_name)
        print(f"Words saved to split files. Total words: {len(words)}")
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')
        if use_compress:
            if compress_type == "gzip":
                with open(output_file, 'rb') as f_in:
                    with gzip.open(output_file + '.gz', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(output_file)
            elif compress_type == "bzip2":
                with open(output_file, 'rb') as f_in:
                    with bz2.BZ2File(output_file + '.bz2', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(output_file)
            elif compress_type == "lzma":
                with open(output_file, 'rb') as f_in:
                    with lzma.open(output_file + '.xz', 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(output_file)
        print(f"Words saved to {output_file}. Total words: {len(words)}")
else:
    print("Generated words:")
    for word in words[:100]:
        print(word)
    if len(words) > 100:
        print("... (only first 100 words displayed)")
    print(f"Total words: {len(words)}")
