from complaint_data import ComplaintData

class TrieNode:
    def __init__(self):
        self.children = {}
        self.complaint = None  # Armazena o ComplaintData no final da palavra
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, complaint: ComplaintData):
        key = str(complaint.CMPLNT_NUM)
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.complaint = complaint

    def get(self, complaint_number: str):
        node = self.root
        for char in str(complaint_number):
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end:
            return node.complaint
        return None

    def remove(self, complaint_number: str):
        def _remove(node, key, depth):
            if node is None:
                return False
            if depth == len(key):
                if not node.is_end:
                    return False
                node.is_end = False
                node.complaint = None
                return len(node.children) == 0
            char = key[depth]
            if char in node.children and _remove(node.children[char], key, depth + 1):
                del node.children[char]
                return not node.is_end and len(node.children) == 0
            return False

        removed = _remove(self.root, str(complaint_number), 0)
        return removed

    def print_all(self):
        def _print_node(node, prefix):
            if node.is_end and node.complaint:
                print(f"Complaint #{prefix}:")
                for key, value in vars(node.complaint).items():
                    print(f"  {key}: {value}")
                print("-----------------------------")
            for char, child in node.children.items():
                _print_node(child, prefix + char)

        if self.root.children:
            print("=== Lista completa de reclamações (Trie) ===")
            _print_node(self.root, "")
            print("===========================================")
        else:
            print("[INFO] Árvore Prefixada vazia")
