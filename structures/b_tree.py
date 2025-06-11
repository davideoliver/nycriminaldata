from complaint_data import ComplaintData

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def insert_non_full(self, k, v):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            self.values.append(None)
            while i >= 0 and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                self.values[i + 1] = self.values[i]
                i -= 1
            self.keys[i + 1] = k
            self.values[i + 1] = v
        else:
            while i >= 0 and self.keys[i] > k:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if self.keys[i] < k:
                    i += 1
            self.children[i].insert_non_full(k, v)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        y.keys = y.keys[:t-1]
        y.values = y.values[:t-1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop())
        self.values.insert(i, y.values.pop())

    def find_key(self, k):
        """Retorna índice da chave k, ou -1 se não encontrar."""
        for i, key in enumerate(self.keys):
            if key >= k:
                return i
        return len(self.keys)

    def remove(self, k):
        idx = self.find_key(k)

        # Caso 1: chave está no 
        if idx < len(self.keys) and self.keys[idx] == k:
            if self.leaf:
                # Remover da folha direto
                self.keys.pop(idx)
                self.values.pop(idx)
                print(f"[DEBUG] Removido {k} de folha")
            else:
                #  interno: tem 3 subcasos
                self.remove_from_internal_node(idx)
        else:
            # Caso 2: chave não está no nó
            if self.leaf:
                print(f"[DEBUG] Chave {k} não encontrada na árvore.")
                return

            # Verifica se o filho onde poderia estar a chave tem ao menos t chaves
            flag = (idx == len(self.keys))

            if len(self.children[idx].keys) < self.t:
                self.fill(idx)

            if flag and idx > len(self.keys):
                self.children[idx - 1].remove(k)
            else:
                self.children[idx].remove(k)

    def remove_from_internal_node(self, idx):
        k = self.keys[idx]
        if len(self.children[idx].keys) >= self.t:
            pred_key, pred_val = self.get_pred(idx)
            self.keys[idx] = pred_key
            self.values[idx] = pred_val
            self.children[idx].remove(pred_key)
        elif len(self.children[idx + 1].keys) >= self.t:
            succ_key, succ_val = self.get_succ(idx)
            self.keys[idx] = succ_key
            self.values[idx] = succ_val
            self.children[idx + 1].remove(succ_key)
        else:
            self.merge(idx)
            self.children[idx].remove(k)

    def get_pred(self, idx):
        current = self.children[idx]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1], current.values[-1]

    def get_succ(self, idx):
        current = self.children[idx + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0], current.values[0]

    def fill(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]

        child.keys.insert(0, self.keys[idx - 1])
        child.values.insert(0, self.values[idx - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        self.keys[idx - 1] = sibling.keys.pop()
        self.values[idx - 1] = sibling.values.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys[idx])
        child.values.append(self.values[idx])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        self.keys[idx] = sibling.keys.pop(0)
        self.values[idx] = sibling.values.pop(0)

    def merge(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]

        child.keys.append(self.keys.pop(idx))
        child.values.append(self.values.pop(idx))

        child.keys.extend(sibling.keys)
        child.values.extend(sibling.values)

        if not child.leaf:
            child.children.extend(sibling.children)

        self.children.pop(idx + 1)

class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    def insert(self, complaint):
        k = complaint.CMPLNT_NUM
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, leaf=False)
            s.children.append(r)
            self.root = s
            s.split_child(0)
            s.insert_non_full(k, complaint)
        else:
            r.insert_non_full(k, complaint)

    def remove(self, k):
        if not self.root:
            print("[DEBUG] Árvore vazia")
            return

        self.root.remove(k)

        if len(self.root.keys) == 0:
            if self.root.leaf:
                self.root = None
            else:
                self.root = self.root.children[0]

    def print_all(self):
        def _print_node(node, level=0):
            print(f"{'  '*level}Nó (nível {level}):")
            for key, value in zip(node.keys, node.values):
                print(f"{'  '*(level+1)}{key}: {value.OFNS_DESC}")
            if not node.leaf:
                for child in node.children:
                    _print_node(child, level + 1)
        if self.root:
            _print_node(self.root)
        else:
            print("[INFO] Árvore vazia")
