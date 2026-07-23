from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL
import owlrl
import networkx as nx
from pyvis.network import Network
import webbrowser
import os

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


# ===============================
# VISUALIZADOR DO GRAFO COMPLETO
# ===============================
print("\nGerando interface visual colorida e corrigindo conflito de nomes...")

# ==========================================================
# FUNÇÃO INTELIGENTE DE EXTRAÇÃO DE NOMES
# ==========================================================
def extrair_nome(uri):
    texto = str(uri)
    if '#' in texto:
        return texto.split('#')[-1]
    elif '/' in texto:
        return texto.split('/')[-1]
    return texto

# ==========================================================
# MAPEAMENTO DE CLASSES E CORES (COM PRIORIDADE BLINDADA)
# ==========================================================
ordem_prioridade = [
    "Boss", "InimigoComum", "Vendedor", "NPC", "Personagem",
    "ArteDeUnha", "Chave", "Relíquia", "Amuleto", "Equipamento", "Habilidade",
    "SubRegiao", "Regiao", "Localidade",
    "Item", "Entidade"
]

tipos_entidades = {}

# Varredura para encontrar os tipos (Ignorando Literais)
for s, p, o in g:
    # Se o sujeito for um texto/número solto, pula. Ele não tem classe ontológica.
    if isinstance(s, Literal):
        continue

    if str(p) == str(RDF.type) and not isinstance(o, BNode):
        tipo_str = extrair_nome(o)
        sujeito_str = extrair_nome(s)
        
        # Ignora as classes estruturais padrão
        if tipo_str not in ["Class", "Ontology", "ObjectProperty", "DatatypeProperty", "TransitiveProperty", "SymmetricProperty", "FunctionalProperty", "NamedIndividual"]:
            
            if sujeito_str in tipos_entidades:
                tipo_atual = tipos_entidades[sujeito_str]
                
                # Regra de prioridade corrigida
                if tipo_str in ordem_prioridade:
                    if tipo_atual in ordem_prioridade:
                        if ordem_prioridade.index(tipo_str) < ordem_prioridade.index(tipo_atual):
                            tipos_entidades[sujeito_str] = tipo_str
                    else:
                        # Se o tipo atual for lixo (ex: "string"), sobrepõe na força
                        tipos_entidades[sujeito_str] = tipo_str
            else:
                tipos_entidades[sujeito_str] = tipo_str

cores_classes = {
    "Boss": "#e31a1c",          
    "InimigoComum": "#fb9a99",  
    "NPC": "#33a02c",           
    "Vendedor": "#b2df8a",      
    "Personagem": "#1f78b4",    
    "Regiao": "#ff7f00",        
    "SubRegiao": "#fdbf6f",     
    "Amuleto": "#6a3d9a",       
    "Relíquia": "#cab2d6",      
    "Habilidade": "#00bcd4",    
    "ArteDeUnha": "#a6cee3",    
    "Equipamento": "#b15928",   
    "Chave": "#ffff99",
    "Localidade": "#ff7f00",    
    "Item": "#6a3d9a",          
    "Entidade": "#ffffff"       
}
cor_padrao = "#555555" 

def obter_cor(nome_entidade):
    tipo = tipos_entidades.get(nome_entidade)
    return cores_classes.get(tipo, cor_padrao)

# ==========================================================
# CONSTRUÇÃO DO GRAFO (NETWORKX) COM SEPARAÇÃO DE IDS
# ==========================================================
G = nx.DiGraph()

predicados_ignorados = [
    # Tipagem e Classes
    RDF.type, RDFS.subClassOf, OWL.equivalentClass, OWL.disjointWith,
    
    # Textos e Ontologia
    RDFS.label, RDFS.comment, OWL.Ontology,
    
    # Propriedades e Lógica de Inferência
    RDFS.domain, RDFS.range, OWL.inverseOf, 
    OWL.TransitiveProperty, OWL.SymmetricProperty, OWL.FunctionalProperty, 
    RDFS.subPropertyOf, OWL.equivalentProperty, 
    
    # Identidade
    OWL.sameAs, OWL.differentFrom, OWL.AllDifferent
]

for s, p, o in g:
    if p in predicados_ignorados or isinstance(s, BNode):
        continue

    # Sujeito (Entidade Real)
    sujeito_label = extrair_nome(s)
    sujeito_id = sujeito_label # O ID da entidade é ela mesma
    predicado = extrair_nome(p)
    
    classe_sujeito = tipos_entidades.get(sujeito_label, "Não Mapeado")
    
    # Adicionamos a entidade usando ID e LABEL separados
    G.add_node(sujeito_id, label=sujeito_label, title=f"[{classe_sujeito}] {sujeito_label}\n(Clique para ver conexões)", color=obter_cor(sujeito_label), size=25, shape="dot") 
    
    # Objeto (Pode ser Entidade ou Texto/Número)
    if isinstance(o, Literal):
        objeto_label = str(o)
        objeto_id = f"lit_{objeto_label}" # Evita a fusão entre entidade "Greenpath" e texto "Greenpath"
        
        G.add_node(objeto_id, label=objeto_label, title="Valor (Literal)", color="#333333", shape="box", font={"color": "#aaaaaa", "size": 12})
        
        estilo_texto_aresta = {"color": "#00e5ff", "strokeWidth": 3, "strokeColor": "#111111", "size": 14}
        G.add_edge(sujeito_id, objeto_id, label=predicado, title=f"Relação: {predicado}", color="#444444", font=estilo_texto_aresta)
    else:
        if isinstance(o, BNode): continue
        objeto_label = extrair_nome(o)
        objeto_id = objeto_label # O ID da entidade destino é ela mesma
        
        classe_objeto = tipos_entidades.get(objeto_label, "Não Mapeado")
        
        G.add_node(objeto_id, label=objeto_label, title=f"[{classe_objeto}] {objeto_label}\n(Clique para ver conexões)", color=obter_cor(objeto_label), size=20, shape="dot")   
        
        estilo_texto_aresta = {"color": "#00e5ff", "strokeWidth": 3, "strokeColor": "#111111", "size": 14}
        G.add_edge(sujeito_id, objeto_id, label=predicado, title=f"Relação: {predicado}", color="#444444", font=estilo_texto_aresta)

# ==========================================================
# GERAÇÃO DO ARQUIVO PYVIS E CONFIGURAÇÕES
# ==========================================================
net = Network(notebook=False, directed=True, height="800px", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(G)

configuracao_avancada = """
var options = {
  "interaction": { "hover": true, "selectConnectedEdges": true },
  "edges": {
    "color": { "highlight": "#ffffff", "hover": "#aaaaaa" },
    "smooth": { "enabled": true, "type": "dynamic" }
  },
  "nodes": { "font": { "size": 16, "strokeWidth": 2, "strokeColor": "#000" } },
  "physics": {
    "forceAtlas2Based": { "gravitationalConstant": -80, "centralGravity": 0.01, "springLength": 200, "springConstant": 0.05 },
    "solver": "forceAtlas2Based"
  }
}
"""
net.set_options(configuracao_avancada)

nome_arquivo = "hollow_knight_grafo.html"
net.write_html(nome_arquivo)

# ==========================================================
# INJEÇÃO DOS PAINÉIS LATERAIS E SCRIPTS (Atualizado para Labels)
# ==========================================================
with open(nome_arquivo, "r", encoding="utf-8") as f:
    conteudo_html = f.read()

itens_legenda_html = ""
for classe, cor in cores_classes.items():
    if classe not in ["Localidade", "Item", "Entidade"]:
        itens_legenda_html += f"""
        <div style="margin-bottom: 6px; display: flex; align-items: center;">
            <span style="display:inline-block; width:14px; height:14px; background-color:{cor}; border-radius:50%; margin-right:8px; border: 1px solid #000;"></span>
            <span style="font-size: 13px;">{classe}</span>
        </div>
        """

itens_legenda_html += f"""
    <div style="margin-bottom: 6px; display: flex; align-items: center; margin-top: 10px; padding-top: 10px; border-top: 1px solid #555;">
        <span style="display:inline-block; width:14px; height:10px; background-color:#333333; border-radius:2px; margin-right:8px; border: 1px solid #666;"></span>
        <span style="font-size: 13px; color: #ccc;">Valores Literais (Nomes, HP, Geo)</span>
    </div>
"""

paineis_e_scripts = f"""
<!-- LEGENDA -->
<div style="position: absolute; top: 20px; left: 20px; background-color: rgba(34, 34, 34, 0.9); padding: 15px; border-radius: 8px; border: 1px solid #ffffff; color: white; z-index: 1000; font-family: sans-serif; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
    <h3 style="margin-top: 0; margin-bottom: 15px; font-size: 16px;">Classes da Ontologia</h3>
    {itens_legenda_html}
</div>

<!-- PAINEL LATERAL -->
<div id="painel-conexoes" style="position: absolute; top: 20px; right: 20px; width: 320px; background-color: rgba(34, 34, 34, 0.95); padding: 20px; border-radius: 8px; border: 1px solid #ffffff; color: white; z-index: 1000; font-family: sans-serif; display: none; box-shadow: -2px 2px 15px rgba(0,0,0,0.7); max-height: 80%; overflow-y: auto;">
    <h2 id="nome-no" style="margin-top: 0; border-bottom: 1px solid #555; padding-bottom: 10px;">Nome</h2>
    <div id="lista-conexoes" style="font-size: 14px; line-height: 1.6;"></div>
    <button onclick="document.getElementById('painel-conexoes').style.display='none'" style="margin-top: 20px; width: 100%; padding: 8px; background: #555; border: 1px solid #fff; border-radius: 4px; cursor: pointer; color: #fff; font-weight: bold;">Fechar Painel</button>
</div>

<!-- SCRIPT DE INTERAÇÃO ATUALIZADO PARA RESGATAR O LABEL -->
<script type="text/javascript">
    network.once("stabilizationIterationsDone", function() {{
        network.setOptions({{ physics: false }});
    }});

    network.on("click", function (params) {{
        if (params.nodes.length > 0) {{
            var nodeId = params.nodes[0];
            var nodeObj = network.body.data.nodes.get(nodeId);
            var nodeLabel = nodeObj.label || nodeId; // Usa o Label legível, sem o "lit_"
            
            var edges = network.getConnectedEdges(nodeId);
            var htmlConexoes = "<b>Relações (Triplas):</b><ul style='padding-left: 20px;'>";
            var edgesData = edges.map(edgeId => network.body.data.edges.get(edgeId));
            
            edgesData.forEach(edge => {{
                var fromLabel = network.body.data.nodes.get(edge.from).label || edge.from;
                var toLabel = network.body.data.nodes.get(edge.to).label || edge.to;
                
                if (edge.from === nodeId) {{
                    htmlConexoes += "<li style='margin-bottom:8px;'>--[ <i style='color:#00e5ff'>" + edge.label + "</i> ]--> <b>" + toLabel + "</b></li>";
                }} else if (edge.to === nodeId) {{
                    htmlConexoes += "<li style='margin-bottom:8px;'><b>" + fromLabel + "</b> --[ <i style='color:#00e5ff'>" + edge.label + "</i> ]--></li>";
                }}
            }});
            htmlConexoes += "</ul>";
            
            document.getElementById("nome-no").innerText = nodeLabel;
            document.getElementById("lista-conexoes").innerHTML = htmlConexoes;
            document.getElementById("painel-conexoes").style.display = "block";
        }} else {{
            document.getElementById("painel-conexoes").style.display = "none";
        }}
    }});
</script>
"""

conteudo_html = conteudo_html.replace("</body>", paineis_e_scripts + "\n</body>")
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write(conteudo_html)

caminho_completo = f"file://{os.path.abspath(nome_arquivo)}"
webbrowser.open(caminho_completo)
