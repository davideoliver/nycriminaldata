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

    def print_all(self):
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
        print("====================================")

    # Prompt: Create a search by CMPLNT_NUM in skip list
    def search_by_id(self, cmplnt_num):
        """Busca uma reclamação pelo número CMPLNT_NUM."""
        return self.get(cmplnt_num)
