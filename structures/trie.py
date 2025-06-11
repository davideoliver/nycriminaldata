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

    def print_all(self, i = 10):
        c = 0
        def _print_node(node, prefix):
            if node.is_end and node.complaint:
                print(f"Complaint #{prefix}:")
                for key, value in vars(node.complaint).items():
                    print(f"  {key}: {value}")
                    c  = c + 1
                    if(c < i): break
                print("-----------------------------")
            for char, child in node.children.items():
                _print_node(child, prefix + char)

        if self.root.children:
            print("=== Lista completa de reclamações (Trie) ===")
            _print_node(self.root, "")
            print("===========================================")
        else:
            print("[INFO] Árvore Prefixada vazia")

    # Prompt: I'd to create a function called filter_nulls() in each of the structures, it will receive a value
    # and basing on it will change his behavior to removing whole camps with more than 50% of null data,
    # to removing all the lines with any null values
    def filter_nulls(self, value):
        all_complaints = []

        def collect(node):
            if node.is_end and node.complaint:
                all_complaints.append(node.complaint)
            for child in node.children.values():
                collect(child)
        collect(self.root)

        if value == "columns":
            null_counts = {}
            total = len(all_complaints)
            for complaint in all_complaints:
                for k, v in vars(complaint).items():
                    if v is None:
                        null_counts[k] = null_counts.get(k, 0) + 1
            to_remove = {k for k, v in null_counts.items() if v / total > 0.5}
            def remove_fields(node):
                if node.is_end and node.complaint:
                    for k in to_remove:
                        setattr(node.complaint, k, None)
                for child in node.children.values():
                    remove_fields(child)
            remove_fields(self.root)
        elif value == "rows":
            def remove_nodes(node, prefix=""):
                if node.is_end and node.complaint and any(v is None for v in vars(node.complaint).values()):
                    self.remove(prefix)
                for char, child in node.children.items():
                    remove_nodes(child, prefix + char)
            remove_nodes(self.root)
        # Always return the current list after filtering
        result = []
        def collect_again(node):
            if node.is_end and node.complaint:
                result.append(node.complaint)
            for child in node.children.values():
                collect_again(child)
        collect_again(self.root)
        return result

    def sort_by_id(self, reverse=False):
        """Retorna uma lista dos ComplaintData ordenados por CMPLNT_NUM."""
        result = []
        def collect(node):
            if node.is_end and node.complaint:
                result.append(node.complaint)
            for child in node.children.values():
                collect(child)
        collect(self.root)
        result.sort(key=lambda x: x.CMPLNT_NUM, reverse=reverse)
        return result