import heapq
from complaint_data import ComplaintData

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0  # contador para desempate estável

    def insert(self, complaint: ComplaintData, priority=None):
        """
        Insere uma reclamação com prioridade.
        Se priority for None, usa CMPLNT_NUM convertido para int (exemplo).
        """
        if priority is None:
            try:
                priority = int(complaint.CMPLNT_NUM)
            except ValueError:
                priority = 0  # fallback caso CMPLNT_NUM não seja numérico

        # Usamos 'count' para manter a ordem de inserção quando prioridades iguais
        heapq.heappush(self.heap, (priority, self.count, complaint))
        self.count += 1

    def pop(self):
        """
        Remove e retorna o item com a maior prioridade (menor valor).
        """
        if not self.heap:
            print("[INFO] Fila de prioridade vazia")
            return None
        priority, count, complaint = heapq.heappop(self.heap)
        return complaint

    def peek(self):
        """
        Retorna o item de maior prioridade sem remover.
        """
        if not self.heap:
            return None
        return self.heap[0][2]

    def is_empty(self):
        return len(self.heap) == 0

    def print_all(self):
        if not self.heap:
            print("[INFO] Fila de prioridade vazia")
            return

        print("=== Lista completa de reclamações (Fila com Prioridade) ===")
        for priority, count, complaint in sorted(self.heap):
            print(f"Complaint #{complaint.CMPLNT_NUM} (Prioridade: {priority}):")
            for attr, val in vars(complaint).items():
                print(f"  {attr}: {val}")
            print("-" * 30)
        print("===========================================================")
