import sys
import utils

class Pow(object):
  max_nonce = sys.maxsize

  def __init__(self, block):
    self._block = block
    self._target = 1 << (256 - block.target_bits)
  
  def prepare_data(self, nonce):
    data = [str(nonce),
            self._block.prev_hash,
            self._block.hash_transactions()]
    return utils.encode(''.join(data))

  def run(self):
    nonce = 0
    # print('Mining a new block')
    while nonce < Pow.max_nonce:
      prepared_data = self.prepare_data(nonce)
      hash_hex = utils.sum256_hex(prepared_data)
      hash_int = int(hash_hex, 16)
      # sys.stdout.write("%s \r" % (hash_hex))
      if self._target > hash_int:
        break
      else: nonce += 1

    return nonce, hash_hex

  def validate(self):
    data = self.prepare_data(self._block.nonce)
    hash_hex = utils.sum256_hex(data)
    hash_int = int(hash_hex, 16)
    return self._target > hash_int

