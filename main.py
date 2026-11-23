"""
Sistema de Controle de Logística Portuária
Tema 4 - Projeto Final de Estruturas de Dados

Estruturas utilizadas:
- Fila  : collections.deque  (ordem de chegada de caminhões)
- Pilha : list               (empilhamento de contêineres)
- Lista : list               (frota de veículos e transportadoras)
- Árvore: dict aninhado      (rotas marítimas e portos)

Persistência: arquivo texto dados_sistema.txt
"""

from collections import deque
import os

# ============================================================================
# ESTRUTURAS DE DADOS GLOBAIS (iniciam vazias)
# ============================================================================
fila_caminhoes = deque()      # Fila: FIFO - chegada de caminhões
pilha_containers = []         # Pilha: LIFO - empilhamento de contêineres
frota = []                    # Lista: frota de veículos/transportadoras
rotas = {}                    # Árvore: {origem -> {intermediario -> [destinos]}}

ARQUIVO_DADOS = "dados_sistema.txt"
DELIMITADOR = "|"


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def pausar():
    """Pausa a execução para o usuário ler a saída."""
    input("\nPressione ENTER para continuar...")


def obter_opcao(msg="Opção: "):
    """Lê uma opção numérica do usuário de forma segura."""
    try:
        return int(input(msg))
    except ValueError:
        return -1


def menu(titulo, opcoes):
    """Exibe um menu genérico e retorna a opção escolhida."""
    print(f"\n{'='*50}")
    print(f"  {titulo}")
    print(f"{'='*50}")
    for chave, descricao in opcoes.items():
        print(f"  {chave}. {descricao}")
    print(f"{'='*50}")
    return obter_opcao("Escolha uma opção: ")


# ============================================================================
# FILA - Ordem de chegada de caminhões
# ============================================================================

def fila_inserir():
    """Insere caminhão no final da fila (chegada no pátio)."""
    print("\n--- Novo Caminhão na Fila ---")
    placa = input("Placa: ").strip().upper()
    motorista = input("Motorista: ").strip()
    transportadora = input("Transportadora: ").strip()
    carga = input("Descrição da carga: ").strip()

    if not placa:
        print("Erro: placa é obrigatória.")
        return

    caminhao = {
        "placa": placa,
        "motorista": motorista,
        "transportadora": transportadora,
        "carga": carga
    }
    fila_caminhoes.append(caminhao)  # FIFO: entra no final
    print(f"Caminhão {placa} entrou no final da fila.")


def fila_listar():
    """Lista todos os caminhões na ordem de chegada."""
    print("\n--- Fila de Caminhões (ordem de chegada) ---")
    if not fila_caminhoes:
        print("Fila vazia.")
        return

    for pos, cam in enumerate(fila_caminhoes, start=1):
        print(f"{pos}. {cam['placa']} | {cam['motorista']} | "
              f"{cam['transportadora']} | {cam['carga']}")


def fila_atualizar():
    """Atualiza dados de um caminhão na fila (busca por placa)."""
    if not fila_caminhoes:
        print("Fila vazia.")
        return

    placa = input("\nDigite a placa do caminhão a atualizar: ").strip().upper()
    for cam in fila_caminhoes:
        if cam["placa"] == placa:
            cam["motorista"] = input(f"Novo motorista [{cam['motorista']}]: ").strip() or cam["motorista"]
            cam["transportadora"] = input(f"Nova transportadora [{cam['transportadora']}]: ").strip() or cam["transportadora"]
            cam["carga"] = input(f"Nova carga [{cam['carga']}]: ").strip() or cam["carga"]
            print("Caminhão atualizado.")
            return
    print("Placa não encontrada.")


def fila_remover():
    """Remove o primeiro caminhão da fila (liberação para embarque)."""
    if not fila_caminhoes:
        print("Fila vazia. Nenhum caminhão para liberar.")
        return

    cam = fila_caminhoes.popleft()  # FIFO: sai do início
    print(f"Caminhão {cam['placa']} liberado para embarque.")


def gerenciar_fila():
    """Submenu da fila de caminhões."""
    opcoes = {
        1: "Inserir caminhão (chegada)",
        2: "Listar fila",
        3: "Atualizar caminhão",
        4: "Liberar primeiro caminhão",
        0: "Voltar"
    }
    while True:
        opcao = menu("FILA DE CAMINHÕES", opcoes)
        if opcao == 1:
            fila_inserir()
        elif opcao == 2:
            fila_listar()
        elif opcao == 3:
            fila_atualizar()
        elif opcao == 4:
            fila_remover()
        elif opcao == 0:
            break
        else:
            print("Opção inválida.")
        pausar()


# ============================================================================
# PILHA - Empilhamento de contêineres
# ============================================================================

def pilha_inserir():
    """Empilha um contêiner no topo."""
    print("\n--- Empilhar Contêiner ---")
    codigo = input("Código do contêiner: ").strip().upper()
    tipo = input("Tipo (seco/refrigerado/perigoso): ").strip()
    peso = input("Peso (kg): ").strip()
    destino = input("Destino: ").strip()

    if not codigo:
        print("Erro: código é obrigatório.")
        return

    container = {
        "codigo": codigo,
        "tipo": tipo,
        "peso": peso,
        "destino": destino
    }
    pilha_containers.append(container)  # LIFO: topo da pilha
    print(f"Contêiner {codigo} empilhado no topo.")


def pilha_listar():
    """Lista os contêineres do topo para a base."""
    print("\n--- Pilha de Contêineres (topo -> base) ---")
    if not pilha_containers:
        print("Pilha vazia.")
        return

    for pos, cont in enumerate(reversed(pilha_containers), start=1):
        print(f"{pos}. {cont['codigo']} | {cont['tipo']} | "
              f"{cont['peso']}kg | {cont['destino']}")


def pilha_topo():
    """Consulta o contêiner no topo sem removê-lo."""
    if not pilha_containers:
        print("Pilha vazia.")
        return

    cont = pilha_containers[-1]
    print("\n--- Topo da Pilha ---")
    print(f"Código: {cont['codigo']}")
    print(f"Tipo: {cont['tipo']}")
    print(f"Peso: {cont['peso']}kg")
    print(f"Destino: {cont['destino']}")


def pilha_remover():
    """Desempilha o contêiner do topo."""
    if not pilha_containers:
        print("Pilha vazia. Nenhum contêiner para remover.")
        return

    cont = pilha_containers.pop()  # LIFO: remove do topo
    print(f"Contêiner {cont['codigo']} removido do topo.")


def gerenciar_pilha():
    """Submenu da pilha de contêineres."""
    opcoes = {
        1: "Empilhar contêiner",
        2: "Listar pilha",
        3: "Ver topo",
        4: "Desempilhar",
        0: "Voltar"
    }
    while True:
        opcao = menu("PILHA DE CONTÊINERES", opcoes)
        if opcao == 1:
            pilha_inserir()
        elif opcao == 2:
            pilha_listar()
        elif opcao == 3:
            pilha_topo()
        elif opcao == 4:
            pilha_remover()
        elif opcao == 0:
            break
        else:
            print("Opção inválida.")
        pausar()


# ============================================================================
# LISTA - Frota de veículos e transportadoras
# ============================================================================

def lista_inserir():
    """Adiciona um veículo à frota."""
    print("\n--- Cadastrar Veículo na Frota ---")
    id_veiculo = input("ID do veículo: ").strip().upper()
    placa = input("Placa: ").strip().upper()
    transportadora = input("Transportadora: ").strip()
    capacidade = input("Capacidade (toneladas): ").strip()
    status = input("Status (ativo/manutenção/inativo): ").strip()

    if not id_veiculo:
        print("Erro: ID é obrigatório.")
        return

    for v in frota:
        if v["id"] == id_veiculo:
            print("Erro: ID já cadastrado.")
            return

    frota.append({
        "id": id_veiculo,
        "placa": placa,
        "transportadora": transportadora,
        "capacidade": capacidade,
        "status": status
    })
    print(f"Veículo {id_veiculo} cadastrado na frota.")


def lista_listar():
    """Lista todos os veículos cadastrados."""
    print("\n--- Frota Cadastrada ---")
    if not frota:
        print("Nenhum veículo cadastrado.")
        return

    for idx, v in enumerate(frota):
        print(f"{idx}. {v['id']} | {v['placa']} | {v['transportadora']} | "
              f"{v['capacidade']}t | {v['status']}")


def lista_atualizar():
    """Atualiza veículo pelo índice na lista."""
    lista_listar()
    if not frota:
        return

    try:
        idx = int(input("\nÍndice do veículo a atualizar: "))
        if idx < 0 or idx >= len(frota):
            print("Índice inválido.")
            return
    except ValueError:
        print("Índice inválido.")
        return

    v = frota[idx]
    v["placa"] = input(f"Nova placa [{v['placa']}]: ").strip().upper() or v["placa"]
    v["transportadora"] = input(f"Nova transportadora [{v['transportadora']}]: ").strip() or v["transportadora"]
    v["capacidade"] = input(f"Nova capacidade [{v['capacidade']}]: ").strip() or v["capacidade"]
    v["status"] = input(f"Novo status [{v['status']}]: ").strip() or v["status"]
    print("Veículo atualizado.")


def lista_remover():
    """Remove veículo pelo índice na lista."""
    lista_listar()
    if not frota:
        return

    try:
        idx = int(input("\nÍndice do veículo a remover: "))
        if idx < 0 or idx >= len(frota):
            print("Índice inválido.")
            return
    except ValueError:
        print("Índice inválido.")
        return

    removido = frota.pop(idx)
    print(f"Veículo {removido['id']} removido da frota.")


def gerenciar_lista():
    """Submenu da lista de frota."""
    opcoes = {
        1: "Cadastrar veículo",
        2: "Listar frota",
        3: "Atualizar veículo",
        4: "Remover veículo",
        0: "Voltar"
    }
    while True:
        opcao = menu("FROTA DE VEÍCULOS (LISTA)", opcoes)
        if opcao == 1:
            lista_inserir()
        elif opcao == 2:
            lista_listar()
        elif opcao == 3:
            lista_atualizar()
        elif opcao == 4:
            lista_remover()
        elif opcao == 0:
            break
        else:
            print("Opção inválida.")
        pausar()


# ============================================================================
# ÁRVORE - Rotas marítimas (dict aninhado)
# ============================================================================

def arvore_inserir():
    """Insere uma rota marítima na árvore hierárquica."""
    print("\n--- Cadastrar Rota Marítima ---")
    origem = input("Porto de origem: ").strip().title()
    intermediario = input("Porto intermediário: ").strip().title()
    destino = input("Destino final: ").strip().title()

    if not origem or not intermediario or not destino:
        print("Erro: todos os campos são obrigatórios.")
        return

    # Cria hierarquia: origem -> intermediario -> [destinos]
    if origem not in rotas:
        rotas[origem] = {}
    if intermediario not in rotas[origem]:
        rotas[origem][intermediario] = []

    if destino not in rotas[origem][intermediario]:
        rotas[origem][intermediario].append(destino)
        print(f"Rota {origem} -> {intermediario} -> {destino} cadastrada.")
    else:
        print("Essa rota já existe.")


def arvore_listar():
    """Lista todas as rotas marítimas em formato hierárquico."""
    print("\n--- Rotas Marítimas ---")
    if not rotas:
        print("Nenhuma rota cadastrada.")
        return

    for origem, intermediarios in rotas.items():
        print(f"🚢 {origem}")
        for intermediario, destinos in intermediarios.items():
            print(f"   ↳ {intermediario}")
            for destino in destinos:
                print(f"      ↳ {destino}")


def arvore_buscar():
    """Busca destinos a partir de uma origem e porto intermediário."""
    if not rotas:
        print("Nenhuma rota cadastrada.")
        return

    origem = input("\nPorto de origem: ").strip().title()
    if origem not in rotas:
        print("Origem não encontrada.")
        return

    intermediario = input("Porto intermediário: ").strip().title()
    if intermediario not in rotas[origem]:
        print("Porto intermediário não encontrado.")
        return

    print(f"\nDestinos de {origem} -> {intermediario}:")
    for dest in rotas[origem][intermediario]:
        print(f"  - {dest}")


def arvore_remover():
    """Remove um destino, porto intermediário ou origem da árvore."""
    arvore_listar()
    if not rotas:
        return

    origem = input("\nPorto de origem: ").strip().title()
    if origem not in rotas:
        print("Origem não encontrada.")
        return

    intermediario = input("Porto intermediário (deixe em branco para remover origem): ").strip().title()
    if not intermediario:
        del rotas[origem]
        print(f"Origem {origem} removida.")
        return

    if intermediario not in rotas[origem]:
        print("Porto intermediário não encontrado.")
        return

    destino = input("Destino final (deixe em branco para remover intermediário): ").strip().title()
    if not destino:
        del rotas[origem][intermediario]
        if not rotas[origem]:  # se não houver mais intermediários, remove origem
            del rotas[origem]
        print(f"Porto intermediário {intermediario} removido.")
        return

    if destino in rotas[origem][intermediario]:
        rotas[origem][intermediario].remove(destino)
        if not rotas[origem][intermediario]:
            del rotas[origem][intermediario]
        if not rotas[origem]:
            del rotas[origem]
        print(f"Destino {destino} removido.")
    else:
        print("Destino não encontrado.")


def gerenciar_arvore():
    """Submenu da árvore de rotas."""
    opcoes = {
        1: "Cadastrar rota",
        2: "Listar rotas",
        3: "Buscar destinos",
        4: "Remover rota",
        0: "Voltar"
    }
    while True:
        opcao = menu("ROTAS MARÍTIMAS (ÁRVORE)", opcoes)
        if opcao == 1:
            arvore_inserir()
        elif opcao == 2:
            arvore_listar()
        elif opcao == 3:
            arvore_buscar()
        elif opcao == 4:
            arvore_remover()
        elif opcao == 0:
            break
        else:
            print("Opção inválida.")
        pausar()


# ============================================================================
# PERSISTÊNCIA EM ARQUIVO TXT
# ============================================================================

def salvar_dados():
    """Exporta o estado atual das estruturas para o arquivo texto."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        # Salva FILA
        for cam in fila_caminhoes:
            linha = f"FILA{DELIMITADOR}{cam['placa']}{DELIMITADOR}{cam['motorista']}{DELIMITADOR}{cam['transportadora']}{DELIMITADOR}{cam['carga']}\n"
            f.write(linha)

        # Salva PILHA (ordem do arquivo: topo primeiro para reconstrução correta)
        for cont in reversed(pilha_containers):
            linha = f"PILHA{DELIMITADOR}{cont['codigo']}{DELIMITADOR}{cont['tipo']}{DELIMITADOR}{cont['peso']}{DELIMITADOR}{cont['destino']}\n"
            f.write(linha)

        # Salva LISTA
        for v in frota:
            linha = f"LISTA{DELIMITADOR}{v['id']}{DELIMITADOR}{v['placa']}{DELIMITADOR}{v['transportadora']}{DELIMITADOR}{v['capacidade']}{DELIMITADOR}{v['status']}\n"
            f.write(linha)

        # Salva ÁRVORE
        for origem, intermediarios in rotas.items():
            for intermediario, destinos in intermediarios.items():
                for destino in destinos:
                    linha = f"ARVORE{DELIMITADOR}{origem}{DELIMITADOR}{intermediario}{DELIMITADOR}{destino}\n"
                    f.write(linha)

    print(f"Dados salvos com sucesso em '{ARQUIVO_DADOS}'.")


def carregar_dados():
    """Reconstrói as estruturas a partir do arquivo texto."""
    global fila_caminhoes, pilha_containers, frota, rotas

    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Arquivo '{ARQUIVO_DADOS}' não encontrado.")
        return

    # Limpa estruturas antes de carregar
    fila_caminhoes = deque()
    pilha_containers = []
    frota = []
    rotas = {}

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split(DELIMITADOR)
            tipo = partes[0]

            if tipo == "FILA" and len(partes) == 5:
                fila_caminhoes.append({
                    "placa": partes[1],
                    "motorista": partes[2],
                    "transportadora": partes[3],
                    "carga": partes[4]
                })
            elif tipo == "PILHA" and len(partes) == 5:
                # Empilha na ordem inversa de leitura para restaurar o topo
                pilha_containers.insert(0, {
                    "codigo": partes[1],
                    "tipo": partes[2],
                    "peso": partes[3],
                    "destino": partes[4]
                })
            elif tipo == "LISTA" and len(partes) == 6:
                frota.append({
                    "id": partes[1],
                    "placa": partes[2],
                    "transportadora": partes[3],
                    "capacidade": partes[4],
                    "status": partes[5]
                })
            elif tipo == "ARVORE" and len(partes) == 4:
                origem = partes[1]
                intermediario = partes[2]
                destino = partes[3]
                if origem not in rotas:
                    rotas[origem] = {}
                if intermediario not in rotas[origem]:
                    rotas[origem][intermediario] = []
                if destino not in rotas[origem][intermediario]:
                    rotas[origem][intermediario].append(destino)

    print(f"Dados carregados com sucesso de '{ARQUIVO_DADOS}'.")


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def main():
    """Fluxo principal do sistema."""
    opcoes = {
        1: "Gerenciar Fila de Caminhões",
        2: "Gerenciar Pilha de Contêineres",
        3: "Gerenciar Frota (Lista)",
        4: "Gerenciar Rotas Marítimas (Árvore)",
        5: "Salvar Dados",
        6: "Carregar Dados",
        0: "Sair"
    }

    while True:
        opcao = menu("CONTROLE DE LOGÍSTICA PORTUÁRIA", opcoes)
        if opcao == 1:
            gerenciar_fila()
        elif opcao == 2:
            gerenciar_pilha()
        elif opcao == 3:
            gerenciar_lista()
        elif opcao == 4:
            gerenciar_arvore()
        elif opcao == 5:
            salvar_dados()
            pausar()
        elif opcao == 6:
            carregar_dados()
            pausar()
        elif opcao == 0:
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":
    main()
