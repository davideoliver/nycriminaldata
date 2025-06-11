from dataclasses import dataclass
import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'structures')))
from complaint_data import ComplaintData # importa a classe ComplaintData pronta
from hash_table import hashTable # importa a classe hashTable pronta
from b_tree import BTree  # importa a classe BTree pronta
from skip_list import SkipList 
from dlinklist import DoublyLinkedList  # importa a lista duplamente encadeada
from trie import Trie  # importa a classe Trie pronta

# Caminho para o dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'NYPD_Complaint_Data_Historic.csv')

hash = hashTable() # inicializa a tabela hash
btree = BTree(t=3)  # inicializa com grau mínimo 3 (pode ajustar)
skiplist = SkipList() # inicializa a skip list
dlinked_list = DoublyLinkedList()  # inicializa a lista duplamente encadeada
trie = Trie()

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

def main_individual(id):

    structures = [
        "Lista Duplamente Encadeada",
        "Tabela Hash",
        "Árvore B",
        "Lista de Pulos",
        "Árvore Prefixada"
    ]

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Esta seção é dedicada a operações individuais. Você escolheu a estrutura: ", structures[id])
    print("O que você gostaria de fazer?")
    print("1. Inserir uma nova reclamação")
    print("2. Buscar uma reclamação por número")
    print("3. Remover uma reclamação por número")
    print("4. Filtragem e ordenação das reclamações")
    print("5. Cálculos Estatísticos com os Dados")
    print("6. Simulações com Dados Novos")
    print("0. Voltar ao menu principal")

    while True:
        choice = input("Digite sua escolha: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == '1':
            data = {}
            print("Digite os dados da reclamação:\n")
            for i in range(3):
                type = ["Tipo de crime: ", "Condado: ", "Localidade: "]
                data[i] = input(type[i])
            if id == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                complaint = ComplaintData(
                    OFNS_DESC=data[0],
                    BORO_NM=data[1],
                    PREM_TYP_DESC=data[2],
                    CMPLNT_NUM=None,
                    CMPLNT_FR_DT=None,
                    CMPLNT_FR_TM=None,
                    CMPLNT_TO_DT=None,
                    CMPLNT_TO_TM=None,
                    ADDR_PCT_CD=None,
                    RPT_DT=None,
                    KY_CD=None,
                    PD_CD=None,
                    PD_DESC=None,
                    CRM_ATPT_CPTD_CD=None,
                    LAW_CAT_CD=None,
                    LOC_OF_OCCUR_DESC=None,
                    JURIS_DESC=None,
                    JURISDICTION_CODE=None,
                    PARKS_NM=None,
                    HADEVELOPT=None,
                    HOUSING_PSA=None,
                    X_COORD_CD=None,
                    Y_COORD_CD=None,
                    SUSP_AGE_GROUP=None,
                    SUSP_RACE=None,
                    SUSP_SEX=None,
                    TRANSIT_DISTRICT=None,
                    Latitude=None,
                    Longitude=None,
                    Lat_Lon=None,
                    PATROL_BORO=None,
                    STATION_NAME=None,
                    VIC_AGE_GROUP=None,
                    VIC_RACE=None,
                    VIC_SEX=None
                )
                dlinked_list.print_all()
                dlinked_list.append(complaint)
                print("Reclamação inserida na Lista Duplamente Encadeada com sucesso!")
        elif choice == '2':
            print("Buscar uma reclamação por número")
        elif choice == '3':
            print("Remover uma reclamação por número")
        elif choice == '4':
            print("Filtragem e ordenação das reclamações")
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
        else:
            print("Opção inválida. Tente novamente.")
            main_individual(id)

def main_benchmark():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Esta seção é dedicada a testes de benchmark.")
    # Aqui você pode implementar os testes de benchmark
    # Exemplo: medir o tempo de inserção, busca, etc.
    print("Testes de benchmark ainda não implementados.")

def main_structures():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Escolha uma estrutura para trabalhar:")
    print("1. Lista Duplamente Encadeada")
    print("2. Tabela Hash")
    print("3. Árvore B")
    print("4. Lista de Pulos")
    print("5. Árvore Prefixada (Trie)")
    print("0. Voltar ao menu principal")

    while True:
        choice = input("Digite sua escolha: ")
        if choice == '1':
            main_individual(0)
        elif choice == '2':
            main_individual(1)
        elif choice == '3':
            main_individual(2)
        elif choice == '4':
            main_individual(3)
        elif choice == '5':
            main_individual(4)
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
        else:
            print("Opção inválida. Tente novamente.")
            main_structures()

def main_restrictions():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Esta seção é dedicada a restrições e limitações.")
    print("Aqui você pode definir restrições para as operações.")
    # Aqui você pode implementar as restrições
    print("Restrições ainda não implementadas.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Bem vindo ao sistema de gerenciamento de reclamações da NYPD")

    print("O que você gostaria de fazer?")
    print("1. Operações Individuais")
    print("2. Testes de Benchmark")
    print("3. Restrições")
    print("0. Sair")
    while True:
        choice = input("Digite sua escolha: ")
        if choice == '1':
            main_structures()
        elif choice == '2':
            main_benchmark()
        elif choice == '3':
            main_restrictions()
        elif choice == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
main()