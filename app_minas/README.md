# Otimização de Trajetos em Túneis de Mineração

Uma aplicação desktop em Python para encontrar caminhos ótimos em redes de túneis de mineração usando algoritmos de busca.

## Características

- **Interface Gráfica Intuitiva**: Interface desktop desenvolvida com PyQt5
- **Múltiplos Algoritmos de Busca**:
  - Busca em Amplitude (BFS)
  - Busca em Profundidade (DFS)
  - Busca em Profundidade Limitada
  - Busca por Aprofundamento Iterativo
  - Busca Bidirecional
  - **Custo Uniforme (UCS)**
  - **Busca Gulosa (Greedy)**
  - **A-estrela (A\*)**
  - **AIA-estrela (IDA\*)**
- **Visualização Aprimorada do Grafo**: Representação visual da rede de túneis com nós e arestas, agora com as seguintes melhorias:
  - **Exibição de Custos nas Arestas**: Os custos entre os nós são exibidos diretamente sobre as arestas.
  - **Layout Circular Otimizado**: O raio do layout circular foi aumentado para melhorar a separação dos nós e a legibilidade.
  - **Posicionamento Inteligente de Rótulos**: Os rótulos de custo são deslocados perpendicularmente às arestas para evitar sobreposição.
  - **Zoom Ancorado no Cursor**: A funcionalidade de zoom (roda do mouse) agora se concentra na posição do cursor, facilitando a inspeção de detalhes.
- **Visualização Aprimorada da Árvore de Busca**: Mostra como o algoritmo explora o espaço de busca, agora com **Zoom Ancorado no Cursor** para melhor navegação.
- **Resultados de Busca Corrigidos**: Exibição correta dos campos **"Nós visitados"** e **"Ordem de visitação"** para todos os algoritmos, incluindo os métodos ponderados.
- **Carregamento de Arquivos**: Suporte para carregar grafos de arquivos de texto.

## Requisitos

- Python 3.7+
- PyQt5

## Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:

   ```bash
   pip install PyQt5
   ```

### Executar a Aplicação GUI

Abra a pasta "FINAL P1 - IA - 02_11" no terminal
Se houver VS Code instalado em sua máquina, use 

```bash
code .
```
para acessar o app no editor.

Siga o caminho e execute o arquivo principal:
```bash
cd app_minas/
python main.py
```

## Formato do Arquivo de Grafo

O arquivo deve seguir o formato:

```
<número_de_nós>
<origem> <destino> <custo>
<origem> <destino> <custo>
...
```

**Nota:** Para grafos não ponderados, o campo `<custo>` pode ser omitido ou definido como `1`.

Exemplo de grafo ponderado:

```
5
1 2 10
1 3 5
2 4 15
3 4 20
4 5 5
```

## Estrutura do Projeto

```
mining_path_optimizer/
├── main.py                       # Ponto de entrada da aplicação
├── app_controller.py             # Controlador principal (Corrigido para resultados de busca)
├── test_console.py               # Testes em modo console
├── gui/                          # Interface gráfica
│   ├── main_window.py            # Janela principal
│   ├── graph_viewer.py           # Visualização do grafo (Melhorias de visualização e zoom)
│   └── tree_viewer.py            # Visualização da árvore (Zoom ancorado no cursor)
├── core/                         # Lógica de negócios
│   ├── graph_model.py            # Modelo do grafo
│   ├── node_p.py                 # Modelo do grafo ponderado
│   ├── search_algorithms.py      # Algoritmos de busca não ponderados
│   ├── search_algorithms_p.py    # Algoritmos de busca ponderados (Corrigido para ordem de visitação)
│   └── utils.py                  # Funções utilitárias
├── data/                         # Arquivos de dados
│   └── exemplo_grafo.txt         # Exemplo de grafo
|   └── exemplo_ponderado.txt     # Exemplo de grafo ponderado
└── README.md
```

## Algoritmos Implementados

### Busca Não Ponderada

| Algoritmo | Descrição | Complexidade |
| :--- | :--- | :--- |
| **Busca em Amplitude (BFS)** | Explora todos os nós de um nível antes de passar para o próximo. Garante encontrar o caminho com menor número de arestas. | O(V + E) |
| **Busca em Profundidade (DFS)** | Explora o mais profundo possível antes de retroceder. Pode não encontrar o caminho ótimo. | O(V + E) |
| **Busca em Profundidade Limitada** | DFS com limite de profundidade. Evita loops infinitos. | O(V + E) |
| **Busca por Aprofundamento Iterativo** | Executa DFS limitada com limite crescente. Combina vantagens de BFS e DFS. | O(V + E) |
| **Busca Bidirecional** | Executa busca simultaneamente do início e do fim. Reduz o espaço de busca pela metade. | O(V + E) |

### Busca Ponderada (Heurística)

| Algoritmo | Descrição | Função de Avaliação |
| :--- | :--- | :--- |
| **Custo Uniforme (UCS)** | Expande o nó com o menor custo acumulado ($g(n)$). Garante o caminho de menor custo. | $f(n) = g(n)$ |
| **Busca Gulosa (Greedy)** | Expande o nó mais próximo do objetivo, baseado apenas na heurística ($h(n)$). Não garante o caminho de menor custo. | $f(n) = h(n)$ |
| **A-estrela (A\*)** | Expande o nó com o menor custo total estimado ($g(n) + h(n)$). Garante o caminho de menor custo se a heurística for admissível. | $f(n) = g(n) + h(n)$ |
| **AIA-estrela (IDA\*)** | Versão de A\* com aprofundamento iterativo. Usa menos memória que A\*. | $f(n) = g(n) + h(n)$ |

## Exemplo de Uso

1. Execute a aplicação.
2. Carregue um arquivo de grafo ou use o exemplo pré-carregado.
3. Digite o nó de origem (ex: 1).
4. Digite o nó de destino (ex: 10).
5. Selecione o algoritmo de busca.
6. Clique em "EXECUTAR".
7. Visualize o resultado no painel de texto (agora com a **Ordem de Visitação** correta) e nas visualizações gráficas (agora com **custos nas arestas** e **zoom ancorado**).

## Modelagem do Problema

### Representação
- **Grafo**: Rede de túneis representada como grafo não-direcionado.
- **Nós**: Interseções ou pontos de interesse nos túneis.
- **Arestas**: Segmentos de túnel com custos associados (distância, tempo, etc.).

### Estado
- Posição atual da máquina no grafo (nó atual).
- Custo acumulado do caminho.
- Profundidade na árvore de busca.

### Função Sucessor
- Retorna todos os nós adjacentes ao nó atual.
- Inclui o custo para alcançar cada sucessor.

### Função Custo
- Custo acumulado do caminho do início até o nó atual.
- Soma dos custos das arestas percorridas.

## Contribuição

Este projeto foi desenvolvido como parte de um sistema de otimização de trajetos em túneis de mineração, implementando algoritmos clássicos de busca em grafos com visualização interativa.

**Desenvolvido e aprimorado por:** Wellington Rodrigues
**Semestre:** 6º
**Instituição:** FATEC Cruzeiro
