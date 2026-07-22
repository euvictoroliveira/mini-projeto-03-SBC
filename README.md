# Mini-Projeto 3: Ontologia de Hollow Knight (Sistemas Baseados em Conhecimento)

**Instituição:** Universidade Federal da Paraíba (UFPB) - Ciência da Computação  
**Período:** 2026.1  

---

## Equipe

| #   | Nome completo             | Matrícula       |
| --- | ------------------------- | --------------- |
| 1   | João Victor Oliveira      | (20240008468)   |
| 2   | Kevin Gabriel Mangueira   | (20240008000)   |
| 3   | Luiz Henrique Santos      | (20240008261)   |
| 4   | Victor Gabriel Menezes    | (20240008323)   |

---

## Resumo da Base
Este projeto consiste na modelagem de um Grafo de Conhecimento baseado no universo do jogo Hollow Knight. A base foi construída utilizando as linguagens RDF, RDFS e OWL, e estruturada no formato Turtle (`.ttl`). O objetivo da ontologia é mapear as complexas relações do jogo, interligando os personagens, as localidades que habitam, os itens que comercializam e as habilidades que o jogador pode adquirir. Além do armazenamento estático, o projeto utiliza raciocínio lógico (inferência) para deduzir novas relações no grafo dinamicamente.

## Principais Entidades e Classes
* **Entidade:** A classe raiz que engloba tudo no universo mapeado.
* **Personagem:** Subdividido para representar os diferentes tipos de seres encontrados.
* **Localidade:** Representa o mapa do jogo, desde grandes áreas até salas específicas.
* **Item:** Engloba tudo que pode ser coletado, equipado ou comprado.
* **Boss (Chefão):** Entidades de alto nível de combate.
* **Amuleto:** Itens que consomem espaços e concedem vantagens.

## Explicação Básica da Taxonomia (Hierarquia)
A taxonomia foi desenhada com dois níveis principais abaixo da raiz (`hk:Entidade`), garantindo a organização hierárquica exigida. A classe `hk:Personagem` ramifica-se em `hk:Boss`, `hk:NPC` e `hk:InimigoComum`. A classe `hk:Localidade` divide-se em `hk:Regiao` (áreas amplas como Hallownest e Dirtmouth) e `hk:SubRegiao` (áreas menores contidas nas regiões maiores). Por fim, a classe `hk:Item` ramifica-se em `hk:Amuleto`, `hk:Habilidade` e `hk:Equipamento`. Classes disjuntas foram aplicadas para garantir que, por exemplo, um personagem não possa ser classificado simultaneamente como um mapa ou um item.

---

## Instruções de Execução

**Pré-requisitos:**
* Python 3.x instalado na máquina.
* Editor de código (VS Code) ou ambiente Jupyter Notebook.

**Passo a Passo:**
1. Clone este repositório em sua máquina local.
2. Abra o terminal na pasta raiz do projeto e crie um ambiente virtual (`.venv`) para isolar as dependências. 
3. Ative o ambiente virtual criado. No Windows, utilize o comando `.\.venv\Scripts\activate`. No Linux, utilize `source .venv/bin/activate`.
4. Instale as bibliotecas necessárias executando o comando: `pip install rdflib owlrl ipykernel`.
5. Execute a aplicação principal rodando `python consultas.py` no terminal, ou certifique-se de selecionar o Kernel do ambiente virtual recém-criado caso opte por executar as células do arquivo `consultas.ipynb`.
6. A aplicação carregará o arquivo `hollow_knight_ontologia.ttl`, aplicará as regras de inferência em memória e imprimirá automaticamente no terminal os resultados das consultas `g.triples()` e SPARQL.