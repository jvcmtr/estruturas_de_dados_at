# from AgendadorOtimizado import BinaryHeap
import random
import time

class Tarefa:
    def __init__(self, id_tarefa, tempo, tecnologia):
        self.id_tarefa = id_tarefa
        self.tempo = tempo
        self.tecnologia = tecnologia

# Aqui não foi utilizado a mesma classe disponível em BinaryHeap.py por
#  questões de otimização e funcionalidade (prioridade composta + lazy evaluation)
class AgendadorOtimizado:
    def __init__(self):
        self.heap = []
    
    def adicionar_tarefa(self, id_tarefa, tempo, tecnologia):
        tarefa = Tarefa(id_tarefa, tempo, tecnologia)
        self.heap.append((tempo, tarefa))
        self._heapify_up(len(self.heap) - 1)

    def executar_proxima(self, tecnologia_atual, penalidade):
        if not self.heap:
            return None

        while self.heap:
            
            # Troca o primeiro item com o ultimo do vetor antes de remove-lo. 
            # Isso é nescessario pois ao retirar o primeiro (usando pop) precisamos deslocar
            # Todos os demais itens ( O(n) ). Esta foi a otimização que fez a classe rodar em 
            # menos de 0.5 sec para 50.000 itens com penalidade=5
            last_idx = len(self.heap)-1
            self.heap[0], self.heap[last_idx] = self.heap[last_idx], self.heap[0]
            p, tarefa = self.heap.pop()
            
            if self.heap:
                self._heapify_down(0)

            p_real = tarefa.tempo if tarefa.tecnologia == tecnologia_atual else tarefa.tempo + penalidade

            # Lazy evaluation: Aqui comparamos o valor esperado com o mais recente.
            if p_real > p and self.heap:
                self.heap.append((p_real, tarefa))
                self._heapify_up(len(self.heap) - 1)
                continue
            
            return tarefa

        return None

    # ===================== FUNÇÕES PRIVADAS ===========================

    # As funções a seguir foram comentadas para evitar o overhead de chamada de funções.
    # def _get_left(self, idx):
    #     return 2*idx+1

    # def _get_right(self, idx):
    #     return 2*idx+2

    # def _get_parent(self, idx):
    #     return (idx-1)//2

    # def _troca(idx_a, idx_b):
    #     self.heap[idx_a], self.heap[idx_b] = self.heap[idx_b], self.heap[idx_a]

    def _heapify_up(self, idx):
        if idx <= 0:
            return
        pai = (idx-1)//2
        if self.heap[idx][0] < self.heap[pai][0]:
            self.heap[idx], self.heap[pai] = self.heap[pai], self.heap[idx]
            self._heapify_up(pai)

    def _heapify_down(self, idx):
        n = len(self.heap)
        while True:
            menor = idx
            l, r = 2*idx+1, 2*idx+2
            
            if l < n and self.heap[l][0] < self.heap[menor][0]:
                menor = l
            if r < n and self.heap[r][0] < self.heap[menor][0]:
                menor = r
            
            if menor != idx:
                self.heap[idx], self.heap[menor] = self.heap[menor], self.heap[idx]
                idx = menor
            else:
                break


def test_performance(name, n, tecnologias, penalidades):
    print("______________________________")
    print(f"    TESTE - {name}")

    print(f"- Numero de elementos: {n}")
    if len(penalidades) >1:
        print(f"- Possiveis penalidades: {penalidades[0]}, {penalidades[1]}, ... , {penalidades[-1]}")
    else:
        print(f"- Penalidade constante: {penalidades[0]}")
    print(f"- Numero de penalidades: {len(penalidades)}")
    print(f"- Numero de tecnologias distintas: {len(tecnologias)}")
    
    # Precalcula variaveis para não afetar o tempo
    pens = [random.choice(penalidades) for x in range(n)]
    tecs = [random.choice(tecnologias) for x in range(n)]
    priorities = [random.randint(2, 20) for x in range(n)]

    h = AgendadorOtimizado()
    curr = tecnologias[0]

    start = time.time()
    for i in range(n):
        h.adicionar_tarefa(i, priorities[i], tecs[i])
    delta_insert = time.time() - start

    start = time.time()
    for i in range(n):
        curr = h.executar_proxima(curr, pens[i] ).tecnologia
    delta_exec = time.time() - start

    print(f"Tempo para a INSERÇÃO de {n} elementos: \t {delta_insert:.2f} sec")
    print(f"Tempo para a REMOÇÃO de {n} elementos: \t {delta_exec:.2f} sec")
    print(f"Tempo TOTAL de operação para {n} elementos: \t {(delta_exec + delta_insert):.2f} sec")


if __name__ == "__main__":
    h = AgendadorOtimizado()
    tecs = ["Python", "Docker", "C++", "Java"]
    pen = [5]
    pen_l = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    tecs_l = [ f"{i}" for i in range(100)]

    test_performance("20.000 Elementos", 20000, tecs, pen)
    test_performance("30.000 Elementos", 30000, tecs, pen)
    test_performance("40.000 Elementos", 40000, tecs, pen)
    test_performance("50.000 Elementos", 50000, tecs, pen)

    test_performance("50.000 Elementos (tecnologias distintas)", 50000, tecs_l, pen)
    test_performance("50.000 Elementos (penalidades distintas 5)", 50000, tecs, pen_l[:5])

    # Nos casos a baixo a classe não conseguiu processar 50000 items a baixo de 0.5s
    test_performance("50.000 Elementos (penalidades distintas 10)", 50000, tecs, pen_l)
    test_performance("50.000 Elementos (tecnologias e penalidades distintas 10)", 50000, tecs_l, pen_l)
