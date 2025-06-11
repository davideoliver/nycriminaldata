from complaint_data import ComplaintData

class PerfectHashTable:
    def __init__(self, complaints_list):
        # complaints_list: lista com todos os ComplaintData carregados antes
        self.size = len(complaints_list)
        self.index_map = {}  # mapa complaint_num -> índice único
        self.data = [None] * self.size  # lista para armazenar reclamações

        for i, complaint in enumerate(complaints_list):
            key = complaint.CMPLNT_NUM
            self.index_map[key] = i
            self.data[i] = complaint

    def insert(self, complaint: ComplaintData):
        key = complaint.CMPLNT_NUM
        if key in self.index_map:
            # Atualiza existente
            idx = self.index_map[key]
            self.data[idx] = complaint
        else:
            # Inserção simples: adiciona no final da lista e no map
            # Atenção: esta inserção quebra a "perfect hashing" se a lista crescer!
            self.data.append(complaint)
            self.index_map[key] = len(self.data) - 1

    def get(self, complaint_number):
        idx = self.index_map.get(complaint_number)
        if idx is not None:
            return self.data[idx]
        return None

    def remove(self, complaint_number):
        idx = self.index_map.get(complaint_number)
        if idx is None:
            return False  # não encontrado

        # Remove do index_map
        del self.index_map[complaint_number]

        # Remove da lista — para manter índices consistentes, 
        # substituímos o elemento removido pelo último e atualizamos o map
        last_idx = len(self.data) - 1
        if idx != last_idx:
            last_complaint = self.data[last_idx]
            self.data[idx] = last_complaint
            self.index_map[last_complaint.CMPLNT_NUM] = idx
        self.data.pop()
        return True

    def check_collisions(self):
        indices = list(self.index_map.values())
        unique_indices = set(indices)
        if len(indices) != len(unique_indices):
            print("[ALERTA] Colisão detectada: índices duplicados no mapa!")
            return True
        print("[INFO] Nenhuma colisão detectada. Perfect hashing válida.")
        return False

    def print_all(self):
        if not self.data:
            print("[INFO] Nenhuma reclamação cadastrada.")
            return
        print("=== Lista completa de reclamações (Perfect Hashing) ===")
        for complaint in self.data:
            print(f"Complaint #{complaint.CMPLNT_NUM}:")
            for key, value in vars(complaint).items():
                print(f"  {key}: {value}")
            print("-----------------------------")
        print("======================================================")
