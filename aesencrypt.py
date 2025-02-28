#!/usr/bin/env python3

# aesencrypt.py - Encrypts the given plaintext with the provided key (AES-128, ECB).

import sys
from AES_impl import encrypt_ecb

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 aesencrypt.py <hex_key> <plaintext>")
        sys.exit(1)

    hex_key = sys.argv[1]
    plaintext = sys.argv[2]

    # Convert hex key string to bytes
    key_bytes = bytes.fromhex(hex_key)
    # Convert plaintext to bytes (UTF-8)
    plaintext_bytes = plaintext.encode('utf-8')

    # Encrypt
    ciphertext = encrypt_ecb(plaintext_bytes, key_bytes)

    # Print ciphertext in hex
    print(ciphertext.hex())

if __name__ == "__main__":
    main()