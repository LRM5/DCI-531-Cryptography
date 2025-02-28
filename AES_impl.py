# AES_impl..py - Implements AES-128 from scratch in Python (ECB mode, PKCS#7 padding).
#          Contains all transformations: SubBytes, ShiftRows, MixColumns, AddRoundKey,
#          and the corresponding inverse operations, plus the key schedule.

S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

# Round constant for Key Expansion (for AES-128, we need 10 round constants)
R_CON = [
    0x00000000,
    0x01000000,
    0x02000000,
    0x04000000,
    0x08000000,
    0x10000000,
    0x20000000,
    0x40000000,
    0x80000000,
    0x1b000000,
    0x36000000
]

NB = 4   # number of columns (32-bit words) comprising the State. For AES, NB=4
NR = 10  # number of rounds for AES-128
NK = 4   # key length in 32-bit words for AES-128


def sub_word(word):
    """Apply S-Box substitution on each of 4 bytes of a 32-bit word."""
    return (
        (S_BOX[(word >> 24) & 0xFF] << 24) |
        (S_BOX[(word >> 16) & 0xFF] << 16) |
        (S_BOX[(word >> 8) & 0xFF]  <<  8) |
        (S_BOX[word & 0xFF])
    )

def rot_word(word):
    """Perform a cyclic permutation: [a0, a1, a2, a3] -> [a1, a2, a3, a0]."""
    return ((word << 8) & 0xFFFFFFFF) | ((word >> 24) & 0xFF)

def key_expansion(key_bytes):
    """
    Expand the 128-bit key into an array of 44 32-bit words (NB*(NR+1) = 4*(10+1)).
    key_bytes: 16-byte array (Python bytes).
    """
    # Convert key_bytes (16 bytes) into an array of 4 32-bit words.
    key_words = []
    for i in range(NK):
        word = (key_bytes[4*i] << 24) | (key_bytes[4*i+1] << 16) | \
               (key_bytes[4*i+2] << 8) | (key_bytes[4*i+3])
        key_words.append(word)

    for i in range(NK, NB * (NR + 1)):
        temp = key_words[i - 1]
        if i % NK == 0:
            # Rotate, sub, then XOR with Rcon
            temp = sub_word(rot_word(temp)) ^ R_CON[i // NK]
        key_words.append(key_words[i - NK] ^ temp)

    return key_words

def add_round_key(state, round_key):
    """XOR the state with the round key."""
    for r in range(4):
        for c in range(4):
            state[r][c] ^= (round_key[c] >> (24 - r*8)) & 0xFF

def sub_bytes(state):
    """Apply S-Box substitution on each byte of state."""
    for r in range(4):
        for c in range(4):
            state[r][c] = S_BOX[state[r][c]]

def inv_sub_bytes(state):
    """Apply inverse S-Box substitution on each byte of state."""
    for r in range(4):
        for c in range(4):
            state[r][c] = INV_S_BOX[state[r][c]]

def shift_rows(state):
    """Left-shift each row r by r bytes."""
    # row 0 doesn't shift
    state[1] = state[1][1:] + state[1][:1]  # shift left by 1
    state[2] = state[2][2:] + state[2][:2]  # shift left by 2
    state[3] = state[3][3:] + state[3][:3]  # shift left by 3

def inv_shift_rows(state):
    """Right-shift each row r by r bytes."""
    # row 0 doesn't shift
    state[1] = state[1][-1:] + state[1][:-1]  # shift right by 1
    state[2] = state[2][-2:] + state[2][:-2]  # shift right by 2
    state[3] = state[3][-3:] + state[3][:-3]  # shift right by 3

def xtime(a):
    """Multiply a by x in GF(2^8)."""
    a <<= 1
    return ((a ^ 0x1B) & 0xFF) if (a & 0x100) else (a & 0xFF)

def mul(a, b):
    """
    Multiply two numbers in the GF(2^8) finite field.
    This is repeated addition and xtime operation based on bits of b.
    """
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res & 0xFF

def mix_columns(state):
    """
    Mix columns operation for each column of the state.
    Using the fixed polynomial a(x)={03}x^3+{01}x^2+{01}x+{02}.
    """
    for c in range(4):
        a0 = state[0][c]
        a1 = state[1][c]
        a2 = state[2][c]
        a3 = state[3][c]

        state[0][c] = mul(a0, 2) ^ mul(a1, 3) ^ mul(a2, 1) ^ mul(a3, 1)
        state[1][c] = mul(a0, 1) ^ mul(a1, 2) ^ mul(a2, 3) ^ mul(a3, 1)
        state[2][c] = mul(a0, 1) ^ mul(a1, 1) ^ mul(a2, 2) ^ mul(a3, 3)
        state[3][c] = mul(a0, 3) ^ mul(a1, 1) ^ mul(a2, 1) ^ mul(a3, 2)

def inv_mix_columns(state):
    """
    Inverse of mix columns operation.
    Using the fixed polynomial a^-1(x)={0B}x^3+{0D}x^2+{09}x+{0E}.
    """
    for c in range(4):
        a0 = state[0][c]
        a1 = state[1][c]
        a2 = state[2][c]
        a3 = state[3][c]

        state[0][c] = mul(a0, 0x0E) ^ mul(a1, 0x0B) ^ mul(a2, 0x0D) ^ mul(a3, 0x09)
        state[1][c] = mul(a0, 0x09) ^ mul(a1, 0x0E) ^ mul(a2, 0x0B) ^ mul(a3, 0x0D)
        state[2][c] = mul(a0, 0x0D) ^ mul(a1, 0x09) ^ mul(a2, 0x0E) ^ mul(a3, 0x0B)
        state[3][c] = mul(a0, 0x0B) ^ mul(a1, 0x0D) ^ mul(a2, 0x09) ^ mul(a3, 0x0E)

def bytes_to_state(block16):
    """Convert 16 bytes into a 4x4 matrix (state)."""
    state = [list(block16[i:i+4]) for i in range(0, 16, 4)]
    # state[r][c]: r is row, c is column
    return state

def state_to_bytes(state):
    """Convert a 4x4 matrix (state) back into 16 bytes."""
    return bytes(sum(state, []))

def encrypt_block(plaintext_block, expanded_key):
    """
    Encrypt a single 16-byte block using AES-128.
    :param plaintext_block: bytes of length 16
    :param expanded_key: list of 44 words (4*(10+1)) from key_expansion
    :return: 16-byte ciphertext block
    """
    state = bytes_to_state(plaintext_block)

    # Initial round key addition
    add_round_key(state, expanded_key[0:NB])

    # Rounds 1..9
    for round_idx in range(1, NR):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, expanded_key[round_idx*NB:(round_idx+1)*NB])

    # Final round 10 (no mix_columns)
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, expanded_key[NR*NB:(NR+1)*NB])

    return state_to_bytes(state)

def decrypt_block(ciphertext_block, expanded_key):
    """
    Decrypt a single 16-byte block using AES-128.
    :param ciphertext_block: bytes of length 16
    :param expanded_key: list of 44 words (4*(10+1)) from key_expansion
    :return: 16-byte plaintext block
    """
    state = bytes_to_state(ciphertext_block)

    # Initial round
    add_round_key(state, expanded_key[NR*NB:(NR+1)*NB])
    inv_shift_rows(state)
    inv_sub_bytes(state)

    # Rounds 1..9
    for round_idx in range(NR-1, 0, -1):
        add_round_key(state, expanded_key[round_idx*NB:(round_idx+1)*NB])
        inv_mix_columns(state)
        inv_shift_rows(state)
        inv_sub_bytes(state)

    # Final round
    add_round_key(state, expanded_key[0:NB])

    return state_to_bytes(state)

def pkcs7_pad(data, block_size=16):
    """Apply PKCS#7 padding to data for a given block size."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(data, block_size=16):
    """Remove PKCS#7 padding."""
    if not data or len(data) % block_size != 0:
        raise ValueError("Invalid data or block size for unpadding.")
    pad_len = data[-1]
    # Basic sanity checks
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding length.")
    if data[-pad_len:] != bytes([pad_len])*pad_len:
        raise ValueError("Invalid PKCS#7 padding.")
    return data[:-pad_len]

def encrypt_ecb(plaintext, key_bytes):
    """Encrypt plaintext in ECB mode (PKCS#7 padded) with the given 16-byte key."""
    expanded_key = key_expansion(key_bytes)
    padded = pkcs7_pad(plaintext, 16)
    blocks = [padded[i:i+16] for i in range(0, len(padded), 16)]
    ciphertext = b''
    for block in blocks:
        ciphertext += encrypt_block(block, expanded_key)
    return ciphertext

def decrypt_ecb(ciphertext, key_bytes):
    """Decrypt ciphertext in ECB mode (PKCS#7 padded) with the given 16-byte key."""
    expanded_key = key_expansion(key_bytes)
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext is not a multiple of 16 bytes.")
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    plaintext_padded = b''
    for block in blocks:
        plaintext_padded += decrypt_block(block, expanded_key)
    return pkcs7_unpad(plaintext_padded, 16)