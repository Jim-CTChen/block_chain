import time
import random
import pickle
import binascii

import utils
from merkle_tree import MerkleTree
from pow import Pow

class Block(object):
  def __init__(self, height = 0, prev_hash = '', transaction = []):
    self._height = height
    self._hash = None
    self._prev_hash = prev_hash
    self._timestamp = utils.encode(str(int(time.time())))
    self._target_bits = 4
    self._nonce = None
    self._transaction = transaction

  @property
  def hash(self):
    return self._hash
  
  @property
  def height(self):
    return self._height

  @property
  def nonce(self):
    return self._nonce

  @property
  def time(self):
    return self._timestamp

  @property
  def prev_hash(self):
    return self._prev_hash

  @property
  def transactions(self):
    return self._transaction

  @property
  def target_bits(self):
    return self._target_bits

  def print_transactions(self):
    print('Transactions :')
    for tx in self._transaction:
      print(tx)

  def print_block(self):
    print('#####################################################################################')
    print('Block height      : {}'.format(self.height))
    print('Previous hash     : {}'.format(self.prev_hash))
    print('Hash              : {}'.format(self.hash))
    print('Hash transactions : {}'.format(self.hash_transactions()))
    self.print_transactions()
    print('#####################################################################################')

  def hash_transactions(self):
    '''
     get hashed transactions by merkle tree
    '''
    tx_byte_list = [utils.serialize(tx) for tx in self._transaction]
    merkle_tree = MerkleTree(tx_byte_list)
    return utils.decode(binascii.hexlify(merkle_tree.root_hash))

  def set_hash(self):
    pow = Pow(self)
    self._nonce, self._hash = pow.run()
    while not pow.validate():
      random.shuffle(self._transaction)
      self._nonce, self._hash = pow.run()

  def serialize(self):
    return pickle.dumps(self)

  def deserialize(self, data):
    return pickle.loads(data)
