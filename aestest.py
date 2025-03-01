import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        
        print("Usage: python3 aestest.py <plaintext>") # Either prompt or instruct usage in CLI 
        sys.exit(1)
    plaintext = sys.argv[1]

    
    key = os.urandom(16) # Generate a random 128-bit key
    hex_key = key.hex()

    print(f"Generated Key (hex): {hex_key}")

    # Call aesencrypt.py
    encrypt_cmd = ["python3", "aesencrypt.py", hex_key, plaintext]
    result_enc = subprocess.run(encrypt_cmd, capture_output=True, text=True)
    ciphertext_hex = result_enc.stdout.strip()
    print("Encrypt command:", encrypt_cmd)
    print("Return code (encrypt):", result_enc.returncode)
    print("STDOUT (encrypt):", result_enc.stdout)
    print("STDERR (encrypt):", result_enc.stderr)
    print(f"Ciphertext (hex): {ciphertext_hex}")

    # Call aesdecrypt.py
    decrypt_cmd = ["python3", "aesdecrypt.py", hex_key, ciphertext_hex]
    result_dec = subprocess.run(decrypt_cmd, capture_output=True, text=True)
    recovered_plaintext = result_dec.stdout.strip()

    print(f"Recovered Plaintext: {recovered_plaintext}")

if __name__ == "__main__":
    main()