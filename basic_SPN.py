# A basic Substitution-Permutation Network cipher, implemented by following 
# 'A Tutorial on Linear and Differential Cryptanalysis'
# by Howard M. Heys
#
# 02/12/16 Chris Hicks 
#
# Basic SPN cipher which takes as input a 16-bit input block and has 4 rounds.
# Each round consists of (1) substitution (2) transposition (3) key mixing

import random
import hashlib

blockSize = 16
verboseState = True

# (1) Substitution: 4x4 bijective, one sbox used for all 4 sub-blocks of size 4. Nibble wise
sbox =     {0:0xE, 1:0x4, 2:0xD, 3:0x1, 4:0x2, 5:0xF, 6:0xB, 7:0x8, 8:0x3, 9:0xA, 0xA:0x6, 0xB:0xC, 0xC:0x5, 0xD:0x9, 0xE:0x0, 0xF:0x7} #key:value
sbox_inv = {0xE:0, 0x4:1, 0xD:2, 0x1:3, 0x2:4, 0xF:5, 0xB:6, 0x8:7, 0x3:8, 0xA:9, 0x6:0xA, 0xC:0xB, 0x5:0xC, 0x9:0xD, 0x0:0xE, 0x7:0xF}

# Apply sbox (1) to a 16 bit state and return the result
def apply_sbox(state, sbox:dict):
    subStates = [state&0x000f, (state&0x00f0)>>4, (state&0x0f00)>>8, (state&0xf000)>>12]
    for idx,subState in enumerate(subStates):
        subStates[idx] = sbox[subState]
    return subStates[0]|subStates[1]<<4|subStates[2]<<8|subStates[3]<<12
    

# (2) Permutation. Applied bit-wise 
# OBS: 0-indexed, Heys uses 1-indexed
pbox = {0:0, 1:4, 2:8, 3:12, 4:1, 5:5, 6:9, 7:13, 8:2, 9:6, 10:10, 11:14, 12:3, 13:7, 14:11, 15:15}

# (3) Key mixing: bitwise XOR between round subkey and data block input to round
# Key schedule: independant random round keys.
# We take the sha-hash of a 128-bit 'random' seed and then take the first 80-bits
# of the output as out round keys K1-K5 (Each 16 bits long). (not secure, this is just a demo)
def keyGeneration():
    k = hashlib.sha1( hex(random.getrandbits(128)).encode('utf-8') ).hexdigest()[2:2+20]
    return k
# k is hex of 20 digits, that is 80 bits


# Simple SPN Cipher encrypt function
def encrypt(pt, k:str):
    state = pt
    if verboseState: print('**pt = {:04x}**'.format(state))
    
    subKeys = [ int(subK,16) for subK in [ k[0:4],k[4:8], k[8:12], k[12:16], k[16:20] ] ]
    
    #First three rounds of sinple SPN cipher
    for roundN in range(0,3):
    
        if verboseState: print(f"Round {roundN}")
        #XOR state with round key (3, subkeys 1,..,4)
        state = state^subKeys[roundN]
        if verboseState: print ('After key addition:',hex(state))
        
        #Break state into nibbles, perform sbox on each nibble, write to state (1)
        state = apply_sbox(state,sbox)
        if verboseState: print("After Sboxes", hex(state))
        
        #Permute the state bitwise (2)
        state_temp = 0      
        for bitIdx in range(0,blockSize):
            if(state & (1 << bitIdx)):
                state_temp |= (1 << pbox[bitIdx])
        state = state_temp
        if verboseState: print ("After LL",hex(state))
    
    # Final round of SPN cipher (k4, sbox, s5)
    state = state^subKeys[-2] #penultimate subkey (key 4) mixing
    if verboseState: 
        print ("Round: 3",)
        print("After key addition:",hex(state))


    state = apply_sbox(state,sbox)
    if verboseState:print("After Sboxes", hex(state))
    state = state^subKeys[-1] #Final subkey (key 5) mixing
    if verboseState: print("After Key Whitening", hex(state))
    if verboseState: print('**ct = {:04x}**'.format(state))
    
    return state

# Simple SPN Cipher decrypt function
def decrypt(ct, k):
    state = ct
    if verboseState: print('**ct = {:04x}**'.format(state))
    
    #Derive round keys
    subKeys = [ int(subK,16) for subK in [ k[0:4],k[4:8], k[8:12], k[12:16], k[16:20] ] ]
    
    if verboseState: print (str(3), hex(state), end= ' ')
    
    #Undo final round key
    state = state^subKeys[4]
    if verboseState: print (hex(state), end= ' ')
    
    #Apply inverse s-box
    state = apply_sbox(state,sbox_inv)
    if verboseState: print (hex(state))
    
    #Undo first 3 rounds of simple SPN cipher
    for roundN in range(2, -1, -1):
        
        if verboseState: print(roundN, end = ' ')
        #XOR state with round key (3, subkeys 4,..,0)
        state = state^subKeys[roundN+1]
        if verboseState: print (hex(state), end=' ')
        
        #Un-permute the state bitwise (2)
        state_temp = 0      
        for bitIdx in range(0, blockSize):
            if(state & (1 << bitIdx)):
                state_temp |= (1 << pbox[bitIdx])
        state = state_temp
        if verboseState: print (hex(state), end = ' ')
        
        #Apply inverse s-box
        state = apply_sbox(state,sbox_inv)
        if verboseState: print (hex(state))
    if verboseState: print(roundN, end = ' ')
    
    #XOR state with round key 0
    state = state^subKeys[0]
    if verboseState: print('**pt = {:04x}**'.format(state))     
     
    return state
if __name__ == "__main__":
    
    # Generate a random key

    k = keyGeneration()



    # Test the simple SPN cipher

    
    # Produce a CSV of plaintext, key value pairs for cryptanalysis from the plaintexts on /testData/plaintexts.txt
    fileName = 'testData/' + k[0:20] + '.dat'
    fd_w = open(fileName,"w+")
    print ('Running basic SPN cipher with key K = {:}'.format(k))

    with open("testData/plaintexts.txt", "r") as fd:
        for line in fd:
            pt = int(line)
            ct = encrypt(pt, k)
            fd_w.write(str(pt)+','+str(ct)+'\n')

