#!/usr/bin/env python
# coding: utf-8

# In[1]:


from test_des import *
from bitstring import BitArray


# # Exam 1: DES Encryption and Decryption
# 
# The Data Encryption Standard (DES) is a symmetric-key block cipher published by the National Institute of Standards and Technology (NIST).
# 
# DES is an implementation of a Feistel Cipher. It uses 16 round Feistel structure. The block size is 64-bit. Though, key length is 64-bit, DES has an effective key length of 56 bits, since 8 of the 64 bits of the key are not used by the encryption algorithm.
# 
# <img src='images/des_structure.jpg' width=35%>
# 
# Since DES is based on the Feistel Cipher, all that is required to specify DES is
# 
#     - Round function
#     - Key schedule
#     - Any additional processing 
#     - Initial and final permutation
# 

# ## 1. Initial and Final Permutation
# The initial and final permutations are straight Permutation boxes (P-boxes) that are inverses of each other. They have no cryptography significance in DES.
# 
# <img src='images/initial_and_final_permutation.jpg' width=35%>
# 
# 
# ### 1.1 Initial permutation (IP)
# This table specifies the input permutation on a 64-bit block. 
# 
# ```
# 58 	50 	42 	34 	26 	18 	10 	2
# 60 	52 	44 	36 	28 	20 	12 	4
# 62 	54 	46 	38 	30 	22 	14 	6
# 64 	56 	48 	40 	32 	24 	16 	8
# 57 	49 	41 	33 	25 	17 	9 	 1
# 59 	51 	43 	35 	27 	19 	11 	3
# 61 	53 	45 	37 	29 	21 	13 	5
# 63 	55 	47 	39 	31 	23 	15 	7 
# ```
# 
# The meaning is as follows: the first bit of the output is taken from the 58th bit of the input; the second bit from the 50th bit, and so on, with the last bit of the output taken from the 7th bit of the input.
# This information is presented as a table for ease of presentation; it is a vector, not a matrix. 
# 
# **Exercise:** Implement `get_IP_vector()` that return initial permutation (IP) vector. 

# In[2]:


def get_IP_vector():
    IP = (58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7)
    return IP


# In[3]:


print('Sanity Check (get_IP_vector): ', test_get_IP_vector(get_IP_vector))


# **Exercise:** Implement `init_permute()` to perform initial permutation of DES

# In[4]:


def init_permute(input_block):
    # get the initial permutation vector
    IP = get_IP_vector()
    
    # make a bitarray with size equal to input_block
    output_block = BitArray(len(input_block))
    
    # perform permutation
    for i in range(len(output_block)):
        output_block[i] = input_block[IP[i]-1]
    
    return output_block
    


# In[5]:


print('Sanity Check (init_permute): ', test_init_permute(init_permute))


# ### 1.2 Final Permutation
# 
# The final permutation is the inverse of the initial permutation; the table is interpreted similarly. The reference table for the final permutation is as follows:
# 
# ```
# 40 	8 	48 	16 	56 	24 	64 	32
# 39 	7 	47 	15 	55 	23 	63 	31
# 38 	6 	46 	14 	54 	22 	62 	30
# 37 	5 	45 	13 	53 	21 	61 	29
# 36 	4 	44 	12 	52 	20 	60 	28
# 35 	3 	43 	11 	51 	19 	59 	27
# 34 	2 	42 	10 	50 	18 	58 	26
# 33 	1 	41 	9 	49 	17 	57 	 25 
# ```
# 
# **Exercise:** Implement the `get_FP_vector()` that returns the final permutation reference vector.

# In[6]:


def get_FP_vector():
    FP = (40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14, 54,22,62,30,37,5,45,13,53,21,61,29,
          36,4, 44,12,52,20,60,28,35,3,43,11,51,19,59,27,34, 2,42,10,50,18,58,26,33,1,41,9,49,17,57, 25)
    
    return FP


# In[7]:


print('Sanity Check (get_FP_vector): ', test_get_FP_vector(get_FP_vector))


# **Exercise:** Implement `final_permutation()` that performs final permutation of the DES encryption.

# In[8]:


def final_permutation(input_block):
    # get the final permutation reference vector
    FP = get_FP_vector()
    
    # make an empty bitarray with the size equal to the input_block
    output_block = BitArray(len(input_block))
    
    # perform final permutation
    for i in range(len(FP)):
        output_block[i] = input_block[FP[i]-1]
    
    return output_block 


# In[9]:


print('Sanity Check: (final_permutation): ', test_final_permutation(final_permutation))


# ## 2. Round Function
# 
# The heart of this cipher is the DES function, $F$. The DES function applies a **48-bit** key to the rightmost **32 bits** to produce a **32-bit** output.
# 
# <img src='images/round_function.jpg' width=35% >

# ### 2.1 Expansion function (E)
# 
# The expansion function is interpreted as for the initial and final permutations. Note that some bits from the input are duplicated at the output; e.g. the fifth bit of the input is duplicated in both the sixth and eighth bit of the output. Thus, the 32-bit half-block is expanded to 48 bits. The following table is the reference vector for the Expansion function:
# 
# ```
# 32  1   2   3   4   5
# 4   5   6   7   8   9
# 8   9   10  11  12  13
# 12  13  14  15  16  17
# 16  17  18  19  20  21
# 20  21  22  23  24  25
# 24  25  26  27  28  29
# 28  29  30  31  32  1 
# ```
# 
# **Exercise:** Implement `get_E_vector()` that returns the reference vector for expansion function.
# 

# In[10]:


def get_E_vector():
    E = (32,  1,   2,   3,   4,   5,
            4,   5,   6,   7,   8,   9,
            8,   9,   10,  11,  12,  13,
            12,  13,  14,  15,  16,  17,
            16,  17,  18,  19,  20,  21,
            20,  21,  22,  23,  24,  25,
            24,  25,  26,  27,  28,  29,
            28,  29,  30,  31,  32,  1)
    
    return E


# In[11]:


print('Sanity Check (get_E_vector): ', test_get_E_vector(get_E_vector))


# Since right input is 32-bit and round key is a 48-bit, we first need to expand right input to 48 bits. Permutation logic is graphically depicted in the following illustration.
# 
# <img src='images/ex_permutation_logic.jpg'>
# 
# **Exercise:** Implement `expansion_function()` to perform expansion of the input block based on the expansion reference vector. 

# In[12]:


def expansion_function(input_block):
    # get expansion reference vector
    E = get_E_vector()
    
    # make a BitArray with the size equal to the length of the expasion vector
    output_block = BitArray(len(E))
    
    # perform expansion based on the reference vector
    for i in range(len(E)):
        output_block[i] = input_block[E[i]-1]
    
    return output_block


# In[13]:


print('Sanity Check (expansion_function): ', test_expansion_function(expansion_function))


# ### 2.2 S-box Calculation
# 
# The main part of this round function is the S-box calculation. In abstract view, this takes a 48-bit binary string as input and produce a 32-bit binary string as output with the help of 8 S-boxes. Each S-box has four rows and 16 columns numbered from (0–3 and 0–15) and each row has predefined value between 0 to 15. Figure 2 shows the S-boxes.
# <img src='images\des_s_box.png'>
# 
# 
# <table class="wikitable" cellspacing="0" style="text-align:right">
# <caption align="top">S-boxes
# </caption>
# <tbody><tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>1</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>14</td>
# <td>4</td>
# <td>13</td>
# <td>1</td>
# <td>2</td>
# <td>15</td>
# <td>11</td>
# <td>8</td>
# <td>3</td>
# <td>10</td>
# <td>6</td>
# <td>12</td>
# <td>5</td>
# <td>9</td>
# <td>0</td>
# <td>7
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>0</td>
# <td>15</td>
# <td>7</td>
# <td>4</td>
# <td>14</td>
# <td>2</td>
# <td>13</td>
# <td>1</td>
# <td>10</td>
# <td>6</td>
# <td>12</td>
# <td>11</td>
# <td>9</td>
# <td>5</td>
# <td>3</td>
# <td>8
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>4</td>
# <td>1</td>
# <td>14</td>
# <td>8</td>
# <td>13</td>
# <td>6</td>
# <td>2</td>
# <td>11</td>
# <td>15</td>
# <td>12</td>
# <td>9</td>
# <td>7</td>
# <td>3</td>
# <td>10</td>
# <td>5</td>
# <td>0
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>15</td>
# <td>12</td>
# <td>8</td>
# <td>2</td>
# <td>4</td>
# <td>9</td>
# <td>1</td>
# <td>7</td>
# <td>5</td>
# <td>11</td>
# <td>3</td>
# <td>14</td>
# <td>10</td>
# <td>0</td>
# <td>6</td>
# <td>13
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>2</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>15</td>
# <td>1</td>
# <td>8</td>
# <td>14</td>
# <td>6</td>
# <td>11</td>
# <td>3</td>
# <td>4</td>
# <td>9</td>
# <td>7</td>
# <td>2</td>
# <td>13</td>
# <td>12</td>
# <td>0</td>
# <td>5</td>
# <td>10
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>3</td>
# <td>13</td>
# <td>4</td>
# <td>7</td>
# <td>15</td>
# <td>2</td>
# <td>8</td>
# <td>14</td>
# <td>12</td>
# <td>0</td>
# <td>1</td>
# <td>10</td>
# <td>6</td>
# <td>9</td>
# <td>11</td>
# <td>5
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>0</td>
# <td>14</td>
# <td>7</td>
# <td>11</td>
# <td>10</td>
# <td>4</td>
# <td>13</td>
# <td>1</td>
# <td>5</td>
# <td>8</td>
# <td>12</td>
# <td>6</td>
# <td>9</td>
# <td>3</td>
# <td>2</td>
# <td>15
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>13</td>
# <td>8</td>
# <td>10</td>
# <td>1</td>
# <td>3</td>
# <td>15</td>
# <td>4</td>
# <td>2</td>
# <td>11</td>
# <td>6</td>
# <td>7</td>
# <td>12</td>
# <td>0</td>
# <td>5</td>
# <td>14</td>
# <td>9
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>3</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>10</td>
# <td>0</td>
# <td>9</td>
# <td>14</td>
# <td>6</td>
# <td>3</td>
# <td>15</td>
# <td>5</td>
# <td>1</td>
# <td>13</td>
# <td>12</td>
# <td>7</td>
# <td>11</td>
# <td>4</td>
# <td>2</td>
# <td>8
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>13</td>
# <td>7</td>
# <td>0</td>
# <td>9</td>
# <td>3</td>
# <td>4</td>
# <td>6</td>
# <td>10</td>
# <td>2</td>
# <td>8</td>
# <td>5</td>
# <td>14</td>
# <td>12</td>
# <td>11</td>
# <td>15</td>
# <td>1
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>13</td>
# <td>6</td>
# <td>4</td>
# <td>9</td>
# <td>8</td>
# <td>15</td>
# <td>3</td>
# <td>0</td>
# <td>11</td>
# <td>1</td>
# <td>2</td>
# <td>12</td>
# <td>5</td>
# <td>10</td>
# <td>14</td>
# <td>7
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>1</td>
# <td>10</td>
# <td>13</td>
# <td>0</td>
# <td>6</td>
# <td>9</td>
# <td>8</td>
# <td>7</td>
# <td>4</td>
# <td>15</td>
# <td>14</td>
# <td>3</td>
# <td>11</td>
# <td>5</td>
# <td>2</td>
# <td>12
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>4</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>7</td>
# <td>13</td>
# <td>14</td>
# <td>3</td>
# <td>0</td>
# <td>6</td>
# <td>9</td>
# <td>10</td>
# <td>1</td>
# <td>2</td>
# <td>8</td>
# <td>5</td>
# <td>11</td>
# <td>12</td>
# <td>4</td>
# <td>15
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>13</td>
# <td>8</td>
# <td>11</td>
# <td>5</td>
# <td>6</td>
# <td>15</td>
# <td>0</td>
# <td>3</td>
# <td>4</td>
# <td>7</td>
# <td>2</td>
# <td>12</td>
# <td>1</td>
# <td>10</td>
# <td>14</td>
# <td>9
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>10</td>
# <td>6</td>
# <td>9</td>
# <td>0</td>
# <td>12</td>
# <td>11</td>
# <td>7</td>
# <td>13</td>
# <td>15</td>
# <td>1</td>
# <td>3</td>
# <td>14</td>
# <td>5</td>
# <td>2</td>
# <td>8</td>
# <td>4
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>3</td>
# <td>15</td>
# <td>0</td>
# <td>6</td>
# <td>10</td>
# <td>1</td>
# <td>13</td>
# <td>8</td>
# <td>9</td>
# <td>4</td>
# <td>5</td>
# <td>11</td>
# <td>12</td>
# <td>7</td>
# <td>2</td>
# <td>14
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>5</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>2</td>
# <td>12</td>
# <td>4</td>
# <td>1</td>
# <td>7</td>
# <td>10</td>
# <td>11</td>
# <td>6</td>
# <td>8</td>
# <td>5</td>
# <td>3</td>
# <td>15</td>
# <td>13</td>
# <td>0</td>
# <td>14</td>
# <td>9
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>14</td>
# <td>11</td>
# <td>2</td>
# <td>12</td>
# <td>4</td>
# <td>7</td>
# <td>13</td>
# <td>1</td>
# <td>5</td>
# <td>0</td>
# <td>15</td>
# <td>10</td>
# <td>3</td>
# <td>9</td>
# <td>8</td>
# <td>6
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>4</td>
# <td>2</td>
# <td>1</td>
# <td>11</td>
# <td>10</td>
# <td>13</td>
# <td>7</td>
# <td>8</td>
# <td>15</td>
# <td>9</td>
# <td>12</td>
# <td>5</td>
# <td>6</td>
# <td>3</td>
# <td>0</td>
# <td>14
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>11</td>
# <td>8</td>
# <td>12</td>
# <td>7</td>
# <td>1</td>
# <td>14</td>
# <td>2</td>
# <td>13</td>
# <td>6</td>
# <td>15</td>
# <td>0</td>
# <td>9</td>
# <td>10</td>
# <td>4</td>
# <td>5</td>
# <td>3
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>6</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>12</td>
# <td>1</td>
# <td>10</td>
# <td>15</td>
# <td>9</td>
# <td>2</td>
# <td>6</td>
# <td>8</td>
# <td>0</td>
# <td>13</td>
# <td>3</td>
# <td>4</td>
# <td>14</td>
# <td>7</td>
# <td>5</td>
# <td>11
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>10</td>
# <td>15</td>
# <td>4</td>
# <td>2</td>
# <td>7</td>
# <td>12</td>
# <td>9</td>
# <td>5</td>
# <td>6</td>
# <td>1</td>
# <td>13</td>
# <td>14</td>
# <td>0</td>
# <td>11</td>
# <td>3</td>
# <td>8
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>9</td>
# <td>14</td>
# <td>15</td>
# <td>5</td>
# <td>2</td>
# <td>8</td>
# <td>12</td>
# <td>3</td>
# <td>7</td>
# <td>0</td>
# <td>4</td>
# <td>10</td>
# <td>1</td>
# <td>13</td>
# <td>11</td>
# <td>6
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>4</td>
# <td>3</td>
# <td>2</td>
# <td>12</td>
# <td>9</td>
# <td>5</td>
# <td>15</td>
# <td>10</td>
# <td>11</td>
# <td>14</td>
# <td>1</td>
# <td>7</td>
# <td>6</td>
# <td>0</td>
# <td>8</td>
# <td>13
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>7</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>4</td>
# <td>11</td>
# <td>2</td>
# <td>14</td>
# <td>15</td>
# <td>0</td>
# <td>8</td>
# <td>13</td>
# <td>3</td>
# <td>12</td>
# <td>9</td>
# <td>7</td>
# <td>5</td>
# <td>10</td>
# <td>6</td>
# <td>1
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>13</td>
# <td>0</td>
# <td>11</td>
# <td>7</td>
# <td>4</td>
# <td>9</td>
# <td>1</td>
# <td>10</td>
# <td>14</td>
# <td>3</td>
# <td>5</td>
# <td>12</td>
# <td>2</td>
# <td>15</td>
# <td>8</td>
# <td>6
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>1</td>
# <td>4</td>
# <td>11</td>
# <td>13</td>
# <td>12</td>
# <td>3</td>
# <td>7</td>
# <td>14</td>
# <td>10</td>
# <td>15</td>
# <td>6</td>
# <td>8</td>
# <td>0</td>
# <td>5</td>
# <td>9</td>
# <td>2
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>6</td>
# <td>11</td>
# <td>13</td>
# <td>8</td>
# <td>1</td>
# <td>4</td>
# <td>10</td>
# <td>7</td>
# <td>9</td>
# <td>5</td>
# <td>0</td>
# <td>15</td>
# <td>14</td>
# <td>2</td>
# <td>3</td>
# <td>12
# </td></tr>
# <tr>
# <th colspan="17" style="text-align:center">
# </th></tr>
# <tr>
# <th>S<sub>8</sub>
# </th>
# <th>x0000x</th>
# <th>x0001x</th>
# <th>x0010x</th>
# <th>x0011x</th>
# <th>x0100x</th>
# <th>x0101x</th>
# <th>x0110x</th>
# <th>x0111x
# </th>
# <th>x1000x</th>
# <th>x1001x</th>
# <th>x1010x</th>
# <th>x1011x</th>
# <th>x1100x</th>
# <th>x1101x</th>
# <th>x1110x</th>
# <th>x1111x
# </th></tr>
# <tr>
# <th>0yyyy0
# </th>
# <td>13</td>
# <td>2</td>
# <td>8</td>
# <td>4</td>
# <td>6</td>
# <td>15</td>
# <td>11</td>
# <td>1</td>
# <td>10</td>
# <td>9</td>
# <td>3</td>
# <td>14</td>
# <td>5</td>
# <td>0</td>
# <td>12</td>
# <td>7
# </td></tr>
# <tr>
# <th>0yyyy1
# </th>
# <td>1</td>
# <td>15</td>
# <td>13</td>
# <td>8</td>
# <td>10</td>
# <td>3</td>
# <td>7</td>
# <td>4</td>
# <td>12</td>
# <td>5</td>
# <td>6</td>
# <td>11</td>
# <td>0</td>
# <td>14</td>
# <td>9</td>
# <td>2
# </td></tr>
# <tr>
# <th>1yyyy0
# </th>
# <td>7</td>
# <td>11</td>
# <td>4</td>
# <td>1</td>
# <td>9</td>
# <td>12</td>
# <td>14</td>
# <td>2</td>
# <td>0</td>
# <td>6</td>
# <td>10</td>
# <td>13</td>
# <td>15</td>
# <td>3</td>
# <td>5</td>
# <td>8
# </td></tr>
# <tr>
# <th>1yyyy1
# </th>
# <td>2</td>
# <td>1</td>
# <td>14</td>
# <td>7</td>
# <td>4</td>
# <td>10</td>
# <td>8</td>
# <td>13</td>
# <td>15</td>
# <td>12</td>
# <td>9</td>
# <td>0</td>
# <td>3</td>
# <td>5</td>
# <td>6</td>
# <td>11
# </td></tr></tbody></table>
# <p>This table lists the eight S-boxes used in DES. Each S-box replaces a 6-bit input with a 4-bit output. Given a 6-bit input, the 4-bit output is found by selecting the row using the outer two bits, and the column using the inner four bits. For example, an input "<b>0</b>1101<b>1</b>" has outer bits "<b>01</b>" and inner bits "1101"; noting that the first row is "00" and the first column is "0000", the corresponding output for S-box S<sub>5</sub> would be "1001" (=9), the value in the second row, 14th column. (See <a href="/wiki/S-box" title="S-box">S-box</a>).
# </p>
# 
# 
# We implement S_Box reference table using a three dimensional lists:
# 
# - **First dimension:** a Python list with 8 element representing each of these eight S-boxes.
# - **Second dimension:** each of these 8 element will further have four list, one for each row.
# - **Third dimension:** and finally each row itself will be a Python list holding row values indexed between 0–15. 
# 
# So to access a value, the list will have three layer index. For example, if SBOX is the list representing the S-boxes then it can be access as SBOX$[box][row][column]$, where $box$ will be between $0–7$, $row$ $[0–3]$ and $column$ $[0–15]$. 
# 
# 
# 
# **Exercise:** Implement `get_S_box()` that returns the three dimensional list of s_box reference tables.

# In[14]:


def get_S_box():
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
    return SBOX


# In[15]:


print('Sanity Check (get_S_box): ', test_get_S_box(get_S_box))


# The S-boxes carry out the real mixing (confusion). DES uses 8 S-boxes, each with a 6-bit input and a 4-bit output.
# 
# <img src='images/sboxes.jpg'>
# 
# **Exercise:** implement `s_box_calculation()` to convert 48-bit input_block into 32-bit output block. The s_box  table lists the eight S-boxes used in DES. Each S-box replaces a 6-bit input with a 4-bit output. Given a 6-bit input, the 4-bit output is found by selecting the row using the outer two bits, and the column using the inner four bits. 
# 
# 
# <img src='images/s_box_rule.jpg' width=35%>
# 
# For example, an input "011011" has outer bits "01" and inner bits "1101"; noting that the first row is "00" and the first column is "0000", the corresponding output for S-box S5 would be "1001" (=9), the value in the second row, 14th column.

# In[16]:


def s_box_calculation(input_block):
    # get the s_box_reference list
    s_box = get_S_box()
    
    # make an empty BitArray
    output_block = BitArray()
    
    # go throught the input_block every 6 bits 
    for i in range(0, len(input_block), 6):
        
        # calculate the sbox_num based on the index
        sbox_num = int(i / 6)
        
        # get the segment of the input_block correnpoding to 6-bit
        segment = input_block[i:i+6]
        
        # get the outer two bits of this segment
        outer_bits = BitArray(2)
        outer_bits[0] = segment[0]
        outer_bits[1] = segment[5]
        
        # convert the outer bit to int to represent the row index
        row_index = outer_bits.uint
        
        # get the inner four bits
        inner_bits = segment[1:5]
        
        # convert the inner bits to int to represent the column index
        column_index = inner_bits.uint
        
        # get the corresponding value from the s_box
        value = s_box[sbox_num][row_index][column_index]
        
        # convert the value to a binary representation
        binary_value = BitArray(4)
        binary_value[0:4] = format(value, '#06b') 
        
        # add the binary_value to the output
        output_block+= binary_value

    
    
    return output_block
        
    


# In[17]:


print('Sanity Check (s_box_calculation): ', test_s_box_calculation(s_box_calculation))


# ### 2.3 Permutation
# The 32 bit output of S-boxes is then subjected to the straight permutation. The P permutation shuffles the bits of a 32-bit half-block using the following reference table:
# 
# <table class="wikitable" cellspacing="0" style="text-align:right">
# <tbody><tr>
# <td>16</td>
# <td>7</td>
# <td>20</td>
# <td>21</td>
# <td>29</td>
# <td>12</td>
# <td>28</td>
# <td>17
# </td></tr>
# <tr>
# <td>1</td>
# <td>15</td>
# <td>23</td>
# <td>26</td>
# <td>5</td>
# <td>18</td>
# <td>31</td>
# <td>10
# </td></tr>
# <tr>
# <td>2</td>
# <td>8</td>
# <td>24</td>
# <td>14</td>
# <td>32</td>
# <td>27</td>
# <td>3</td>
# <td>9
# </td></tr>
# <tr>
# <td>19</td>
# <td>13</td>
# <td>30</td>
# <td>6</td>
# <td>22</td>
# <td>11</td>
# <td>4</td>
# <td>25
# </td></tr></tbody></table>
# <p>The P permutation shuffles the bits of a 32-bit half-block.
# </p>
# 
# **Exercise:** Implement `get_P_box()` that returns the permutation reference vector. 

# In[18]:


def get_P_box():
    P = (16, 7, 20, 21, 29, 12, 28, 17,
1, 15, 23, 26, 5, 18, 31, 10,
2, 8, 24, 14, 32, 27, 3, 9,
19, 13, 30, 6, 22, 11, 4, 25)
    return P


# In[19]:


print('Sanity Check (get_P_box): ', test_get_P_box(get_P_box))


# **Exercise:** Implement `permutation()` that uses the permutation box to perform permutation on the 32-bit input.

# In[20]:


def permutation(input_block):
    # get permutation box
    P_box = get_P_box()
    
    # make a BitArray with length equal to the input_block
    output_block = BitArray(len(input_block))
    
    # perform permutation based on the P_box
    for i in range(len(P_box)):
        output_block[i] = input_block[P_box[i]-1]
    
    return output_block


# In[21]:


print('Sanity Check (permutation): ', test_permutation(permutation))


# ### 2.4 Round function (F)
# The structure of the round function is presented below:
# 
# <img src='images/round_function.jpg' width=35% >
# 
# **Exercise:** Implement `round_function()`. Use the Python modules `expansion_function()`, `s_box_calculation()`, and `permutation()` to implement DES round function.

# In[22]:


def round_function(input_block, round_key):
    # peform expansion
    output_block = expansion_function(input_block)
    
    # perform XOR with the round_key
    output_block = output_block^round_key
    
    # apply sbox calculation
    output_block = s_box_calculation(output_block)
    
    # apply permutation
    output_block = permutation(output_block)
    
    return output_block
    


# In[23]:


print('Sanity Check (round_function): ', test_round_function(round_function))


# ## 3. Key Generation
# 
# The round-key generator creates sixteen 48-bit keys out of a 56-bit cipher key. The process of key generation is depicted in the following illustration:
# 
# <img src='images/key_generation.jpg' >
# 
# To implement DES key generation, we first need to implement the following functions:
# 1. Parity drop
# 2. Left shift
# 3. Compression P-box

# ### 3.1 Parity Drop - Permuted choice 1 (PC-1)
# The very first step of subkey generation is **parity drop** which is carried out by the following permutation table (PC1), so this step also known as **permutation choice 1 (PC1)**. The permutation table has 56 number between 1–64 in a predefined order and do has 8,16,24,32,40,48,56 and 64 (these are parities bits). 
# 
# <table cellspacing="0" style="text-align:right">
# <tbody><tr>
# <td>
# <table class="wikitable">
# <caption><i>Left</i>
# </caption>
# <tbody><tr>
# <td>57</td>
# <td>49</td>
# <td>41</td>
# <td>33</td>
# <td>25</td>
# <td>17</td>
# <td>9
# </td></tr>
# <tr>
# <td>1</td>
# <td>58</td>
# <td>50</td>
# <td>42</td>
# <td>34</td>
# <td>26</td>
# <td>18
# </td></tr>
# <tr>
# <td>10</td>
# <td>2</td>
# <td>59</td>
# <td>51</td>
# <td>43</td>
# <td>35</td>
# <td>27
# </td></tr>
# <tr>
# <td>19</td>
# <td>11</td>
# <td>3</td>
# <td>60</td>
# <td>52</td>
# <td>44</td>
# <td>36
# </td></tr></tbody></table>
# </td>
# <td>
# <table class="wikitable">
# <caption><i>Right</i>
# </caption>
# <tbody><tr>
# <td>63</td>
# <td>55</td>
# <td>47</td>
# <td>39</td>
# <td>31</td>
# <td>23</td>
# <td>15
# </td></tr>
# <tr>
# <td>7</td>
# <td>62</td>
# <td>54</td>
# <td>46</td>
# <td>38</td>
# <td>30</td>
# <td>22
# </td></tr>
# <tr>
# <td>14</td>
# <td>6</td>
# <td>61</td>
# <td>53</td>
# <td>45</td>
# <td>37</td>
# <td>29
# </td></tr>
# <tr>
# <td>21</td>
# <td>13</td>
# <td>5</td>
# <td>28</td>
# <td>20</td>
# <td>12</td>
# <td>4
# </td></tr></tbody></table>
# </td></tr></tbody></table>
# <p>The "Left" and "Right" halves of the table show which bits from the input <a href="/wiki/Key_(cryptography)" title="Key (cryptography)">key</a> form the left and right sections of the key schedule state. Note that only 56 bits of the 64 bits of the input are selected; the remaining eight (8, 16, 24, 32, 40, 48, 56, 64) were specified for use as <a href="/wiki/Parity_bit" title="Parity bit">parity bits</a>.
# </p>
# 
# The "Left" and "Right" halves of the table show which bits from the input key form the left and right sections of the key schedule state. Note that only 56 bits of the 64 bits of the input are selected; the remaining eight (8, 16, 24, 32, 40, 48, 56, 64) were specified for use as parity bits. 
# 
# **Exercise:** Implement `get_PC1_vector()` that returns the PC1 reference table as a vector. For the Python implementation, the PC1 table can be consider as a tuple object and it value will be used as index to select bit from the initial 64-bit key. 

# In[24]:


def get_PC1_vector():
    PC1 = (57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,
           43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,
           7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,
           28,20,12,4)
    
    return PC1


# In[25]:


print('Sanity Check (get_PC1_vector): ', test_get_PC1_vector(get_PC1_vector))


# **Exercise:** Implement `permutation_choice_1()` that performs parity drop on the initial key. 

# In[26]:


def permutation_choice_1(initial_key):
    # get PC1 table
    PC1 = get_PC1_vector()
    
    # make an BitArray with size of PC1 (e.g., 56 bits)
    output_block = BitArray(len(PC1))
    
    # perform permutation choice 1
    for i in range(len(PC1)):
        output_block[i] = initial_key[PC1[i]-1]
    
    return output_block


# In[27]:


print('Sanity Check (permutation_choice_1): ', test_permutation_choice_1(permutation_choice_1))


# ### 3.2 Circular Left shift
# In every round of key generation, the both half is circularly left shifted and the number of bits for left shifting is round dependent according to the following table:
# 
# <table class="wikitable" cellspacing="0" style="text-align:center">
# <tbody><tr>
# <th>Round<br />number
# </th>
# <th>Number of<br />left rotations
# </th></tr>
# <tr>
# <td>1</td>
# <td>1
# </td></tr>
# <tr>
# <td>2</td>
# <td>1
# </td></tr>
# <tr>
# <td>3</td>
# <td>2
# </td></tr>
# <tr>
# <td>4</td>
# <td>2
# </td></tr>
# <tr>
# <td>5</td>
# <td>2
# </td></tr>
# <tr>
# <td>6</td>
# <td>2
# </td></tr>
# <tr>
# <td>7</td>
# <td>2
# </td></tr>
# <tr>
# <td>8</td>
# <td>2
# </td></tr>
# <tr>
# <td>9</td>
# <td>1
# </td></tr>
# <tr>
# <td>10</td>
# <td>2
# </td></tr>
# <tr>
# <td>11</td>
# <td>2
# </td></tr>
# <tr>
# <td>12</td>
# <td>2
# </td></tr>
# <tr>
# <td>13</td>
# <td>2
# </td></tr>
# <tr>
# <td>14</td>
# <td>2
# </td></tr>
# <tr>
# <td>15</td>
# <td>2
# </td></tr>
# <tr>
# <td>16</td>
# <td>1
# </td></tr></tbody></table>
# 
# 
# **Exercise:** Implement `get_key_rotation()` that returns the number of rotation based on the round number. 

# In[28]:


def get_key_rotation(round_number):
    # define routation table as a dictionary
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
                       16: 1}
    
    return rotation_table[round_number]


# In[29]:


print('Sanity Check (get_key_rotation): ', test_get_key_rotation(get_key_rotation))


# **Exercise:** Implement `circular_shift()` that performs left rotation shift based on the number of rotations.

# In[30]:


def circular_left(input_block, rotation):
    return input_block[rotation:] + input_block[:rotation]


# In[31]:


print('Sanity Check (circular_left): ', test_circular_left(circular_left))


# ### 3.3 Compression P box: Permuted choice 2 (PC-2)
# 
# In each round the circular left shifted both half is passed to compression which utilized a compression table to compress 56 bits key to a 48 bits key. 
# 
# 
# <table class="wikitable" cellspacing="0" style="text-align:right">
# <tbody><tr>
# <td>14</td>
# <td>17</td>
# <td>11</td>
# <td>24</td>
# <td>1</td>
# <td>5
# </td></tr>
# <tr>
# <td>3</td>
# <td>28</td>
# <td>15</td>
# <td>6</td>
# <td>21</td>
# <td>10
# </td></tr>
# <tr>
# <td>23</td>
# <td>19</td>
# <td>12</td>
# <td>4</td>
# <td>26</td>
# <td>8
# </td></tr>
# <tr>
# <td>16</td>
# <td>7</td>
# <td>27</td>
# <td>20</td>
# <td>13</td>
# <td>2
# </td></tr>
# <tr>
# <td>41</td>
# <td>52</td>
# <td>31</td>
# <td>37</td>
# <td>47</td>
# <td>55
# </td></tr>
# <tr>
# <td>30</td>
# <td>40</td>
# <td>51</td>
# <td>45</td>
# <td>33</td>
# <td>48
# </td></tr>
# <tr>
# <td>44</td>
# <td>49</td>
# <td>39</td>
# <td>56</td>
# <td>34</td>
# <td>53
# </td></tr>
# <tr>
# <td>46</td>
# <td>42</td>
# <td>50</td>
# <td>36</td>
# <td>29</td>
# <td>32
# </td></tr></tbody></table>
# 
# 
# The output of compression is the final key of a particular round.
# 
# **Exercise:** Implement `get_PC2_vector()` that returns the PC2 reference table as a vector.

# In[32]:


def get_PC2_vector():
    PC2 = (14,17,11,24,1,5,3,28,15,
           6,21,10,23,19,12,4,26,8,
           16,7,27,20,13,2,41,52,31,
           37,47,55,30,40,51,45,33,
           48,44,49,39,56,34,53,46,
           42,50,36,29,32)
    
    return PC2


# In[33]:


print('Sanity Check (get_PC2_vector): ', test_get_PC2_vector(get_PC2_vector))


# **Exercise:** Implement `compression_pbox()` that performs *permutation_choice_2*. 

# In[34]:


def compression_pbox(input_block):
    # get the PC2 vector
    PC2 = get_PC2_vector()
    
    # make an BitArray with the size of PC2
    output_block = BitArray(len(PC2))
    
    # perform compression_P_box
    for i in range(len(PC2)):
        output_block[i] = input_block[PC2[i]-1]
        
    return output_block


# In[35]:


print('Sanity Check (compression_pbox): ', test_compression_pbox(compression_pbox))


# ### 3.4 Round Keys generation
# **Exercise:** Using `permutation_choice_1()`, `get_key_rotation()`, `circular_left()`, `compression_pbox()` implement the DES key generation for each round based on the initial key shown as below:
# 
# <img src='images/key_generation.jpg' >

# In[36]:


def key_generation(initial_key):
    # make an empty dictionary to store each generate round keys
    round_key = {}
    
    # perform parity drop in initial_key
    output_block = permutation_choice_1(initial_key)
    
    # split output_block into left and right side
    split_index = int(len(output_block)/2)
    L0 = output_block[:split_index]
    R0 = output_block[split_index:]
    
    # getnerate keys for each round
    for round_number in range(1,17):
        # get the rotation based on the current round number
        rotation = get_key_rotation(round_number)
        
        # perfrom left shift on the left and right sides
        new_L = circular_left(L0,rotation)
        new_R = circular_left(R0,rotation)
        
        # apply the compression box on the shifted left and right
        round_key[round_number] = compression_pbox(new_L+new_R)
        
        # update the L0 and R0 for the next round
        L0 = new_L
        R0 = new_R
    
    return round_key
    

    


# In[37]:


print('Sanity Check (key_generation): ', test_key_generation(key_generation))


# ## 4. DES Cipher
# 
# Recall that DES is an implementation of a Feistel Cipher. It uses 16 round Feistel structure. In order to implement DES cipher, first we need to implement Feistel round procedure.
# 
# ### 4.1 Feistel round procedure
# 
# **Exercise:** Implement `feistel_round()` to implement the procedure for each round in Feistel Algorithm. Use `round_function()` implemented in section 2.4 of this notebook as a round function.
# 
# 1. assign right input side to the left output
# 2. apply round function (F) on the right input
# 3. XOR the result with Left input and assign it to Right output
# 4. return left and right output
# 
# 
# 

# In[38]:


def feistel_round(input_block, round_key): 
    
    # get the left and right side of the input block
    split_index = int(len(input_block)/2)
    L_in = input_block[:split_index]
    R_in = input_block[split_index:]
    
    # assign right input side to the left output
    L_out = R_in
    
    # apply round function on the right input
    R_scrambled = round_function(R_in,round_key)
    
    # XOR R_scrambled with Left input and assign it to Right output
    R_out = R_scrambled^L_in
    
    # concatenate left and right output as an output_block
    output_block = L_out+R_out
    
    return output_block


# In[39]:


print('Sanity Check (feistel_round): ', test_feistel_round(feistel_round))


# ### 4.2 DES Cipher
# 
# Now, we have all the required function to implement DES cipher.
# 
# <img src='images/des_enc.png' width=35%>
# 
# 
# **Exercise:** Use `init_permute()`,`key_generation()`,`feistel_round()`, and `final_permutation()` to implement `des_cipher()` to perform DES encryption and decryption. Note that *DES decryption uses the same encryption algorithm, except that the application of the round keys is reversed.* 
# 

# In[40]:


def des_cipher(input_block, initial_key, mode='E'):
    
    # generate key rounds based on the initial key
    round_keys = key_generation(initial_key)
    
        
    # perform initial permutation
    output_block = init_permute(input_block)
    
    
    # perform Feistel round operations
    for i in range(0,16):
        
        # reverse the application of round keys is the mode is not E (encryption)
        round_num = i+1 if mode == 'E' else 16-i
        
        # apply round operation
        output_block = feistel_round(output_block,round_keys[round_num])
        
    
    # perform 32-bit swap
    output_block = output_block[32:]+output_block[:32] 
    
    # perform final permutation
    output_block = final_permutation(output_block)
    
    
    
    return output_block
        
        


# In[41]:


print('Sanity Check (des_cipher): ', test_des_cipher(des_cipher))


# ## 5. Application
# 
# In this application, we are going to get an input from the user, encrypt and decrypt the input text and display the decoded string in the terminal.
# 
# **Exercise:** Write `des_app()` to perform the followings:
# 1. Get an input string from the terminal
# 2. Construct the corresponding binary representation of the input string
# 3. Convert the binary representation into the plain text block each with size of 64 bits
# 4. Encrypt each plain text block using `des_cipher()` and generate the corresponding cipher block 
# 5. Concatenate all the cipher blocks to make a cipher string
# 6. Decode each cipher block in the cipher string
# 7. Convert the decoded binary cipher into the character
# 8. Display the decoded string in the terminal
# 
# 

# In[42]:


def des_app(input_text, initial_key):
    
    # make an empty binary array
    input_bin = BitArray()

    # convert the input to binary arrays
    for char in input_text:
        input_bin += format(ord(char),'#010b')

    # make sure the input_bin is a multiple of 64-bit by padding zeros to the end
    res = 0
    if len(input_bin) % 64:
        res = 64 - len(input_bin) % 64
    for cnt in range(res):
        input_bin += bin(0)
        

    # encode the input string
    cipher_bin = BitArray()
    for i in range(0,len(input_bin), 64):
        # get 64-bit plain_block
        input_block = input_bin[i:i+64]
        # cipher it
        cipher_bin += des_cipher(input_block,initial_key,mode ='E')

    # make an empty string for decoded_input
    decoded_input = ""
    
    # decode the cipher string
    for i in range(0,len(cipher_bin), 64):
        # get each cipher block
        input_block = cipher_bin[i:i+64]
        
        # decrypt the cipher block
        decoded_bin = des_cipher(input_block,initial_key,mode='D')
        
        # convert the cipher block into a character
        for j in range(0,len(decoded_bin),8):
            # get 8-bit BitArray
            word_bin = decoded_bin[j:j+8]
            # convert it to character
            decoded_input += chr(word_bin.uint)
    
    return decoded_input

    


# In[45]:


initial_key = BitArray('0b0000110010111110001100000100100111110011010001010001111001110011')
# get an input string from the terminal
input_text = input('user input: ')
decoded_text = des_app(input_text, initial_key)
# print the decoded string
print("decoded input: ", decoded_text)





