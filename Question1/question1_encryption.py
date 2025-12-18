def encrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'z':
        if ch <= 'm':
            return chr((ord(ch) - ord('a') + shift1 * shift2) % 26 + ord('a'))
        else:
            return chr((ord(ch) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))

    if 'A' <= ch <= 'Z':
        if ch <= 'M':
            return chr((ord(ch) - ord('A') - shift1) % 26 + ord('A'))
        else:
            return chr((ord(ch) - ord('A') + (shift2 ** 2)) % 26 + ord('A'))

    return ch


def decrypt_char(ch, shift1, shift2):
    for i in range(26):
        candidate = chr(ord('a') + i)
        if encrypt_char(candidate, shift1, shift2) == ch:
            return candidate

        candidate = chr(ord('A') + i)
        if encrypt_char(candidate, shift1, shift2) == ch:
            return candidate

    return ch


def encrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    result = "".join(encrypt_char(c, shift1, shift2) for c in text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)


def decrypt_file(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    result = "".join(decrypt_char(c, shift1, shift2) for c in text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)


def verify(shift1, shift2):
    encrypt_file("raw_text.txt", "check_encrypted.txt", shift1, shift2)
    encrypt_file("decrypted_text.txt", "check_reencrypted.txt", shift1, shift2)

    with open("check_encrypted.txt", "r", encoding="utf-8") as f1, \
         open("check_reencrypted.txt", "r", encoding="utf-8") as f2:
        if f1.read() == f2.read():
            print("Decryption successful: verification passed.")
        else:
            print("Decryption failed: verification failed.")


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    verify(shift1, shift2)


main()
