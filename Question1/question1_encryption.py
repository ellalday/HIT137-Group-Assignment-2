"""
HIT137 – Assignment 2
Question 1: Text Encryption / Decryption / Verification

Program requirements:
- Prompt user for shift1 and shift2
- Encrypt raw_text.txt -> encrypted_text.txt using given rules
- Decrypt encrypted_text.txt -> decrypted_text.txt
- Verify decrypted_text.txt matches raw_text.txt and print result

Notes:
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional, Tuple
import argparse
import sys


# ---------------------------
# Configuration (file paths)
# ---------------------------

BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "raw_text.txt"
ENC_FILE = BASE_DIR / "encrypted_text.txt"
DEC_FILE = BASE_DIR / "decrypted_text.txt"


# ---------------------------
# Data container
# ---------------------------

@dataclass(frozen=True, slots=True)
class Shifts:
    """Holds user-provided shift values."""
    shift1: int
    shift2: int

    @property
    def lower_first_half_forward(self) -> int:
        # a-m forward by shift1 * shift2
        return self.shift1 * self.shift2

    @property
    def lower_second_half_backward(self) -> int:
        # n-z backward by shift1 + shift2
        return self.shift1 + self.shift2

    @property
    def upper_first_half_backward(self) -> int:
        # A-M backward by shift1
        return self.shift1

    @property
    def upper_second_half_forward(self) -> int:
        # N-Z forward by shift2^2
        return self.shift2 ** 2


# ---------------------------
# Core helpers
# ---------------------------

def _shift_letter(ch: str, base: str, amount: int) -> str:
    """
    Shift a single letter by amount with wrap-around.
    base must be 'a' or 'A'. amount can be negative.
    """
    idx = ord(ch) - ord(base)          # 0..25
    idx2 = (idx + amount) % 26         # wrap-around
    return chr(ord(base) + idx2)


def encrypt_char(ch: str, s: Shifts) -> str:
    """Encrypt exactly according to the assignment."""
    # Lowercase
    if "a" <= ch <= "m":
        return _shift_letter(ch, "a", s.lower_first_half_forward)
    if "n" <= ch <= "z":
        return _shift_letter(ch, "a", -s.lower_second_half_backward)

    # Uppercase
    if "A" <= ch <= "M":
        return _shift_letter(ch, "A", -s.upper_first_half_backward)
    if "N" <= ch <= "Z":
        return _shift_letter(ch, "A", s.upper_second_half_forward)

    # Other characters unchanged
    return ch


def build_decrypt_map(s: Shifts) -> Dict[str, str]:
    """
    Build a robust inverse mapping for letters:
        encrypted_letter -> original_letter

    This avoids edge cases where encryption wrap-around can move letters
    across the a-m / n-z (or A-M / N-Z) boundary.
    """
    decrypt_map: Dict[str, str] = {}

    # Lowercase letters
    for code in range(ord("a"), ord("z") + 1):
        original = chr(code)
        encrypted = encrypt_char(original, s)
        decrypt_map[encrypted] = original

    # Uppercase letters
    for code in range(ord("A"), ord("Z") + 1):
        original = chr(code)
        encrypted = encrypt_char(original, s)
        decrypt_map[encrypted] = original

    return decrypt_map


def decrypt_char(ch: str, decrypt_map: Dict[str, str]) -> str:
    """Decrypt using the inverse mapping. Non-letters are unchanged."""
    return decrypt_map.get(ch, ch)


# ---------------------------
# File processing (streaming)
# ---------------------------

def _read_lines(path: Path) -> Iterator[str]:
    """Yield lines from a text file (UTF-8)."""
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield line


def _write_lines(path: Path, lines: Iterable[str]) -> None:
    """Write lines to a text file (UTF-8)."""
    with path.open("w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)


def encrypt_file(s: Shifts, src: Path = RAW_FILE, dst: Path = ENC_FILE) -> None:
    """Encrypt src -> dst."""
    def gen() -> Iterator[str]:
        for line in _read_lines(src):
            yield "".join(encrypt_char(ch, s) for ch in line)

    _write_lines(dst, gen())


def decrypt_file(s: Shifts, src: Path = ENC_FILE, dst: Path = DEC_FILE) -> None:
    """Decrypt src -> dst."""
    decrypt_map = build_decrypt_map(s)

    def gen() -> Iterator[str]:
        for line in _read_lines(src):
            yield "".join(decrypt_char(ch, decrypt_map) for ch in line)

    _write_lines(dst, gen())


# ---------------------------
# Verification (with helpful diff)
# ---------------------------

def _first_difference(a: str, b: str) -> Optional[Tuple[int, str, str]]:
    """
    Return (index, a_char, b_char) for first difference, or None if identical.
    """
    limit = min(len(a), len(b))
    for i in range(limit):
        if a[i] != b[i]:
            return i, a[i], b[i]
    if len(a) != len(b):
        # difference occurs at end-of-shorter
        i = limit
        a_char = a[i] if i < len(a) else "<EOF>"
        b_char = b[i] if i < len(b) else "<EOF>"
        return i, a_char, b_char
    return None


def verify_files(original: Path = RAW_FILE, decrypted: Path = DEC_FILE) -> bool:
    """
    Compare original and decrypted files.
    Prints a clear message, including the first mismatch position if any.
    """
    original_text = original.read_text(encoding="utf-8")
    decrypted_text = decrypted.read_text(encoding="utf-8")

    diff = _first_difference(original_text, decrypted_text)
    if diff is None:
        print("Decryption successful: decrypted text matches original.")
        return True

    i, a_ch, b_ch = diff
    print("Decryption failed: decrypted text does NOT match original.")
    print(f"First difference at character index {i}: original={repr(a_ch)} decrypted={repr(b_ch)}")
    return False


# ---------------------------
# Input handling
# ---------------------------

def _prompt_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer (e.g., 3, -2).")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """
    Optional CLI arguments (for convenience).
    If not provided, we still prompt the user (to match the brief).
    """
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--shift1", type=int, default=None, help="Shift value 1 (integer)")
    parser.add_argument("--shift2", type=int, default=None, help="Shift value 2 (integer)")
    return parser.parse_args(argv)


# ---------------------------
# Main
# ---------------------------

def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not RAW_FILE.exists():
        print(f"ERROR: Missing input file: {RAW_FILE}")
        print("Create raw_text.txt inside question_1 and run again.")
        return 1

    # Requirement: prompt user for shift1 and shift2.
    # We still prompt if they weren't provided via CLI.
    shift1 = args.shift1 if args.shift1 is not None else _prompt_int("Enter shift1: ")
    shift2 = args.shift2 if args.shift2 is not None else _prompt_int("Enter shift2: ")
    shifts = Shifts(shift1=shift1, shift2=shift2)

    # Encrypt -> Decrypt -> Verify (automatic, as required)
    encrypt_file(shifts)
    decrypt_file(shifts)
    ok = verify_files()

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
