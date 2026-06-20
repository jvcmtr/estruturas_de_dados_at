
class Kruskal:
    # Edges aqui deve estar no formato: (nodeA, nodeB, custo)
    def __init__(self, cities, edges):
        self.cities = cities
        self.edges = sorted(edges, key=lambda x: x[2])

        # Dados adicionais para a computação da MST
        self.n_conn = {city: 0 for city in cities}
        self.max_conn = {city: 3 for city in cities}
        self.max_conn['Madrid'] = 4
        
        # Estrutura auxiliar de subarvore estruturada da seguinte forma: 
        #   subtrees[node] = (pai, nodes_conectados)
        # Desta forma a estrutura se torna bidirecional, ou seja, podemos encontrar 
        # a raiz apartir dos nodes e nodes a partir da raiz em O(1)
        self.subtrees = {city: (city, [city]) for city in cities}
        self.roots = [*cities]

    def _find_root(self, node):
        "Retorna a raiz da sub arvore a qual node pertence"
        if self.subtrees[node][0] == node: 
            return node
        return self._find_root(self.subtrees[node][0])
    
    def _find_children(self, node):
        return self.subtrees[node][1]

    def _try_connect(self, a, b):
        """ Tenta conectar os nodes A e B,
            retorna T ou F a depender se a conexão foi ou não feita.
        """
        root_a = self._find_root(a)
        root_b = self._find_root(b)

        if root_a != root_b: 
            self.n_conn[a] += 1
            self.n_conn[b] += 1
            self.subtrees[root_b] = (root_a, self.subtrees[root_b][1])
            self.subtrees[root_a][1].extend(self.subtrees[root_b][1])
            self.roots.remove(root_b)
            return True
        return False

    def _can_conect(self, a, b):
        "Aplica a 'Restrição de Conectividade Física' definida na questão "
        return ( 
            self.n_conn[a] < self.max_conn[a] 
            and self.n_conn[b] < self.max_conn[b]
        )

    def run(self):
        """Constroi uma mst e retorna: (edges, total_cost, subtrees)"""
        mst = []
        total_cost = 0
        for a, b, weight in self.edges:
            if not self._can_conect(a, b): continue 
            if not self._try_connect(a, b): continue
            mst.append((a, b, weight))
            total_cost += weight

        return mst, total_cost, [ self._find_children(x) for x in self.roots ]

def analize_resiliencia(cities, edges):
    mst, cost, subtrees = Kruskal(cities, edges).run()
    if len(subtrees) > 1:
        raise "ERRO - Nenhuma MST foi encontrada para o caso fornescido"
    
    result = [] # {"failed":None, "backup":None, "impact":-1}

    for failed_edge in mst:
        n_edges = [x for x in edges if x != failed_edge]
        partial_mst = [x for x in mst if x != failed_edge]
        _, n_cost, n_subtrees = Kruskal(cities, partial_mst).run()

        if len(n_subtrees) != 2:
            raise "ERRO - Numero de subarvores diferente de 2"
        
        # Encontra melhor backup (edge que conecta as duas subarvores)
        menor, bk = None, None
        for n1, n2, cost in n_edges:
            if (n1 in n_subtrees[0] and n2 in n_subtrees[1] or 
                n2 in n_subtrees[0] and n1 in n_subtrees[1]):
                if not menor or cost < menor:
                    menor = cost
                    bk = (n1, n2, cost)
        impact = bk[2] - failed_edge[2] if bk else -1
        result.append({"failed":failed_edge, "backup":bk, "impact": impact})
    return result


EDGES = [
    ("Coruna", "Vigo", 171),
    ("Coruna", "Valladolid", 455),
    ("Oviedo", "Bilbao", 304),
    ("Bilbao", "Valladolid", 193),
    ("Bilbao", "Madrid", 395),
    ("Bilbao", "Zaragoza", 324),
    ("Vigo", "Valladolid", 356),
    ("Valladolid", "Madrid", 193),
    ("Zaragoza", "Madrid", 325),
    ("Zaragoza", "Barcelona", 296),
    ("Gerona", "Barcelona", 100),
    ("Barcelona", "Valencia", 349),
    ("Madrid", "Badajoz", 403),
    ("Madrid", "Jaen", 335),
    ("Madrid", "Albacete", 251),
    ("Jaen", "Sevilla", 242),
    ("Jaen", "Granada", 99),
    ("Albacete", "Valencia", 191),
    ("Albacete", "Murcia", 150),
    ("Valencia", "Murcia", 241),
    ("Sevilla", "Cadiz", 125),
    ("Sevilla", "Granada", 256),
    ("Granada", "Murcia", 279)
]


CIDADES = [
    "Coruna",
    "Oviedo", 
    "Bilbao", 
    
    "Vigo", 
    "Valladolid", 
    "Zaragoza", 
    "Gerona",
    "Barcelona", 

    "Madrid",

    "Badajoz", 
    "Jaen", 
    "Albacete", 
    "Valencia", 
    
    "Sevilla", 
    "Granada", 
    "Murcia",
    "Cadiz"
]

if __name__ == "__main__":

    mst, custo, _ = Kruskal(CIDADES, EDGES).run()
    
    def line(edge, include_cost=False, strip=False):
        c = ' '
        spacer = c * (11 - len(edge[0]))
        spacer2 = c * (11 - len(edge[1]))
        cost = "" if not include_cost else f"(custo:{edge[2]})"
        s =  f"{spacer} {edge[0]}  =>  {edge[1]} {spacer2} {cost}"
        return s.strip() if strip else s 

    print("___________________________")
    print("   Gerando MST com restrição de conectividade física:")
    print(f"Custo total: {custo}")
    print(f"Arestas selecionadas:")
    for e in mst:
        print("    " + line(e))
    

    print("___________________________")
    print("   Gerando Analise de resiliencia:")
    results = analize_resiliencia(CIDADES, EDGES)
    

    # Linhas que conectam 'folhas' no grafo não podem ser substituidas por linhas alternativas,
    # Logo representam as linhas mais criticas, já que não possuem backup possivel.
    results_unsolved = [x for x in results if not x['backup']] 
    results_solved = [x for x in results if x['backup']!=None] 
    print(f"Linhas criticas insolucionaveis : ")
    for x in results_unsolved:
        print("    " + line(x['failed']))


    # Linhas solucionaveis cujo da implantação de um backup é mais caro,
    # ou seja, considerando que todas as linhas tem a mesma probabilidade
    # de falha, representam o pior investimento possivel. 
    results_bkcost = sorted(results_solved, key=lambda e: e["backup"][2])
    c_reparo = results_bkcost[-1]
    print(f"Linha com maior custo de reparo : {line(c_reparo['failed'], strip=True)} ")
    print(f"    Melhor backup : { line(c_reparo['backup'], True, True)}")
    print(f"    Custo total incluindo backup: { custo + c_reparo['backup'][2]}")


    # O "impacto" é calculado como: 
    #       impacto = preço da alternativa - preço da linha original
    # Assim como o caso anterior, também aponta backups caros, mas leva
    # em conta a diferença de custo entre o backup e a linha original
    results_impact = sorted(results_solved, key=lambda e: e["impact"])
    c_impact = results_impact[-1]
    print(f"Linha com maior impacto : {line(c_impact['failed'], strip=True)} ")
    print(f"    Melhor backup : { line(c_impact['backup'], True, True)}")
    print(f"    Custo total incluindo backup: { custo + c_impact['backup'][2]}")

    # Linhas solucionaveis cuja da implantação de um backup é mais barata,
    # ou seja, considerando que todas as linhas tem a mesma probabilidade
    # de falha, representam bons investimentos que melhoram a estabilidade da rede
    # sem agregar muito custo. 
    results_bk = sorted(results_solved, key=lambda e: e["backup"][2])
    c_bk = results_impact[0]
    print(f"Linha backup mais barato : {line(c_bk['failed'], strip=True)} ")
    print(f"    Melhor backup : { line(c_bk['backup'], True, True)}")
    print(f"    Custo total incluindo backup: { custo + c_bk['backup'][2]}")

   


