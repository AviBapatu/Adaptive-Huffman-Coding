# Adaptive Huffman Coding (FGK Algorithm) Demonstration

Adaptive Huffman Coding is a lossless data compression technique based on dynamic tree construction. Unlike traditional static Huffman coding, which requires an initial pass over the data to determine symbol frequencies, Adaptive Huffman encoding constructs and updates the Huffman tree on-the-fly (one-pass encoding) as the data is processed. This demonstration uses the Faller-Gallager-Knuth (FGK) algorithm to showcase dynamic tree updates, correct bitwise encoding and decoding boundaries, and performance metrics.

## Features

* **Adaptive Huffman Encoding (FGK):** Fully implements the theoretical FGK model without relying on prior frequency knowledge.
* **Dynamic Tree Updates:** Continuously adjusts character weights and structural layout on every transmission.
* **NYT (Not Yet Transmitted) Node Handling:** Safely delegates out-of-tree bits to explicit 8-bit ASCII fallbacks when encountering novel symbols.
* **Real-time Encoding and Decoding:** Strictly processes characters synchronously as a stream.
* **Step-by-step Visualization:** Renders the ASCII tree evolution alongside character identity logs, explicitly isolating dynamic tree restructurings and node swaps.
* **Compression Metrics:** Provides an end-to-end analytical comparison between Adaptive and Static Huffman compression yields.

## Theory

### What is Huffman Coding?
Traditional Huffman Coding is an optimal prefix algorithm that assigns variable-length binary codes to input characters. Characters that appear more frequently are assigned shorter codes to reduce the overall size of the data. 

### What is Adaptive Huffman Coding?
Adaptive Huffman Coding evaluates frequency distributions dynamically. It relies on a one-pass algorithm where both the encoder and decoder simultaneously build matching trees driven by the incoming bitstream. This makes it suitable for streaming scenarios where analyzing the entire dataset in advance is impossible.

### FGK Algorithm Basics
* **NYT Node:** A special "Not Yet Transmitted" node with zero weight is kept in the tree. When a new character appears, the NYT node splits to accommodate the new character and a new NYT placeholder.
* **Encoding Rules:** 
    * *New Symbols:* The current NYT path is transmitted, followed by the fixed-length (e.g., 8-bit ASCII) representation of the character.
    * *Existing Symbols:* The exact current path to the symbol's existing node is transmitted.
* **Tree Update Mechanism:** After every character is transmitted (or received), the tree traverses upward from the leaf node to the root, incrementing node weights along the way.
* **Sibling Property:** The fundamental rule of the FGK algorithm requires the tree nodes to remain sorted primarily by weight. If incrementing a node's weight violates this grouping, it must immediately swap with the highest-ordered node in its current weight block (the "block leader") before the weight is finalized.

## Project Structure

```
adaptive-huffman/
│
├── node.py                   # Contains the standard Node class implementation
├── adaptive_huffman_tree.py  # Core Adaptive Huffman Tree class handling the FGK logic
├── static_huffman.py         # Standard 2-pass Static Huffman logic for baseline metric comparison
├── main.py                   # Demonstration script overseeing narrative steps and visual outputs
├── input.txt                 # Target dataset sample fed into the algorithms
├── encoded.txt               # Output file containing the final binary representation (1s and 0s)
└── decoded.txt               # Output file containing the reconstructed text sequence
```

## How It Works

1. **Start with NYT node:** The tree begins empty, populated solely by a weight-0 NYT node.
2. **Process characters one by one:** The stream is read character by character.
3. **Transmission:**
    * *If new character:* Emit the NYT code + the ASCII representation.
    * *If existing character:* Emit the existing character's dynamic Huffman code.
4. **Update and Swap:** The tree structurally adapts. If a node needs to increment its weight, the script verifies if it is the "block leader". If not, the node swaps places with the leader to maintain the sibling property.

## Example Output

```text
Step 3
Char: 'c'
Status: NEW
Output: NYT code 00 + ASCII('c') = 0001100011
Action:
- Insert node for 'c'
- split NYT
- Found block leader (weight = 1)
- Swapped nodes: (* <-> a)
- Maintaining sibling property: nodes reordered within same weight group
Then show tree:
    /-- (a,1)
--- (*,3)
|   |   /-- (b,1)
|   \-- (*,2)
|       |   /-- (c,1)
|       \-- (*,1)
|           \-- (NYT,0)
```

## How to Run

Ensure you have Python 3.x installed. Provide your test string in `input.txt`, and execute the demonstration script in your terminal:

```bash
python main.py
```

The script will render the first 15 characters of the dataset in verbose mode (displaying the tree and logs) before silently running the remainder to compute metrics.

## Results & Metrics

At the end of the demonstration, the script calculates:
* **Original Size:** Length of the raw uncompressed ASCII text.
* **Adaptive (FGK) Size:** The total length of the dynamically generated bitstream.
* **Static Huffman Size:** The total length of the conventionally mapped bitstream.

**Note:** Static Huffman appears more efficient initially because it leverages complete frequency knowledge in advance. However, static methods natively require transmitting the frequency table or tree to the decoder (which incurs overhead not included in raw payload metrics). Adaptive Huffman requires no such overhead, excelling in unpredictable data streams.

## Key Observations

* **Proximity to Root:** The dynamic weighting effectively migrates high-frequency characters toward the root. Their respective code paths shorten, decreasing overall sequence footprints.
* **Dynamic Structuring over Frequency:** In datasets where all characters share identical frequencies, variations in resulting bit lengths manifest explicitly as a result of tree structure evolution during the sequential updates rather than static frequency weighting.

## Limitations

* **Execution Speed:** Substantially slower than static Huffman due to continuous structural adjustments and re-balancing over O(n) array lookups.
* **Input Dependency:** Compression efficiency is fundamentally tied to the arbitrary sequence order of the incoming data, not just uniform distribution.
* **Update Overhead:** Traversing from leaves to the root during every sequence imposes consistent processing friction.

## Future Improvements

* Integrate comprehensive GUI/Web visualizers to animate the tree's traversal and swapping behavior.
* Expand the pipeline to natively ingest true binary payload packaging instead of character mapping streams.
* Restructure weight tracking logic to abstract nodes into explicit O(1) linked-blocks, significantly boosting execution speeds for highly randomized, large-scale data points.
