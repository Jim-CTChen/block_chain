import argparse

from blockchain import BlockChain
import utils

def my_parser():
  parser = argparse.ArgumentParser()
  sub_parser = parser.add_subparsers(help='commands')

  print_all_parser = sub_parser.add_parser(
    'printchain', help='Print all blocks in blockchain.'
  )
  print_all_parser.set_defaults(func=print_all_blocks)

  print_parser = sub_parser.add_parser(
    'printblock', help='Print block with specified height'
  )
  print_parser.add_argument(
    '-height', help='Print block with height {height}', type=int, required=True
  )
  print_parser.set_defaults(func=print_block_with_height)

  add_parser = sub_parser.add_parser(
    'add_block', help='Mine a new block with given transactions.'
  )
  add_parser.add_argument(
    '-transaction', help='Provide transaction to new block.', type=str, required=True
  )
  add_parser.set_defaults(func=mine_block)

  return parser

def mine_block(args):
  blockchain = BlockChain()
  blockchain.add_block([args.transaction])
  print('Done!')

def print_all_blocks(args):
  blockchain = BlockChain()
  blockchain.print_all_blocks()

def print_block_with_height(args):
  blockchain = BlockChain()
  blockchain.print_block_with_height(args.height)

if __name__ == '__main__':
  parser = my_parser()
  args = parser.parse_args()
  args.func(args)

  # if hasattr(args, 'height'):
  #   print_block_with_height(args.height)
  
  # if hasattr(args, 'transaction'):
  #   mine_block(args.transaction)
  # if hasattr(args, 'printchain'):
  #   print('test')
  # blockchain1.add_block(['This is the first block!'])
  # blockchain1.add_block(['This is the second block!'])
  # blockchain1.add_block(['This is the third block!'])

  # blockchain1.print_all_blocks()
  # blockchain1.print_block_with_height(0)
  # blockchain1.print_block_with_height(1)
  # blockchain1.print_block_with_height(2)
  # blockchain1.print_block_with_height(6)