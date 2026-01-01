"""
HIT137 – Assignment 2
Question 1: Text Encryption / Decryption / Verification

Program requirements:
- Prompt user for shift1 and shift2 (arbitrary value between 0 - 9)
- Encrypt raw_text.txt -> encrypted_text.txt using given rules
- Decrypt encrypted_text.txt -> decrypted_text.txt
- Verify decrypted_text.txt matches raw_text.txt and print result

Outputs:
- encrypted_text.txt
- decrypted_text.txt
- encryption_mask.txt

Bug Fixes:
- Decryption errors occurred using certain values in shift1 and shift2.
- Two different letters could encrypt to the same letter, causing a collision.
- To prevent this and encryption_mask.txt file stores which rule was used for each character.
- The mask is then used in decryption to apply the correct inverse rule for each character.
"""

from pathlib import Path

# ---------------------------
# File Paths
# ---------------------------
BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "raw_text.txt"
ENC_FILE = BASE_DIR / "encrypted_text.txt"
DEC_FILE = BASE_DIR / "decrypted_text.txt"
MASK_FILE = BASE_DIR / "encryption_mask.txt"


# ---------------------------
# Helper Function: Shift Letter
# ---------------------------
def shift_letter(ch: str, base: str, amount: int) -> str:
    """Shift a letter by amount with wrap-around inside alphabet."""
    idx = ord(ch) - ord(base)
    return chr(ord(base) + ((idx + amount) % 26))


# ---------------------------
# Encryption Rule Identification
# ---------------------------
def rule_code(ch: str) -> str:
    """
    Return a single-character code describing which rule applies:
    0 = lowercase a-m
    1 = lowercase n-z
    2 = uppercase A-M
    3 = uppercase N-Z
    4 = other character (unchanged)
    """
    if "a" <= ch <= "m":
        return "0" # lowercase first half
    if "n" <= ch <= "z":
        return "1" # lowercase second half
    if "A" <= ch <= "M":
        return "2" # uppercase first half
    if "N" <= ch <= "Z":
        return "3" # uppercase second half
    return "4"     # not a letter


# ---------------------------
# Encrypt / Decrypt Each Character
# ---------------------------
def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """Encrypt one character using the assignment rules."""
    # Lowercase
    if "a" <= ch <= "m":
        return shift_letter(ch, "a", shift1 * shift2)
    if "n" <= ch <= "z":
        return shift_letter(ch, "a", -(shift1 + shift2))

    # Uppercase
    if "A" <= ch <= "M":
        return shift_letter(ch, "A", -shift1)
    if "N" <= ch <= "Z":
        return shift_letter(ch, "A", shift2 ** 2)

    # if character is not a letter, return unchanged
    return ch


def decrypt_char_using_rule(enc_ch: str, code: str, shift1: int, shift2: int) -> str:
    """
    Decrypt one character using the recorded rule code (mask).
    This prevents collisions.
    """
    if code == "0":  # lowercase a-m originally, forward by shift1*shift2 => invert by backward
        return shift_letter(enc_ch, "a", -(shift1 * shift2))

    if code == "1":  # lowercase n-z originally, backward by shift1+shift2 => invert by forward
        return shift_letter(enc_ch, "a", (shift1 + shift2))

    if code == "2":  # uppercase A-M originally, backward by shift1 => invert by forward
        return shift_letter(enc_ch, "A", shift1)

    if code == "3":  # uppercase N-Z originally, forward by shift2^2 => invert by backward
        return shift_letter(enc_ch, "A", -(shift2 ** 2))

    # code == "4" : other chars unchanged
    return enc_ch


# ---------------------------
# File operations (encrypt/decrypt whole file)
# ---------------------------
def encrypt_file(shift1: int, shift2: int) -> None:
    """
    Read raw_text.txt and write:
    - encrypted_text.txt (encrypted output)
    - encryption_mask.txt (rule codes per character)
    """
    # read the entire file as one string
    raw = RAW_FILE.read_text(encoding="utf-8")

    encrypted_chars = []
    mask_chars = []

    # loop through each character in the text
    for ch in raw:
        mask = rule_code(ch)
        enc = encrypt_char(ch, shift1, shift2)
        encrypted_chars.append(enc)
        mask_chars.append(mask)

    # join the lists into strings and write them into files
    ENC_FILE.write_text("".join(encrypted_chars), encoding="utf-8")
    MASK_FILE.write_text("".join(mask_chars), encoding="utf-8")


def decrypt_file(shift1: int, shift2: int) -> None:
    """
    Read encrypted_text.txt and encryption_mask.txt, then write decrypted_text.txt.
    """
    encrypted = ENC_FILE.read_text(encoding="utf-8")
    mask = MASK_FILE.read_text(encoding="utf-8")

    if len(encrypted) != len(mask):
        raise ValueError(
            "Mask length does not match encrypted text length. "
            "Re-run encryption to regenerate matching files."
        )

    # zip() allows loop over two strings at same time
    decrypted_chars = []
    for enc_ch, code in zip(encrypted, mask):
        decrypted_chars.append(decrypt_char_using_rule(enc_ch, code, shift1, shift2))

    DEC_FILE.write_text("".join(decrypted_chars), encoding="utf-8")


def verify_files() -> bool:
    """Compare raw_text.txt and decrypted_text.txt and print success/failure."""
    raw = RAW_FILE.read_text(encoding="utf-8")
    dec = DEC_FILE.read_text(encoding="utf-8")

    if raw == dec:
        print("Decryption successful: decrypted text matches original.")
        return True

    print("Decryption failed: decrypted text does NOT match original.")

    # Show first mismatch to help debugging
    limit = min(len(raw), len(dec))
    for i in range(limit):
        if raw[i] != dec[i]:
            print(f"First difference at index {i}: original={repr(raw[i])} decrypted={repr(dec[i])}")
            break
    else:
        if len(raw) != len(dec):
            print(f"Files differ in length: original={len(raw)} decrypted={len(dec)}")

    return False


# ---------------------------
# Main 
# ---------------------------
def main() -> None:
    if not RAW_FILE.exists():
        print(f"ERROR: Missing input file: {RAW_FILE}")
        print("Place raw_text.txt in the same folder as this script.")
        return

    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_files()


if __name__ == "__main__":
    main()