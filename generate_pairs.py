from random import randint
from basic_SPN import encrypt

# Generate n random 16-bit plaintexts
n = 20
plaintexts = [randint(0, 2**16-1) for _ in range(n)]

# for each plaintext we generate another plaintext that is the XOR of the original plaintext with 0b0000 1011 0000 0000

diff = 0b0000_1011_0000_0000


def generate_xored_pairs(numbers:list[int], diff:int) -> list[int]:
    """
    Generate a list of length 2n from the input list of integers of length n, where each even index
    contains the original integer and each odd index contains the XOR of the previous element and diff.
    
    Parameters:
    numbers: list of int
        The original list of integers.
    diff: int
        The value to XOR with each element.
    
    Returns:
    result: list of int
        The resulting list of length 2n with original and XORed values.
    """
    result = []
    for num in numbers:
        result.append(num)  # Append the original number
        result.append(num ^ diff)  # Append the number XORed with diff

    return result

# Generate the pairs of plaintexts and store them in a file with the format: plaintext, plaintext XOR diff
pairs = generate_xored_pairs(plaintexts, diff)
'''
file_path = 'testData/plaintexts.dat'
with open(file_path, 'w') as file:
    for i in range(0, len(pairs), 2):
        file.write(f'{pairs[i]:04x}, {pairs[i+1]:04x}\n')

'''
for i in range(0, len(pairs), 2):
    print(f'{pairs[i] ^ pairs[i+1]:016b}')
