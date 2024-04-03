from random import randint
from basic_SPN import encrypt

def generate_pairs(n_vals: int, diff: int, key: int):
    """
    Generate a set of n_vals pairs of plaintexts and ciphertext with XOR difference equal to diff.
    We generate pairs of plaintext-ciphertext (m1, c1), (m2, c2) such that m2 = m1 XOR diff.
    The plaintexts are 16-bit integers, and the ciphertexts are also 16-bit integers.
        
    We use the key to encrypt the plaintexts.

    Parameters:
    n_vals: int
        The number of pairs to generate
    diff: int
        The XOR difference between the plaintexts
    key: int
        The key to use for encryption

    Returns:
    None. The pairs are written to a file in the format:
    name = key[0:20] + '.dat'
    The file will have 2 columns, plaintext and ciphertext.
    m1, c1
    m2, c2
    ...
    m_n_vals, c_n_vals
    where m2 onwards, all plaintexts will be mi-1 XOR diff.
    """

    # Produce a CSV of plaintext, key value pairs for cryptanalysis
    file_name = 'testData/' + key[0:20] + '.dat'
    with open(file_name, "w+") as fd_w:
        print(f'Running basic SPN cipher with key K = {key}')

        # We select random plaintexts and encrypt them
        plaintexts = [randint(0, 65535) for _ in range(n_vals)]

        for i in plaintexts:
            fd_w.write(f'{i:04x}, {encrypt(i, key):04x}\n')
            fd_w.write(f'{(i ^ diff):04x}, {encrypt((i ^ diff), key):04x}\n')

        print(f'Simple SPN plaintext, ciphertext CSV written to {file_name}')

if __name__ == "__main__":

    # Generate a random key
    k = '0x1234567890abcdef'
    # now generate pairs of plaintexts and ciphertexts with XOR difference 0b0000 1011 0000 0000 under the key k
    generate_pairs(5000, int('0000101100000000', 2), k)
