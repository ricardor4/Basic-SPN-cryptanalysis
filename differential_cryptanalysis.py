'''
Here we want to implement the differential cryptanalysis attack of the simple SPN cipher of Heys tutorial
We have a differential characteristic of the form (0x0, 0x6, 0x0, 0x0) -> (0x0, 0x6, 0x0, 0x6) after 3 rounds of the cipher
with a probability of 27/1024 (around 2.6%).
In a ideal cipher, the probability of all differential characteristics would be 1/2^16 = 1/65536 = 0.001526
'''

