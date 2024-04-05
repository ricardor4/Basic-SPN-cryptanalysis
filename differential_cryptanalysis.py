'''
Here we want to implement the differential cryptanalysis attack of the simple SPN cipher of Heys tutorial
We have a differential characteristic of the form (0x0, 0x6, 0x0, 0x0) -> (0x0, 0x6, 0x0, 0x6) after 3 rounds of the cipher
with a probability of 27/1024 (around 2.6%).
In an ideal cipher, the probability of all differential characteristics would be 1/2^16 = 1/65536 = 0.001526
So the characteristic that we have is around 1700 times more probable than in an ideal cipher. That distinguishes the cipher from a random permutation.
'''

# Load the file containing the pairs of plaintexts and ciphertexts and store them as a list of tuples of tuples (plaintext, ciphertext)
# The file has the format: message, ciphertext as columns
pairs = []
file_path = '/home/ricardo/Basic-SPN-cryptanalysis/testData/50c0453cc2eb5f03210e.dat'
with open(file_path, 'r') as file:
    # We want a list of tuples where the first element is the first value on the line and the second element is the second value on the line
    for line in file:
        # We split the line by the comma and remove the newline character
        pair = line.strip().split(',')
        # We convert the pair to a tuple of integers
        pair = tuple([int(p, 10) for p in pair])
        # We add the pair to the list of pairs
        pairs.append(pair)

# Now we want to get tuples of tuples of plaintexts and ciphertexts 
# we need tuples of the form ((m0, c0), (m1, c1)) where m0 XOR m1 = 0b0000 1011 0000 0000
# We will store the tuples in a list called valid_pairs
print(len(pairs))
valid_pairs = []
for i in range(0, len(pairs), 2):
    # We get the pair of plaintexts
    m0, m1 = pairs[i][0], pairs[i+1][0]
    # We get the pair of ciphertexts
    c0, c1 = pairs[i][1], pairs[i+1][1]
    # We check that m0 XOR m1 = 0b0000 1011 0000 0000
    diff = bin(m0 ^ m1)[2:].zfill(16)
    if diff == '0000101100000000':
        valid_pairs.append(((m0, c0), (m1, c1)))

# We want to store the valid pairs in a file called valid_pairs.txt
with open('./testData/valid_pairs.txt', 'w') as file:
    for pair in valid_pairs:
        file.write(str(pair) + '\n')