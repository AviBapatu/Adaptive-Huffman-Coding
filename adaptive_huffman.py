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


class AdaptiveHuffmanTree:
    def __init__(self):
        self.MAX_ORDER = 512
        self.nyt_node = Node(symbol="NYT", weight=0, order=self.MAX_ORDER)
        self.root = self.nyt_node
        self.nodes_by_symbol = {}
        self.nodes_by_order = {self.MAX_ORDER: self.nyt_node}

    def get_code(self, target_node):
        code = ""
        curr = target_node
        while curr.parent is not None:
            if curr.parent.left == curr:
                code = "0" + code
            else:
                code = "1" + code
            curr = curr.parent
        return code

    def _swap_nodes(self, n1, n2):
        if n1.parent == n2 or n2.parent == n1:
            return  # Can't swap parent and child

        p1, p2 = n1.parent, n2.parent

        # Swap in parents
        if p1.left == n1:
            p1.left = n2
        else:
            p1.right = n2

        if p2.left == n2:
            p2.left = n1
        else:
            p2.right = n1

        # Swap parent pointers
        n1.parent, n2.parent = p2, p1

        # Swap orders
        n1.order, n2.order = n2.order, n1.order

        # Update dictionary
        self.nodes_by_order[n1.order] = n1
        self.nodes_by_order[n2.order] = n2

    def _find_block_leader(self, weight):
        """Finds the node with the highest order for a given weight. O(n) lookup."""
        leader = None
        max_order = -1
        for order, node in self.nodes_by_order.items():
            if node.weight == weight and order > max_order:
                max_order = order
                leader = node
        return leader

    def _update_tree(self, node):
        actions = []
        curr = node
        while curr is not self.root:
            leader = self._find_block_leader(curr.weight)
            # If a leader exists, is different from curr, and is not curr's parent, swap them
            if leader is not None and leader != curr and leader != curr.parent:
                actions.append(f"Found block leader (weight = {curr.weight})")
                sym1 = repr(curr.symbol) if curr.symbol else "*"
                sym2 = repr(leader.symbol) if leader.symbol else "*"
                if sym1.startswith("'") and sym1.endswith("'"): sym1 = sym1[1:-1]
                if sym2.startswith("'") and sym2.endswith("'"): sym2 = sym2[1:-1]
                actions.append(f"Swapped nodes: ({sym1} <-> {sym2})")
                actions.append("Maintaining sibling property: nodes reordered within same weight group")
                self._swap_nodes(curr, leader)
            
            # Increment weight
            curr.weight += 1
            curr = curr.parent
        
        # Increment root weight
        self.root.weight += 1
        
        if not actions:
            actions.append("No swap required (already block leader)")
            
        return actions

    def process_char(self, char):
        """
        Processes a single character, updating the tree.
        Returns: (status, output_code, action_summary)
        """
        if char not in self.nodes_by_symbol:
            # 1. New character
            nyt_code = self.get_code(self.nyt_node)
            ascii_code = format(ord(char), '08b')
            output_code = nyt_code + ascii_code
            status = "NEW"

            # Split NYT node
            old_nyt = self.nyt_node
            
            # Create new NYT and new char node
            new_nyt = Node(symbol="NYT", weight=0, order=old_nyt.order - 2)
            new_char_node = Node(symbol=char, weight=1, order=old_nyt.order - 1)
            
            # Update old NYT to be an internal node
            old_nyt.symbol = None
            old_nyt.left = new_nyt
            old_nyt.right = new_char_node
            
            # Update parent pointers
            new_nyt.parent = old_nyt
            new_char_node.parent = old_nyt

            # Update structures
            self.nyt_node = new_nyt
            self.nodes_by_symbol[char] = new_char_node
            self.nodes_by_order[new_nyt.order] = new_nyt
            self.nodes_by_order[new_char_node.order] = new_char_node
            
            # We don't increment old_nyt weight here directly, 
            # the _update_tree will handle it by starting from old_nyt.
            # However, new_char_node is already weight 1, so old_nyt should be updated starting from there
            update_actions = self._update_tree(old_nyt)
            actions = [f"Insert node for {repr(char)}", "split NYT"] + update_actions
            action = ", ".join(actions)

        else:
            # 2. Existing character
            char_node = self.nodes_by_symbol[char]
            output_code = self.get_code(char_node)
            status = "EXISTING"
            
            update_actions = self._update_tree(char_node)
            actions = ["Increment weight"] + update_actions
            action = ", ".join(actions)

        return status, output_code, action

    def get_ascii_tree(self, node=None, prefix="", is_left=None):
        if node is None:
            node = self.root
            if self.root is None:
                return "Empty Tree"
                
        tree_str = ""
        
        if node.right is not None:
            tree_str += self.get_ascii_tree(node.right, prefix + ("|   " if is_left else "    "), False)
            
        symbol_str = repr(node.symbol) if node.symbol else ('NYT' if node == self.nyt_node else '*')
        # Remove single quotes from repr if it's a char, just for cleaner look
        if symbol_str.startswith("'") and symbol_str.endswith("'"):
            symbol_str = symbol_str[1:-1]
            
        branch = "\\-- " if is_left else "/-- "
        if is_left is None:
            branch = "--- "
            
        tree_str += prefix + branch + f"({symbol_str},{node.weight})\n"
        
        if node.left is not None:
            tree_str += self.get_ascii_tree(node.left, prefix + ("    " if is_left else "|   "), True)
            
        return tree_str

    def encode(self, text):
        encoded_bits = ""
        for char in text:
            _, out_code, _ = self.process_char(char)
            encoded_bits += out_code
        return encoded_bits

    def decode(self, bitstring):
        decoded_text = ""
        curr = self.root
        i = 0
        
        while i < len(bitstring):
            # If tree is just NYT (at start) or we reached NYT
            if curr == self.nyt_node:
                # Read 8 bits for ASCII
                if i + 8 <= len(bitstring):
                    ascii_bits = bitstring[i:i+8]
                    char = chr(int(ascii_bits, 2))
                    decoded_text += char
                    self.process_char(char)
                    i += 8
                    curr = self.root
                    continue
                else:
                    break # Not enough bits left
                    
            if bitstring[i] == '0':
                curr = curr.left
            else:
                curr = curr.right
                
            if curr.is_leaf() and curr != self.nyt_node:
                decoded_text += curr.symbol
                self.process_char(curr.symbol)
                curr = self.root
                
            i += 1
            
        return decoded_text
