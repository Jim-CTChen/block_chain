import pickle
import sys
import random
import string
import utils
from collections import defaultdict
from db import Bucket
from tx_input import TXInput
from tx_output import TXOutput


class Transaction(object):
  def __init__(self, id, input, output):
    self._id = id
    self._vin = input
    self._vout = output

  def set_id(self):
    self._id = utils.sum256_hex(pickle.dumps(self))

  def __repr__(self):
    return 'Transaction(id={}, vin={}, vout={}'.format(self.id, self.vin, self.vout)

  @property
  def id(self):
    return self._id

  @property
  def vout(self):
    return self._vout

  @property
  def vin(self):
    return self._vin


class CoinBaseTx(object):
  def __init__(self, address):
    random_address = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(20))
    vout = [TXOutput(TXOutput.subsidy, address)]
    vin = [TXInput('', None, random_address)]
    self._tx = Transaction(None, vin, vout)
    self._tx.set_id()

  def __repr__(self):
    return 'Coinbase Transaction\n\tid = {}\n\tvout = {})'.format(self.id, self.vout)

  @property
  def id(self):
    return self._tx.id

  @property
  def vout(self):
    return self._tx.vout

  @property
  def vin(self):
    return self._tx.vin


class UTXOTx(object):
  '''
  Usual UTXO transaction

  Args:
    from_addr(string): money source address
    to_addr(string): money destination address
    amount(int): amount of money
    utxo_set(object): unspent transaction set
  '''

  def __init__(self, from_addr, to_addr, amount, utxo_set):
    inputs = []
    outputs = []

    accumulate, spendable_outputs = utxo_set.find_spendable_output(
      from_addr, amount)
    if accumulate < amount:
      print('Not enough funds! QQ')
      sys.exit()

    else:
      for tx_id, outs in spendable_outputs.items():
        for out_idx in outs:
          inputs.append(TXInput(tx_id, out_idx, from_addr))

    outputs.append(TXOutput(amount, to_addr))
    if accumulate > amount:
      outputs.append(TXOutput(accumulate-amount, from_addr))

    self._tx = Transaction(None, inputs, outputs)
    self._tx.set_id()
    self._utxo_set = utxo_set

  def __repr__(self):
    return 'UTXO Transaction\n\tid = {}\n\tvin = {}\n\tvout = {})'.format(self.id, self.vin, self.vout)

  @property
  def id(self):
    return self._tx.id

  @property
  def vin(self):
    return self._tx.vin

  @property
  def vout(self):
    return self._tx.vout


class UTXOSet(object):
  db_file = 'block_chain.db'
  bucket = 'utxo'

  def __init__(self, block_chain):
    self._bucket = Bucket(UTXOSet.db_file, UTXOSet.bucket)
    self._bc = block_chain

  def reset(self):
    self._bucket = Bucket(UTXOSet.db_file, UTXOSet.bucket)
    self._bucket.reset()
    utxos = self._bc.find_all_utxo()
    for tx_id, vout_idx in utxos.items():
        self._bucket.put(tx_id, utils.serialize(vout_idx))

    self._bucket.commit()

  def update(self, block):
    self._bucket = Bucket(UTXOSet.db_file, UTXOSet.bucket)
    transactions = block.transactions
    for tx in transactions:
      if not isinstance(tx, CoinBaseTx):
        for vin in tx.vin:
          update_outs = []
          encoded_outs = self._bucket.get(vin.txid)
          outs = utils.deserialize(encoded_outs)

          for out_idx, out in enumerate(outs):
            if out_idx != vin.vout_idx:
              update_outs.append(out)

          if len(update_outs) == 0:
            self._bucket.delete(vin.txid)
          else:
            self._bucket.put(
              vin.txid, utils.serialize(update_outs))

      new_output = [out for out in tx.vout]
      self._bucket.put(tx.id, utils.serialize(new_output))
    self._bucket.commit()

  def find_spendable_output(self, address, amount):
    accumulate = 0
    spendable_output = defaultdict(list)

    for tx_id, outs in self._bucket.kv.items():
      outs = utils.deserialize(outs)

      for out_idx, out in enumerate(outs):
        if out.address == address:
          accumulate += out.value
          spendable_output[tx_id].append(out_idx)
          if accumulate >= amount:
            return accumulate, spendable_output

    return accumulate, spendable_output

  def find_utxo_by_address(self, address):
    accumulate = 0
    utxos = defaultdict(list)

    for tx_id, outs in self._bucket.kv.items():
      outs = utils.deserialize(outs)

      for out_idx, out in enumerate(outs):
        if out.address == address:
          accumulate += out.value
          utxos[tx_id].append(out_idx)

    return accumulate, utxos
