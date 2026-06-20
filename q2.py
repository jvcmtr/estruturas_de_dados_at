from BinaryHeap import BinaryHeap
from BaseTrie import BaseTrie
import time

BANCO_DE_PALAVRAS = [
    ("teclado", 45),
    ("tecnologia", 90),
    ("tecnico", 75),
    ("tecido", 30),
    ("computacao", 100),
    ("computador", 100),
    ("compilador", 85),
    ("complexo", 85),
    ("componente", 60),
    ("compartilhar", 95),
    ("comunidade", 70),
    ("comunismo", 10),
    ("corpo", 40),
    ("carro", 55)
]


class AutocompleteTrie(BaseTrie):
    
    # Remove a possibilidade de inserir palavras direto no construtor
    def __init__(self):
        self.palaras_prioridades = {}
        super().__init__()

    def inserir_termo(self, termo, peso):
        self.palaras_prioridades[termo] = peso
        self._insert(self.root,  termo)

    # Override das funções default para cumprir com os requisitos da questão
    def insert(self): raise ("Função insert não existe, Utilize 'inserir_termo()'")

    def sugerir_top_k(self, prefixo, k=5):
        words = self.list_tree(prefixo)

        words = sorted(words, reverse=True) # Para manter a ordenação lexicografica em caso de empate
        heap = BinaryHeap(
            data=words,
            is_min=False,
            get_priority_override=lambda w: self.palaras_prioridades[w]
        )

        return heap.get_next_k(k)

def timed(n, func):
    """
        Executa a função n vezes e retorna:
        retorno, duração maxima, duração minima, tempo total, tempo medio
    """
    times = []
    for i in range(n):
        start = time.time()
        result = func()
        times.append( time.time() - start)
    return result, max(times), min(times), sum(times), sum(times)/n, 

def test_search(trie, term, n):
    r, maior, menor, total, media = timed(500, lambda: t.sugerir_top_k(term, 5))
    print(f"____________________________")
    print(f"    Testando busca pelo termo '{term}'")
    print(f"Tempo (max/min) : {(maior*1000):.4f} ms / {(menor*1000):.4f} ms ")
    print(f"Tempo medio     : {(media*1000):.4f} ms")
    print(f"Tempo total     : {total:.2f} sec ({n} iteracoes)")
    print(f"Resultados      : { ', '.join(r)}")


if __name__ == "__main__":
    # Comentado pois a questão exige a inserção manual de palavra e peso 
    # t = AutocompleteTrie([x[0] for x in BANCO_DE_PALAVRAS]) 
    t = AutocompleteTrie()
    for pal, peso in BANCO_DE_PALAVRAS:
        t.inserir_termo(pal, peso)        

    print(f"____________________________")
    print(f"INICIANDO TESTES COM OS SEGUINTES DADOS")
    print("+ Banco de palavras : ")
    print(f"  peso\t|\tpalavra")
    for p, v in BANCO_DE_PALAVRAS:
        print(f"   {v} \t| \t{p}")

    print("+ Trie:")
    t.print_tree()
    
    termos = ("tec", "comp", "com" , "c")
    for s in termos:
        test_search(t, s, 5000)