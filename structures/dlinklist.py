import pandas as pd

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

    def insert_after_id(self, id_value, data: dict):
        current = self.head
        while current:
            if current.data.get('id') == id_value:
                new_node = Node(data)
                new_node.prev = current
                new_node.next = current.next
                if current.next:
                    current.next.prev = new_node
                else:
                    self.tail = new_node
                current.next = new_node
                return True
            current = current.next
        return False

    def remove_by_id(self, id_value):
        current = self.head
        while current:
            if current.data.get('id') == id_value:
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
            if current.data.get('id') == id_value:
                return current.data
            current = current.next
        return None
