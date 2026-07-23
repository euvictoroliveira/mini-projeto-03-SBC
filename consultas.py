import owlrl
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

# Responsável por carregar o grafo RDF
g = Graph()
g.parse("hollow_knight_ontologia.ttl", format="turtle")

# Deduz e expande as triplas com base nas regras OWL (Problema 2 resolvido: Ativação Global)
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

HK = Namespace("http://example.org/hollowknight#")

print(f"Grafo carregado e expandido com {len(g)} triplas.\n")

print("="*50)
print("PARTE 1: Consultas g.triples()")
print("="*50)

# 1. Sujeito Fixo: Encontrar todas as propriedades e objetos para 'The Knight'
print("\n1. Tudo sobre The Knight:")
for s, p, o in g.triples((HK.TheKnight, None, None)):
    print(f"  - {p.split('#')[-1]} -> {o.split('#')[-1] if '#' in o else o}")

# 2. Predicado Fixo: Encontrar todas as entidades que são Bosses (Chefões)
print("\n2. Todos os Bosses:")
for s, p, o in g.triples((None, RDF.type, HK.Boss)):
    print(f"  - {s.split('#')[-1]}")

# 3. Objeto Fixo: Encontrar quem vive em 'Dirtmouth'
print("\n3. Vivem em Dirtmouth:")
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

# 1. SELECT com FILTER: Encontrar itens que custam mais do que 250 Geo
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

# 2. SELECT com ORDER BY: Ordenar personagens por nome (Problema 2 resolvido: DISTINCT)
q2 = """
SELECT DISTINCT ?nome WHERE {
    ?char rdf:type/rdfs:subClassOf* hk:Personagem .
    ?char hk:nome ?nome .
} ORDER BY ASC(?nome)
"""
print("\n2. SPARQL SELECT (Order By): Personagens em ordem alfabética (sem duplicatas)")
for row in g.query(q2):
    print(f"  - {row.nome}")

# 3. ASK: A Hornet Protector vive em Greenpath? (Problema 3 resolvido: Instância real)
q3 = """
ASK { hk:HornetProtector hk:habitaEm hk:Greenpath . }
"""
print("\n3. SPARQL ASK: A Hornet Protector vive em Greenpath?")
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

if sub_graph:
    tam_max_sujeito = max(len(stmt[0].split('#')[-1]) for stmt in sub_graph)
    tam_max_objeto = max(len(stmt[2].split('#')[-1]) for stmt in sub_graph)
    for stmt in sub_graph:
        sujeito = stmt[0].split('#')[-1]
        objeto = stmt[2].split('#')[-1]
        print(f"  - {sujeito:<{tam_max_sujeito+1}} vende {objeto:<{tam_max_objeto}}")
else:
    print("  - Nenhum mercador encontrado.")

# 5. UPDATE - INSERT: Adicionar um novo personagem chamado 'Myla'
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

# 6.1. UPDATE - VERIFICAÇÃO: Checar se 'Soul Master' existe antes de deletar
query_check = """
PREFIX hk: <http://example.org/hollowknight#>
ASK { 
    hk:SoulMaster ?p ?o . 
}
"""
existe_soul_master = bool(g.query(query_check))

if existe_soul_master:
    print("\n6.1. SPARQL UPDATE (VERIFICAÇÃO): O Soul Master EXISTE no grafo. Preparando para a remoção...")
else:
    print("\n6.1. SPARQL UPDATE (VERIFICAÇÃO): O Soul Master NÃO FOI ENCONTRADO no grafo.")

# 6.2. UPDATE - DELETE: Remover 'Soul Master' do grafo
update_delete = """
PREFIX hk: <http://example.org/hollowknight#>
DELETE WHERE {
    hk:SoulMaster ?p ?o .
}
"""
g.update(update_delete)
print("6.2. SPARQL UPDATE (DELETE): Soul Master removido do grafo.")

# 6.3 UPDATE - VERIFICAÇÃO: Checar se 'Soul Master' existe antes de deletar
# O rdflib permite converter o resultado do ASK diretamente para um booleano (True/False)
existe_soul_master = bool(g.query(query_check))

if existe_soul_master:
    print("6.3. SPARQL UPDATE (VERIFICAÇÃO): O Soul Master EXISTE no grafo. Preparando para a remoção...")
else:
    print("6.3. SPARQL UPDATE (VERIFICAÇÃO): O Soul Master NÃO FOI ENCONTRADO no grafo.")

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