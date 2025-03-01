import sys
from AES_impl import encrypt_ecb

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 aesencrypt.py <hex_key> <plaintext>")
        sys.exit(1)

    hex_key = sys.argv[1]
    plaintext = sys.argv[2]

   
    key_bytes = bytes.fromhex(hex_key) # Convert hex key string to bytes
    
    plaintext_bytes = plaintext.encode('utf-8') # Convert plaintext to bytes (UTF-8)

    
    ciphertext = encrypt_ecb(plaintext_bytes, key_bytes) # Encrypt the plaintext

    
    print(ciphertext.hex()) # Print the now ciphertext in hex

if __name__ == "__main__":
    main()