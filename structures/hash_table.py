from complaint_data import ComplaintData

class hashTable:
    def __init__(self):
        self.data = {}

    def insert(self, complaint: ComplaintData):
        self.data[complaint.CMPLNT_NUM] = complaint
        print(f"[DEBUG] Inserido: Complaint #{complaint.CMPLNT_NUM}")

    def get(self, complaint_number: str):
        return self.data.get(complaint_number)

    def remove(self, complaint_number: str):
        removed = self.data.pop(complaint_number, None) is not None
        if removed:
            print(f"[DEBUG] Removido Complaint #{complaint_number}")
        else:
            print(f"[DEBUG] Complaint #{complaint_number} não encontrado para remoção")
        return removed

    def print_all(self):
        if not self.data:
            print("[INFO] Nenhuma reclamação cadastrada.")
            return
        print("=== Lista completa de reclamações ===")
        for number, complaint in self.data.items():
            print(f"Complaint #{number}:")
            for key, value in vars(complaint).items():
                print(f"  {key}: {value}")
            print("-----------------------------")
        print("====================================")
