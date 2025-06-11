from complaint_data import ComplaintData

class Node:
    def __init__(self, complaint: ComplaintData):
        self.complaint = complaint
        self.prev = None
        self.next = None

class DLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, complaint: ComplaintData):
        new_node = Node(complaint)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        print(f"[DEBUG] Inserido: Complaint #{complaint.CMPLNT_NUM}")

    def search(self, complaint_number: str):
        current = self.head
        while current:
            if current.complaint.CMPLNT_NUM == complaint_number:
                return current.complaint
            current = current.next
        return None

    def remove(self, complaint_number: str):
        current = self.head
        while current:
            if current.complaint.CMPLNT_NUM == complaint_number:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                print(f"[DEBUG] Removido Complaint #{complaint_number}")
                return True
            current = current.next
        print(f"[DEBUG] Complaint #{complaint_number} não encontrado para remoção")
        return False

    def print_all(self):
        if not self.head:
            print("[INFO] Nenhuma reclamação cadastrada.")
            return
        print("=== Lista completa de reclamações (Doubly Linked List) ===")
        current = self.head
        while current:
            print(f"Complaint #{current.complaint.CMPLNT_NUM}:")
            for key, value in vars(current.complaint).items():
                print(f"  {key}: {value}")
            print("-----------------------------")
            current = current.next
        print("====================================")
