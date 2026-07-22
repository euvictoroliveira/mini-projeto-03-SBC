from pathlib import Path
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF
import owlrl

BASE_DIR = Path(__file__).resolve().parent
ONTOLOGY_PATH = BASE_DIR / "hollow_knight_ontologia.ttl"

# Carregar o grafo
print("Carregando ontologia...")
g = Graph()
g.parse(ONTOLOGY_PATH, format="turtle")

HK = Namespace("http://example.org/hollowknight#")

print(f"Grafo carregado com sucesso! Triplas carregadas: {len(g)}")
print()

print("=" * 60)
print("PARTE 1: Consultas g.triples()")
print("=" * 60)

# 1. Sujeito Fixo: Encontrar todas as propriedades e objetos para 'The Knight'
print("\n1. Tudo sobre The Knight:")
for s, p, o in g.triples((HK.TheKnight, None, None)):
    print(f"  - {p.split('#')[-1]} -> {o.split('#')[-1] if '#' in o else o}")

# 2. Predicado Fixo: Encontrar todas as entidades que são Bosses (Chefões)
print("\n2. Todos os Bosses:")
for s, p, o in g.triples((None, RDF.type, HK.Boss)):
    print(f"  - {s.split('#')[-1]}")

# 3. Objeto Fixo: Encontrar quem vive em 'Forgotten Crossroads'
print("\n3. Quem vive em Dirthmouth:")
for s, p, o in g.triples((None, HK.habitaEm, HK.Dirtmouth)):
    print(f"  - {s.split('#')[-1]}")

# 4. Sujeito e Predicado Fixos: Encontrar o que a Iselda vende
print("\n4. O que a Iselda vende:")
for s, p, o in g.triples((HK.Iselda, HK.vende, None)):
    print(f"  - {o.split('#')[-1]}")

# 5. Predicado e Objeto Fixos: Encontrar amuletos que custam 220 Geo
print("\n5. Amuletos que custam 220 Geo:")
for s, p, o in g.triples((None, HK.custoGeo, Literal(220))):
    print(f"  - {s.split('#')[-1]}")

print()
print("=" * 60)
print("PARTE 2: Consultas SPARQL")
print("=" * 60)

# 1. SELECT com FILTER: Encontrar itens que custam mais de 250 Geo
q1 = """
PREFIX hk: <http://example.org/hollowknight#>
SELECT ?nome ?custo WHERE {
    ?item rdf:type hk:Amuleto .
    ?item hk:nome ?nome .
    ?item hk:custoGeo ?custo .
    FILTER(?custo > 250)
}
"""
print("\n1. SPARQL SELECT (Filter): Amuletos > 250 Geo")
for row in g.query(q1):
    print(f"  - {row.nome} custa {row.custo}")

# 2. SELECT com ORDER BY: Ordenar personagens por nome
q2 = """
PREFIX hk: <http://example.org/hollowknight#>
SELECT ?nome WHERE {
    ?char rdf:type/rdfs:subClassOf* hk:Personagem .
    ?char hk:nome ?nome .
} ORDER BY ASC(?nome)
"""
print("\n2. SPARQL SELECT (Order By): Personagens em ordem alfabética")
for row in g.query(q2):
    print(f"  - {row.nome}")

# 3. ASK: A Hornet vive em Greenpath?
q3 = """
PREFIX hk: <http://example.org/hollowknight#>
ASK { hk:Hornet hk:habitaEm hk:Dirtmouth . }
"""
print("\n3. SPARQL ASK: A Hornet vive em Dirtmouth?")
result = g.query(q3)
print(f"  - Resultado: {result.askAnswer}")

# 4. CONSTRUCT: Criar um sub-grafo de mercadores e o que eles vendem
q4 = """
PREFIX hk: <http://example.org/hollowknight#>
CONSTRUCT { ?merchant hk:vende ?item . }
WHERE { ?merchant hk:vende ?item . }
"""
print("\n4. SPARQL CONSTRUCT: Sub-grafo de mercadores criado (ordenado)")
sub_graph = g.query(q4)
sub_graph = sorted(sub_graph, key=lambda tripla: str(tripla[0]))

if sub_graph:
    tam_max_sujeito = max(len(str(stmt[0]).split('#')[-1]) for stmt in sub_graph)
    tam_max_objeto = max(len(str(stmt[2]).split('#')[-1]) for stmt in sub_graph)

    for stmt in sub_graph:
        sujeito = str(stmt[0]).split('#')[-1]
        objeto = str(stmt[2]).split('#')[-1]
        print(f"  - {sujeito:<{tam_max_sujeito + 1}} vende {objeto:<{tam_max_objeto}}")
else:
    print("  - Nenhuma relação encontrada.")

print()
print("=" * 60)
print("PARTE 3: Inferência OWL RL")
print("=" * 60)

# 5. Relação inversa de vende é compradoDe (verificando as novas relações inferidas)
g_ = Graph()
for tripla in g:
    g_.add(tripla)

print(f"Total de triplas ANTES da inferência: {len(g_)}")

query_pre_expansao = """
PREFIX hk: <http://example.org/hollowknight#>
SELECT ?item ?npc
WHERE {
    ?item hk:compradoDe ?npc .
}
"""

resultado_pre_expansao = g_.query(query_pre_expansao)
print("\nTripla de 'comprado de' antes da expansão:")
for linha in resultado_pre_expansao:
    item = str(linha.item).split('#')[-1]
    npc = str(linha.npc).split('#')[-1]
    print(f"  - {item:<25} comprado de '{npc}'")

print(f"\n{'-' * 45}")

owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g_)

print(f"\nTotal de triplas DEPOIS da inferência: {len(g_)}")

query_inferida = """
PREFIX hk: <http://example.org/hollowknight#>
SELECT ?item ?npc
WHERE {
    ?item hk:compradoDe ?npc .
}
"""

resultados = g_.query(query_inferida)
print("\nTripla de 'comprado de' depois da expansão:")
for linha in resultados:
    item = str(linha.item).split('#')[-1]
    npc = str(linha.npc).split('#')[-1]
    print(f"  - {item:<25} comprado de '{npc}'")

print()
print("=" * 60)
print("PARTE 4: SPARQL UPDATE")
print("=" * 60)

# 6. UPDATE - INSERT: Adicionar um novo personagem 'Myla'
update_insert = """
PREFIX hk: <http://example.org/hollowknight#>
INSERT DATA {
    hk:Myla rdf:type hk:NPC ;
            hk:nome "Myla" ;
            hk:habitaEm hk:ForgottenCrossroads .
}
"""
g.update(update_insert)
print("\n6. SPARQL UPDATE (INSERT): Myla adicionada ao grafo.")

# 7. UPDATE - DELETE: Remover 'Tiktik' do grafo
update_delete = """
PREFIX hk: <http://example.org/hollowknight#>
DELETE WHERE {
    hk:Tiktik ?p ?o .
}
"""
g.update(update_delete)
print("\n7. SPARQL UPDATE (DELETE): Tiktik removido do grafo.")

# 8. UPDATE - DELETE/INSERT: Mover Elderbug para Greenpath
update_move = """
PREFIX hk: <http://example.org/hollowknight#>
DELETE { hk:Elderbug hk:habitaEm hk:Dirtmouth . }
INSERT { hk:Elderbug hk:habitaEm hk:Greenpath . }
WHERE  { hk:Elderbug hk:habitaEm hk:Dirtmouth . }
"""
g.update(update_move)
print("\n8. SPARQL UPDATE (DELETE/INSERT): Elderbug movido para Greenpath.")

# 9. SELECT (Agregação): Contar o total de bosses
q8 = """
PREFIX hk: <http://example.org/hollowknight#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT (COUNT(?boss) AS ?totalBosses) WHERE {
    ?boss rdf:type hk:Boss .
}
"""
print("\n9. SPARQL SELECT (Agregação): Total de Bosses")
for row in g.query(q8):
    print(f"  - Total: {row.totalBosses}")
