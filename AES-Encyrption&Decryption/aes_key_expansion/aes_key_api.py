#!/usr/bin/env python
# coding: utf-8

# ### Utility functions
# Run the following cell to import the utility functions needed for this notebook

# In[70]:


def get_rcon():
    Rcon = ( 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a )
    return Rcon

def get_sbox():
    
    Sbox = (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)
    return Sbox
        

def rotate(word, n):
    return word[n:] + word[0:n]


# # AES Key Expansion
# 
# AES key expansion uses a `g(.)` function that performs the following operations on a given word:
#     
# - **Rotate:** takes a 4-byte word and rotates everything one byte to the left, e.g. rotate([1,2,3,4]) → [2, 3, 4, 1]
# - **SubBytes:** each byte of a word is substituted with the value in the S-Box whose index is the value of the original byte
# - **Rcon:** the first byte of a word is XORed with the round constant. Each value of the Rcon table is a member of the Rinjdael finite field.
# 
# 
# <img src='aes_images/aes_key_expansion.png' width=50%>
# 
# **Exercise:** Implement `g()` to perform the above operations on a given word based on the round number $i$
# 

# In[71]:


# takes 4-byte word and iteration number
def g(input_word, i):
    
    # get the RCON array
    rcon = get_rcon()
    
    # Get the SBOX
    sbox = get_sbox()
    
    # rotate word 1 byte to the left
    word = rotate(input_word,1)
    
    # make an byte array with the length of word
    new_word = bytearray(len(word))
    
    # apply sbox substitution on all bytes of word
    for k in range(len(input_word)):
        new_word[k] = sbox[word[k]]
    
    # XOR the output of the rcon[i] transformation with the first part
    # of the word
    new_word[0] = new_word[0]^rcon[i]
    
    return new_word


# ## Expanding a 128-bit key
# Expanding a 128-bit key uses an array with 176 bytes as follows:
# 1. The first 16 bytes of the expanded key are simply the encryption key
# 2. The rcon iteration value i is set to 0
# 
# Until we have 176 bytes of expanded key, we do the following to generate 16 more bytes of expanded key:
# 
#    1. We do the following to create the first four bytes of expanded key:
#       - We create a 4-byte temporary variable, $t$
#       - We assign the value of the previous four bytes in the temporary key to $t$
#       - We perform `g()` (see above) on $t$, with $i$ as the rcon iteration value.
#       - We increment $i$ by one.
#       - We exclusive-or $t$ with the four-byte block 16 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
#    2. We then do the following three times to create the next twelve bytes of expanded key:
#       - We assign the value of the previous four bytes in the temporary key to $t$
#       - We exclusive-or $t$ with the four-byte block 16 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
# 

# In[73]:


def expand_key_128(initial_key):
    
    # initialize expanded_key with a size of the intial 
    expanded_key = bytearray(len(initial_key))
    
    # copy initial key to expanded key
    for q in range(len(initial_key)):
        expanded_key[q] = initial_key[q]
    
    # set Rcon iterator to 0
    i = 0
    
    # make a temporary bytearray with the size of a word (representing t) 
    temp = bytearray(4)  # 4-byte container for temp storage
    
    while len(expanded_key) < 176:
        
        # temp → last 4 bytes of expandedKey
        temp = expanded_key[len(expanded_key)-4:]

        # every 16 bytes apply core schedule to temp
        if len(expanded_key)% 16 == 0:
            # apply g()
            temp = g(temp,i)
            
            #increament i
            i =  i + 1

        
        # XOR temp with the 4-byte block 16 bytes before the end of the current expanded key.
        # These 4 bytes become the next bytes in the expanded key
        # NOTE: xor is note defined on the bytearray, you need to perform xor on each element on temp
        # and add it to expanded_key
        block = expanded_key[len(expanded_key)-16:len(expanded_key)-12]
        for j in range(4):
            t = temp[j]^block[j]
            expanded_key.append(t)
            
    return expanded_key
                           


# ## Expanding a 192-bit key
# This is almost identical to a 128-bit key schedule:
# 
# 1. The first 24 bytes of the expanded key are simply the encryption key
# 2. The rcon iteration value i is set to 0
# 
# Until we have 208 bytes of expanded key, we do the following to generate 24 more bytes of expanded key:
#    1. We do the following to create the first four bytes of expanded key:
#         - We create a 4-byte temporary variable, t
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We perform schedule_core (see above) on t, with i as the rcon iteration value.
#         - We increment i by one.
#         - We exclusive-or t with the four-byte block 24 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
#    2. We then do the following five times to create the next 20 bytes of expanded key:
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We exclusive-or t with the four-byte block 24 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
# 
# We now have 208 bytes of expanded key generated. 

# In[75]:


def expand_key_192(initial_key):
    
     # initialize expanded_key with a size of the intial 
    expanded_key = bytearray(len(initial_key))
    
    # copy initial key to expanded key
    for q in range(len(initial_key)):
        expanded_key[q] = initial_key[q]
    
    
    # set Rcon iterator to 0
    i = 0
    
    # make a temporary bytearray with the size of a word (representing t) 
    temp = bytearray(4)  # 4-byte container for temp storage
    
    while len(expanded_key) < 208:
        
        # temp → last 4 bytes of expandedKey
        temp = expanded_key[len(expanded_key)-4:]

    
        if len(expanded_key)%24 == 0:
            # apply g()
            temp = g(temp,i)
            
            #increament i
            i =  i + 1

        
        block = expanded_key[len(expanded_key)-24:len(expanded_key)-20]
        for j in range(4):
            t = temp[j]^block[j]
            expanded_key.append(t)
            
    return expanded_key
      


# ## Expanding a 256-bit key
# This is similar to the 128-bit and 192-bit key schedule, but includes an extra application of the s-box.
# 
# 1. The first 32 bytes of the expanded key are simply the encryption key
# 2. The rcon iteration value i is set to 0
# 
# Until we have 240 bytes of expanded key, we do the following to generate 32 more bytes of expanded key:
#    1. We do the following to create the first four bytes of expanded key:
#         - We create a 4-byte temporary variable, t
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We perform schedule_core (see above) on t, with i as the rcon iteration value.
#         - We increment i by one.
#         - We exclusive-or t with the four-byte block 32 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
#    2. We then do the following three times to create the next twelve bytes of expanded key:
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We exclusive-or t with the four-byte block 32 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
#    3. We then do the following to create the next four bytes of expanded key:
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We run each of the four bytes in t through Rijndael's S-box
#         - We exclusive-or t with the four-byte block 32 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
#    4. We then do the following three times to create the next twelve bytes of expanded key:
#         - We assign the value of the previous four bytes in the temporary key to t
#         - We exclusive-or t with the four-byte block 32 bytes before the new expanded key. This becomes the next four bytes in the expanded key. 
# 
# We now have 240 bytes of expanded key generated. 

# In[77]:


def expand_key_256(initial_key):
      # initialize expanded_key with a size of the intial 
    expanded_key = bytearray(len(initial_key))
    
    # copy initial key to expanded key
    for q in range(len(initial_key)):
        expanded_key[q] = initial_key[q]
    
    sbox = get_sbox()
    # set Rcon iterator to 0
    i = 0
    
    # make a temporary bytearray with the size of a word (representing t) 
    temp = bytearray(4)  # 4-byte container for temp storage
    
    while len(expanded_key) < 240:
        
        # temp → last 4 bytes of expandedKey
        temp = expanded_key[len(expanded_key)-4:]

    
        if len(expanded_key)%32 == 0:
            # apply g()
            temp = g(temp,i)
            
            #increament i
            i =  i + 1   
        
        block = expanded_key[len(expanded_key)-32:len(expanded_key)-28]
        for l in range(4):
                temp[l] = sbox[temp[l]]
        for j in range(4):
            t = temp[j]^block[j]
            expanded_key.append(t)
            
    return expanded_key


# In[ ]:




