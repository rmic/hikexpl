from io import BytesIO
import re
from itertools import cycle
from pprint import pprint

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
def pad_to_16(s):
  """Pads the input string with null bytes to a multiple of 16 bytes."""
  r = len(s) % 16
  if r != 0:
    s += b'\0' * (16 - r)
  return s

def xor_bytes(data, key):
    return bytes(a ^ b for a, b in zip(data, cycle(key)))
def decrypt(ciphertext, hex_key, xor_key, encoding='ISO-8859-1'):
    key = bytes.fromhex(hex_key)
    ciphertext = pad_to_16(ciphertext)
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = plaintext.rstrip(b"\0")
    with BytesIO(plaintext) as f:
        xored = xor_bytes(f.read(), xor_key)

    return xored.decode(encoding)

def extract_words(file, min_length=2):
  """Extracts all words (alphanumeric, some symbols) with a minimum length from a file.

  Args:
      file: The file object or string containing the data.
      min_length: The minimum length for a word to be considered (default 2).

  Returns:
      A list of extracted words.
  """
  chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
  pattern = re.compile('[%s]{%d,}' % (chars, min_length))
  return pattern.findall(file)  # Handle both file and string input

def find_admin_index(words, keyword='admin'):
    """Finds the index of the first occurrence of the keyword in a list of words.

    Args:
      words: The list of words to search.
      keyword: The keyword to search for (default 'admin').

    Returns:
      The index of the first occurrence of the keyword,
      raises a KeyError if not found.
    """

    if keyword not in words:
        raise KeyError(f"Keyword '{keyword}' not found in list")
    indices = [i for i, x in enumerate(words) if x == keyword]
    return indices[-1]


def extract(target, word_list, admin_index):
    """Builds the desired result string based on target, word list, and admin index.

    Args:
      target: The base string to start the result.
      word_list: The list of extracted words.
      admin_index: The index of the 'admin' keyword (from find_admin_index).

    Returns:
        The a tuple containing the admin name and password
    Raises:
        IndexError if the admin_index is invalid
    """

    return (target, word_list[admin_index], word_list[admin_index + 1])


def split_list(iteration, n):
   k, m = divmod(len(iteration), n)
   split_data = [iteration[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]
   return split_data