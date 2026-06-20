
REDE_MICROSSERVICOS = {
    "Auth": ["Gateway", "Billing"],
    "Gateway": ["Frontend", "MobileApp"],
    "Billing": ["Notification", "Analytics"],
    "Frontend": ["CacheUI", "Billing"],
    "MobileApp": ["CacheUI", "Logger"],
    "Notification": ["Logger"],
    "Analytics": [],
    "CacheUI": [],
    "Logger": [],
}



def dfs(graph, start):
    seen = []
    paths = {}
    to_see = [ (start, [])  ] # (node, caminho)
    
    while len(to_see) > 0:
        node, path = to_see.pop() # operamos como uma pilha
        seen.append(node)
        paths[node] = [*path, node]

        discovered = graph[node]
        to_see.extend([
            (x, [*path, node]) for x in discovered
            if x not in seen and x not in [x[0] for x in to_see ]
        ])

    return seen, paths

def bfs(graph, start):
    seen = []
    to_see = [ (start, [])  ] # (node, caminho)
    paths = {}
    
    while len(to_see) > 0:
        node, path = to_see[0] # operamos como uma fila
        to_see = to_see[1:]
        seen.append(node)
        paths[node] = [*path, node]

        discovered = graph[node]
        to_see.extend([
            (x, [*path, node]) for x in discovered
            if x not in seen and x not in [x[0] for x in to_see ]
        ])
    return seen, paths


def mapear_raio_falha_bfs(grafo, no_inicial):
    nodes, paths = bfs(grafo, no_inicial)
    return nodes

def encontrar_cadeia_profunda_dfs(grafo, no_inicial):
    nodes, paths = dfs(grafo, no_inicial)
    return sorted(paths.values(), key=lambda i: len(i), reverse=True)[0]

def main(g):
    start = "Auth"
    _bfs, bfs_paths = bfs(g, start)
    _dfs, dfs_paths = dfs(g, start)
    omi = mapear_raio_falha_bfs(g, start)
    ccd = encontrar_cadeia_profunda_dfs(g, start)
    
    print("___________________________")
    print(f"   IMPACTO DA QUEDA DO SERVIÇO {start}")
    
    print("______")
    print("Ordem de Mitigação Imediata:")
    print(f"    Todos os nós afetados: { ', '.join(omi)}")
    distancias = { }
    maior = 0
    for k, v in bfs_paths.items():
        l = len(v)
        if l > maior: maior = l
        if not distancias.get(l): distancias[l] = []
        distancias[l].append(k)

    for i in range(2, maior+1):
        print(f"      Distancia {i}: { ', '.join(distancias[i])}")


    print("______")
    print("Caminho Crítico de Dependência:")
    print(f"    Maior caminho linear: { ' => '.join(ccd)}")
    print(f"    Caminhos relevantes (3 ou mais passos):")
    
    cam = [ v for v in dfs_paths.values() if len(v) > 2]
    cam = sorted(cam, key=lambda i: len(i), reverse=True)
    for cam in cam:
        print(f"        {' => '.join(cam)}")

if __name__ == "__main__":
    main(REDE_MICROSSERVICOS)