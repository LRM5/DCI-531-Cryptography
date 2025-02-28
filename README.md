# AES-128 Cryptography
#### This project provides a pure Python implementation of AES-128 (Advanced Encryption Standard) in ECB mode with PKCS#7 padding—all written from scratch, without using any external cryptographic libraries. This is a basic example demonstrating the internals of AES encryption and decryption.

## Files
**1.	AES_impl.py**
-	Contains the core AES-128 logic:
-	Key expansion (round keys)
-	Byte-level transformations (SubBytes, ShiftRows, MixColumns, AddRoundKey)
-	Block encryption/decryption (16-byte blocks)
-	PKCS#7 padding methods
-	Exports functions like encrypt_ecb() and decrypt_ecb().

**2. aesencrypt.py**
	-	A command-line script to encrypt a given plaintext using a specified 128-bit key.
	-	Usage:
   *     python3 aesencrypt.py <hex_key> <plaintext>
     
  -	Outputs the ciphertext in hex format.

**3. aesdecrypt.py**
  - A command-line script to decrypt a given ciphertext using a specified 128-bit key.
	-	Usage:
   *      python3 aesdecrypt.py <hex_key> <plaintext>

- Outputs the recovered text as a UTF-8 String

**4.	aestest.py**
-- A demonstration script showing how to encrypt and decrypt using the local AES-128 implementation:
  
- 1.Generates a random 16-byte (128-bit) key via os.urandom().
- 2.Prints the generated key (hex).
- 3.Encrypts a user-provided plaintext by calling aesencrypt.py.
- 4.Prints the resulting ciphertext (hex).
- 5.Decrypts the ciphertext by calling aesdecrypt.py.
- 6.Prints the recovered plaintext.

   *     python3 aestest.py "Hello AES World"
 
