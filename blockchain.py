import utils

from block import Block

class BlockChain(object):
  def __init__(self):
    self._blocks = []
    self._height = 0
    self.add_genesis_block()

  def add_block(self, transactions):
    self._height += 1
    new_block = Block(self._height, self._blocks[-1].hash, transactions)
    new_block.set_hash()
    self._blocks.append(new_block)
  
  def add_genesis_block(self):
    g_block = Block(0, '', ['This is a Genesis block!'])
    g_block.set_hash()
    self._blocks.append(g_block)

  def print_all_blocks(self):
    for block in self._blocks:
      print('block {}:'.format(block.height))
      print('hash {}:'.format(block.hash.zfill(64)))
      block.print_transactions()