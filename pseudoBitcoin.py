import argparse

from transaction import UTXOSet, UTXOTx, CoinBaseTx
from blockchain import BlockChain
import utils

def my_parser():
  parser = argparse.ArgumentParser()
  sub_parser = parser.add_subparsers(help='commands')
  
  parser.set_defaults(func=idle)

  create_blockchain_parser = sub_parser.add_parser(
    'createblockchain', help='Create a blockchain with a coinbase Tx reward to {address}.'
  )
  create_blockchain_parser.add_argument(
    '-address', help='Give the coinbase Tx reward of genesis block to address.', type=str, required=True
  )
  create_blockchain_parser.set_defaults(func=create_blockchain)


  print_all_parser = sub_parser.add_parser(
    'printchain', help='Print all blocks in blockchain.'
  )
  print_all_parser.set_defaults(func=print_all_blocks)


  print_parser = sub_parser.add_parser(
    'printblock', help='Print block with specified height.'
  )
  print_parser.add_argument(
    '-height', help='Print block with height {height}.', type=int, required=True
  )
  print_parser.set_defaults(func=print_block_with_height)


  balance_parser = sub_parser.add_parser(
    'getbalance', help='Get balance by address.'
  )
  balance_parser.add_argument(
    '-address', help='Specified address.', type=str, required=True
  )
  balance_parser.set_defaults(func=get_balance_by_address)


  add_parser = sub_parser.add_parser(
    'send', help='Mine a new block and record sending transaction.'
  )
  add_parser.add_argument(
    '-from', help='Transaction\'s money giver.', type=str, required=True, dest='From'
  )
  add_parser.add_argument(
    '-to', help='Transaction\'s money receiver.', type=str, required=True
  )
  add_parser.add_argument(
    '-amount', help='Transaction amount.', type=int, required=True
  )
  add_parser.set_defaults(func=mine_block)

  return parser

def idle(args):
  print('positional arguments:\n { createblockchain, printchain, printblock, add_block }')

def create_blockchain(args):
  bc = BlockChain(args.address).reset(args.address)
  UTXOSet(bc).reset()
  print('Create successfully! Miner address is set to {}'.format(args.address))

def mine_block(args):
  blockchain = BlockChain()
  utxo_set = UTXOSet(blockchain)
  utxo_tx = UTXOTx(args.From, args.to, args.amount, utxo_set)
  coin_base_tx = CoinBaseTx(blockchain.address)
  blockchain.add_block([coin_base_tx, utxo_tx])
  utxo_set.update(blockchain.last_block)

  print('Done!')

def print_all_blocks(args):
  blockchain = BlockChain()
  blockchain.print_all_blocks()

def print_block_with_height(args):
  blockchain = BlockChain()
  blockchain.print_block_with_height(args.height)

def get_balance_by_address(args):
  blockchain = BlockChain()
  utxo_set = UTXOSet(blockchain)
  balance, utxos = utxo_set.find_utxo_by_address(args.address)
  print('balance: {}'.format(balance))
  print('transaction ID with spendable money:')
  for utxo in utxos:
    print(utxo)

if __name__ == '__main__':
  parser = my_parser()
  args = parser.parse_args()
  args.func(args)