import hashlib
import pickle

def encode(str, code='utf-8'):
  '''
    encode string into bytes by utf-8
  '''
  return str.encode(code)

def decode(str, code='utf-8'):
  '''
    decode bytes into string by utf-8
  '''
  return str.decode(code)

def sum256_byte(*args) -> bytes:
  '''
    hash function
    input type: bytes
    output type: bytes
  '''
  h = hashlib.sha256()
  for arg in args: # arg needs to be encoded
    h.update(arg)
  return h.digest()


def sum256_hex(*args) -> str:
  '''
    hash function
    input type: bytes
    output type: hex string
  '''
  h = hashlib.sha256()
  for arg in args: # arg needs to be encoded
    h.update(arg)
  return h.hexdigest()

def serialize(obj):
  return pickle.dumps(obj)

def deserialize(obj):
  return pickle.loads(obj)


class ContinueIt(Exception):
    pass