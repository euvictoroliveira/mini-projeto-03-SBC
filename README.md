# Mini-Projeto 3: Ontologia de Hollow Knight (Sistemas Baseados em Conhecimento)

**Equipe:**

Período: **2026.1**
---
## Equipe

| #   | Nome completo             | Matrícula       |
| --- | ------------------------- | --------------- |
| 1   | *João Victor Oliveira*    | *(20240008468)* |
| 2   | *Kevin Gabriel Mangueira* | *(20240008000)* |
| 3   | *Luiz Henrique Santos*    | *(20240008261)* |
| 4   | *Victor Gabriel Menezes*  | *(20240008323)* |

## Resumo da Base
Este projeto consiste na modelagem de um Grafo de Conhecimento baseado no universo do jogo Hollow Knight. A base foi construída utilizando as linguagens RDF, RDFS e OWL, e estruturada no formato Turtle (`.ttl`). O objetivo da ontologia é mapear as complexas relações do jogo, interligando os personagens, as localidades que habitam, os itens que comercializam e as habilidades que o jogador pode adquirir.

## Principais Entidades e Classes
* **Entidade:** A classe raiz que engloba tudo no universo mapeado.
* **Personagem:** Subdividido para representar os diferentes tipos de seres encontrados.
* **Localidade:** Representa o mapa do jogo, desde grandes áreas até salas específicas.
* **Item:** Engloba tudo que pode ser coletado, equipado ou comprado.
* **Boss (Chefão):** Entidades de alto nível de combate.
* **Amuleto:** Itens que consomem espaços e concedem vantagens.

## Explicação Básica da Taxonomia (Hierarquia)
A taxonomia foi desenhada com dois níveis principais abaixo da raiz (`hk:Entidade`), garantindo a organização hierárquica exigida. A classe `hk:Personagem` ramifica-se em `hk:Boss`, `hk:NPC` e `hk:InimigoComum`. A classe `hk:Localidade` divide-se em `hk:Regiao` (áreas amplas como Hallownest e Dirtmouth) e `hk:SubRegiao` (áreas menores contidas nas regiões maiores). Por fim, a classe `hk:Item` ramifica-se em `hk:Amuleto`, `hk:Habilidade` e `hk:Equipamento`. Classes disjuntas foram aplicadas para garantir que, por exemplo, um personagem não possa ser classificado como um mapa ou um item.

## Instruções de Execução

**Pré-requisitos:**
* Python 3.x instalado.
* Biblioteca `rdflib` instalada.

**Passo a passo:**
1. Clone este repositório em sua máquina local.
2. Abra o terminal na pasta do projeto.
3. Instale a dependência necessária executando o comando: `pip install rdflib`
4. Execute a aplicação principal com o comando: `python consultas.py` (ou execute as células caso esteja usando um Jupyter Notebook `consultas.ipynb`).
5. A aplicação carregará o arquivo `hollow_knight_ontologia.ttl` e imprimirá automaticamente no terminal os resultados das 5 consultas `g.triples()` e das 8 consultas SPARQL, detalhando o propósito de cada uma.