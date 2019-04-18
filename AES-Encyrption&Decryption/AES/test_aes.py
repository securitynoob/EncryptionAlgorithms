#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import inspect, sys
from terminaltables import AsciiTable


# In[ ]:


def test_aes_128(aes_cipher):
    input_block = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    initial_key = bytearray(b'\x8fM\xcd@)\x9d\x1eto<\xd1\tnc\x9e\x94')
    cipher_block = aes_cipher(input_block, initial_key, mode='E')
    decoded_block = aes_cipher(cipher_block, initial_key, mode='D')
    return decoded_block == input_block


# In[ ]:


def test_aes_192(aes_cipher):
    input_block = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    initial_key = bytearray(b'\xa5\x1e\n\xaawHK\xd6\xf6V\xef\xb2\x0f\n\xaf\x94\x0f\xd6\x17W\x13\xaa\x01s')
    cipher_block = aes_cipher(input_block, initial_key, mode='E')
    decoded_block = aes_cipher(cipher_block, initial_key, mode='D')
    return decoded_block == input_block


# In[ ]:


def test_aes_256(aes_cipher):
    input_block = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    initial_key = bytearray(b'$l\xc7L\x905\xbb\xfb\xa3\xffz\xbbyH\xa0\x91\xa6\xbb\xc1)\xe5\x019G\x90\x9e\xddy\xba\x18-\xe5')
    cipher_block = aes_cipher(input_block, initial_key, mode='E')
    decoded_block = aes_cipher(cipher_block, initial_key, mode='D')
    return decoded_block == input_block


# In[ ]:


def test_key_size(aes_cipher):
    input_block = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    initial_key = bytearray(b'\xa5\x1e\n\xaawHK\xd6\xf6V\xef\xb2\x0f\n\xaf\x94\x0f\xd6\x17W\x13')
    try:
        cipher_block = aes_cipher(input_block, initial_key, mode='E')
    except AssertionError:
        return True
    except Exception:
        return False


# In[ ]:


def test_mode(aes_cipher):
    input_block = bytearray(b'\x8c\xd1X\xbaHe\xf4(W\x9a\x0eQ\\\\\xf1T')
    initial_key = bytearray(b'\x8fM\xcd@)\x9d\x1eto<\xd1\tnc\x9e\x94')
    try:
        cipher_block = aes_cipher(input_block, initial_key, mode='F')
    except AssertionError:
        return True
    except Exception:
        return False


# In[ ]:


def get_module_functions(module):
    ret = {}
    for name,obj in inspect.getmembers(module):
        if (inspect.isfunction(obj) and not name.startswith('test')):
            ret[name] = obj
    return ret

