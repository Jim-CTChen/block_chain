import utils

class MerkleTreeNode(object):
  def __init__(self, left, right, data):
    if left == None and right == None:
      self.data = utils.sum256_byte(data)
    else:
      self.data = utils.sum256_byte(left.data, right.data)

    self.left = left
    self.right = right


class MerkleTree(object):
  def __init__(self, data_list):
    nodes = []
    for data in data_list:
      nodes.append(MerkleTreeNode(None, None, data))

    while(len(nodes) > 1):
      new_level_nodes = []
      
      for i in range(0, len(nodes), 2):
        node = MerkleTreeNode(nodes[i], nodes[i+1], None)
        new_level_nodes.append(node)
      
      nodes = new_level_nodes
    
    self._root = nodes[0]

  @property
  def root(self):
    return self._root

  @property
  def root_hash(self):
    return self._root.data

