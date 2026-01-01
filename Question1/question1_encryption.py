"""
HIT137 – Group Assignment 2
Question 1: Text Encryption / Decryption / Verification
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "raw_text.txt"
ENC_FILE = BASE_DIR / "encrypted_text.txt"
DEC_FILE = BASE_DIR / "decrypted_text.txt"


def shift_letter(ch: str, base: str, amount: int) -> str:
    """Shift a letter by amount with wrap-around inside alphabet."""
    return chr(ord(base) + ((ord(ch) - ord(base) + amount) % 26))


def rule_code(ch: str) -> int:
    """
    Identify which rule applies to the ORIGINAL character.
    0 = lowercase a-m
    1 = lowercase n-z
    2 = uppercase A-M
    3 = uppercase N-Z
    4 = other (unchanged)
    """
    if "a" <= ch <= "m":
        return 0
    if "n" <= ch <= "z":
        return 1
    if "A" <= ch <= "M":
        return 2
    if "N" <= ch <= "Z":
        return 3
    return 4


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    # Lowercase letters
    if "a" <= ch <= "z":
        if ch <= "m":
            return shift_letter(ch, "a", shift1 * shift2)         # forward
        return shift_letter(ch, "a", -(shift1 + shift2))          # backward

    # Uppercase letters
    if "A" <= ch <= "Z":
        if ch <= "M":
            return shift_letter(ch, "A", -shift1)                 # backward
        return shift_letter(ch, "A", shift2 ** 2)                 # forward (shift2 squared)

    # Other characters unchanged
    return ch


def decrypt_char(enc_ch: str, code: int, shift1: int, shift2: int) -> str:
    """Decrypt one character using the ORIGINAL rule code (stored in memory)."""
    if code == 0:   # was lowercase a-m, forward by shift1*shift2
        return shift_letter(enc_ch, "a", -(shift1 * shift2))
    if code == 1:   # was lowercase n-z, backward by shift1+shift2
        return shift_letter(enc_ch, "a", (shift1 + shift2))
    if code == 2:   # was uppercase A-M, backward by shift1
        return shift_letter(enc_ch, "A", shift1)
    if code == 3:   # was uppercase N-Z, forward by shift2^2
        return shift_letter(enc_ch, "A", -(shift2 ** 2))
    return enc_ch   # other chars unchanged


def get_shift(prompt: str) -> int:
    """Get a shift value between 0 and 9 inclusive."""
    while True:
        try:
            n = int(input(prompt))
        except ValueError:
            print("Please enter an integer from 0 to 9.")
            continue
        if 0 <= n <= 9:
            return n
        print("Shift must be between 0 and 9 (inclusive).")


def verify_decryption(raw_text: str, decrypted_text: str) -> None:
    if raw_text == decrypted_text:
        print("Verification: SUCCESS ✅ Decrypted text matches the original.")
    else:
        print("Verification: FAIL ❌ Decrypted text does NOT match the original.")
        # show first mismatch for debugging
        limit = min(len(raw_text), len(decrypted_text))
        for i in range(limit):
            if raw_text[i] != decrypted_text[i]:
                print(f"First difference at index {i}: original={repr(raw_text[i])} decrypted={repr(decrypted_text[i])}")
                break
        else:
            if len(raw_text) != len(decrypted_text):
                print(f"Files differ in length: original={len(raw_text)} decrypted={len(decrypted_text)}")


def main() -> None:
    if not RAW_FILE.exists():
        print("ERROR: raw_text.txt not found in the same folder as this script.")
        return

    shift1 = get_shift("Enter shift1 (0-9): ")
    shift2 = get_shift("Enter shift2 (0-9): ")

    raw_text = RAW_FILE.read_text(encoding="utf-8")

    # Record the rule used for each ORIGINAL character (in memory only)
    codes = [rule_code(ch) for ch in raw_text]

    # Encrypt raw -> encrypted_text.txt
    encrypted_text = "".join(encrypt_char(ch, shift1, shift2) for ch in raw_text)
    ENC_FILE.write_text(encrypted_text, encoding="utf-8")

    # Decrypt encrypted -> decrypted_text.txt (using the stored codes)
    decrypted_text = "".join(
        decrypt_char(enc_ch, code, shift1, shift2)
        for enc_ch, code in zip(encrypted_text, codes)
    )
    DEC_FILE.write_text(decrypted_text, encoding="utf-8")

    # Verify
    verify_decryption(raw_text, decrypted_text)


if __name__ == "__main__":
    main()
