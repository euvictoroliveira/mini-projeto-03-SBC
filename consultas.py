import owlrl
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

# Responsável por carregar o grafo RDF
g = Graph()
g.parse("hollow_knight_ontologia.ttl", format="turtle")

# Deduz e expande as triplas com base nas regras OWL
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

HK = Namespace("http://example.org/hollowknight#")

print(f"Grafo carregado com {len(g)} triplas.\n")

print("="*50)
print("PARTE 1: Consultas g.triples()")
print("="*50)

# Consultas com g.triples()

# 1. Sujeito Fixo: Encontrar todas as propriedades e objetos para 'Elderbug'
print("\n1. Tudo sobre The Knight:")
for s, p, o in g.triples((HK.TheKnight, None, None)):
    print(f"  - {p.split('#')[-1]} -> {o.split('#')[-1] if '#' in o else o}")

# 2. Predicado Fixo: Encontrar todas as entidades que são Bosses (Chefões)
print("\n2. Todos os Bosses:")
for s, p, o in g.triples((None, RDF.type, HK.Boss)):
    print(f"  - {s.split('#')[-1]}")

# 3. Objeto Fixo: Encontrar quem vive em 'Forgotten Crossroads'
print("\n3. Vivem em Dirthmouth:")
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


print("\n" + "="*50)
print("PARTE 2: Consultas SPARQL")
print("="*50)

# Consultas SPARQL

# 1. SELECT com FILTER: Encontrar itens que custam mais do que 200 Geo
q1 = """
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
ASK { hk:Hornet hk:habitaEm hk:Dirtmouth . }
"""
print("\n3. SPARQL ASK: A Hornet vive em Dirtmouth?")
for row in g.query(q3):
    print(f"  - Resultado: {row}")

# 4. CONSTRUCT: Criar um sub-grafo de mercadores e o que eles vendem
q4 = """
CONSTRUCT { ?merchant hk:vende ?item . }
WHERE { ?merchant hk:vende ?item . }
"""
print("\n4. SPARQL CONSTRUCT: Sub-grafo de mercadores criado. (ordenado)")
sub_graph = g.query(q4)
sub_graph = sorted(sub_graph, key=lambda tripla : tripla[0])

tam_max_sujeito = max(len(stmt[0].split('#')[-1]) for stmt in sub_graph)
tam_max_objeto = max(len(stmt[2].split('#')[-1]) for stmt in sub_graph)


for stmt in sub_graph:
    sujeito = stmt[0].split('#')[-1]
    objeto = stmt[2].split('#')[-1]
    
    # E passamos as variáveis de tamanho entre as chaves extras
    print(f"  - {sujeito:<{tam_max_sujeito+1}} vende {objeto:<{tam_max_objeto}}")

# 5. UPDATE - INSERT: Adicionar um novo personagem chamado'Myla'
update_insert = """
PREFIX hk: <http://example.org/hollowknight#>
INSERT DATA {
    hk:Myla rdf:type hk:NPC ;
            hk:nome "Myla" ;
            hk:habitaEm hk:ForgottenCrossroads .
}
"""
g.update(update_insert)
print("\n5. SPARQL UPDATE (INSERT): Myla adicionada ao grafo.")

# 6. UPDATE - DELETE: Remover 'Tiktik' do grafo
update_delete = """
PREFIX hk: <http://example.org/hollowknight#>
DELETE WHERE {
    hk:Tiktik ?p ?o .
}
"""
g.update(update_delete)
print("\n6. SPARQL UPDATE (DELETE): Tiktik removido do grafo.")

# 7. UPDATE - DELETE/INSERT: Mover Elderbug para Greenpath
update_move = """
PREFIX hk: <http://example.org/hollowknight#>
DELETE { hk:Elderbug hk:habitaEm hk:Dirtmouth . }
INSERT { hk:Elderbug hk:habitaEm hk:Greenpath . }
WHERE  { hk:Elderbug hk:habitaEm hk:Dirtmouth . }
"""
g.update(update_move)
print("\n7. SPARQL UPDATE (DELETE/INSERT): Elderbug movido para Greenpath.")

# 8. SELECT (Agregação): Contar o total de bosses
q8 = """
SELECT (COUNT(?boss) AS ?totalBosses) WHERE {
    ?boss rdf:type hk:Boss .
}
"""
print("\n8. SPARQL SELECT (Agregação): Total de Bosses")
for row in g.query(q8):
    print(f"  - Total: {row.totalBosses}")