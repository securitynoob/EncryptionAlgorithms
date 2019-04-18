#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
from bitstring import BitArray
from terminaltables import AsciiTable


# In[2]:


def test_get_IP_vector(get_IP_vector):
    passed = (get_IP_vector() == (58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7))
    return passed


# In[3]:


def test_init_permute(init_permute):
    input_block = BitArray('0b1011011000100010100111011001000011011100100010001100001100110101')
    output_block = init_permute(input_block)
    test_output_block = BitArray('0b0101000010011101100101011100010001111101100000110011010001000011')
    return output_block == test_output_block


# In[4]:


def test_get_FP_vector(get_FP_vector):
    FP = (40,   8,     48,     16,     56,     24,     64,     32,
39,     7,     47,     15,     55,     23,     63,     31,
38,     6,     46,     14,     54,     22,     62,     30,
37,     5,     45,     13,     53,     21,     61,     29,
36,     4,     44,     12,     52,     20,     60,     28,
35,     3,     43,     11,     51,     19,     59,     27,
34,     2,     42,     10,     50,     18,     58,     26,
33,     1,     41,     9,    49,     17,    57,     25)
    return FP == get_FP_vector()


# In[5]:


def test_final_permutation(final_permutation):
    input_block = BitArray('0b0101000010011101100101011100010001111101100000110011010001000011')
    output_block = final_permutation(input_block)
    test_output_block = BitArray('0b1011011000100010100111011001000011011100100010001100001100110101')
    return output_block == test_output_block
    


# In[6]:


def test_get_E_vector(get_E_vector):
    E = (32,  1,   2,   3,   4,   5,
            4,   5,   6,   7,   8,   9,
            8,   9,   10,  11,  12,  13,
            12,  13,  14,  15,  16,  17,
            16,  17,  18,  19,  20,  21,
            20,  21,  22,  23,  24,  25,
            24,  25,  26,  27,  28,  29,
            28,  29,  30,  31,  32,  1)
    return E == get_E_vector()


# In[7]:


def test_expansion_function(expansion_function):
    input_block = BitArray('0b11010111100001101111100001110001')
    output_block = expansion_function(input_block)
    expected_output = BitArray('0b111010101111110000001101011111110000001110100011')
    return output_block == expected_output
    


# In[8]:


def test_get_S_box(get_S_box):
    SBOX = [
# Box-1
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
# Box-2

[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],

# Box-3

[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

],

# Box-4
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],

# Box-5
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
# Box-6

[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

],
# Box-7
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
# Box-8

[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]

]
    return SBOX == get_S_box()


# In[9]:


def test_s_box_calculation(s_box_calculation):
    input_block = BitArray('0b111010101111110000001101011111110000001110100011')
    output_block = s_box_calculation(input_block)
    expected_output = BitArray('0b10100010101100000110011111010001')
    return expected_output == output_block


# In[10]:


def test_get_P_box(get_P_box):
    P = (16, 7, 20, 21, 29, 12, 28, 17,
1, 15, 23, 26, 5, 18, 31, 10,
2, 8, 24, 14, 32, 27, 3, 9,
19, 13, 30, 6, 22, 11, 4, 25 )
    return P == get_P_box()


# In[11]:


def test_permutation(permutation):
    input_block = BitArray('0b11010111100001101111100001110001')
    output_block = permutation(input_block)
    expected_output = BitArray('0b01110011110101001101110110010010')
    return expected_output == output_block 


# In[12]:


def test_round_function(round_function):
    round_key = BitArray('0b001100001101010011000001100110000111110001110010')
    input_block = BitArray('0b11010111100001101111100001110001')
    output_block = round_function(input_block, round_key)
    expected_output = BitArray('0b11001001001110001010001111111111')
    return expected_output == output_block 
    


# In[13]:


def test_get_PC1_vector(get_PC1_vector):
    PC1 = (57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,
           43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,
           7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,
           28,20,12,4)
    return PC1 == get_PC1_vector()


# In[14]:


def test_permutation_choice_1(permutation_choice_1):
    initial_key = BitArray('0b0010011010010100100110001011110000001001111111000000000000000000')
    output_block = permutation_choice_1(initial_key)
    expected_output = BitArray('0b00101110001000000010100100100000000100101011001111001110')
    return expected_output == output_block


# In[15]:


def test_get_key_rotation(get_key_rotation):
    rotation_table = {1: 1,
                       2: 1,
                       3: 2,
                       4: 2,
                       5: 2,
                       6: 2,
                       7: 2,
                       8: 2,
                       9: 1,
                       10: 2,
                       11: 2,
                       12: 2,
                       13: 2,
                       14: 2,
                       15: 2,
                       16: 1
                      }
    count = 0
    for round_number in range(1,17):
        count += int(get_key_rotation(round_number) == rotation_table[round_number])
    
    return count == 16    


# In[16]:


def test_circular_left(circular_left):
    input_block = BitArray('0b11010111100001101111100001110001')
    rotation = 1
    output_block = circular_left(input_block, rotation)
    expected_output = BitArray('0b10101111000011011111000011100011')
    return expected_output == output_block


# In[17]:


def test_get_PC2_vector(get_PC2_vector):
    PC2 = (14,17,11,24,1,5,3,28,15,
           6,21,10,23,19,12,4,26,8,
           16,7,27,20,13,2,41,52,31,
           37,47,55,30,40,51,45,33,
           48,44,49,39,56,34,53,46,
           42,50,36,29,32)
    return PC2 == get_PC2_vector()


# In[18]:


def test_compression_pbox(compression_pbox):
    input_block = BitArray('0b01010111100111101010011000011000110001001111110100000000')
    output_block = compression_pbox(input_block)
    expected_output = BitArray('0b110000011100111101010011100000000111100010110010')
    return expected_output == output_block
    


# In[19]:


def test_key_generation(key_generation):
    initial_key = BitArray('0b0100101000011010011101111110100000001000000000010000010110101011')
    round_key = key_generation(initial_key)
    expected_output = {1: BitArray('0b000000011010001100100110100110001011100111001000'),
                       2: BitArray('0b101000101000011000001100010011010010010011101101'),
                       3: BitArray('0b010010000001001000000010101010101101100011001001'),
                       4: BitArray('0b001000001001100001111000000000101101011100110111'),
                       5: BitArray('0b100001000110000001000010100111110000110110100000'),
                       6: BitArray('0b001000100100111100010000110010000100101101010001'),
                       7: BitArray('0b010011000011000100000001010100111110001000011100'),
                       8: BitArray('0b000000111000010001011001111100010001010110001000'),
                       9: BitArray('0b100010000100000010011001000111111011011010010100'),
                       10: BitArray('0b000101010000001100101000001110010100010111100001'),
                       11: BitArray('0b100000100001100010000001000010101110100000000111'),
                       12: BitArray('0b000110010010101001000100111001100110010110010100'),
                       13: BitArray('0b000000000111010010001000101010010000001111001011'),
                       14: BitArray('0b010100000000010101100100110101101101001000000011'),
                       15: BitArray('0b110000001100100000000001010101100000011101101100'),
                       16: BitArray('0b110011000010000000100010010001001101010010010110')
                      }
    count = 0
    for round_num in range(1,17):
        count += int(expected_output[round_num] == round_key[round_num])
    
    return count == 16
        


# In[20]:


def test_feistel_round(feistel_round):
    L_in = BitArray('0b01011101011000100011001111101000')
    R_in = BitArray('0b00101000011101011011011111100010')
    input_block = L_in + R_in
    round_key = BitArray('0b100001101010110110100001011111011011100000101101')
    output_block = feistel_round(input_block, round_key)
    expected_L = BitArray('0b00101000011101011011011111100010')
    expected_R = BitArray('0b00111001101100111110010111000000')
    expected_output = expected_L + expected_R
    
    return expected_output == output_block


# In[21]:


def test_des_cipher(des_cipher):
    initial_key = BitArray('0b0000110010111110001100000100100111110011010001010001111001110011')
    plain_block = BitArray('0b1000110111100111011100000010010101001100001001010110010000111110')
    cipher_block = des_cipher(plain_block, initial_key)                    
    decrypted_plain_block = des_cipher(cipher_block, initial_key, mode='D')
    return plain_block == decrypted_plain_block


# In[22]:


def test_des_app(des_app):
    initial_key = BitArray('0b0000110010111110001100000100100111110011010001010001111001110011')
    # get an input string from the terminal
    input_text = 'This is a test SRCAFAffdfdsFDSADF23423423gwfasfs~!@#$$^$&%   4$%$#&**#$@!!#@%$)(ujuljrf)'
    decoded_text = des_app(input_text, initial_key)
    return decoded_text[:len(input_text)] == input_text
