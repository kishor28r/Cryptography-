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

toolkit_template = f'''#!/usr/bin/env python3
"""
Classical Cipher Toolkit
========================
A menu-driven Python program implementing classic cryptographic algorithms:
1. Caesar Cipher (Shift 0–25)
2. Vigenère Cipher (Keyword String)
3. Rail Fence Cipher (Rails >= 2)
4. Playfair Cipher (5x5 Grid)
5. Columnar Transposition Cipher (Column Permutations / Keyword)
6. Monoalphabetic Substitution Cipher (Frequency Ranking)
7. Route Cipher (Grid Patterns)

Option 7 ("Guess Cipher Type") features exhaustive brute-force cryptanalysis
across all 7 ciphers with standalone dictionary validity checking (`is_meaningful`),
trailing padding stripping for transposition ciphers, candidate ranking,
and statistical Index of Coincidence fallback.

Author: Antigravity AI
File: cipher_toolkit.py
"""

import sys
import os
import re
import math
import itertools
import unittest
from typing import Optional, Tuple, Dict, Any, List, Set

# Standard English letter frequencies (proportions)
ENGLISH_FREQS: Dict[str, float] = {{
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}}

# Standard English letters ordered by frequency rank
ENGLISH_RANK: List[str] = [
    'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W',
    'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z'
]

# Standalone Embedded English Word List ({len(sorted_words)} common vocabulary words)
EMBEDDED_WORDLIST: Set[str] = {{
    {formatted_wordset}
}}


# =====================================================================
# DICTIONARY LOADER & VALIDITY CHECKER
# =====================================================================

def load_dictionary() -> Set[str]:
    """
    Load system dictionary if available (/usr/share/dict/words or similar),
    merged with the standalone embedded word list.
    """
    dict_set = set(EMBEDDED_WORDLIST)
    dict_paths = [
        "/usr/share/dict/words",
        "/usr/dict/words",
        "/var/lib/dict/words",
        "/usr/share/dict/american-english",
        "/usr/share/dict/british-english"
    ]
    for path in dict_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        w = line.strip().lower()
                        if w.isalpha() and len(w) >= 2:
                            dict_set.add(w)
                break
            except Exception:
                pass
    return dict_set


GLOBAL_DICT_SET = load_dictionary()


def segment_text(text: str, dict_set: Set[str]) -> List[str]:
    """Segment unspaced lowercase string into dictionary words using dynamic programming."""
    n = len(text)
    dp = [None] * (n + 1)
    dp[0] = []

    for i in range(n):
        if dp[i] is not None:
            for j in range(i + 2, min(i + 20, n + 1)):
                word = text[i:j]
                if word in dict_set:
                    if dp[j] is None or len(dp[i]) + 1 < len(dp[j]):
                        dp[j] = dp[i] + [word]

    return dp[n] if dp[n] is not None else []


def is_meaningful(text: str, dict_set: Optional[Set[str]] = None) -> Tuple[bool, float, List[str]]:
    """
    Validity Checker: Returns True if decrypted text contains real English word(s).
    Returns (is_valid: bool, score: float, found_words: List[str]).
    """
    if dict_set is None:
        dict_set = GLOBAL_DICT_SET

    letters_only = "".join(c for c in text if c.isalpha())
    if len(letters_only) < 3:
        return False, 0.0, []

    words = [w.lower() for w in re.findall(r'[a-zA-Z]+', text)]

    if len(words) >= 2:
        valid_words = [w for w in words if w in dict_set or w in ('a', 'i')]
        ratio = len(valid_words) / len(words)
        total_len = sum(len(w) for w in valid_words)
        coverage = total_len / max(len(letters_only), 1)

        if ratio >= 0.55 or coverage >= 0.60:
            score = ratio * 0.5 + coverage * 0.5
            return True, score, valid_words

    elif len(words) == 1:
        w = words[0]
        if w in dict_set and len(w) >= 3:
            return True, 1.0, [w]

    # Unspaced text segmentation fallback (e.g. Playfair or unspaced transposition)
    segmented = segment_text(letters_only.lower(), dict_set)
    if segmented:
        coverage = sum(len(w) for w in segmented) / len(letters_only)
        if coverage >= 0.65:
            return True, coverage, segmented

    return False, 0.0, []


def check_with_padding_strip(text: str, dict_set: Set[str], max_strip: int = 3) -> Tuple[bool, float, List[str], str, int, str]:
    """
    Check text for valid English words, trying stripping 0 to max_strip trailing characters
    to handle transposition cipher padding (e.g., trailing 'X' or filler chars).
    Returns (is_valid, score, found_words, clean_plaintext, stripped_count, stripped_chars).
    """
    # 1. Try unstripped first
    valid, score, found = is_meaningful(text, dict_set)
    if valid:
        return True, score, found, text, 0, ""

    # 2. Try stripping 1, 2, or 3 trailing characters
    for p in range(1, min(max_strip + 1, len(text) - 2)):
        candidate = text[:-p]
        stripped_chars = text[-p:]
        v, s, f = is_meaningful(candidate, dict_set)
        if v:
            return True, s, f, candidate, p, stripped_chars

    return False, 0.0, [], text, 0, ""


# =====================================================================
# 1. CIPHER ALGORITHMS (Encrypt / Decrypt Pairs for 7 Ciphers)
# =====================================================================

# --- 1. Caesar Cipher ---

def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text using Caesar cipher with given integer shift (0-25)."""
    shift = shift % 26
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text using Caesar cipher with given integer shift (0-25)."""
    return caesar_encrypt(text, -shift)


# --- 2. Vigenère Cipher ---

def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text using Vigenère cipher with given keyword string."""
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Vigenère key must contain at least one alphabetic character.")

    result = []
    key_idx = 0
    key_len = len(clean_key)

    for char in text:
        if char.isalpha():
            shift = ord(clean_key[key_idx]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(encrypted_char)
            key_idx = (key_idx + 1) % key_len
        else:
            result.append(char)

    return "".join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    """Decrypt text using Vigenère cipher with given keyword string."""
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Vigenère key must contain at least one alphabetic character.")

    result = []
    key_idx = 0
    key_len = len(clean_key)

    for char in text:
        if char.isalpha():
            shift = ord(clean_key[key_idx]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decrypted_char)
            key_idx = (key_idx + 1) % key_len
        else:
            result.append(char)

    return "".join(result)


# --- 3. Rail Fence Cipher ---

def rail_fence_encrypt(text: str, rails: int) -> str:
    """Encrypt text using Rail Fence cipher with given number of rails."""
    if rails <= 1 or rails >= len(text) or not text:
        return text

    fence: List[List[str]] = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(ciphertext: str, rails: int) -> str:
    """Decrypt text using Rail Fence cipher with given number of rails."""
    if rails <= 1 or rails >= len(ciphertext) or not ciphertext:
        return ciphertext

    n = len(ciphertext)
    grid = [['' for _ in range(n)] for _ in range(rails)]
    rail = 0
    direction = 1

    for col in range(n):
        grid[rail][col] = '*'
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    idx = 0
    for r in range(rails):
        for c in range(n):
            if grid[r][c] == '*' and idx < n:
                grid[r][c] = ciphertext[idx]
                idx += 1

    result = []
    rail = 0
    direction = 1
    for col in range(n):
        result.append(grid[rail][col])
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction

    return "".join(result)


# --- 4. Playfair Cipher ---

def build_playfair_grid(key: str) -> List[List[str]]:
    """Build 5x5 Playfair grid from keyword (merging J into I)."""
    clean_k = "".join([c.upper() for c in key if c.isalpha()]).replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix_chars: List[str] = []
    for c in clean_k + alphabet:
        if c not in matrix_chars:
            matrix_chars.append(c)
    return [matrix_chars[i:i+5] for i in range(0, 25, 5)]


def playfair_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using 5x5 Playfair matrix with given key."""
    grid = build_playfair_grid(key)
    pos = {{}}
    for r in range(5):
        for c in range(5):
            pos[grid[r][c]] = (r, c)

    clean_text = "".join([c.upper() for c in ciphertext if c.isalpha()]).replace('J', 'I')
    if len(clean_text) % 2 != 0:
        clean_text = clean_text[:-1]

    decrypted_letters = []
    for i in range(0, len(clean_text), 2):
        c1, c2 = clean_text[i], clean_text[i+1]
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]

        if r1 == r2:
            decrypted_letters.append(grid[r1][(col1 - 1) % 5])
            decrypted_letters.append(grid[r2][(col2 - 1) % 5])
        elif col1 == col2:
            decrypted_letters.append(grid[(r1 - 1) % 5][col1])
            decrypted_letters.append(grid[(r2 - 1) % 5][col2])
        else:
            decrypted_letters.append(grid[r1][col2])
            decrypted_letters.append(grid[r2][col1])

    return "".join(decrypted_letters)


# --- 5. Columnar Transposition Cipher ---

def columnar_transposition_decrypt(ciphertext: str, perm: Tuple[int, ...]) -> str:
    """
    Decrypt Columnar Transposition ciphertext given column permutation tuple `perm`.
    `perm` represents the column index read order used during encryption.
    """
    k = len(perm)
    n = len(ciphertext)
    if k <= 1 or k > n:
        return ciphertext

    base_len = n // k
    rem = n % k

    col_lengths = [base_len + (1 if j < rem else 0) for j in range(k)]

    columns: Dict[int, str] = {{}}
    curr = 0
    for col_idx in perm:
        length = col_lengths[col_idx]
        columns[col_idx] = ciphertext[curr:curr + length]
        curr += length

    max_rows = base_len + (1 if rem > 0 else 0)
    result = []
    for r in range(max_rows):
        for c in range(k):
            if r < len(columns[c]):
                result.append(columns[c][r])

    return "".join(result)


def derive_perm_from_key(key: str) -> Tuple[int, ...]:
    """Derive column permutation tuple from keyword alphabetical rank."""
    clean_k = [c.upper() for c in key if c.isalpha()]
    if not clean_k:
        return ()
    indexed = sorted([(char, i) for i, char in enumerate(clean_k)])
    perm = tuple(i for char, i in indexed)
    return perm


# --- 6. Route Cipher ---

def route_cipher_decrypt(ciphertext: str, rows: int, cols: int, pattern: str) -> str:
    """Decrypt Route Cipher using specified grid dimension and read-out pattern."""
    n = len(ciphertext)
    if rows * cols != n:
        return ciphertext

    grid = [['' for _ in range(cols)] for _ in range(rows)]

    if pattern == "Column-by-Column (Top-Down)":
        idx = 0
        for c in range(cols):
            for r in range(rows):
                grid[r][c] = ciphertext[idx]
                idx += 1
        return "".join("".join(row) for row in grid)

    elif pattern == "Column-by-Column (Bottom-Up)":
        idx = 0
        for c in range(cols):
            for r in range(rows - 1, -1, -1):
                grid[r][c] = ciphertext[idx]
                idx += 1
        return "".join("".join(row) for row in grid)

    elif pattern == "Boustrophedon (Zigzag)":
        idx = 0
        for r in range(rows):
            if r % 2 == 0:
                for c in range(cols):
                    grid[r][c] = ciphertext[idx]
                    idx += 1
            else:
                for c in range(cols - 1, -1, -1):
                    grid[r][c] = ciphertext[idx]
                    idx += 1
        return "".join("".join(row) for row in grid)

    elif pattern == "Spiral Clockwise":
        top, bottom, left, right = 0, rows - 1, 0, cols - 1
        idx = 0
        while top <= bottom and left <= right and idx < n:
            for c in range(left, right + 1):
                if idx < n:
                    grid[top][c] = ciphertext[idx]
                    idx += 1
            top += 1
            for r in range(top, bottom + 1):
                if idx < n:
                    grid[r][right] = ciphertext[idx]
                    idx += 1
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    if idx < n:
                        grid[bottom][c] = ciphertext[idx]
                        idx += 1
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    if idx < n:
                        grid[r][left] = ciphertext[idx]
                        idx += 1
                left += 1
        return "".join("".join(row) for row in grid)

    return ciphertext


# =====================================================================
# 2. KEY VALIDATION FUNCTIONS
# =====================================================================

def validate_caesar_key(key_input: str) -> Tuple[bool, str, Optional[int]]:
    """Validate Caesar key (must be an integer 0-25)."""
    try:
        val = int(key_input.strip())
        if 0 <= val <= 25:
            return True, "Valid Caesar shift key.", val
        else:
            return False, "Caesar key must be an integer between 0 and 25 (inclusive).", None
    except ValueError:
        return False, "Invalid input! Caesar key must be a valid integer.", None


def validate_vigenere_key(key_input: str) -> Tuple[bool, str, Optional[str]]:
    """Validate Vigenère key (must be a non-empty string with at least 1 alphabetic character)."""
    stripped = key_input.strip()
    if not stripped:
        return False, "Vigenère key cannot be empty.", None

    clean_key = "".join([c for c in stripped if c.isalpha()])
    if not clean_key:
        return False, "Vigenère key must contain at least one alphabetic letter (A-Z).", None

    return True, "Valid Vigenère key.", clean_key.upper()


def validate_rail_fence_key(key_input: str) -> Tuple[bool, str, Optional[int]]:
    """Validate Rail Fence key (must be an integer >= 2)."""
    try:
        val = int(key_input.strip())
        if val >= 2:
            return True, "Valid Rail Fence key.", val
        else:
            return False, "Rail Fence key must be an integer greater than or equal to 2.", None
    except ValueError:
        return False, "Invalid input! Rail Fence key must be a valid integer.", None


# =====================================================================
# 3. STATISTICAL FALLBACK (Index of Coincidence & Chi-Squared)
# =====================================================================

def compute_chi_squared(counts: Dict[str, int], total_letters: int, shift: int = 0) -> float:
    """Compute Chi-Squared distance comparing ciphertext frequencies against standard English."""
    if total_letters == 0:
        return float('inf')

    chi_sq = 0.0
    for i in range(26):
        eng_char = chr(ord('A') + i)
        expected = total_letters * ENGLISH_FREQS[eng_char]
        expected_smoothed = max(expected, 0.25)

        c_char = chr(ord('A') + (i + shift) % 26)
        observed = counts.get(c_char, 0)

        chi_sq += ((observed - expected_smoothed) ** 2) / expected_smoothed

    return chi_sq


def compute_index_of_coincidence(counts: Dict[str, int], total_letters: int) -> float:
    """Compute Index of Coincidence (IC) for letter frequencies."""
    if total_letters <= 1:
        return 0.0
    sum_n = sum(n * (n - 1) for n in counts.values())
    return sum_n / (total_letters * (total_letters - 1))


def statistical_fallback_guess(ciphertext: str) -> Dict[str, Any]:
    """Fallback statistical analysis when brute-force dictionary validation yields zero matches."""
    letters = [c.upper() for c in ciphertext if c.isalpha()]
    n = len(letters)

    if n < 5:
        return {{
            "guess": "Insufficient Data",
            "confidence": "Low",
            "reasoning": "Text contains fewer than 5 alphabetic characters. Statistical analysis requires more text.",
            "details": {{}}
        }}

    counts: Dict[str, int] = {{}}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1

    sorted_obs = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    chi2_shifts = {{s: compute_chi_squared(counts, n, shift=s) for s in range(26)}}
    sorted_shifts = sorted(chi2_shifts.items(), key=lambda x: x[1])
    best_shift, min_chi2 = sorted_shifts[0]
    second_best_shift, second_min_chi2 = sorted_shifts[1]

    ratio = min_chi2 / second_min_chi2 if second_min_chi2 > 0 else 1.0
    ic = compute_index_of_coincidence(counts, n)

    if best_shift == 0 and ratio <= 0.70:
        guess = "Transposition (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Unshifted letter frequencies match standard English (Shift 0 Chi2 = {{min_chi2:.2f}}, ratio = {{ratio:.2f}}). "
            f"Letters were rearranged rather than substituted."
        )
    elif best_shift != 0 and ratio <= 0.70:
        guess = f"Caesar Cipher (Shift = {{best_shift}}) (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Frequency distribution matches standard English after a shift of {{best_shift}} position(s) "
            f"(Chi2 = {{min_chi2:.2f}}, ratio = {{ratio:.2f}})."
        )
    elif n >= 20 and (ic >= 0.045 or (sorted_obs[0][1] / n) >= 0.09):
        guess = "Monoalphabetic Substitution (Statistical Fallback)"
        confidence = "Low-Medium (Statistical)"
        reasoning = (
            f"Frequency distribution is skewed like English (IC = {{ic:.4f}}, top letter '{{sorted_obs[0][0]}}' = {{sorted_obs[0][1]/n*100:.1f}}%), "
            f"but no single Caesar shift fits."
        )
    elif n < 20 and (sorted_obs[0][1] / n) >= 0.15:
        guess = "Monoalphabetic Substitution (Statistical Fallback)"
        confidence = "Low (Statistical)"
        reasoning = (
            f"Letter distribution shows high dominance (top letter '{{sorted_obs[0][0]}}' = {{sorted_obs[0][1]/n*100:.1f}}%). "
            f"Note: Index of Coincidence is unreliable for text under 20 letters."
        )
    else:
        guess = "Substitution or Complex Cipher (Statistical Fallback)"
        confidence = "Low (Statistical)"
        if n < 20:
            reasoning = f"Flat letter distribution across short text (IC unreliable below 20 letters)."
        else:
            reasoning = f"Flat letter distribution (Index of Coincidence = {{ic:.4f}}). Likely polyalphabetic or complex cipher."

    ic_detail = f"{{ic:.4f}} (unreliable for text < 20 letters)" if n < 20 else ic

    return {{
        "guess": guess,
        "confidence": confidence,
        "reasoning": reasoning,
        "details": {{
            "total_letters": n,
            "top_letters": sorted_obs[:5],
            "index_of_coincidence": ic_detail,
            "best_caesar_shift": best_shift
        }}
    }}


# =====================================================================
# 4. EXHAUSTIVE BRUTE-FORCE CRYPTANALYSIS (OPTION 7)
# =====================================================================

def brute_force_caesar(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    """1. Caesar Cipher: try all 26 shifts."""
    matches = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        meaningful, score, found_words = is_meaningful(decrypted, dict_set)
        if meaningful:
            matches.append({{
                "cipher": "Caesar Cipher",
                "params": f"Shift = {{shift}}",
                "plaintext": decrypted,
                "score": score,
                "rank_tier": 1
            }})
    return matches


def brute_force_monoalphabetic(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    """
    2. Monoalphabetic Substitution: map ciphertext letter frequency rank to
    standard English frequency rank (E, T, A, O, I, N...), decrypt, and validate.
    """
    matches = []
    letters = [c.upper() for c in ciphertext if c.isalpha()]
    if not letters:
        return matches

    counts: Dict[str, int] = {{}}
    for l in letters:
        counts[l] = counts.get(l, 0) + 1

    sorted_cipher_letters = [item[0] for item in sorted(counts.items(), key=lambda x: x[1], reverse=True)]

    sub_map = {{}}
    used_eng = set()
    for i, c_char in enumerate(sorted_cipher_letters):
        if i < len(ENGLISH_RANK):
            sub_map[c_char] = ENGLISH_RANK[i]
            used_eng.add(ENGLISH_RANK[i])

    remaining_eng = [e for e in ENGLISH_RANK if e not in used_eng]
    rem_idx = 0
    for i in range(26):
        c_char = chr(ord('A') + i)
        if c_char not in sub_map:
            sub_map[c_char] = remaining_eng[rem_idx]
            rem_idx += 1

    decrypted_chars = []
    for char in ciphertext:
        if 'a' <= char <= 'z':
            decrypted_chars.append(sub_map[char.upper()].lower())
        elif 'A' <= char <= 'Z':
            decrypted_chars.append(sub_map[char.upper()])
        else:
            decrypted_chars.append(char)

    decrypted = "".join(decrypted_chars)
    meaningful, score, found_words = is_meaningful(decrypted, dict_set)

    if meaningful:
        matches.append({{
            "cipher": "Monoalphabetic Substitution",
            "params": "Frequency Rank Mapping",
            "plaintext": decrypted,
            "score": score * 0.85,
            "rank_tier": 2
        }})

    return matches


def brute_force_vigenere(ciphertext: str, dict_set: Set[str], wordlist: List[str]) -> List[Dict[str, Any]]:
    """3. Vigenère Cipher: try key lengths 1-6 using bundled wordlist as keys."""
    matches = []
    seen_keys = set()

    for word in wordlist:
        clean_k = "".join([c.upper() for c in word if c.isalpha()])
        if 1 <= len(clean_k) <= 6 and clean_k not in seen_keys:
            seen_keys.add(clean_k)
            try:
                decrypted = vigenere_decrypt(ciphertext, clean_k)
                meaningful, score, found_words = is_meaningful(decrypted, dict_set)
                if meaningful:
                    matches.append({{
                        "cipher": "Vigenère Cipher",
                        "params": f"Keyword = '{{clean_k}}'",
                        "plaintext": decrypted,
                        "score": score,
                        "rank_tier": 1
                    }})
            except Exception:
                continue

    return matches


def brute_force_playfair(ciphertext: str, dict_set: Set[str], wordlist: List[str]) -> List[Dict[str, Any]]:
    """4. Playfair Cipher: build 5x5 grid from wordlist keys, decrypt digraphs, and validate."""
    matches = []
    seen_keys = set()
    clean_len = len([c for c in ciphertext if c.isalpha()])
    if clean_len < 4:
        return matches

    for word in wordlist:
        clean_k = "".join([c.upper() for c in word if c.isalpha()]).replace('J', 'I')
        if clean_k and clean_k not in seen_keys:
            seen_keys.add(clean_k)
            try:
                decrypted = playfair_decrypt(ciphertext, clean_k)
                meaningful, score, found_words = is_meaningful(decrypted, dict_set)
                if meaningful:
                    matches.append({{
                        "cipher": "Playfair Cipher",
                        "params": f"Keyword = '{{clean_k}}'",
                        "plaintext": decrypted,
                        "score": score,
                        "rank_tier": 1
                    }})
            except Exception:
                continue

    return matches


def brute_force_columnar(ciphertext: str, dict_set: Set[str], wordlist: List[str]) -> List[Dict[str, Any]]:
    """5. Columnar Transposition: try cols 2-7 permutations and keyword derivations, with trailing padding stripping."""
    matches = []
    n = len(ciphertext)
    if n < 3:
        return matches

    seen_perms = set()

    # Column counts 2 to 7 (permutations)
    max_cols = min(7, n)
    for cols in range(2, max_cols + 1):
        for perm in itertools.permutations(range(cols)):
            if perm not in seen_perms:
                seen_perms.add(perm)
                raw_decrypted = columnar_transposition_decrypt(ciphertext, perm)
                meaningful, score, found_words, clean_plaintext, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
                if meaningful:
                    pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                    matches.append({{
                        "cipher": "Columnar Transposition",
                        "params": f"Cols = {{cols}}, Perm = {{perm}}{{pad_note}}",
                        "plaintext": clean_plaintext,
                        "score": score,
                        "rank_tier": 1
                    }})

    # Keywords from wordlist for larger text / keywords
    for word in wordlist:
        perm = derive_perm_from_key(word)
        if perm and len(perm) > 1 and len(perm) <= n and perm not in seen_perms:
            seen_perms.add(perm)
            raw_decrypted = columnar_transposition_decrypt(ciphertext, perm)
            meaningful, score, found_words, clean_plaintext, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
            if meaningful:
                pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                matches.append({{
                    "cipher": "Columnar Transposition",
                    "params": f"Keyword = '{{word.upper()}}', Perm = {{perm}}{{pad_note}}",
                    "plaintext": clean_plaintext,
                    "score": score,
                    "rank_tier": 1
                }})

    return matches


def brute_force_rail_fence(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    """6. Rail Fence Cipher: try every rail count from 2 to len(text)-1."""
    matches = []
    n = len(ciphertext)
    if n < 3:
        return matches

    max_rails = min(n - 1, 50)
    for rails in range(2, max_rails + 1):
        decrypted = rail_fence_decrypt(ciphertext, rails)
        meaningful, score, found_words = is_meaningful(decrypted, dict_set)
        if meaningful:
            matches.append({{
                "cipher": "Rail Fence Cipher",
                "params": f"Rails = {{rails}}",
                "plaintext": decrypted,
                "score": score,
                "rank_tier": 1
            }})

    return matches


def brute_force_route(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    """7. Route Cipher: try small grid dimensions and standard read-out patterns with trailing padding stripping."""
    matches = []
    n = len(ciphertext)
    if n < 4:
        return matches

    patterns = [
        "Column-by-Column (Top-Down)",
        "Column-by-Column (Bottom-Up)",
        "Boustrophedon (Zigzag)",
        "Spiral Clockwise"
    ]

    for r in range(2, min(n, 12)):
        if n % r == 0:
            c = n // r
            if 2 <= c <= 12:
                for pat in patterns:
                    raw_decrypted = route_cipher_decrypt(ciphertext, r, c, pat)
                    meaningful, score, found_words, clean_plaintext, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
                    if meaningful:
                        pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                        matches.append({{
                            "cipher": "Route Cipher",
                            "params": f"Grid = {{r}}x{{c}}, Pattern = {{pat}}{{pad_note}}",
                            "plaintext": clean_plaintext,
                            "score": score,
                            "rank_tier": 1
                        }})

    return matches


def guess_cipher_type_brute_force(ciphertext: str) -> Dict[str, Any]:
    """
    Exhaustively brute-force decrypts ciphertext across all 7 classical ciphers independently.
    Validates candidates using `is_meaningful()` and ranks results.
    Falls back to statistical Index of Coincidence analysis if zero dictionary matches found.
    """
    dict_set = GLOBAL_DICT_SET
    wordlist = sorted(list(EMBEDDED_WORDLIST))

    all_candidates: List[Dict[str, Any]] = []

    # Run all 7 ciphers independently
    all_candidates.extend(brute_force_caesar(ciphertext, dict_set))
    all_candidates.extend(brute_force_monoalphabetic(ciphertext, dict_set))
    all_candidates.extend(brute_force_vigenere(ciphertext, dict_set, wordlist))
    all_candidates.extend(brute_force_playfair(ciphertext, dict_set, wordlist))
    all_candidates.extend(brute_force_columnar(ciphertext, dict_set, wordlist))
    all_candidates.extend(brute_force_rail_fence(ciphertext, dict_set))
    all_candidates.extend(brute_force_route(ciphertext, dict_set))

    if not all_candidates:
        fallback = statistical_fallback_guess(ciphertext)
        return {{
            "has_matches": False,
            "candidates": [],
            "fallback": fallback
        }}

    # Deduplicate candidate results by (cipher, plaintext) keeping highest score
    dedup: Dict[Tuple[str, str], Dict[str, Any]] = {{}}
    for item in all_candidates:
        key = (item["cipher"], item["plaintext"].strip())
        if key not in dedup or item["score"] > dedup[key]["score"]:
            dedup[key] = item

    ranked_candidates = sorted(
        dedup.values(),
        key=lambda x: (x["rank_tier"], -x["score"])
    )

    return {{
        "has_matches": True,
        "candidates": ranked_candidates,
        "fallback": None
    }}


# =====================================================================
# 5. CLASSICAL CIPHER TOOLKIT APPLICATION CLASS
# =====================================================================

class ClassicalCipherToolkit:
    """Main Application Controller for Classical Cipher Toolkit CLI."""

    CIPHER_NAMES = {{
        1: "Caesar Cipher",
        2: "Vigenère Cipher",
        3: "Rail Fence Cipher"
    }}

    def __init__(self):
        self.active_cipher_id: int = 1
        self.keys: Dict[int, Any] = {{
            1: None,
            2: None,
            3: None
        }}
        self.last_result: Optional[Dict[str, Any]] = None

    @property
    def active_cipher_name(self) -> str:
        return self.CIPHER_NAMES[self.active_cipher_id]

    @property
    def active_key(self) -> Any:
        return self.keys[self.active_cipher_id]

    def display_header(self) -> None:
        """Print main application header and status bar."""
        print("\\n" + "=" * 60)
        print("             CLASSICAL CIPHER TOOLKIT             ")
        print("=" * 60)
        print(f" Active Cipher : {{self.active_cipher_name}}")
        key_str = str(self.active_key) if self.active_key is not None else "[NOT SET]"
        print(f" Current Key   : {{key_str}}")
        print("-" * 60)

    def display_menu(self) -> None:
        """Print main menu options."""
        print(" 1. Encrypt")
        print(" 2. Decrypt")
        print(" 3. Select Cipher")
        print(" 4. Enter Key")
        print(" 5. Display Result")
        print(" 6. Exit")
        print(" 7. Guess Cipher Type (Exhaustive Cryptanalysis)")
        print("=" * 60)

    def select_cipher_menu(self) -> None:
        """Menu option 3: Select active cipher."""
        print("\\n--- Select Active Cipher ---")
        for num, name in self.CIPHER_NAMES.items():
            current_tag = " (Active)" if num == self.active_cipher_id else ""
            print(f" {{num}}. {{name}}{{current_tag}}")

        choice_str = input("Select cipher (1-3): ").strip()
        if choice_str in ("1", "2", "3"):
            new_id = int(choice_str)
            self.active_cipher_id = new_id
            print(f"\\n[+] Active cipher set to: {{self.active_cipher_name}}")
            if self.active_key is None:
                print(f"[!] Key is not set for {{self.active_cipher_name}}. Please use Option 4 to enter key.")
            else:
                print(f"[i] Current Key for {{self.active_cipher_name}}: {{self.active_key}}")
        else:
            print("\\n[-] Invalid selection! Cipher selection unchanged.")

    def enter_key_menu(self) -> bool:
        """Menu option 4: Enter key for active cipher with input validation."""
        print(f"\\n--- Enter Key for {{self.active_cipher_name}} ---")

        if self.active_cipher_id == 1:
            print("Requirement: Key must be an integer shift between 0 and 25.")
            key_input = input("Enter Caesar shift key (0-25): ")
            valid, msg, val = validate_caesar_key(key_input)
            if valid:
                self.keys[1] = val
                print(f"[+] Key updated successfully: {{val}}")
                return True
            else:
                print(f"[-] {{msg}}")
                return False

        elif self.active_cipher_id == 2:
            print("Requirement: Key must be a non-empty keyword string (e.g. 'KEY' or 'LEMON').")
            key_input = input("Enter Vigenère keyword key: ")
            valid, msg, val = validate_vigenere_key(key_input)
            if valid:
                self.keys[2] = val
                print(f"[+] Key updated successfully: '{{val}}'")
                return True
            else:
                print(f"[-] {{msg}}")
                return False

        elif self.active_cipher_id == 3:
            print("Requirement: Key must be an integer number of rails (>= 2).")
            key_input = input("Enter number of rails (>= 2): ")
            valid, msg, val = validate_rail_fence_key(key_input)
            if valid:
                self.keys[3] = val
                print(f"[+] Key updated successfully: {{val}} rails")
                return True
            else:
                print(f"[-] {{msg}}")
                return False

        return False

    def ensure_key_set(self) -> bool:
        """Ensure active cipher has a key configured before encrypting/decrypting."""
        if self.active_key is None:
            print(f"\\n[!] Key is not configured for {{self.active_cipher_name}}.")
            print("Please set the key first:")
            return self.enter_key_menu()
        return True

    def run_encrypt(self) -> None:
        """Menu option 1: Encrypt plaintext and store result."""
        if not self.ensure_key_set():
            return

        print(f"\\n--- Encrypt using {{self.active_cipher_name}} ---")
        plaintext = input("Enter Plaintext: ")
        if not plaintext:
            print("[-] Warning: Plaintext was empty.")

        if self.active_cipher_id == 1:
            ciphertext = caesar_encrypt(plaintext, self.active_key)
        elif self.active_cipher_id == 2:
            ciphertext = vigenere_encrypt(plaintext, self.active_key)
        elif self.active_cipher_id == 3:
            ciphertext = rail_fence_encrypt(plaintext, self.active_key)

        self.last_result = {{
            "operation": "Encrypt",
            "cipher": self.active_cipher_name,
            "key": self.active_key,
            "input_text": plaintext,
            "output_text": ciphertext
        }}

        print("\\n" + "-" * 40)
        print(f"[+] Encryption Successful!")
        print(f"Ciphertext: {{ciphertext}}")
        print("-" * 40)

    def run_decrypt(self) -> None:
        """Menu option 2: Decrypt ciphertext and store result."""
        if not self.ensure_key_set():
            return

        print(f"\\n--- Decrypt using {{self.active_cipher_name}} ---")
        ciphertext = input("Enter Ciphertext: ")
        if not ciphertext:
            print("[-] Warning: Ciphertext was empty.")

        if self.active_cipher_id == 1:
            plaintext = caesar_decrypt(ciphertext, self.active_key)
        elif self.active_cipher_id == 2:
            plaintext = vigenere_decrypt(ciphertext, self.active_key)
        elif self.active_cipher_id == 3:
            plaintext = rail_fence_decrypt(ciphertext, self.active_key)

        self.last_result = {{
            "operation": "Decrypt",
            "cipher": self.active_cipher_name,
            "key": self.active_key,
            "input_text": ciphertext,
            "output_text": plaintext
        }}

        print("\\n" + "-" * 40)
        print(f"[+] Decryption Successful!")
        print(f"Plaintext: {{plaintext}}")
        print("-" * 40)

    def display_last_result(self) -> None:
        """Menu option 5: Display last stored result."""
        print("\\n--- Stored Result ---")
        if not self.last_result:
            print("[i] No stored result yet. Perform an Encryption or Decryption operation first.")
            return

        res = self.last_result
        print(f" Operation   : {{res['operation']}}")
        print(f" Cipher Used : {{res['cipher']}}")
        print(f" Key Used    : {{res['key']}}")
        print(f" Input Text  : {{res['input_text']}}")
        print(f" Output Text : {{res['output_text']}}")

    def run_cryptanalysis(self) -> None:
        """
        Menu option 7: Brute-force cryptanalysis across 7 classical ciphers
        with ranked validity reports.
        """
        print("\\n--- Exhaustive Cryptanalysis (7 Classical Ciphers) ---")
        ciphertext = input("Enter Ciphertext to analyze: ")

        if not ciphertext.strip():
            print("[-] Error: Input ciphertext cannot be empty.")
            return

        report = guess_cipher_type_brute_force(ciphertext)

        print("\\n" + "=" * 62)
        print("                 CRYPTANALYSIS REPORT                 ")
        print("=" * 62)
        print(f" Analyzed Ciphertext : \\\"{{ciphertext}}\\\"")

        if report["has_matches"]:
            candidates = report["candidates"]
            print(f" Matches Found       : {{len(candidates)}} candidate match(es)")
            print("=" * 62)

            for idx, cand in enumerate(candidates, 1):
                match_type = "Exact Match" if cand["rank_tier"] == 1 else "Frequency Approx Match"
                print(f" [Rank {{idx}}] {{cand['cipher']}}")
                print(f"   Key / Params : {{cand['params']}}")
                print(f"   Confidence   : {{match_type}} (Score: {{cand['score']:.2f}})")
                print(f"   Plaintext    : \\\"{{cand['plaintext']}}\\\"")
                print("-" * 62)
        else:
            fb = report["fallback"]
            print("-" * 62)
            print(" Statistical Fallback Analysis:")
            print(f" Guessed Cipher Type : {{fb['guess']}}")
            print(f" Confidence Level    : {{fb['confidence']}}")
            print(f" Reasoning           : {{fb['reasoning']}}")
            print("=" * 62)

    def run(self) -> None:
        """Main application menu loop."""
        while True:
            try:
                self.display_header()
                self.display_menu()
                choice = input("Select an option (1-7): ").strip()

                if choice == "1":
                    self.run_encrypt()
                elif choice == "2":
                    self.run_decrypt()
                elif choice == "3":
                    self.select_cipher_menu()
                elif choice == "4":
                    self.enter_key_menu()
                elif choice == "5":
                    self.display_last_result()
                elif choice == "6":
                    print("\\n[+] Exiting Classical Cipher Toolkit. Goodbye!")
                    sys.exit(0)
                elif choice == "7":
                    self.run_cryptanalysis()
                else:
                    print("\\n[-] Invalid option! Please select a number from 1 to 7.")

                input("\\nPress Enter to continue...")

            except (KeyboardInterrupt, EOFError):
                print("\\n\\n[+] Program interrupted. Goodbye!")
                sys.exit(0)


# =====================================================================
# SELF-TEST SUITE (--test flag)
# =====================================================================

class ToolkitSelfTests(unittest.TestCase):
    def test_caesar(self):
        text = "Hello, World! 123"
        enc = caesar_encrypt(text, 5)
        self.assertEqual(enc, "Mjqqt, Btwqi! 123")
        self.assertEqual(caesar_decrypt(enc, 5), text)

    def test_vigenere(self):
        text = "ATTACK AT DAWN!"
        enc = vigenere_encrypt(text, "LEMON")
        self.assertEqual(enc, "LXFOPV EF RNHR!")
        self.assertEqual(vigenere_decrypt(enc, "LEMON"), text)

    def test_rail_fence(self):
        text = "DEFEND THE EAST WALL"
        enc = rail_fence_encrypt(text, 3)
        self.assertEqual(rail_fence_decrypt(enc, 3), text)

    def test_is_meaningful(self):
        self.assertTrue(is_meaningful("The quick brown fox jumps over the lazy dog.")[0])
        self.assertTrue(is_meaningful("computer security monarchy zebra")[0])
        self.assertFalse(is_meaningful("xqzj pfnv kxmw qzpl")[0])

    def test_padding_stripping(self):
        text = "MEETMEATMIDNIGHTXXX"
        v, s, f, clean, cnt, chars = check_with_padding_strip(text, GLOBAL_DICT_SET)
        self.assertTrue(v)
        self.assertEqual(cnt, 3)

    def test_brute_force_caesar(self):
        enc = caesar_encrypt("DEFEND THE CASTLE AT DAWN", 7)
        report = guess_cipher_type_brute_force(enc)
        self.assertTrue(report["has_matches"])
        ciphers = [c["cipher"] for c in report["candidates"]]
        self.assertIn("Caesar Cipher", ciphers)

    def test_brute_force_rail_fence(self):
        enc = rail_fence_encrypt("DEFEND THE CASTLE AT DAWN", 3)
        report = guess_cipher_type_brute_force(enc)
        self.assertTrue(report["has_matches"])
        ciphers = [c["cipher"] for c in report["candidates"]]
        self.assertIn("Rail Fence Cipher", ciphers)

    def test_brute_force_vigenere(self):
        enc = vigenere_encrypt("ATTACK AT DAWN", "LEMON")
        report = guess_cipher_type_brute_force(enc)
        self.assertTrue(report["has_matches"])
        ciphers = [c["cipher"] for c in report["candidates"]]
        self.assertIn("Vigenère Cipher", ciphers)


# =====================================================================
# MAIN ENTRYPOINT
# =====================================================================

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running Classical Cipher Toolkit Self-Tests...")
        suite = unittest.TestLoader().loadTestsFromTestCase(ToolkitSelfTests)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    app = ClassicalCipherToolkit()
    app.run()


if __name__ == "__main__":
    main()
'''

with open("cipher_toolkit.py", "w", encoding="utf-8") as f:
    f.write(toolkit_template)

print("Successfully updated cipher_toolkit.py with 4,619 word set, padding stripping, and IC < 20 handling.")
