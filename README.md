# Controle de Logística Portuária

Sistema desenvolvido em Python como projeto final da disciplina de Estruturas de Dados.
Tema sorteado: **Tema 4 — Controle de Logística Portuária**.

## Como executar

1. Tenha o Python 3 instalado na máquina.
2. Baixe ou clone este repositório.
3. No terminal, entre na pasta do projeto:

```bash
cd logistica-portuaria
```

4. Execute o sistema:

```bash
python main.py
```

5. O programa inicia com todas as estruturas vazias e exibe o menu principal no terminal.

## Arquivos do projeto

- `main.py` — código-fonte completo do sistema (arquivo único).
- `dados_sistema.txt` — arquivo de persistência, gerado automaticamente ao salvar os dados.
- `README.md` — documentação técnica do projeto.

O arquivo `dados_sistema.txt` não precisa existir antes da execução. Ele é criado pelo próprio programa quando o usuário escolhe a opção de salvar.

## Funcionalidades

O menu principal oferece as seguintes opções:

1. Gerenciar Fila de Caminhões
2. Gerenciar Pilha de Contêineres
3. Gerenciar Frota (Lista)
4. Gerenciar Rotas Marítimas (Árvore)
5. Salvar Dados
6. Carregar Dados
0. Sair

Cada estrutura possui um submenu próprio com operações de inserção, listagem, atualização e remoção.

## Funcionamento interno do código

O programa é organizado em funções separadas por estrutura de dados, com um menu principal que delega a execução para submenus específicos. As estruturas são inicializadas vazias no início do programa:

- **Fila** — implementada com `collections.deque`. Os caminhões são inseridos no final com `append` e removidos do início com `popleft`, seguindo a regra FIFO. A busca por caminhão para atualização é feita pela placa.

- **Pilha** — implementada com `list`. Os contêineres são inseridos e removidos pelo topo com `append` e `pop`, seguindo a regra LIFO. A listagem é feita em ordem invertida para mostrar o topo primeiro.

- **Lista** — implementada com `list`. Os veículos da frota são acessados por índice, permitindo atualização e remoção em qualquer posição. A verificação de duplicidade é feita pelo ID.

- **Árvore** — implementada com dicionários aninhados. A estrutura é `rotas[origem][intermediario] = [destinos]`. Cada nível da hierarquia é criado conforme o usuário cadastra novas rotas. A remoção pode ocorrer em qualquer nível (destino, intermediário ou origem).

- **Persistência** — o arquivo `dados_sistema.txt` é lido e escrito linha por linha. Cada linha começa com um identificador (`FILA`, `PILHA`, `LISTA`, `ARVORE`) e os campos são separados pelo delimitador `|`. Ao salvar, a pilha é gravada em ordem invertida (topo primeiro) para que, ao carregar, a reconstrução fique correta.

## Exemplo de uso — resultado final para o usuário

Ao executar `python main.py`, o usuário vê o menu principal:

```
==================================================
  CONTROLE DE LOGÍSTICA PORTUÁRIA
==================================================
  1. Gerenciar Fila de Caminhões
  2. Gerenciar Pilha de Contêineres
  3. Gerenciar Frota (Lista)
  4. Gerenciar Rotas Marítimas (Árvore)
  5. Salvar Dados
  6. Carregar Dados
  0. Sair
==================================================
Escolha uma opção:
```

Ao escolher a opção 1, o submenu da fila é exibido:

```
==================================================
  FILA DE CAMINHÕES
==================================================
  1. Inserir caminhão (chegada)
  2. Listar fila
  3. Atualizar caminhão
  4. Liberar primeiro caminhão
  0. Voltar
==================================================
Escolha uma opção:
```

Ao inserir um caminhão (opção 1), o programa pede os dados e confirma:

```
--- Novo Caminhão na Fila ---
Placa: ABC1234
Motorista: João Silva
Transportadora: TransPorto
Descrição da carga: Carga geral
Caminhão ABC1234 entrou no final da fila.
```

Ao listar a fila (opção 2), o resultado é:

```
--- Fila de Caminhões (ordem de chegada) ---
1. ABC1234 | João Silva | TransPorto | Carga geral
2. XYZ5678 | Maria Costa | LogBrasil | Grãos
```

Ao liberar o primeiro caminhão (opção 4), o sistema remove o primeiro da fila:

```
Caminhão ABC1234 liberado para embarque.
```

O mesmo padrão se repete para as demais estruturas, sempre respeitando suas regras: a pilha remove o contêiner do topo, a lista remove o veículo pelo índice escolhido e a árvore remove rotas em qualquer nível da hierarquia.

## Formato do arquivo de persistência

Após salvar, o arquivo `dados_sistema.txt` fica com o seguinte formato:

```text
FILA|ABC1234|João Silva|TransPorto|Carga geral
FILA|XYZ5678|Maria Costa|LogBrasil|Grãos
PILHA|CNT001|Refrigerado|12000|Santos
PILHA|CNT002|Seco|8500|Paranaguá
LISTA|V001|ABC1234|TransPorto|30|Ativo
LISTA|V002|XYZ5678|LogBrasil|45|Manutenção
ARVORE|Santos|Salvador|Recife
ARVORE|Santos|Salvador|Fortaleza
ARVORE|Paranaguá|Itajaí|Rio Grande
```

Cada linha começa com o identificador da estrutura e os campos são separados por `|`. Ao escolher a opção 6 do menu principal, o programa lê esse arquivo e reconstrói todas as estruturas em memória.

## Justificativa técnica das estruturas

**Fila para a ordem de chegada dos caminhões** — o primeiro caminhão a chegar no pátio deve ser o primeiro a embarcar. Esse comportamento é FIFO (First In, First Out), que é exatamente a regra da fila. Usar `deque` garante eficiência tanto na inserção quanto na remoção.

**Pilha para o empilhamento de contêineres** — contêineres são fisicamente empilhados no navio ou no pátio, e o último colocado é o primeiro a ser retirado. Esse comportamento é LIFO (Last In, First Out), que é a regra da pilha.

**Lista para a frota de veículos** — a frota precisa de acesso flexível, onde qualquer veículo pode ser consultado, atualizado ou removido independentemente da ordem de cadastro. A lista permite isso por meio do acesso direto por índice.

**Árvore para as rotas marítimas** — as rotas têm uma hierarquia clara: um porto de origem se conecta a portos intermediários, que por sua vez se conectam a destinos finais. Essa relação de ramificação é naturalmente representada por uma árvore, implementada aqui com dicionários aninhados.

## Autor

Projeto desenvolvido para fins acadêmicos na disciplina de Estruturas de Dados.
