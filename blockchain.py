import utils
import pickle

from block import Block
from db import Bucket
class BlockChain(object):
  bucket = 'blocks'
  db_file = 'block_chain.db'
  last_block = 'l'
  genesis_block_data = 'This is a Genesis block!'

  def __init__(self, address = ''):
    self._bucket = Bucket(BlockChain.db_file, BlockChain.bucket)
    
    try:
      self._last_hash = self._bucket.get('l')
      self._last_block = pickle.loads(self._bucket.get(self._last_hash))
    except KeyError:
      # if not address:
      #   self._last_hash = None
      # else:
      genesis_block = Block(0, '', [BlockChain.genesis_block_data])
      genesis_block.set_hash()
      self._put_block(genesis_block)


  def _put_block(self, block):
    self._last_block = block
    self._last_hash = block.hash
    self._bucket.put('l', block.hash)
    self._bucket.put(block.hash, block.serialize())
    self._bucket.commit()

  
  def add_block(self, transactions):
    '''
    Args:
      transactions (list): List of transactions
    '''
    current_height = self._last_block.height
    new_block = Block(current_height+1, self._last_hash, transactions)
    new_block.set_hash()
    self._put_block(new_block)

  @property
  def blocks(self):
    current_hash = self._last_hash
    while current_hash:
      encoded_block = self._bucket.get(current_hash)
      block = pickle.loads(encoded_block)
      yield block
      current_hash = block.prev_hash

  def print_all_blocks(self):
    for block in self.blocks:
      block.print_block()
    
  def print_block_with_height(self, height):
    for block in self.blocks:
      if block.height == height:
        block.print_block()
        return
    print('No block with height {} found!'.format(height))