import pickle
import sys
import utils

from collections import defaultdict
from tx_input import TXInput
from transaction import UTXOSet, CoinBaseTx, UTXOTx, Transaction
from block import Block
from db import Bucket
class BlockChain(object):
  bucket = 'blocks'
  db_file = 'block_chain.db'
  # last_block = 'l'
  genesis_block_data = 'This is a Genesis block!'

  def __init__(self, address=None):
    self._bucket = Bucket(BlockChain.db_file, BlockChain.bucket)
    
    try:
      self._address = self._bucket.get('address')
      self._last_hash = self._bucket.get('l')
      self._last_block = pickle.loads(self._bucket.get(self._last_hash))
    except KeyError:
      if not address: # no data & no given address
        print('Block Chain not created yet!\nPlease create a new block chain with given address first!')
        sys.exit()
      else:
        self.reset(address)


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

  def reset(self, address):
    self._bucket.reset()
    coinbaseTx = CoinBaseTx(address)
    genesis_block = Block(0, '', [coinbaseTx])
    genesis_block.set_hash()
    self._put_block(genesis_block)
    self._address = address
    self._last_block = genesis_block
    self._last_hash = genesis_block.hash
    self._bucket.put('address', address)
    self._bucket.commit()
    return self

  @property
  def blocks(self):
    current_hash = self._last_hash
    while current_hash:
      encoded_block = self._bucket.get(current_hash)
      block = pickle.loads(encoded_block)
      yield block
      current_hash = block.prev_hash

  @property
  def address(self):
    return self._address

  @property
  def last_block(self):
    return self._last_block

  @property
  def last_hash(self):
    return self._last_hash

  def print_all_blocks(self):
    for block in self.blocks:
      block.print_block()
    
  def print_block_with_height(self, height):
    for block in self.blocks:
      if block.height == height:
        block.print_block()
        return
    print('No block with height {} found!'.format(height))

  def find_all_utxo(self):
    utxo = defaultdict(list)
    stxo = defaultdict(list)

    for block in self.blocks:
      for tx in block.transactions:

        try:
          for out_idx, out in enumerate(tx.vout):
            if stxo[tx.id]:
              for spent_out in stxo[tx.id]:
                if spent_out == out_idx:
                  raise utils.ContinueIt
            
            utxo[tx.id].append(out)
        except utils.ContinueIt:
          pass

        if not isinstance(tx, CoinBaseTx):
          for vin in tx.vin:
            stxo[tx.id].append(vin.vout_idx)
    return utxo