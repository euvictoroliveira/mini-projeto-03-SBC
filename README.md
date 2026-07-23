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

## Resumo do Projeto

Este projeto consiste na modelagem de um **Grafo de Conhecimento** baseado no universo do jogo *Hollow Knight*. A base foi construída utilizando as linguagens semânticas **RDF, RDFS e OWL**, estruturada no formato Turtle (`.ttl`).

O objetivo da ontologia é mapear as complexas relações do jogo, interligando os personagens, as localidades que habitam, os itens que comercializam e as habilidades que o jogador pode adquirir. Além do armazenamento estático, o projeto utiliza **raciocínio lógico (inferência)** para deduzir novas relações no grafo dinamicamente e conta com um **visualizador interativo em HTML** para exploração dos nós.

---

## Principais Entidades e Classes

A taxonomia foi desenhada com dois níveis principais abaixo da raiz (`hk:Entidade`), garantindo a organização hierárquica exigida e a aplicação de classes disjuntas (evitando que um personagem seja classificado simultaneamente como um mapa, por exemplo).

* **Entidade:** A classe raiz que engloba tudo no universo mapeado.


* **Personagem:** Representa os diferentes tipos de seres encontrados.
* *Boss (Chefão):* Entidades de alto nível de combate.
* *NPC & Vendedor:* Personagens de interação e comércio.
* *Inimigo Comum:* Ameaças padrão do mapa.


* **Localidade:** Representa o mapa do jogo.
* *Região:* Áreas amplas (ex: Hallownest, Dirtmouth).
* *Sub-região:* Áreas menores contidas nas regiões maiores.


* **Item:** Engloba tudo que pode ser coletado, equipado ou comprado.
* *Amuleto:* Itens que consomem espaços (*notches*) e concedem vantagens.
* *Habilidade / Arte de Unha:* Movimentos especiais adquiridos.
* *Equipamento / Relíquia:* Ferramentas e itens de valor (Geo).

---

## Instruções de Execução

### Pré-requisitos

* **Python 3.x** instalado na máquina.
* Editor de código (VS Code) ou ambiente Jupyter Notebook.

### Passo a Passo para Configuração

**1. Clone o repositório**
Faça o clone deste repositório em sua máquina local e abra o terminal na pasta raiz do projeto.

**2. Crie e ative o ambiente virtual**
É recomendado o uso de um ambiente virtual (`.venv`) para isolar as dependências do projeto.

* **No Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```


* **No Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```



**3. Instale as dependências**
Com o ambiente ativado, instale as bibliotecas necessárias para manipulação de grafos, inferência lógica e geração da interface visual:

```bash
pip install rdflib owlrl networkx pyvis ipykernel
```

**4. Execução do Projeto**

* **Via Terminal:** Execute a aplicação principal rodando `python consultas.py`.
* **Via Jupyter Notebook:** Abra o arquivo `consultas.ipynb` e certifique-se de selecionar o Kernel do ambiente virtual recém-criado para rodar as células.

**5. Resultados Esperados**
Ao executar o script, a aplicação irá:

1. Carregar o arquivo `hollow_knight_ontologia.ttl`.
2. Aplicar as regras de inferência lógica em memória (`owlrl`).
3. Imprimir automaticamente no terminal os resultados das consultas `g.triples()` e buscas em **SPARQL**.
4. Gerar e abrir automaticamente no seu navegador um arquivo HTML (`hollow_knight_grafo.html`) contendo o **Grafo Visual Interativo** da ontologia.