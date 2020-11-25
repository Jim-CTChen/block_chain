
class TXOutput(object):
  '''
    Args:
      value(int): value of output
      address(string): owner
  '''
  subsidy = 10
  def __init__(self, value, address):
    self._value = value
    self._address = address
  
  def __repr__(self):
    return 'TXOutput(value={}, address={})'.format(self.value, self.address)

  @property
  def value(self):
    return self._value

  @property
  def address(self):
    return self._address