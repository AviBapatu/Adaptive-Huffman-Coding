import heapq
from collections import Counter

class StaticNode:
    def __init__(self, symbol, weight):
        self.symbol = symbol
        self.weight = weight
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.weight < other.weight

def build_static_huffman_tree(text):
    if not text:
        return None
        
    freqs = Counter(text)
    heap = [StaticNode(sym, wt) for sym, wt in freqs.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = StaticNode(None, left.weight + right.weight)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)
        
    return heap[0] if heap else None

def generate_static_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}
        
    if node is not None:
        if node.symbol is not None:
            codes[node.symbol] = current_code if current_code else "0"
        generate_static_codes(node.left, current_code + "0", codes)
        generate_static_codes(node.right, current_code + "1", codes)
        
    return codes

def static_huffman_compress(text):
    if not text:
        return ""
        
    tree = build_static_huffman_tree(text)
    codes = generate_static_codes(tree)
    
    encoded = "".join(codes[char] for char in text)
    # Return encoded bits and the tree (or codes) to allow calculating size including overhead if needed
    # But for a simple metric, usually just the payload or payload + alphabet size is used.
    # We will just return the encoded string.
    return encoded
