import string

ALPHABET = string.ascii_lowercase


# ---------- Caesar Cipher ----------
def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ---------- Vigenere Cipher ----------
def vigenere(text, key, decrypt=False):
    result, k = "", 0
    key = [ord(c.lower()) - 97 for c in key if c.isalpha()]
    if not key:
        raise ValueError("Key must contain at least one letter")
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            s = -key[k % len(key)] if decrypt else key[k % len(key)]
            result += chr((ord(ch) - base + s) % 26 + base)
            k += 1
        else:
            result += ch
    return result


def vigenere_encrypt(text, key):
    return vigenere(text, key, False)


def vigenere_decrypt(text, key):
    return vigenere(text, key, True)


# ---------- Substitution Cipher ----------
def make_sub_key(seed_word):
    seen = []
    for c in seed_word.lower() + ALPHABET:
        if c.isalpha() and c not in seen:
            seen.append(c)
    return "".join(seen)


def substitution(text, key, decrypt=False):
    src, dst = (key, ALPHABET) if decrypt else (ALPHABET, key)
    table = {}
    for a, b in zip(src, dst):
        table[a] = b
        table[a.upper()] = b.upper()
    return "".join(table.get(ch, ch) for ch in text)


# ---------- Atbash Cipher ----------
def atbash(text):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr(base + 25 - (ord(ch) - base))
        else:
            result += ch
    return result


# ---------- XOR + Base64 Cipher ----------
import base64


def xor_encrypt(text, key):
    data = text.encode("utf-8")
    kb = key.encode("utf-8")
    out = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))
    return base64.b64encode(out).decode("ascii")


def xor_decrypt(cipher, key):
    data = base64.b64decode(cipher)
    kb = key.encode("utf-8")
    out = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(data))
    return out.decode("utf-8")


# ---------- Menu Driven Program ----------
def main():
    while True:
        print("\n===== TEXT ENCRYPTION & DECRYPTION =====")
        print("1. Caesar Cipher")
        print("2. Vigenere Cipher")
        print("3. Substitution Cipher")
        print("4. Atbash Cipher")
        print("5. XOR + Base64 Cipher")
        print("6. Exit")
        choice = input("Select algorithm: ").strip()
        if choice == "6":
            print("Thank you!")
            break
        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid choice. Try again.")
            continue
        mode = input("Encrypt (E) or Decrypt (D)? ").strip().upper()
        if mode not in ("E", "D"):
            print("Invalid mode.")
            continue
        text = input("Enter text: ")
        try:
            if choice == "1":
                s = int(input("Enter shift (integer): "))
                out = caesar_encrypt(text, s) if mode == "E" else caesar_decrypt(text, s)
            elif choice == "2":
                k = input("Enter keyword: ")
                out = vigenere(text, k, mode == "D")
            elif choice == "3":
                k = make_sub_key(input("Enter key word: "))
                out = substitution(text, k, mode == "D")
            elif choice == "4":
                out = atbash(text)
            else:
                k = input("Enter secret key: ")
                if not k:
                    raise ValueError("Key cannot be empty")
                out = xor_encrypt(text, k) if mode == "E" else xor_decrypt(text, k)
            print("Result :", out)
        except Exception as ex:
            print("Error:", ex)


if __name__ == "__main__":
    main()
