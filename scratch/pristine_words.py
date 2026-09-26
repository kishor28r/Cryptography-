import re

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

final_words = sorted(list(words))
print(f"Total pristine English words: {len(final_words)}")
for target in ['computer', 'security', 'monarchy', 'zebra', 'matrix', 'rail', 'fence', 'route', 'columnar', 'midnight']:
    print(f"  {target}: {target in final_words}")
