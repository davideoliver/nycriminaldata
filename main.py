from dataclasses import dataclass, fields
import sys
import os
import csv
import time
import tracemalloc
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
    print("6. Classificação de Dados")
    print("7. Imprimir Dados")
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
            print("Filtragem e Ordenação\n")
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
            if value == 'columns':
                print("Campos nulos removidos com sucesso!")
            elif value == 'rows':
                print("Reclamações com nulos removidas com sucesso!")
            os.system('pause')
            os.system('cls' if os.name == 'nt' else 'clear')
            main_individual(id)
        elif choice == '5':
            print("Cálculos Estatísticos dos Dados\n")
        elif choice == '6':
            print("Ordenação e Classificação dos Dados\n")
            order = input("Digite 'asc' para ordem crescente ou 'desc' para ordem decrescente em relação ao número da ocorrência: ").strip().lower()
            if id == 0:
                results = dlinked_list.sort_by_id(order)
            elif id == 1:
                results = hash.sort_by_id(order)
            elif id == 2:
                results = btree.sort_by_id(order)
            elif id == 3:
                results = skiplist.sort_by_id(order)
            elif id == 4:
                results = trie.sort_by_id(order)
            if order == 'asc':
                print("Reclamações ordenadas em ordem crescente!")
            elif order == 'desc':
                print("Reclamações ordenadas em ordem decrescente!")
            os.system('pause')
            m = 1
            main_individual(id)
        elif choice == '0':
            os.system('cls' if os.name == 'nt' else 'clear')
            m = 0
            main()
        elif choice == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Impressão de Dados\n")
            i = int(input("Quantas reclamações você gostaria de imprimir? (Padrão = 10): "))
            if id == 0:
                dlinked_list.print_all(i)
            elif id == 1:
                hash.print_all(i)
            elif id == 2:
                btree.print_all(i)
            elif id == 3:
                skiplist.print_all(i)
            elif id == 4:
                trie.print_all(i)
            print("Dados impressos com sucesso!")
            os.system('pause')
            os.system('cls' if os.name == 'nt' else 'clear')
            m = 1
            main_individual(id)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
            os.system('pause')
            m = 1
            main_individual(id)

def main_benchmark():
    
    def benchmark_operation(operation, *args, **kwargs):
        tracemalloc.start()
        start_time = time.perf_counter()
        result = operation(*args, **kwargs)
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "tempo_segundos": end_time - start_time,
            "memoria_bytes": peak,
            "resultado": result
        }

    def benchmark_insercao(estrutura, dados, tipo):
        def inserir():
            if tipo == "dlinked":
                for dado in dados:
                    estrutura.insert_at_end(dado)
            elif tipo == "hash":
                for dado in dados:
                    estrutura.insert(dado)
            elif tipo == "btree":
                for dado in dados:
                    estrutura.insert(dado)
            elif tipo == "skiplist":
                for dado in dados:
                    estrutura.insert(dado)
            elif tipo == "trie":
                for dado in dados:
                    estrutura.insert(dado)
        return benchmark_operation(inserir)

    def benchmark_busca(estrutura, chaves, tipo):
        def buscar():
            for chave in chaves:
                if tipo == "dlinked":
                    estrutura.search_by_id(chave)
                elif tipo == "hash":
                    estrutura.get(chave)
                elif tipo == "btree":
                    estrutura.search_by_id(chave)
                elif tipo == "skiplist":
                    estrutura.search_by_id(chave)
                elif tipo == "trie":
                    estrutura.get(chave)
        return benchmark_operation(buscar)

    def benchmark_remocao(estrutura, chaves, tipo):
        def remover():
            for chave in chaves:
                if tipo == "dlinked":
                    estrutura.remove_by_id(chave)
                elif tipo == "hash":
                    estrutura.remove(chave)
                elif tipo == "btree":
                    estrutura.remove(chave)
                elif tipo == "skiplist":
                    estrutura.remove(chave)
                elif tipo == "trie":
                    estrutura.remove(chave)
        return benchmark_operation(remover)

    amostra = carregarDados(0)  # ou dados[:10000] para teste rápido
    chaves = [c.CMPLNT_NUM for c in amostra]


    os.system('cls' if os.name == 'nt' else 'clear')
    print("Escolha uma estrutura para trabalhar:")
    print("1. Lista Duplamente Encadeada")
    print("2. Tabela Hash")
    print("3. Árvore B")
    print("4. Lista de Pulos")
    print("5. Árvore Prefixada (Trie)")
    print("0. Voltar ao menu principal")

    # DLinkedList
    dlinked = DoublyLinkedList()
    print("\nBenchmark - Lista Duplamente Encadeada")
    res_ins = benchmark_insercao(dlinked, dados, "dlinked")
    print(f"Inserção: {res_ins['tempo_segundos']:.4f}s, Memória: {res_ins['memoria_bytes']/1024:.2f} KB")
    res_busca = benchmark_busca(dlinked, chaves, "dlinked")
    print(f"Busca: {res_busca['tempo_segundos']:.4f}s, Memória: {res_busca['memoria_bytes']/1024:.2f} KB")
    res_rem = benchmark_remocao(dlinked, chaves, "dlinked")
    print(f"Remoção: {res_rem['tempo_segundos']:.4f}s, Memória: {res_rem['memoria_bytes']/1024:.2f} KB")

    # PerfectHashTable
    hash_bench = PerfectHashTable(DATASET_PATH)
    print("\nBenchmark - Tabela Hash Perfeita")
    res_ins = benchmark_insercao(hash_bench, amostra, "hash")
    print(f"Inserção: {res_ins['tempo_segundos']:.4f}s, Memória: {res_ins['memoria_bytes']/1024:.2f} KB")
    res_busca = benchmark_busca(hash_bench, chaves, "hash")
    print(f"Busca: {res_busca['tempo_segundos']:.4f}s, Memória: {res_busca['memoria_bytes']/1024:.2f} KB")
    res_rem = benchmark_remocao(hash_bench, chaves, "hash")
    print(f"Remoção: {res_rem['tempo_segundos']:.4f}s, Memória: {res_rem['memoria_bytes']/1024:.2f} KB")

    # BTree
    btree_bench = BTree(t=3)
    print("\nBenchmark - Árvore B")
    res_ins = benchmark_insercao(btree_bench, amostra, "btree")
    print(f"Inserção: {res_ins['tempo_segundos']:.4f}s, Memória: {res_ins['memoria_bytes']/1024:.2f} KB")
    res_busca = benchmark_busca(btree_bench, chaves, "btree")
    print(f"Busca: {res_busca['tempo_segundos']:.4f}s, Memória: {res_busca['memoria_bytes']/1024:.2f} KB")
    res_rem = benchmark_remocao(btree_bench, chaves, "btree")
    print(f"Remoção: {res_rem['tempo_segundos']:.4f}s, Memória: {res_rem['memoria_bytes']/1024:.2f} KB")

    # SkipList
    skip_bench = SkipList()
    print("\nBenchmark - Skip List")
    res_ins = benchmark_insercao(skip_bench, amostra, "skiplist")
    print(f"Inserção: {res_ins['tempo_segundos']:.4f}s, Memória: {res_ins['memoria_bytes']/1024:.2f} KB")
    res_busca = benchmark_busca(skip_bench, chaves, "skiplist")
    print(f"Busca: {res_busca['tempo_segundos']:.4f}s, Memória: {res_busca['memoria_bytes']/1024:.2f} KB")
    res_rem = benchmark_remocao(skip_bench, chaves, "skiplist")
    print(f"Remoção: {res_rem['tempo_segundos']:.4f}s, Memória: {res_rem['memoria_bytes']/1024:.2f} KB")

    # Trie
    trie_bench = Trie()
    print("\nBenchmark - Trie")
    res_ins = benchmark_insercao(trie_bench, amostra, "trie")
    print(f"Inserção: {res_ins['tempo_segundos']:.4f}s, Memória: {res_ins['memoria_bytes']/1024:.2f} KB")
    res_busca = benchmark_busca(trie_bench, chaves, "trie")
    print(f"Busca: {res_busca['tempo_segundos']:.4f}s, Memória: {res_busca['memoria_bytes']/1024:.2f} KB")
    res_rem = benchmark_remocao(trie_bench, chaves, "trie")
    print(f"Remoção: {res_rem['tempo_segundos']:.4f}s, Memória: {res_rem['memoria_bytes']/1024:.2f} KB")

    print("\nBenchmark concluído. Pressione qualquer tecla para voltar ao menu.")
    os.system('pause')

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
    print("Esta seção é dedicada a resolução de um problema com uma estrutura de dados.")
    print("1. Ordenar reclamações por data")
    print("0. Voltar ao menu principal")
    choice = input("Digite sua escolha: ")
    if choice == '1':
        if dlinked_list.head is None:
            carregarDados(0)  # Carrega os dados se a lista estiver vazia
        print("Reclamações ordenadas por data:")
        dlinked_list.print_sorted_by_date()
        os.system('pause')
        print("================================================")
        print("Grupos de Idade dos Suspeitos:")
        print("1. 0-17 anos")
        print("2. 18-24 anos")
        print("3. 25-44 anos")
        print("4. 45-64 anos")
        print("5. 65 anos ou mais")
        print("6. Desconhecido ou Nulo")

        choice2 = input("Escolha um grupo de idade para filtrar os suspeitos a partir do número correspondente: ")

        def remover_por_grupo_idade(grupo_idade):
            grupo_idade = grupo_idade.strip().upper()
            atual = dlinked_list.head
            removidos = 0

            while atual:
                prox = atual.next  # guarda o próximo para não perder o ponteiro
                if (atual.data.SUSP_AGE_GROUP.strip().upper() != grupo_idade) and not (grupo_idade == "UNKNOWN" and (atual.data.SUSP_AGE_GROUP.strip() == None or atual.data.SUSP_AGE_GROUP.strip() == '' or atual.data.SUSP_AGE_GROUP.strip() == '(null)')):
                    dlinked_list.remove_by_id(atual.data.CMPLNT_NUM)
                    removidos += 1
                atual = prox

            print(f"\n{removidos} reclamações removidas que não pertencem ao grupo de idade '{grupo_idade}'.")
            if dlinked_list.head is None:
                print("Nenhum suspeito encontrado com os parâmetros fornecidos.")
            os.system('pause')

        if choice2 == '1':
            print("Suspeitos com idade entre 0-17 anos:")
            remover_por_grupo_idade("<18")
        elif choice2 == '2':
            print("Suspeitos com idade entre 18-24 anos:")
            remover_por_grupo_idade("18-24")
        elif choice2 == '3':
            print("Suspeitos com idade entre 25-44 anos:")
            remover_por_grupo_idade("25-44")
        elif choice2 == '4':
            print("Suspeitos com idade entre 45-64 anos:")
            remover_por_grupo_idade("45-64")
        elif choice2 == '5':
            print("Suspeitos com 65 anos ou mais:")
            remover_por_grupo_idade("65+")
        elif choice2 == '6':
            print("Suspeitos com idade desconhecida ou nula:")
            remover_por_grupo_idade("UNKNOWN")
        else:
            print("Opção inválida.")
            os.system('pause')
            main_problem()
        
        dlinked_list.print_sorted_by_date()

        print("================================================")
        print("Raça do Suspeito:")
        print("1. Branco")
        print("2. Negro")
        print("3. Branco Hispânico")
        print("4. Negro Hispânico")
        print("5. Asiático")
        print("6. Desconhecido ou Nulo")

        choice3 = input("Escolha a raça do suspeito para filtrar os suspeitos a partir do número correspondente: ")

        def remover_por_grupo_raca(grupo_raca):
            grupo_raca = grupo_raca.strip().upper()
            atual = dlinked_list.head
            removidos = 0

            while atual:
                prox = atual.next  # guarda o próximo para não perder o ponteiro
                if (atual.data.SUSP_RACE.strip().upper() != grupo_raca) and not (grupo_raca == "UNKNOWN" and (atual.data.SUSP_RACE.strip() == None or atual.data.SUSP_RACE.strip() == '' or atual.data.SUSP_RACE.strip() == '(null)')):
                    dlinked_list.remove_by_id(atual.data.CMPLNT_NUM)
                    removidos += 1
                atual = prox

            print(f"\n{removidos} reclamações removidas que não pertencem à raça '{grupo_raca}'.")
            if dlinked_list.head is None:
                print("Nenhum suspeito encontrado com os parâmetros fornecidos.")
            os.system('pause')
        
        if choice3 == '1':
            print("Suspeitos com raça Branco:")
            remover_por_grupo_idade("WHITE")
        elif choice3 == '2':
            print("Suspeitos com raça Negro:")
            remover_por_grupo_idade("BLACK")
        elif choice3== '3':
            print("Suspeitos com raça Branco Hispânico:")
            remover_por_grupo_idade("WHITE HISPANIC")
        elif choice3 == '4':
            print("Suspeitos com raça Negro Hispânico:")
            remover_por_grupo_idade("BLACK HISPANIC")
        elif choice3 == '5':
            print("Suspeitos com raça Asiático:")
            remover_por_grupo_raca("ASIAN / PACIFIC ISLANDER")
        elif choice3 == '6':
            print("Suspeitos com raça desconhecida ou nula:")
            remover_por_grupo_raca("UNKNOWN")
        else:
            print("Opção inválida.")
            os.system('pause')
            main_problem()

        dlinked_list.print_sorted_by_date()

        print("================================================")
        print("Sexo do Suspeito:")
        print("1. Masculino")
        print("2. Feminino")
        print("3. Desconhecido ou Nulo")

        def remover_por_grupo_sexo(grupo_sexo):
            grupo_sexo = grupo_sexo.strip().upper()
            atual = dlinked_list.head
            removidos = 0

            while atual:
                prox = atual.next  # guarda o próximo para não perder o ponteiro
                if (atual.data.SUSP_SEX.strip().upper() != grupo_sexo) and not (grupo_sexo == "UNKNOWN" and (atual.data.SUSP_SEX.strip() == None or atual.data.SUSP_SEX.strip() == '' or atual.data.SUSP_SEX.strip() == '(null)')):
                    dlinked_list.remove_by_id(atual.data.CMPLNT_NUM)
                    removidos += 1
                atual = prox

            print(f"\n{removidos} reclamações removidas que não pertencem à raça '{grupo_sexo}'.")
            if dlinked_list.head is None:
                print("Nenhum suspeito encontrado com os parâmetros fornecidos.")
            os.system('pause')

        choice4 = input("Escolha a raça do suspeito para filtrar os suspeitos a partir do número correspondente: ")

        if choice4 == '1':
            print("Suspeitos com sexo Masculino:")
            remover_por_grupo_sexo("M")
        elif choice4 == '2':
            print("Suspeitos com sexo Feminino:")
            remover_por_grupo_sexo("F")
        elif choice4 == '3':
            print("Suspeitos com sexo Nulo ou Desconhecido:")
            remover_por_grupo_sexo("UNKNOWN")
        else:
            print("Opção inválida.")
            os.system('pause')
            main_problem()

        dlinked_list.print_sorted_by_date()

    elif choice == '0':
        main()
    else:
        print("Opção inválida.")
        os.system('pause')
        main_problem()

def carregarDados(id):
    dados = []
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
                dados.append(complaint)
                if id == 0: dlinked_list.insert_at_random(complaint)
                if id == 1: hash.insert(complaint)
                if id == 2: btree.insert(complaint)
                if id == 3: skiplist.insert(complaint)
                if id == 4: trie.insert(complaint)

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
            sys.exit(0)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Opção inválida. Tente novamente.")
            os.system('pause')
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
if __name__ == "__main__":
    main()