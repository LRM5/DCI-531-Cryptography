import sys
from AES_impl import decrypt_ecb

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 aesdecrypt.py <hex_key> <hex_ciphertext>")
        sys.exit(1)

    hex_key = sys.argv[1]
    hex_ciphertext = sys.argv[2]

    # Convert hex key and ciphertext to bytes
    key_bytes = bytes.fromhex(hex_key)
    ciphertext_bytes = bytes.fromhex(hex_ciphertext)

    # Decrypt
    plaintext_bytes = decrypt_ecb(ciphertext_bytes, key_bytes)

    # Print the recovered plaintext (UTF-8)
    print(plaintext_bytes.decode('utf-8'))

if __name__ == "__main__":
    main()
