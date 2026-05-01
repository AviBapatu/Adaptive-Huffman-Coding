class Node:
    def __init__(self, symbol=None, weight=0, order=0):
        self.symbol = symbol
        self.weight = weight
        self.order = order
        self.left = None
        self.right = None
        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None
