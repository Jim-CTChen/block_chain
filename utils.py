import hashlib

def encode(str, code='utf-8'):
  return str.encode(code)

def decode(str, code='utf-8'):
  return str.decode(code)

def sum256_byte(*args) -> bytes:
  h = hashlib.sha256()
  for arg in args: # arg needs to be encoded
    h.update(arg)
  print(type(h.digest()))
  return h.digest()


def sum256_hex(*args) -> str:
  h = hashlib.sha256()
  for arg in args: # arg needs to be encoded
    h.update(arg)
  return h.hexdigest()