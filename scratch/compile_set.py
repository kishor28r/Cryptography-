import re

# Load base words string
with open("scratch/build_wordlist.py", "r", encoding="utf-8") as f:
    text = f.read()

# Extract all raw word tokens between triple quotes
match = re.search(r"'''(.*?)'''", text, re.DOTALL)
raw_text = match.group(1) if match else text

raw_words = set(w.lower() for w in raw_text.split() if w.isalpha() and len(w) >= 2)

# Expand with common English inflections
expanded = set(raw_words)
for w in list(raw_words):
    if len(w) >= 3:
        expanded.add(w + 's')
        if w.endswith('e'):
            expanded.add(w + 'd')
            expanded.add(w + 'r')
        elif not w.endswith(('y', 's', 'x', 'z', 'ch', 'sh')):
            expanded.add(w + 'ed')
            expanded.add(w + 'ing')
        elif w.endswith('y') and len(w) > 3 and w[-2] not in 'aeiou':
            expanded.add(w[:-1] + 'ies')
            expanded.add(w[:-1] + 'ied')

final_words = sorted(list(set(w for w in expanded if w.isalpha() and len(w) >= 2)))

print(f"Generated {len(final_words)} words.")
print("Sample words:", final_words[:20])
print("Checking target words:")
for target in ['computer', 'security', 'monarchy', 'zebra', 'matrix', 'rail', 'fence', 'route', 'columnar']:
    print(f"  {target}: {target in final_words}")
