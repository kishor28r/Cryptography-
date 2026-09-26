import os
import re

# Load all 4619 pristine words
with open("scratch/build_wordlist.py", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r"'''(.*?)'''", text, re.DOTALL)
raw_text = match.group(1) if match else text

words = set(w.lower() for w in raw_text.split() if w.isalpha() and len(w) >= 2)

extra = """
computer security monarchy zebra matrix columnar railfence vigenere substitution playfair route caesar
cryptography password ciphertext plaintext decryption encryption algorithm key cipher attack defense
castle kingdom knight secret hidden treasure message signal protocol network server client terminal
midnight
""".split()

for w in extra:
    if w.isalpha() and len(w) >= 2:
        words.add(w.lower())

sorted_words = sorted(list(words))
formatted_wordset = ",\n    ".join(f'"{w}"' for w in sorted_words)

# Now read cipher_toolkit.py base logic and update EMBEDDED_WORDLIST, check_with_padding_strip, and statistical_fallback_guess
with open("cipher_toolkit.py", "r", encoding="utf-8") as f:
    orig_code = f.read()

# Replace EMBEDDED_WORDLIST definition
new_wordlist_code = f"EMBEDDED_WORDLIST: Set[str] = {{\n    {formatted_wordset}\n}}"
orig_code = re.sub(r"EMBEDDED_WORDLIST: Set\[str\] = \{.*?\n\}", new_wordlist_code, orig_code, flags=re.DOTALL)

with open("cipher_toolkit.py", "w", encoding="utf-8") as f:
    f.write(orig_code)

print("Updated EMBEDDED_WORDLIST in cipher_toolkit.py with 4619 words.")
