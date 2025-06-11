import pandas as pd
import random
from datetime import datetime

# Prompt: Created a doubly linked list with a init function siliar to the one present in hash_table,
# and add the funcitons search insert and remove

class Node:
    def __init__(self, data):
        self.data = data  # data is a dict with all features
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self, dataframe: pd.DataFrame = None):
        self.head = None
        self.tail = None
        if dataframe is not None:
            self.from_dataframe(dataframe)

    def from_dataframe(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            self.insert_at_end(row.to_dict())

    def insert_at_end(self, data: dict):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    # Prompt: create a funciton to insert on a random place
    def insert_at_random(self, data: dict):
        """Insert a node at a random position in the list."""
        new_node = Node(data)
        # If the list is empty, insert as the only node
        if self.head is None:
            self.head = self.tail = new_node
            return

        # Count the number of nodes
        length = 0
        current = self.head
        while current:
            length += 1
            current = current.next

        # Choose a random position (0 = head, length = after tail)
        pos = random.randint(0, length)

        if pos == 0:
            # Insert at head
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif pos == length:
            # Insert at tail
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        else:
            # Insert in the middle
            current = self.head
            for _ in range(pos - 1):
                current = current.next
            new_node.next = current.next
            new_node.prev = current
            if current.next:
                current.next.prev = new_node
            current.next = new_node
            
    def insert_at_beginning(self, data: dict):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def remove_by_id(self, id_value):
        current = self.head
        while current:
            data = current.data
            # Suporta dict ou objeto ComplaintData
            cmplnt_num = data.get('CMPLNT_NUM') if isinstance(data, dict) else getattr(data, 'CMPLNT_NUM', None)
            if cmplnt_num == id_value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def search_by_id(self, id_value):
        current = self.head
        while current:
            data = current.data
            # Suporta dict ou objeto ComplaintData
            cmplnt_num = data.get('CMPLNT_NUM') if isinstance(data, dict) else getattr(data, 'CMPLNT_NUM', None)
            if cmplnt_num == id_value:
                return data
            current = current.next
        return None

    def sort_by_date(self):
        """Retorna uma lista dos elementos ordenados por CMPLNT_FR_DT (formato MM/DD/YYYY)."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next

        def parse_datetime(x):
            date_str = x.get('CMPLNT_FR_DT') if isinstance(x, dict) else getattr(x, 'CMPLNT_FR_DT', '')
            time_str = x.get('CMPLNT_FR_TM') if isinstance(x, dict) else getattr(x, 'CMPLNT_FR_TM', '')
            dt_str = f"{date_str} {time_str}".strip()
            try:
                # Exemplo de formato: 12/31/2020 23:59:59
                return datetime.strptime(dt_str, "%m/%d/%Y %H:%M:%S")
            except Exception:
                try:
                    # Caso o horário esteja só com horas e minutos
                    return datetime.strptime(dt_str, "%m/%d/%Y %H:%M")
                except Exception:
                    try:
                        # Caso só tenha a data
                        return datetime.strptime(date_str, "%m/%d/%Y")
                    except Exception:
                        return datetime.min  # datas inválidas vão para o início

        elements.sort(key=parse_datetime)
        return elements
    
    def print_sorted_by_date(self):
        sorted_data = self.sort_by_date()
        print(f"Total de elementos ordenados: {len(sorted_data)}")
        for complaint in sorted_data:
            if hasattr(complaint, '__dict__'):
                for k, v in vars(complaint).items():
                    print(f"{k}: {v}")
                print("-" * 40)
            elif isinstance(complaint, dict):
                for k, v in complaint.items():
                    print(f"{k}: {v}")
                print("-" * 40)
            else:
                print(complaint)

    # Prompt: create a function to print all elements in the list    
    def print_all(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def filter_nulls(self, value):
        # Coleta todos os dados
        all_data = []
        current = self.head
        while current:
            all_data.append(current.data)
            current = current.next

        if value == "columns":
            # Conta nulos por campo
            null_counts = {}
            total = len(all_data)
            for data in all_data:
                for k, v in (data.items() if isinstance(data, dict) else vars(data).items()):
                    if v is None:
                        null_counts[k] = null_counts.get(k, 0) + 1
            # Campos a remover
            to_remove = {k for k, v in null_counts.items() if v / total > 0.5}
            # Remove campos dos objetos
            current = self.head
            while current:
                if isinstance(current.data, dict):
                    for k in to_remove:
                        current.data.pop(k, None)
                else:
                    for k in to_remove:
                        setattr(current.data, k, None)
                current = current.next
        elif value == "rows":
            # Remove nós com qualquer valor nulo
            current = self.head
            while current:
                data = current.data
                has_null = any(v is None for v in (data.values() if isinstance(data, dict) else vars(data).values()))
                next_node = current.next
                if has_null:
                    self.remove_by_id(getattr(data, 'CMPLNT_NUM', data.get('CMPLNT_NUM', None)))
                current = next_node
        # Always return the current list after filtering
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result