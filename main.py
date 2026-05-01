import os
from adaptive_huffman import AdaptiveHuffmanTree
from static_huffman import static_huffman_compress

def run_demo(text, steps=15):
    print("="*50)
    print(" ADAPTIVE HUFFMAN CODING (FGK) DEMONSTRATION")
    print("="*50)
    
    tree = AdaptiveHuffmanTree()
    encoded_bits = ""
    
    for i, char in enumerate(text):
        verbose = i < steps
        
        status, out_code, action = tree.process_char(char)
        encoded_bits += out_code
        
        if verbose:
            print(f"\nStep {i+1}")
            print(f"Char: {repr(char)}")
            print(f"Status: {status}")
            if status == "NEW":
                # Split the out_code into NYT code and ASCII
                nyt_len = len(out_code) - 8
                nyt_part = out_code[:nyt_len] if nyt_len > 0 else ""
                ascii_part = out_code[-8:]
                if nyt_part:
                    print(f"Output: {nyt_part} + {ascii_part}")
                else:
                    print(f"Output: {ascii_part}")
            else:
                print(f"Code: {out_code}")
                
            print("Action:")
            for act in action.split(', '):
                print(f"- {act}")
            
            print("Then show tree:")
            print(tree.get_ascii_tree())
            
    return encoded_bits

def main():
    # Read input
    input_file = "input.txt"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Creating a default one.")
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("this is an example for adaptive huffman coding. it should compress well because it has repeating characters.")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    if not text:
        print("Empty input file.")
        return

    # Run Adaptive Huffman Demo
    encoded_bits = run_demo(text, steps=15)
    
    # Verify Decoding
    tree = AdaptiveHuffmanTree() # fresh tree for decoding
    decoded_text = tree.decode(encoded_bits)
    if text != decoded_text:
        print("\nERROR: Decoding verification failed! The decoded text does not match the original.")
        return
    else:
        print("\n[OK] Decoding successful. Decoded text perfectly matches original input.")
    
    # Save outputs
    with open("encoded.txt", "w", encoding="utf-8") as f:
        f.write(encoded_bits)
        
    with open("decoded.txt", "w", encoding="utf-8") as f:
        f.write(decoded_text)
        
    # Run Static Huffman for comparison
    static_bits = static_huffman_compress(text)
    
    # Calculate Metrics
    original_size = len(text) * 8
    adaptive_size = len(encoded_bits)
    static_size = len(static_bits)
    
    # Print Metrics
    print("\n" + "="*50)
    print(" COMPRESSION METRICS")
    print("="*50)
    print(f"Original size:      {original_size} bits")
    print(f"Adaptive (FGK):     {adaptive_size} bits")
    print(f"Static Huffman:     {static_size} bits (payload only)")
    
    print("\nExplanation:")
    print("Frequent characters are moved closer to the root of the tree dynamically.")
    print("This results in progressively shorter codes for those characters.")
    print("Static Huffman is better when the full data is known in advance.")
    print("Adaptive Huffman is useful for streaming scenarios where a prior pass is impossible.")

if __name__ == "__main__":
    main()
