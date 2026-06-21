from q5_data import *
from q5_utils import *
from Graph import Graph, DirectedWeightedEdge
from BinaryHeap import BinaryHeap
from math import inf

def get_initial_hub(graph, n=3):
    # Encontra lista de hubs possiveis
    possible = [x[0] for x in NODES if x[1]==True]
    # Encontra as 3 entregas mais prioritarias
    entregas_prioritarias = sorted(DELIVERIES, key=get_priority)[n:]

    # Para cada hub calcula o custo para as 3 entregas mais prioritarias
    results = {p:inf for p in possible}
    for p in possible:
        custo_total = 0 
        for e in entregas_prioritarias:
            custo_total += graph.djikstra(p, e[0])[1]
        results[p] = custo_total 
    
    # Retorna o hub com menor custo total
    selected = sorted(results.items(), key=lambda kv: kv[1])[0][0]
    return selected, results[selected]/n, entregas_prioritarias

def questao_5_1(g):
    print("__________________________")
    print("    EXECUTANDO QUESTÃO 5.1")
    print(f"Grafo: {g}")
    print(f"Nós adjacentes de 'Madureira': {g.get_conected('Madureira')}")
    print(f"Nós adjacentes de 'Centro': {g.get_conected('Centro')}")
    
    n = 3
    hub, med, ent = get_initial_hub(g, n)
    print(f"---")
    print(f"Hub inicial selecionado: {hub}")
    print(f"Entregas mais prioritarias (t=0): {[ x[0] for x in ent]}")
    print(f"Custo medio para as {n} mais prioritarias: {med:.2f}")
    

def get_trajetos_relevantes(graph):
    "Retorna (Origem, Destino, Custo_total, passando_por)"
    relevantes = [n[0] for n in NODES if 
        (n[0] in DELIVERY_TARGETS) or (n[0] in HUBS)
    ]

    TRAJETOS_RELEVANTES = []
    for i in relevantes:
        for j in relevantes:
            if i != j:
                path, cost = graph.djikstra(i, j)
                TRAJETOS_RELEVANTES.append((i , j, cost, path))  
    return TRAJETOS_RELEVANTES

def questao_5_2(graph):
    print("__________________________")
    print("    EXECUTANDO QUESTÃO 5.2")

    # pontos relevantes são os bairros de entrega e os hubs
    relevantes = [n[0] for n in NODES if n[0] in DELIVERY_TARGETS or n in HUBS]
    TRAJETOS_RELEVANTES = get_trajetos_relevantes(graph)
    
    print(f"Pontos relevantes: {relevantes}")
    print(f"Trajetos:")
    for t in TRAJETOS_RELEVANTES:
        space1 = ' ' * (12-len(t[0]))
        space2 = ' ' * (12-len(t[1]))
        print(f"    {t[0]}{space1}=>  {t[1]}{space2}(passos:{len(t[3])})\t(custo:{t[2]})")

    def travel_cost(u, v):
        return graph.djikstra(u, v)[1]


class DeliveryProblem:
    # Idealmente as constantes precomputadas seriam argumentos passados no construtor
    # e seriam computadas aqui. Mas não vale a pena refatorar todo o codigo agora.
    def __init__(self):
        # Precomputações
        edges = [DirectedWeightedEdge(a, b, c) for a,b,c in TRAJETOS]
        self._graph = Graph( edges )        
        self.optimized_edges = get_trajetos_relevantes(self._graph)
        
        # Estado inicial
        self.deliveries = DELIVERIES
        self.initial_hub = get_initial_hub(self._graph)[0]

        # Variaveis alteradas durante a resolução do problema
        self.t = 0
        self.atrasos = 0
        self.curent = self.initial_hub
        self.trail = [self.initial_hub]
    
    def _get_edge_to(self, target):
        # Poderiamos fazer self._graph.djikstra(a, b), mas já temos os caminhos precomputados.
        for e in self.optimized_edges:
            if e[0] == self.curent and e[1] == target:
                return e
        raise Exception("CAMINHO INEXISTENTE NOS TRAJETOS PRECOMPUTADOS")

    def get_current_score(self, delivery):
        cost = self._get_edge_to(delivery[0])[2]
        priority = get_priority(delivery, self.t)  
        return priority - cost
    
    def solve(self):
        heap = BinaryHeap(
            self.deliveries, 
            is_min=False, 
            get_priority_override=self.get_current_score
        )
        while len(heap) > 1:
            # Evitamos de dar retirar o item da heap para só fazer isso uma vez que a entrega esteja concluida
            # Isso faz com que as comparações chamadas no heapify_down sejam feitas com o estado mais atual do problema
            delivery = heap.peek()
            self._go_to(delivery[0])
            self._deliver(delivery)
            heap.get_next()
        
        self.return_to_hub()
    
         
    def _deliver(self, delivery):
        if self.t < delivery[1]: # Chegada antecipada
            self.t = delivery[1]

        if self.t < delivery[2]: # Atraso
            self.atrasos += 1

    def _go_to(self, destino):
        _, destino, custo, path = self._get_edge_to(destino)
        self.curent = destino
        self.t += custo
        self.trail.extend(path[1:])

    def return_to_hub(self):
        fim = self.initial_hub
        custo = self._get_edge_to(fim)[2]
        for h in HUBS:
            if h != fim:
                e = self._get_edge_to(h)
                if e[2] < custo:
                    fim, custo = h, e[2]
        self._go_to(fim)
    


def questao_5_3(graph):
    print("__________________________")
    print("    EXECUTANDO SOLUÇÃO DA QUESTÃO 5")
    d = DeliveryProblem()
    d.solve()
    print(f"Horario de inicio: 9:00")
    print(f"Horario de fim: { 9+(d.t//60)}:{(d.t%60):02}")
    print(f"Entregas realizadas: {len(d.deliveries)}")
    print(f"Caminho percorrido: ")
    print("    ", " > ".join(d.trail))
    print("---")
    print(f"Tempo decorrido : {d.t} min")
    print(f"Entregas com atraso: {d.atrasos}")
    print(f"Parametros de score e prioridade: ")
    print(f"   - Espera     : {PESO_ESPERA}")
    print(f"   - Urgencia   : {PESO_URGENCIA}")
    print(f"   - Prioridade : {PESO_PRIORIDADE}")
    print(f"   - Fator      : {FATOR_PRIORIDADE_FINAL}")




if __name__ == "__main__":
    edges = [DirectedWeightedEdge(a, b, c) for a,b,c in TRAJETOS]
    g = Graph( edges )

    # questao_5_1(g)
    # questao_5_2(g)
    questao_5_3(g)