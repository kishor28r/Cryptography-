#!/usr/bin/env python3
"""
Classical Cipher Toolkit
========================
A menu-driven Python program implementing classic cryptographic algorithms:
- Caesar Cipher (Shift 0–25)
- Vigenère Cipher (Keyword String)
- Rail Fence Cipher (Rails >= 2)
Bonus Cryptanalysis Feature: Letter-frequency based cipher type guessing.

Author: Antigravity AI
File: cipher_toolkit.py
"""

import sys
import math
import unittest
from typing import Optional, Tuple, Dict, Any, List

# Standard English letter frequencies (proportions)
ENGLISH_FREQS: Dict[str, float] = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}


# =====================================================================
# 1. CIPHER ALGORITHMS (Encrypt / Decrypt Pairs)
# =====================================================================

def caesar_encrypt(text: str, shift: int) -> str:
    """
    Encrypt text using Caesar cipher with given integer shift (0-25).
    Preserves letter case and leaves non-alphabet characters unchanged.
    """
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
    """
    Decrypt text using Caesar cipher with given integer shift (0-25).
    Preserves letter case and leaves non-alphabet characters unchanged.
    """
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text: str, key: str) -> str:
    """
    Encrypt text using Vigenère cipher with given keyword string.
    Preserves letter case and leaves non-alphabet characters unchanged.
    Non-alphabet characters do not advance key index.
    """
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
    """
    Decrypt text using Vigenère cipher with given keyword string.
    Preserves letter case and leaves non-alphabet characters unchanged.
    Non-alphabet characters do not advance key index.
    """
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


def rail_fence_encrypt(text: str, rails: int) -> str:
    """
    Encrypt text using Rail Fence cipher with given integer number of rails.
    Arranges all characters along a zigzag rail matrix and reads off row by row.
    """
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
    """
    Decrypt text using Rail Fence cipher with given integer number of rails.
    Reconstructs the zigzag pattern grid to retrieve original character positions.
    """
    if rails <= 1 or rails >= len(ciphertext) or not ciphertext:
        return ciphertext

    n = len(ciphertext)
    # Mark positions in zigzag grid
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

    # Fill grid with ciphertext characters row by row
    idx = 0
    for r in range(rails):
        for c in range(n):
            if grid[r][c] == '*' and idx < n:
                grid[r][c] = ciphertext[idx]
                idx += 1

    # Read grid in zigzag pattern
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
# 3. BONUS CRYPTANALYSIS (Option 7: Guess Cipher Type)
# =====================================================================

def compute_chi_squared(counts: Dict[str, int], total_letters: int, shift: int = 0) -> float:
    """
    Compute Chi-Squared distance comparing ciphertext letter frequency distribution
    shifted by 'shift' positions against standard English letter frequencies.
    Uses expected count smoothing for low-frequency letters.
    """
    if total_letters == 0:
        return float('inf')

    chi_sq = 0.0
    for i in range(26):
        # English letter at position i
        eng_char = chr(ord('A') + i)
        expected = total_letters * ENGLISH_FREQS[eng_char]
        expected_smoothed = max(expected, 0.25)

        # Observed letter in ciphertext shifted back by 'shift'
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


def guess_cipher_type(ciphertext: str) -> Dict[str, Any]:
    """
    Analyze ciphertext letter frequency distribution to guess whether the cipher is:
    - Transposition (letters unchanged, just reordered)
    - Caesar Cipher (letters uniformly shifted)
    - Substitution (monoalphabetic substitution, skewed English-like shape without single shift match)

    Returns a dictionary with result details including guess, confidence, and reasoning.
    """
    letters = [c.upper() for c in ciphertext if c.isalpha()]
    n = len(letters)

    if n < 5:
        return {
            "guess": "Insufficient Data",
            "confidence": "Low",
            "reasoning": "Text contains fewer than 5 alphabetic characters. Frequency analysis requires more text.",
            "details": {}
        }

    # Count letter occurrences
    counts: Dict[str, int] = {}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1

    # Sorted observed frequencies
    sorted_obs = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # Calculate Chi-Squared distance for all 26 Caesar shifts
    chi2_shifts = {}
    for s in range(26):
        chi2_shifts[s] = compute_chi_squared(counts, n, shift=s)

    sorted_shifts = sorted(chi2_shifts.items(), key=lambda x: x[1])
    best_shift, min_chi2 = sorted_shifts[0]
    second_best_shift, second_min_chi2 = sorted_shifts[1]

    ratio = min_chi2 / second_min_chi2 if second_min_chi2 > 0 else 1.0
    normalized_min_chi2 = min_chi2 / n

    # Index of Coincidence (IC)
    ic = compute_index_of_coincidence(counts, n)

    # Most common letters in ciphertext
    top_obs_letters = [item[0] for item in sorted_obs[:5]]

    # Transposition Test:
    # If shift 0 is the best shift and significantly outclasses other shifts,
    # the unshifted letter frequencies match standard English directly.
    if best_shift == 0 and ratio <= 0.70:
        guess = "Transposition"
        confidence = "High" if ratio <= 0.40 else "Medium"
        reasoning = (
            f"Letter frequency distribution matches standard English without any shift "
            f"(Shift 0 Chi-Squared = {min_chi2:.2f}, ratio to 2nd best = {ratio:.2f}). "
            f"Top letters ({', '.join(top_obs_letters[:3])}) remain unchanged, indicating letter reordering."
        )
        decrypted_preview = None

    # Caesar Cipher Test:
    # If a non-zero shift is the best shift and significantly outclasses other shifts
    elif best_shift != 0 and ratio <= 0.70:
        guess = "Caesar"
        confidence = "High" if ratio <= 0.40 else "Medium"
        estimated_shift_key = best_shift
        reasoning = (
            f"Letter frequency distribution matches standard English after a single uniform shift of {best_shift} position(s) "
            f"(Shift {best_shift} Chi-Squared = {min_chi2:.2f}, ratio to 2nd best = {ratio:.2f}). "
            f"Estimated Caesar shift key: {estimated_shift_key}."
        )
        decrypted_preview = caesar_decrypt(ciphertext, estimated_shift_key)

    # Monoalphabetic Substitution Test:
    # If no single shift stands out (ratio > 0.70), but distribution has an English-like shape (IC >= 0.045 or dominant top letter)
    elif ic >= 0.045 or (sorted_obs[0][1] / n) >= 0.09:
        guess = "Substitution"
        confidence = "High" if ic >= 0.055 else "Medium"
        reasoning = (
            f"Frequency distribution is non-uniform and skewed like English (Index of Coincidence = {ic:.4f}, "
            f"top letter '{sorted_obs[0][0]}' = {sorted_obs[0][1]/n*100:.1f}%), "
            f"but no single uniform Caesar shift fits (best shift Chi-Squared ratio = {ratio:.2f})."
        )
        decrypted_preview = None

    else:
        guess = "Substitution (Polyalphabetic or Flat Distribution)"
        confidence = "Low-Medium"
        reasoning = (
            f"Letter distribution is flatter than standard monoalphabetic English text (Index of Coincidence = {ic:.4f}). "
            f"Likely a polyalphabetic substitution cipher (e.g. Vigenère) or small/atypical text sample."
        )
        decrypted_preview = None

    return {
        "guess": guess,
        "confidence": confidence,
        "reasoning": reasoning,
        "details": {
            "total_letters": n,
            "top_letters": sorted_obs[:5],
            "index_of_coincidence": ic,
            "best_caesar_shift": best_shift,
            "best_chi2": min_chi2,
            "chi2_ratio": ratio,
            "decrypted_preview": decrypted_preview
        }
    }


# =====================================================================
# 4. CLASSICAL CIPHER TOOLKIT APPLICATION CLASS
# =====================================================================

class ClassicalCipherToolkit:
    """Main Application Controller for Classical Cipher Toolkit CLI."""

    CIPHER_NAMES = {
        1: "Caesar Cipher",
        2: "Vigenère Cipher",
        3: "Rail Fence Cipher"
    }

    def __init__(self):
        self.active_cipher_id: int = 1  # Default: Caesar
        self.keys: Dict[int, Any] = {
            1: None,  # Caesar key (int 0-25)
            2: None,  # Vigenère key (str)
            3: None   # Rail Fence key (int >= 2)
        }
        self.last_result: Optional[Dict[str, Any]] = None

    @property
    def active_cipher_name(self) -> str:
        return self.CIPHER_NAMES[self.active_cipher_id]

    @property
    def active_key(self) -> Any:
        return self.keys[self.active_cipher_id]

    def display_header(self) -> None:
        """Print main application header and status bar."""
        print("\n" + "=" * 58)
        print("             CLASSICAL CIPHER TOOLKIT             ")
        print("=" * 58)
        print(f" Active Cipher : {self.active_cipher_name}")
        key_str = str(self.active_key) if self.active_key is not None else "[NOT SET]"
        print(f" Current Key   : {key_str}")
        print("-" * 58)

    def display_menu(self) -> None:
        """Print main menu options."""
        print(" 1. Encrypt")
        print(" 2. Decrypt")
        print(" 3. Select Cipher")
        print(" 4. Enter Key")
        print(" 5. Display Result")
        print(" 6. Exit")
        print(" 7. Guess Cipher Type")
        print("=" * 58)

    def select_cipher_menu(self) -> None:
        """Menu option 3: Select active cipher."""
        print("\n--- Select Active Cipher ---")
        for num, name in self.CIPHER_NAMES.items():
            current_tag = " (Active)" if num == self.active_cipher_id else ""
            print(f" {num}. {name}{current_tag}")

        choice_str = input("Select cipher (1-3): ").strip()
        if choice_str in ("1", "2", "3"):
            new_id = int(choice_str)
            self.active_cipher_id = new_id
            print(f"\n[+] Active cipher set to: {self.active_cipher_name}")
            if self.active_key is None:
                print(f"[!] Key is not set for {self.active_cipher_name}. Please use Option 4 to enter key.")
            else:
                print(f"[i] Current Key for {self.active_cipher_name}: {self.active_key}")
        else:
            print("\n[-] Invalid selection! Cipher selection unchanged.")

    def enter_key_menu(self) -> bool:
        """Menu option 4: Enter key for active cipher with input validation."""
        print(f"\n--- Enter Key for {self.active_cipher_name} ---")

        if self.active_cipher_id == 1:
            # Caesar Cipher
            print("Requirement: Key must be an integer shift between 0 and 25.")
            key_input = input("Enter Caesar shift key (0-25): ")
            valid, msg, val = validate_caesar_key(key_input)
            if valid:
                self.keys[1] = val
                print(f"[+] Key updated successfully: {val}")
                return True
            else:
                print(f"[-] {msg}")
                return False

        elif self.active_cipher_id == 2:
            # Vigenère Cipher
            print("Requirement: Key must be a non-empty keyword string (e.g. 'KEY' or 'LEMON').")
            key_input = input("Enter Vigenère keyword key: ")
            valid, msg, val = validate_vigenere_key(key_input)
            if valid:
                self.keys[2] = val
                print(f"[+] Key updated successfully: '{val}'")
                return True
            else:
                print(f"[-] {msg}")
                return False

        elif self.active_cipher_id == 3:
            # Rail Fence Cipher
            print("Requirement: Key must be an integer number of rails (>= 2).")
            key_input = input("Enter number of rails (>= 2): ")
            valid, msg, val = validate_rail_fence_key(key_input)
            if valid:
                self.keys[3] = val
                print(f"[+] Key updated successfully: {val} rails")
                return True
            else:
                print(f"[-] {msg}")
                return False

        return False

    def ensure_key_set(self) -> bool:
        """Ensure active cipher has a key configured before encrypting/decrypting."""
        if self.active_key is None:
            print(f"\n[!] Key is not configured for {self.active_cipher_name}.")
            print("Please set the key first:")
            return self.enter_key_menu()
        return True

    def run_encrypt(self) -> None:
        """Menu option 1: Encrypt plaintext and store result."""
        if not self.ensure_key_set():
            return

        print(f"\n--- Encrypt using {self.active_cipher_name} ---")
        plaintext = input("Enter Plaintext: ")
        if not plaintext:
            print("[-] Warning: Plaintext was empty.")

        if self.active_cipher_id == 1:
            ciphertext = caesar_encrypt(plaintext, self.active_key)
        elif self.active_cipher_id == 2:
            ciphertext = vigenere_encrypt(plaintext, self.active_key)
        elif self.active_cipher_id == 3:
            ciphertext = rail_fence_encrypt(plaintext, self.active_key)

        self.last_result = {
            "operation": "Encrypt",
            "cipher": self.active_cipher_name,
            "key": self.active_key,
            "input_text": plaintext,
            "output_text": ciphertext
        }

        print("\n" + "-" * 40)
        print(f"[+] Encryption Successful!")
        print(f"Ciphertext: {ciphertext}")
        print("-" * 40)

    def run_decrypt(self) -> None:
        """Menu option 2: Decrypt ciphertext and store result."""
        if not self.ensure_key_set():
            return

        print(f"\n--- Decrypt using {self.active_cipher_name} ---")
        ciphertext = input("Enter Ciphertext: ")
        if not ciphertext:
            print("[-] Warning: Ciphertext was empty.")

        if self.active_cipher_id == 1:
            plaintext = caesar_decrypt(ciphertext, self.active_key)
        elif self.active_cipher_id == 2:
            plaintext = vigenere_decrypt(ciphertext, self.active_key)
        elif self.active_cipher_id == 3:
            plaintext = rail_fence_decrypt(ciphertext, self.active_key)

        self.last_result = {
            "operation": "Decrypt",
            "cipher": self.active_cipher_name,
            "key": self.active_key,
            "input_text": ciphertext,
            "output_text": plaintext
        }

        print("\n" + "-" * 40)
        print(f"[+] Decryption Successful!")
        print(f"Plaintext: {plaintext}")
        print("-" * 40)

    def display_last_result(self) -> None:
        """Menu option 5: Display last stored result."""
        print("\n--- Stored Result ---")
        if not self.last_result:
            print("[i] No stored result yet. Perform an Encryption or Decryption operation first.")
            return

        res = self.last_result
        print(f" Operation   : {res['operation']}")
        print(f" Cipher Used : {res['cipher']}")
        print(f" Key Used    : {res['key']}")
        print(f" Input Text  : {res['input_text']}")
        print(f" Output Text : {res['output_text']}")

    def run_cryptanalysis(self) -> None:
        """Menu option 7: Guess Cipher Type using letter frequency analysis."""
        print("\n--- Bonus: Guess Cipher Type ---")
        ciphertext = input("Enter Ciphertext to analyze: ")

        if not ciphertext.strip():
            print("[-] Error: Input ciphertext cannot be empty.")
            return

        res = guess_cipher_type(ciphertext)

        print("\n" + "=" * 55)
        print("              CRYPTANALYSIS REPORT              ")
        print("=" * 55)
        print(f" Analyzed Ciphertext : \"{ciphertext}\"")
        details = res.get("details", {})
        if details.get("total_letters"):
            print(f" Letters Counted     : {details['total_letters']}")
            top_str = ", ".join([f"{char} ({cnt})" for char, cnt in details['top_letters']])
            print(f" Top Frequencies     : {top_str}")

        print("-" * 55)
        print(f" Guessed Cipher Type : {res['guess']}")
        print(f" Confidence Level    : {res['confidence']}")
        print(f" Reasoning           : {res['reasoning']}")

        if details.get("decrypted_preview"):
            print("-" * 55)
            print(f" Decrypted Preview   : {details['decrypted_preview']}")
        print("=" * 55)

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
                    print("\n[+] Exiting Classical Cipher Toolkit. Goodbye!")
                    sys.exit(0)
                elif choice == "7":
                    self.run_cryptanalysis()
                else:
                    print("\n[-] Invalid option! Please select a number from 1 to 7.")

                input("\nPress Enter to continue...")

            except (KeyboardInterrupt, EOFError):
                print("\n\n[+] Program interrupted. Goodbye!")
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

    def test_validations(self):
        self.assertTrue(validate_caesar_key("12")[0])
        self.assertFalse(validate_caesar_key("30")[0])
        self.assertTrue(validate_vigenere_key("SECRET")[0])
        self.assertFalse(validate_vigenere_key("123")[0])
        self.assertTrue(validate_rail_fence_key("3")[0])
        self.assertFalse(validate_rail_fence_key("1")[0])

    def test_cryptanalysis(self):
        text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND FEELS HAPPY IN ENGLISH TEXT SAMPLE FOR TESTING CRYPTANALYSIS."
        rf = rail_fence_encrypt(text, 3)
        caes = caesar_encrypt(text, 11)
        sub_map = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "QWERTYUIOPASDFGHJKLZXCVBNM")
        sub = text.upper().translate(sub_map)

        res_rf = guess_cipher_type(rf)
        res_caes = guess_cipher_type(caes)
        res_sub = guess_cipher_type(sub)

        self.assertEqual(res_rf["guess"], "Transposition")
        self.assertEqual(res_caes["guess"], "Caesar")
        self.assertEqual(res_caes["details"]["best_caesar_shift"], 11)
        self.assertEqual(res_sub["guess"], "Substitution")


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
