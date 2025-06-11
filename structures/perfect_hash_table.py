from complaint_data import ComplaintData
import csv
import os
class PerfectHashTable:
    def __init__(self, DATASET_PATH):
        
        complaints_list = []

        def safe_int(val):
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return 0

        def safe_float(val):
            try:
                return float(val)
            except (ValueError, TypeError):
                return 0.0

        # Carregar dados do CSV e inserir no registry
        if os.path.exists(DATASET_PATH):
            with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    complaint = ComplaintData(
                        CMPLNT_NUM=row.get('CMPLNT_NUM', ''),
                        CMPLNT_FR_DT=row.get('CMPLNT_FR_DT', ''),
                        CMPLNT_FR_TM=row.get('CMPLNT_FR_TM', ''),
                        CMPLNT_TO_DT=row.get('CMPLNT_TO_DT', ''),
                        CMPLNT_TO_TM=row.get('CMPLNT_TO_TM', ''),
                        ADDR_PCT_CD=safe_int(row.get('ADDR_PCT_CD', 0)),
                        RPT_DT=row.get('RPT_DT', ''),
                        KY_CD=safe_int(row.get('KY_CD', 0)),
                        OFNS_DESC=row.get('OFNS_DESC', ''),
                        PD_CD=safe_int(row.get('PD_CD', 0)),
                        PD_DESC=row.get('PD_DESC', ''),
                        CRM_ATPT_CPTD_CD=row.get('CRM_ATPT_CPTD_CD', ''),
                        LAW_CAT_CD=row.get('LAW_CAT_CD', ''),
                        BORO_NM=row.get('BORO_NM', ''),
                        LOC_OF_OCCUR_DESC=row.get('LOC_OF_OCCUR_DESC', ''),
                        PREM_TYP_DESC=row.get('PREM_TYP_DESC', ''),
                        JURIS_DESC=row.get('JURIS_DESC', ''),
                        JURISDICTION_CODE=safe_int(row.get('JURISDICTION_CODE', 0)),
                        PARKS_NM=row.get('PARKS_NM', ''),
                        HADEVELOPT=row.get('HADEVELOPT', ''),
                        HOUSING_PSA=row.get('HOUSING_PSA', ''),
                        X_COORD_CD=safe_int(row.get('X_COORD_CD', 0)),
                        Y_COORD_CD=safe_int(row.get('Y_COORD_CD', 0)),
                        SUSP_AGE_GROUP=row.get('SUSP_AGE_GROUP', ''),
                        SUSP_RACE=row.get('SUSP_RACE', ''),
                        SUSP_SEX=row.get('SUSP_SEX', ''),
                        TRANSIT_DISTRICT=safe_int(row.get('TRANSIT_DISTRICT', 0)),
                        Latitude=safe_float(row.get('Latitude', 0.0)),
                        Longitude=safe_float(row.get('Longitude', 0.0)),
                        Lat_Lon=row.get('Lat_Lon', ''),
                        PATROL_BORO=row.get('PATROL_BORO', ''),
                        STATION_NAME=row.get('STATION_NAME', ''),
                        VIC_AGE_GROUP=row.get('VIC_AGE_GROUP', ''),
                        VIC_RACE=row.get('VIC_RACE', ''),
                        VIC_SEX=row.get('VIC_SEX', '')
                    )
                    complaints_list.append(complaint) 

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

    def filter_nulls(self, value):
        if value == "columns":
            null_counts = {}
            total = len(self.data)
            for complaint in self.data:
                for k, v in vars(complaint).items():
                    if v is None:
                        null_counts[k] = null_counts.get(k, 0) + 1
            to_remove = {k for k, v in null_counts.items() if v / total > 0.5}
            for complaint in self.data:
                for k in to_remove:
                    setattr(complaint, k, None)
        elif value == "rows":
            to_remove = []
            for complaint in self.data:
                if any(v is None for v in vars(complaint).values()):
                    to_remove.append(complaint.CMPLNT_NUM)
            for cmplnt_num in to_remove:
                self.remove(cmplnt_num)
        # Always return the current list after filtering
        return list(self.data)
