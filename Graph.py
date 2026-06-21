from math import inf

class DirectedWeightedEdge:
    def __init__(self, source, destination, weight=1, meta={}):
        self.source = source
        self.destination = destination
        self.weight = weight
        self.meta = meta

    def get(self, key):
        return self.meta[key]

    def contains(self, node):
        return self.source==node or self.destination==node

class Graph:
    def __init__(self, edges):
        self.data = {}
        for e in edges:
            self.add_edge(e)

    def add_edge(self, e):
        if not self.data.get(e.source):
            self.data[e.source] = []
        self.data[e.source].append(e)
        
    def get_conected(self, node):
        return [ x.destination for x in self.data[node] ]

    def get_all_edges(self):
        return self.data.values()

    def get_all_nodes(self):
        return [k for k,v in self.data.items()]

    # =========== ALGORITIMOS ===========================
    def dfs(start):
        # Adaptado apartir da questão 4
        seen = []
        paths = {}
        to_see = [ (start, [])  ] # (node, caminho)
        
        while len(to_see) > 0:
            node, path = to_see.pop() # operamos como uma pilha
            seen.append(node)
            paths[node] = [*path, node]

            self.get_conected(node)
            to_see.extend([
                (x, [*path, node]) for x in discovered
                if x not in seen and x not in [x[0] for x in to_see ]
            ])

        return seen, paths

    def bfs(start):
        # Adaptado apartir da questão 4
        seen = []
        to_see = [ (start, [])  ] # (node, caminho)
        paths = {}
        
        while len(to_see) > 0:
            node, path = to_see[0] # operamos como uma fila
            to_see = to_see[1:]
            seen.append(node)
            paths[node] = [*path, node]

            discovered = self.get_conected(node)
            to_see.extend([
                (x, [*path, node]) for x in discovered
                if x not in seen and x not in [x[0] for x in to_see ]
            ])
        return seen, paths

    def djikstra(self, start, end, weight_getter=lambda e: e.weight):
        nodes = self.get_all_nodes()
        
        # Validações
        if start not in nodes: return None, inf
        if end not in nodes: return None, inf

        # Variaveis de controle
        seen_nodes = {node: (inf, []) for node in nodes} # (cost, path)
        seen_nodes[start] = (0, [])
        not_seen = set(nodes)
        
        while len(not_seen) > 0:
            # inicializacao de variaveis
            current = min(not_seen, key=lambda n: seen_nodes[n][0])
            cur_cost, cur_path = seen_nodes[current]
            not_seen.remove(current)
          
            # Logica principal
            if current == end: break
            
            for edge in self.data[current]:
                # Se não tivermos analisado esse nó ainda, continua execução
                if edge.destination not in not_seen: continue 

                # Atualiza o custo se encontrarmos um menor
                cost = cur_cost + weight_getter(edge)
                if cost < seen_nodes[edge.destination][0]:
                    seen_nodes[edge.destination] = (cost, [*cur_path, current])
                        
        # Formata output
        cost, path = seen_nodes[end]
        path.append(end)     
        return path, cost