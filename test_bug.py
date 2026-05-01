import os
from adaptive_huffman_tree import AdaptiveHuffmanTree

def test():
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()
        
    text = text.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    text = text.encode('ascii', errors='ignore').decode('ascii')
    
    tree = AdaptiveHuffmanTree()
    encoded = tree.encode(text)
    
    decoder = AdaptiveHuffmanTree()
    decoded = decoder.decode(encoded)
    
    if text != decoded:
        print("Mismatch!")
    else:
        print("Success! The unicode sanitization fixed it.")

test()
