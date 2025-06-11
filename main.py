from dataclasses import dataclass
import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'structures')))
from complaint_data import ComplaintData # importa a classe ComplaintData pronta
from perfect_hash_table import PerfectHashTable # importa a classe hashTable pronta
from b_tree import BTree  # importa a classe BTree pronta
from skip_list import SkipList 
from dlinklist import DoublyLinkedList  # importa a lista duplamente encadeada
from trie import Trie  # importa a classe Trie pronta
from priority_queue import PriorityQueue # importa a lista de prioridade

# Caminho para o dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'NYPD_Complaint_Data_Historic.csv')

complaints_list = []

with open(DATASET_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Converte as chaves e valores do CSV em argumentos para ComplaintData
        complaint = ComplaintData(**row)
        complaints_list.append(complaint)

perfect_hash = PerfectHashTable(complaints_list) # inicializa a tabela hash
btree = BTree(t=3)  # inicializa com grau mínimo 3 (pode ajustar)
skiplist = SkipList() # inicializa a skip list
dlinked_list = DoublyLinkedList()  # inicializa a lista duplamente encadeada
trie = Trie()
priority_queue = PriorityQueue()  # inicializa a lista de prioridade

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
            # Adaptar os campos conforme o dataclass ComplaintData
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
            perfect_hash.insert(complaint)
            btree.insert(complaint)
            skiplist.insert(complaint)
            dlinked_list.insert_at_random(complaint)
            trie.insert(complaint)
            priority_queue.insert(complaint)

#dlinked_list.print_all()
#perfect_hash.print_all()
#btree.print_all()
#skiplist.print_all()
#trie.print_all()
#priority_queue.print_all()
#perfect_hash.check_collisions()

print("Bem vindo ao sistema de gerenciamento de reclamações da NYPD")

