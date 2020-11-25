
class TXInput(object):
  '''
    Args:
      Txid(int): vout's tx id
      vout_idx(int): idx in tx's vout list
      address(string): giver
  '''
  def __init__(self, txid, vout_idx, address):
    self._Txid = txid
    self._vout_idx = vout_idx
    self._address = address

  def __repr__(self):
    return 'TXInput(txid={}, vout_idx={}, address={}'.format(self.txid, self.vout_idx, self.address)

  @property
  def address(self):
    return self._address

  @property
  def txid(self):
    return self._Txid

  @property
  def vout_idx(self):
    return self._vout_idx