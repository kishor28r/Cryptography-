import os

with open("scratch/build_wordlist.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("base_words = '''", "base_text = '''")
content = content.replace("words = set(w.lower() for w in base_words.split()", "words = set(w.lower() for w in base_text.split()")

with open("scratch/build_wordlist.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed build_wordlist.py")
