#!/usr/bin/env python3

# aestest.py - Demonstrates the AES-128 implementation.
#  1) Generates a random 16-byte key.
#  2) Prints that key in hex.
#  3) Calls aesencrypt.py with the key + plaintext.
#  4) Prints the resulting ciphertext in hex.
#  5) Calls aesdecrypt.py with the key + ciphertext.
#  6) Prints the recovered plaintext.

import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        # Either prompt or instruct usage
        print("Usage: python3 aestest.py <plaintext>")
        sys.exit(1)
    plaintext = sys.argv[1]

    # Generate a random 128-bit key
    key = os.urandom(16)
    hex_key = key.hex()

    print(f"Generated Key (hex): {hex_key}")

    # Call aesencrypt.py
    encrypt_cmd = ["python3", "aesencrypt.py", hex_key, plaintext]
    result_enc = subprocess.run(encrypt_cmd, capture_output=True, text=True)
    ciphertext_hex = result_enc.stdout.strip()

    print(f"Ciphertext (hex): {ciphertext_hex}")

    # Call aesdecrypt.py
    decrypt_cmd = ["python3", "aesdecrypt.py", hex_key, ciphertext_hex]
    result_dec = subprocess.run(decrypt_cmd, capture_output=True, text=True)
    recovered_plaintext = result_dec.stdout.strip()

    print(f"Recovered Plaintext: {recovered_plaintext}")

if __name__ == "__main__":
    main()