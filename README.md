# Crunch Simulator

A Python script that simulates the functionality of the `crunch` wordlist generator tool, allowing users to create custom wordlists based on specified character sets, patterns, and constraints. This script is ideal for generating wordlists for password cracking, penetration testing, or other applications requiring custom string combinations.

## Features
- **Custom Word Lengths**: Specify minimum and maximum word lengths (`min-len`, `max-len`).
- **Character Sets**: Define custom sets for lowercase, uppercase, numbers, and symbols.
- **Patterns**: Use patterns like `-t @@%%` to control word structure (e.g., two lowercase letters + two numbers).
- **Duplicate Limits**: Restrict consecutive character repetitions with `-d` (e.g., `-d 2@` to limit lowercase letters).
- **Word Permutations**: Generate permutations of specific words with `-p` (e.g., `dog cat bird`).
- **Start/End Words**: Start generation from a specific word (`-s`) and stop at another (`-e`).
- **Output Options**: Save output to a file (`-o`), split files by size (`-b`), and compress files (`-z` with gzip, bzip2, or lzma).
- **Interactive Interface**: Prompts guide users through all configuration options.

## Requirements
- **Python 3.x** (tested with Python 3.8+)
- Standard Python libraries: `itertools`, `os`, `gzip`, `bz2`, `lzma`, `shutil`
- No external dependencies required for core functionality

## Installation
1. **Download the Script**:
   - Save `crunch_simulator.py` to your local machine.
2. **Ensure Python is Installed**:
   - Verify Python 3.x is installed by running:
     ```bash
     python3 --version
     ```
   - If not installed, download it from [python.org](https://www.python.org/downloads/).
3. **Run the Script**:
   - Navigate to the script's directory and execute:
     ```bash
     python3 crunch_simulator.py
     ```

## Usage
Run the script and follow the interactive prompts to configure your wordlist generation. The script supports most `crunch` options, including:

### Key Options
- **Permutations (`-p`)**: Generate all permutations of specific words (e.g., `dog cat bird` → `dogcatbird`, `catdogbird`, etc.).
- **Word Length**: Set minimum and maximum lengths for generated words.
- **Character Sets**: Define custom sets for lowercase (`@`), uppercase (`,`), numbers (`%`), and symbols (`^`).
- **Pattern (`-t`)**: Specify a pattern to control word structure (e.g., `@@%%` for two lowercase + two numbers).
- **Duplicate Limit (`-d`)**: Limit consecutive characters (e.g., `-d 2@` prevents `aaa`).
- **Start/End (`-s`, `-e`)**: Start from a specific word and stop at another.
- **Output File (`-o`)**: Save output to a file.
- **File Splitting (`-b`)**: Split output into files of specified size (e.g., `10mb`).
- **Compression (`-z`)**: Compress output files using `gzip`, `bzip2`, or `lzma`.

### Example Runs

#### Example 1: Basic Wordlist
Generate words of length 2 to 3 using characters `ab`:
```bash
$ python3 crunch_simulator.py
*** Crunch Simulator ***
Do you want to generate permutations of specific words (-p)? (yes/no): no
Enter minimum word length: 2
Enter maximum word length: 3
Enter lowercase charset (e.g., abc, empty for default): ab
Enter uppercase charset (e.g., ABC, empty for default or +): 
Enter numbers charset (e.g., 123, empty for default): 
Enter symbols charset (e.g., !@#, empty for default): 
Do you want to specify a pattern (-t)? (yes/no): no
Do you want to apply duplicate limits (-d)? (yes/no): no
Do you want to start from a specific word (-s)? (yes/no): no
Do you want to stop at a specific word (-e)? (yes/no): no
Do you want to save output to a file (-o)? (yes/no): yes
Enter output file name (e.g., wordlist.txt, empty to print): output.txt
Do you want to split output files (-b)? (yes/no): no
Do you want to compress output (-z)? (yes/no): no
Words saved to output.txt. Total words: 6
```
**Output in `output.txt`**:
```
aa
ab
ba
bb
aaa
aab
aba
abb
baa
bab
bba
bbb
```

#### Example 2: Pattern-Based Wordlist
Simulate `crunch 4 4 ab12 -t @@%%`:
```bash
$ python3 crunch_simulator.py
*** Crunch Simulator ***
Do you want to generate permutations of specific words (-p)? (yes/no): no
Enter minimum word length: 4
Enter maximum word length: 4
Enter lowercase charset (e.g., abc, empty for default): ab
Enter uppercase charset (e.g., ABC, empty for default or +): 
Enter numbers charset (e.g., 123, empty for default): 12
Enter symbols charset (e.g., !@#, empty for default): 
Do you want to specify a pattern (-t)? (yes/no): yes
Enter pattern (e.g., @@%% for two lowercase + two numbers, empty for none): @@%%
Do you want to apply duplicate limits (-d)? (yes/no): no
Do you want to start from a specific word (-s)? (yes/no): no
Do you want to stop at a specific word (-e)? (yes/no): no
Do you want to save output to a file (-o)? (yes/no): no
Generated words:
aa11
aa12
aa21
aa22
ab11
ab12
ab21
ab22
ba11
ba12
ba21
ba22
bb11
bb12
bb21
bb22
Total words: 16
```

#### Example 3: Word Permutations
Simulate `crunch 1 1 -p dog cat bird`:
```bash
$ python3 crunch_simulator.py
*** Crunch Simulator ***
Do you want to generate permutations of specific words (-p)? (yes/no): yes
Enter words (separated by spaces, e.g., dog cat bird): dog cat bird
Do you want to save output to a file (-o)? (yes/no): yes
Enter output file name (e.g., wordlist.txt, empty to print): permute.txt
Do you want to split output files (-b)? (yes/no): no
Do you want to compress output (-z)? (yes/no): no
Words saved to permute.txt. Total words: 6
```
**Output in `permute.txt`**:
```
dogcatbird
dogbirdcat
catdogbird
catbirddog
birddogcat
birdcatdog
```

#### Example 4: With Splitting and Compression
Generate words with file splitting and compression:
```bash
$ python3 crunch_simulator.py
*** Crunch Simulator ***
Do you want to generate permutations of specific words (-p)? (yes/no): no
Enter minimum word length: 3
Enter maximum word length: 3
Enter lowercase charset (e.g., abc, empty for default): abc
Enter uppercase charset (e.g., ABC, empty for default or +): 
Enter numbers charset (e.g., 123, empty for default): 
Enter symbols charset (e.g., !@#, empty for default): 
Do you want to specify a pattern (-t)? (yes/no): no
Do you want to apply duplicate limits (-d)? (yes/no): no
Do you want to start from a specific word (-s)? (yes/no): no
Do you want to stop at a specific word (-e)? (yes/no): no
Do you want to save output to a file (-o)? (yes/no): yes
Enter output file name (e.g., wordlist.txt, empty to print): wordlist.txt
Do you want to split output files (-b)? (yes/no): yes
Enter file size (e.g., 10mb or 20kib): 10kb
Do you want to compress output (-z)? (yes/no): yes
Enter compression type (gzip, bzip2, lzma): gzip
Words saved to split files. Total words: 27
```
**Output**: Files like `aaa-acc.txt.gz`, `aca-ccc.txt.gz`.

## Notes
- **Character Sets**: Leave empty or enter `+` to use defaults:
  - Lowercase: `abcdefghijklmnopqrstuvwxyz`
  - Uppercase: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
  - Numbers: `0123456789`
  - Symbols: `!@#$%^&*()-_+=~`[]{}|\:;"'<>,.?/ `
- **Empty Sets**: To exclude a character set (e.g., no uppercase), enter a space (` `) for that set.
- **Large Outputs**: Be cautious with large charsets or lengths, as memory usage can be high. Test with small inputs first.
- **Unsupported Features**: The script does not support `-r` (resume), `-q` (read from file), `-c` (line count limit), or `7z` compression. For `7z`, install `py7zr` and modify the script.
- **Error Handling**: The script validates inputs but may not handle all edge cases. Report issues for improvements.

## Limitations
- Memory-intensive for large combinations (e.g., length 8 with many characters).
- No support for resuming interrupted sessions (`-r`).
- Compression limited to `gzip`, `bzip2`, and `lzma` (no `7z` without additional libraries).
- No support for reading character sets from a file like `charset.lst` (`-f`).

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository (if hosted).
2. Create a feature branch.
3. Submit a pull request with clear descriptions of changes.

Report bugs or request features by opening an issue on the repository (if hosted) or contacting the author.

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Author
Developed as a simulation of the `crunch` tool for educational and testing purposes. Contact for support or feedback via GitHub issues (if hosted).

---
*Generated on June 26, 2025*
