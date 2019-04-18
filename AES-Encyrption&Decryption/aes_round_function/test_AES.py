#!/usr/bin/env python
# coding: utf-8

# In[3]:


import inspect, sys
from terminaltables import AsciiTable


# In[4]:


def test_add_round_key(add_round_key):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    input_key = bytearray(b'D8\xa2\\\xf7c\x12\xd4\xee\xb3\xc2$hy\xbf\x00\xb3\xcf\x8e\xd1:\xbf\x12\x9a0\x97\xad\x96\xb4B\xd6\xd1')
    round_key = input_key[:16]
    output_state = add_round_key(input_state, round_key)
    return input_state == add_round_key(output_state, round_key)


# In[5]:


def test_sub_bytes(sub_bytes):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    output_state_E = sub_bytes(input_state,'E')
    output_state_D = sub_bytes(output_state_E,'D')
    return input_state == output_state_D


# In[6]:


def test_rotate(rotate):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    rotated_word = rotate(word=input_state[:4], n=2)
    return input_state[:4] == rotate(word=rotated_word, n=-2)


# In[7]:


def test_shift_rows(shift_rows):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    shifted_state_E = shift_rows(input_state,'E')
    shifted_state_D = shift_rows(shifted_state_E,'D')
    return input_state == shifted_state_D


# In[8]:


def test_reshape(reshape_as_matrix, reshape_as_state):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    output_matrix = reshape_as_matrix(input_state)
    output_state = reshape_as_state(output_matrix)
    return input_state == output_state


# In[9]:


def test_mix_column(mix_column):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    encrypt = mix_column(input_state, mode='E')
    decrypt = mix_column(encrypt, mode='D')
    return decrypt == input_state


# In[10]:


def test_aes_round(add_round_key, aes_round_enc, aes_round_dec):
    input_state = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    input_key = bytearray(b'D8\xa2\\\xf7c\x12\xd4\xee\xb3\xc2$hy\xbf\x00\xb3\xcf\x8e\xd1:\xbf\x12\x9a0\x97\xad\x96\xb4B\xd6\xd1')
    round_key = input_key[:16]
    encrypt_state = add_round_key(input_state, round_key)
    encrypt_state = aes_round_enc(encrypt_state, round_key)
    encrypt_state = aes_round_enc(encrypt_state, round_key, last_round=True)

    decrypt_round = add_round_key(encrypt_state, round_key)
    decrypt_round = aes_round_dec(decrypt_round, round_key)
    decrypt_round = aes_round_dec(decrypt_round, round_key, last_round=True)

    return decrypt_round == input_state


# In[ ]:


def get_module_functions(module):
    ret = {}
    for name,obj in inspect.getmembers(module):
        if (inspect.isfunction(obj) and not name.startswith('test')):
            ret[name] = obj
    return ret