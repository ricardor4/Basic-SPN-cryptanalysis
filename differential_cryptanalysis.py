'''
Here we want to implement the differential cryptanalysis attack of the simple SPN cipher of Heys tutorial
We have a differential characteristic of the form (0x0, 0x6, 0x0, 0x0) -> (0x0, 0x6, 0x0, 0x6) after 3 rounds of the cipher
with a probability of 27/1024 (around 2.6%).
In a ideal cipher, the probability of all differential characteristics would be 1/2^16 = 1/65536 = 0.001526
So the characteristic that we have is around 1700 times more probable than in an ideal cipher. That distinguishes the cipher from a random permutation.
'''

# Load the file containing the pairs of plaintexts and ciphertexts and store them as a list of tuples of tuples (plaintext, ciphertext)
# The file has the format: message, ciphertext as columns
pairs = []
file_path = '/home/ricardo/Basic-SPN-cryptanalysis/testData/0x1234567890abcdef.dat'
with open(file_path, 'r') as file:
    data = file.readlines()
    for i in range(0, len(data), 2):
        line1 = data[i]
        line2 = data[i+1]
        m0, c0 = line1.split(',')
        m1, c1 = line2.split(',')
        pairs.append(((bin(int(m0, 16))[2:], bin(int(c0, 16))[2:]), (bin(int(m1, 16))[2:], bin(int(c1, 16))[2:])))


# Check that for all tuples of pairs, the XOR difference between the plaintexts is 0000 1011 0000 0000
# each pair is of the form (m0, c0), (m1, c1)
# We need to check that  m1 XOR m0 = 0b0000 1011 0000 0000
diff = '0000101100000000'
for pair in pairs:
    print(pair)
    m0, m1 = pair[0][0], pair[1][0]
    print(m0, m1)
    if bin(int(m0, 2) ^ int(m1, 2))[2:] != diff:
        print('Error: XOR difference between plaintexts is not 0b0000 1011 0000 0000')
        print(f'XOR difference is {bin(int(m0, 2) ^ int(m1, 2))[2:]}')
        break




