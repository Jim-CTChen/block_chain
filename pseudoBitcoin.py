import argparse

from blockchain import BlockChain
import utils

blockchain1 = BlockChain()
blockchain1.add_block(['This is the first block!'])
blockchain1.print_all_blocks()