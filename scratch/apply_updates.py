import re

with open("cipher_toolkit.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add check_with_padding_strip after is_meaningful
padding_function_code = '''
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
'''

if "def check_with_padding_strip" not in code:
    code = code.replace("return False, 0.0, []\n\n\n# =", f"return False, 0.0, []\n\n{padding_function_code}\n\n# =")

# 2. Update statistical_fallback_guess for n < 20
old_stat_fallback = """def statistical_fallback_guess(ciphertext: str) -> Dict[str, Any]:
    \"\"\"Fallback statistical analysis when brute-force dictionary validation yields zero matches.\"\"\"
    letters = [c.upper() for c in ciphertext if c.isalpha()]
    n = len(letters)

    if n < 5:
        return {
            "guess": "Insufficient Data",
            "confidence": "Low",
            "reasoning": "Text contains fewer than 5 alphabetic characters. Statistical analysis requires more text.",
            "details": {}
        }

    counts: Dict[str, int] = {}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1

    sorted_obs = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    chi2_shifts = {s: compute_chi_squared(counts, n, shift=s) for s in range(26)}
    sorted_shifts = sorted(chi2_shifts.items(), key=lambda x: x[1])
    best_shift, min_chi2 = sorted_shifts[0]
    second_best_shift, second_min_chi2 = sorted_shifts[1]

    ratio = min_chi2 / second_min_chi2 if second_min_chi2 > 0 else 1.0
    ic = compute_index_of_coincidence(counts, n)
    top_obs_letters = [item[0] for item in sorted_obs[:5]]

    if best_shift == 0 and ratio <= 0.70:
        guess = "Transposition (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Unshifted letter frequencies match standard English (Shift 0 Chi2 = {min_chi2:.2f}, ratio = {ratio:.2f}). "
            f"Letters were rearranged rather than substituted."
        )
    elif best_shift != 0 and ratio <= 0.70:
        guess = f"Caesar Cipher (Shift = {best_shift}) (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Frequency distribution matches standard English after a shift of {best_shift} position(s) "
            f"(Chi2 = {min_chi2:.2f}, ratio = {ratio:.2f})."
        )
    elif ic >= 0.045 or (sorted_obs[0][1] / n) >= 0.09:
        guess = "Monoalphabetic Substitution (Statistical Fallback)"
        confidence = "Low-Medium (Statistical)"
        reasoning = (
            f"Frequency distribution is skewed like English (IC = {ic:.4f}, top letter '{sorted_obs[0][0]}' = {sorted_obs[0][1]/n*100:.1f}%), "
            f"but no single Caesar shift fits."
        )
    else:
        guess = "Substitution or Complex Cipher (Statistical Fallback)"
        confidence = "Low (Statistical)"
        reasoning = f"Flat letter distribution (Index of Coincidence = {ic:.4f}). Likely polyalphabetic or complex cipher."

    return {
        "guess": guess,
        "confidence": confidence,
        "reasoning": reasoning,
        "details": {
            "total_letters": n,
            "top_letters": sorted_obs[:5],
            "index_of_coincidence": ic,
            "best_caesar_shift": best_shift
        }
    }"""

new_stat_fallback = """def statistical_fallback_guess(ciphertext: str) -> Dict[str, Any]:
    \"\"\"Fallback statistical analysis when brute-force dictionary validation yields zero matches.\"\"\"
    letters = [c.upper() for c in ciphertext if c.isalpha()]
    n = len(letters)

    if n < 5:
        return {
            "guess": "Insufficient Data",
            "confidence": "Low",
            "reasoning": "Text contains fewer than 5 alphabetic characters. Statistical analysis requires more text.",
            "details": {}
        }

    counts: Dict[str, int] = {}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1

    sorted_obs = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    chi2_shifts = {s: compute_chi_squared(counts, n, shift=s) for s in range(26)}
    sorted_shifts = sorted(chi2_shifts.items(), key=lambda x: x[1])
    best_shift, min_chi2 = sorted_shifts[0]
    second_best_shift, second_min_chi2 = sorted_shifts[1]

    ratio = min_chi2 / second_min_chi2 if second_min_chi2 > 0 else 1.0
    ic = compute_index_of_coincidence(counts, n)

    if best_shift == 0 and ratio <= 0.70:
        guess = "Transposition (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Unshifted letter frequencies match standard English (Shift 0 Chi2 = {min_chi2:.2f}, ratio = {ratio:.2f}). "
            f"Letters were rearranged rather than substituted."
        )
    elif best_shift != 0 and ratio <= 0.70:
        guess = f"Caesar Cipher (Shift = {best_shift}) (Statistical Fallback)"
        confidence = "Medium (Statistical)"
        reasoning = (
            f"Frequency distribution matches standard English after a shift of {best_shift} position(s) "
            f"(Chi2 = {min_chi2:.2f}, ratio = {ratio:.2f})."
        )
    elif n >= 20 and (ic >= 0.045 or (sorted_obs[0][1] / n) >= 0.09):
        guess = "Monoalphabetic Substitution (Statistical Fallback)"
        confidence = "Low-Medium (Statistical)"
        reasoning = (
            f"Frequency distribution is skewed like English (IC = {ic:.4f}, top letter '{sorted_obs[0][0]}' = {sorted_obs[0][1]/n*100:.1f}%), "
            f"but no single Caesar shift fits."
        )
    elif n < 20 and (sorted_obs[0][1] / n) >= 0.15:
        guess = "Monoalphabetic Substitution (Statistical Fallback)"
        confidence = "Low (Statistical)"
        reasoning = (
            f"Letter distribution shows high dominance (top letter '{sorted_obs[0][0]}' = {sorted_obs[0][1]/n*100:.1f}%). "
            f"Note: Index of Coincidence is unreliable for text under 20 letters."
        )
    else:
        guess = "Substitution or Complex Cipher (Statistical Fallback)"
        confidence = "Low (Statistical)"
        if n < 20:
            reasoning = "Flat letter distribution across short text (IC unreliable for text under 20 letters)."
        else:
            reasoning = f"Flat letter distribution (Index of Coincidence = {ic:.4f}). Likely polyalphabetic or complex cipher."

    ic_detail = f"{ic:.4f} (unreliable for text < 20 letters)" if n < 20 else ic

    return {
        "guess": guess,
        "confidence": confidence,
        "reasoning": reasoning,
        "details": {
            "total_letters": n,
            "top_letters": sorted_obs[:5],
            "index_of_coincidence": ic_detail,
            "best_caesar_shift": best_shift
        }
    }"""

if old_stat_fallback in code:
    code = code.replace(old_stat_fallback, new_stat_fallback)

# 3. Update brute_force_columnar to use check_with_padding_strip
old_columnar = """def brute_force_columnar(ciphertext: str, dict_set: Set[str], wordlist: List[str]) -> List[Dict[str, Any]]:
    \"\"\"5. Columnar Transposition: try cols 2-7 permutations and keyword derivations.\"\"\"
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
                decrypted = columnar_transposition_decrypt(ciphertext, perm)
                meaningful, score, found_words = is_meaningful(decrypted, dict_set)
                if meaningful:
                    matches.append({
                        "cipher": "Columnar Transposition",
                        "params": f"Cols = {cols}, Perm = {perm}",
                        "plaintext": decrypted,
                        "score": score,
                        "rank_tier": 1
                    })

    # Keywords from wordlist for larger text / keywords
    for word in wordlist:
        perm = derive_perm_from_key(word)
        if perm and len(perm) > 1 and len(perm) <= n and perm not in seen_perms:
            seen_perms.add(perm)
            decrypted = columnar_transposition_decrypt(ciphertext, perm)
            meaningful, score, found_words = is_meaningful(decrypted, dict_set)
            if meaningful:
                matches.append({
                    "cipher": "Columnar Transposition",
                    "params": f"Keyword = '{word.upper()}', Perm = {perm}",
                    "plaintext": decrypted,
                    "score": score,
                    "rank_tier": 1
                })

    return matches"""

new_columnar = """def brute_force_columnar(ciphertext: str, dict_set: Set[str], wordlist: List[str]) -> List[Dict[str, Any]]:
    \"\"\"5. Columnar Transposition: try cols 2-7 permutations and keyword derivations, with trailing padding stripping.\"\"\"
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
                meaningful, score, found_words, clean_pt, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
                if meaningful:
                    pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                    matches.append({
                        "cipher": "Columnar Transposition",
                        "params": f"Cols = {cols}, Perm = {perm}{pad_note}",
                        "plaintext": clean_pt,
                        "score": score,
                        "rank_tier": 1
                    })

    # Keywords from wordlist for larger text / keywords
    for word in wordlist:
        perm = derive_perm_from_key(word)
        if perm and len(perm) > 1 and len(perm) <= n and perm not in seen_perms:
            seen_perms.add(perm)
            raw_decrypted = columnar_transposition_decrypt(ciphertext, perm)
            meaningful, score, found_words, clean_pt, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
            if meaningful:
                pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                matches.append({
                    "cipher": "Columnar Transposition",
                    "params": f"Keyword = '{word.upper()}', Perm = {perm}{pad_note}",
                    "plaintext": clean_pt,
                    "score": score,
                    "rank_tier": 1
                })

    return matches"""

if old_columnar in code:
    code = code.replace(old_columnar, new_columnar)

# 4. Update brute_force_route to use check_with_padding_strip
old_route = """def brute_force_route(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    \"\"\"7. Route Cipher: try small grid dimensions and standard read-out patterns.\"\"\"
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
                    decrypted = route_cipher_decrypt(ciphertext, r, c, pat)
                    meaningful, score, found_words = is_meaningful(decrypted, dict_set)
                    if meaningful:
                        matches.append({
                            "cipher": "Route Cipher",
                            "params": f"Grid = {r}x{c}, Pattern = {pat}",
                            "plaintext": decrypted,
                            "score": score,
                            "rank_tier": 1
                        })

    return matches"""

new_route = """def brute_force_route(ciphertext: str, dict_set: Set[str]) -> List[Dict[str, Any]]:
    \"\"\"7. Route Cipher: try small grid dimensions and standard read-out patterns with trailing padding stripping.\"\"\"
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
                    meaningful, score, found_words, clean_pt, stripped_cnt, stripped_chars = check_with_padding_strip(raw_decrypted, dict_set)
                    if meaningful:
                        pad_note = f" (trailing padding '{stripped_chars}' removed)" if stripped_cnt > 0 else ""
                        matches.append({
                            "cipher": "Route Cipher",
                            "params": f"Grid = {r}x{c}, Pattern = {pat}{pad_note}",
                            "plaintext": clean_pt,
                            "score": score,
                            "rank_tier": 1
                        })

    return matches"""

if old_route in code:
    code = code.replace(old_route, new_route)

with open("cipher_toolkit.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Applied updates successfully.")
