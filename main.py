from dataclasses import dataclass, fields
import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'structures')))
from complaint_data import ComplaintData # importa a classe ComplaintData pronta
from perfect_hash_table import PerfectHashTable # importa a classe PerfectHashTable pronta
from b_tree import BTree  # importa a classe BTree pronta
from skip_list import SkipList 
from dlinklist import DoublyLinkedList  # importa a lista duplamente encadeada
from trie import Trie  # importa a classe Trie pronta

m = 0
# Caminho para o dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'NYPD_Complaint_Data_Historic.csv')

# Inicialize a tabela hash após carregar os dados
hash = PerfectHashTable(DATASET_PATH)
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

def create_complaint_with_minimal_fields(data):
    # Cria um dicionário com todos os campos como None
    complaint_dict = {f.name: None for f in fields(ComplaintData)}
    # Atualiza apenas os campos principais
    complaint_dict.update({
        "CMPLNT_NUM": data[0],
        "OFNS_DESC": data[1],
        "BORO_NM": data[2],
        "PREM_TYP_DESC": data[3]
    })
    return ComplaintData(**complaint_dict)

def main_individual(id):
    global m

    structures = [
        "Lista Duplamente Encadeada",
        "Tabela Hash Perfeita",
        "Árvore B",
        "Lista de Pulos",
        "Árvore Prefixada"
    ]

    if os.path.exists(DATASET_PATH) and m == 0:
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
                if id == 0: dlinked_list.insert_at_random(complaint)
                if id == 1: hash.insert(complaint)
                if id == 2: btree.insert(complaint)
                if id == 3: skiplist.insert(complaint)
                if id == 4: trie.insert(complaint)

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
        if choice == '1':
            data = {}
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Digite os dados da reclamação:\n")
            type = ["Identificação Númerica: ","Tipo de crime:", "Condado:", "Localidade:"]
            for i in range(4):
                data[i] = input(type[i])
            complaint = create_complaint_with_minimal_fields(data)
            if id == 0:
                where = input("Onde você gostaria de inserir a reclamação? (início/fim/aleatório): ")
                if where.lower() == 'início':
                    dlinked_list.insert_at_beginning(complaint)
                elif where.lower() == 'fim':
                    dlinked_list.insert_at_end(complaint)
                elif where.lower() == 'aleatório':
                    dlinked_list.insert_at_random(complaint)
                else:
                    print("Opção inválida. Inserindo no aleatóriamente por padrão.")
                dlinked_list.insert_at_random(complaint)       
                print("Reclamação inserida na lista duplamente encadeada.")
            if id == 1:
                hash.insert(complaint)  
                print("Reclamação inserida na tabela hash perfeita.")
            if id == 2:
                btree.insert(complaint)
                print("Reclamação inserida na árvore B.")
            if id == 3:
                skiplist.insert(complaint)
                print("Reclamação inserida na lista de pulos.")
            if id == 4:
                trie.insert(complaint)
                print("Reclamação inserida na árvore prefixada (Trie).")
            os.system('pause')
            m = 1
            main_individual(id)
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            nid = input("Digite o número de identificação da reclamação:\n")
            result = None
            if id == 0:
                result = dlinked_list.search_by_id(nid)
            elif id == 1:
                result = hash.get(nid)
            elif id == 2:
                result = btree.search_by_id(nid)
            elif id == 3:
                result = skiplist.search_by_id(nid)
            elif id == 4:
                result = trie.get(nid)
            if result:
                print("Reclamação encontrada:")
                print(result)
            else:
                print("Reclamação não encontrada para o número informado.")
            os.system('pause')
            m = 1
            main_individual(id)
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            nid = input("Digite o número de identificação da reclamação:\n")
            # Prompt: I'd like this code search for the data of with a CMPLNT_NUM informed as a number
            # to the user, and then if it founds it, it's removed from the structure
            result = None
            if id == 0:
                result = dlinked_list.search_by_id(nid)
            elif id == 1:
                result = hash.get(nid)
            elif id == 2:
                result = btree.search_by_id(nid)
            elif id == 3:
                result = skiplist.search_by_id(nid)
            elif id == 4:
                result = trie.get(nid)
            if result:
                print("Reclamação encontrada:")
                print(result)
                confirm = input("Deseja remover esta reclamação? (s/n): ")
                if confirm.lower() == 's':
                    if id == 0:
                        dlinked_list.remove_by_id(nid)
                        print("Reclamação removida da lista duplamente encadeada.")
                    elif id == 1:
                        hash.remove(nid)
                        print("Reclamação removida da tabela hash perfeita.")
                    elif id == 2:
                        btree.remove(nid)
                        print("Reclamação removida da árvore B.")
                    elif id == 3:
                        skiplist.remove(nid)
                        print("Reclamação removida da lista de pulos.")
                    elif id == 4:
                        trie.remove(nid)
                        print("Reclamação removida da árvore prefixada (Trie).")
                else:
                    print("Remoção cancelada.")
                    os.system('pause')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    m = 1
                    main_individual(id)
            else:
                print("Reclamação não encontrada para o número informado.")
            os.system('pause')
            m = 1
            main_individual(id)
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Filtragem e ordenação das reclamações\n")
            print("Escolha uma opção:")
            print("1. Filtragem de reclamações com nulos")
            print("2. Ordenação das reclamações por número de identificação")
            sub_choice = input("Escolha uma opção: ")
            if sub_choice == '1':
                print("Você gostaria de eliminar campos com mais da metade de nulos? Ou  de eliminar reclamações inteiras que contenham nulos?")
                value = input("Digite 'colums' para eliminar campos nulos ou 'rows' para eliminar reclamações com nulos: ").strip().lower()
                if id == 0:
                    results = dlinked_list.filter_nulls(value)
                elif id == 1:
                    results = hash.filter_nulls(value)
                elif id == 2:
                    results = btree.filter_nulls(value)
                elif id == 3:
                    results = skiplist.filter_nulls(value)
                elif id == 4:
                    results = trie.filter_nulls(value)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Filtragem concluída.")
                os.system('pause')
                os.system('cls' if os.name == 'nt' else 'clear')
                main_individual(id)
            elif sub_choice == '2':
                print("Reclamações ordenadas por número de identificação:")
                if id == 0:
                    results = dlinked_list.sort_by_id()
                elif id == 1:
                    results = hash.sort_by_id()
                elif id == 2:
                    results = btree.sort_by_id()
                elif id == 3:
                    results = skiplist.sort_by_id()
                elif id == 4:
                    results = trie.sort_by_id()
                os.system('pause')
                m = 1
                main_individual(id)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Opção inválida.")
                os.system('pause')
                m = 1
                main_individual(id)
            os.system('pause')
            m = 1
            main_individual(id)
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            m = 0
            main()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('pause')
            m = 1
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
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('pause')
            main_structures()

def main_problem():
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
    print("2. Testes de Benchmark e Restrições")
    print("3. Resolução de Problema")
    print("0. Sair")
    while True:
        choice = input("Digite sua escolha: ")
        if choice == '1':
            main_structures()
        elif choice == '2':
            main_benchmark()
        elif choice == '3':
            main_problem()
        elif choice == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
            os.system('pause')
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
main()