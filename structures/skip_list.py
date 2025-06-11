import random
from complaint_data import ComplaintData

class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    MAX_LEVEL = 6  # número máximo de níveis (ajustável)

    def __init__(self):
        self.header = self._create_node(None, None, self.MAX_LEVEL)
        self.level = 0

    def _create_node(self, key, value, level):
        return SkipListNode(key, value, level)

    def _random_level(self):
        level = 0
        while random.random() < 0.5 and level < self.MAX_LEVEL:
            level += 1
        return level

    def insert(self, complaint: ComplaintData):
        key = complaint.CMPLNT_NUM
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            current.value = complaint  # Atualiza se já existe
        else:
            new_level = self._random_level()
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            new_node = self._create_node(key, complaint, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def get(self, key):
        current = self.header
        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]

        if current and current.key == key:
            return current.value
        return None

    def remove(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            return True
        else:
            print(f"[DEBUG] Complaint #{key} não encontrado para remoção")
            return False

    def print_all(self, i=10):
        c = 0
        current = self.header.forward[0]
        if not current:
            print("[INFO] Skip List vazia")
            return
        print("=== Lista completa de reclamações (Skip List) ===")
        while current:
            print(f"Complaint #{current.key}:")
            for key, value in vars(current.value).items():
                print(f"  {key}: {value}")
            print("-----------------------------")
            current = current.forward[0]
            c  = c + 1
            if(c < i): break
        print("====================================")

    # Prompt: Create a search by CMPLNT_NUM in skip list
    def search_by_id(self, cmplnt_num):
        """Busca uma reclamação pelo número CMPLNT_NUM."""
        return self.get(cmplnt_num)
    
    # Prompt: I'd to create a function called filter_nulls() in each of the structures, it will receive a value
    # and basing on it will change his behavior to removing whole camps with more than 50% of null data,
    # to removing all the lines with any null values
    def filter_nulls(self, value):
        # Coleta todos os ComplaintData
        complaints = []
        current = self.header.forward[0]
        while current:
            complaints.append(current.value)
            current = current.forward[0]

        if value == "columns":
            null_counts = {}
            total = len(complaints)
            for complaint in complaints:
                for k, v in vars(complaint).items():
                    if v is None:
                        null_counts[k] = null_counts.get(k, 0) + 1
            to_remove = {k for k, v in null_counts.items() if v / total > 0.5}
            current = self.header.forward[0]
            while current:
                for k in to_remove:
                    setattr(current.value, k, None)
                current = current.forward[0]
        elif value == "rows":
            current = self.header.forward[0]
            to_remove = []
            while current:
                if any(v is None for v in vars(current.value).values()):
                    to_remove.append(current.key)
                current = current.forward[0]
            for key in to_remove:
                self.remove(key)
        # Always return the current list after filtering
        result = []
        current = self.header.forward[0]
        while current:
            result.append(current.value)
            current = current.forward[0]
        return result

    def sort_by_id(self, reverse=False):
        """Retorna uma lista dos ComplaintData ordenados por CMPLNT_NUM."""
        elements = []
        current = self.header.forward[0]
        while current:
            elements.append(current.value)
            current = current.forward[0]
        elements.sort(key=lambda x: x.CMPLNT_NUM, reverse=reverse)
        return elements
