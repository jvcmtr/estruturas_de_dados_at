

class BinaryHeap:
    def __init__(self, data = [], is_min=True, get_priority_override=None):
        """
            data                    -> dados para inserir valores na heap direto no construtor.
            is_min                  -> Permite que a classe seja usada tanto como heap minima quanto heap maxima
            get_priority_override   -> Permite que a heap guarde qualquer tipo de valor. (tuplas, dicionarios, outras classes, etc...)
        """
        self.arr = []
        self.is_min = is_min
        
        self._get_priority = get_priority_override
        if not get_priority_override:
            self._get_priority = lambda e: e
        
        self.insert_bulk(data)


    # ================ FUNCIONALIDADES PUBLICAS ================ 
    def insert(self, val):
        self.arr.append(val)
        self._heapify_up(self._get_last_idx())

    def get_next(self):
        if not self.arr:
            return None

        self._troca(0, self._get_last_idx())
        val = self.arr.pop()
        self._heapify_down(0)
        return val

    def get_next_k(self, k):
        "Metodo utilitario que estrai os k elementos mais prioritarios"
        if k < 1: return []
        result = []
        for _ in range(k):
            r = self.get_next()
            if r: result.append(r)
        return result

    def insert_bulk(self, arr):
        "Metodo utilitario que insere um conjunto de elementos"
        for i in arr:
            self.insert(i)

    # ================ OVERRIDES ================ 
    def __len__(self):
        return len(self.arr)

    def __str__(self):
        return f"{self.arr}"
    
    def _get_last_idx(self):
        return len(self.arr)-1

    # ================ UTILITARIAS PRIVADAS ================ 
    # Para que a Heap possa funcionar tanto como maxima quanto como minima
    # abstraimos o conceito de prioridade
    def _has_priority_over(self, a, b):
        if self.is_min:
            return self._get_priority( self.arr[a] ) < self._get_priority( self.arr[b] )
        return self._get_priority( self.arr[a] ) > self._get_priority( self.arr[b] )
    
    def _get_left(self, idx):
        return 2*idx+1

    def _get_right(self, idx):
        return 2*idx+2

    def _get_parent(self, idx):
        return (idx-1)//2
        pass

    # ================ IMPLEMENTAÇÃO PRIVADA ================ 
    def _troca(self, a, b):
        self.arr[a], self.arr[b] = self.arr[b], self.arr[a]

    def _heapify_up(self, start):
        pai_idx = self._get_parent(start)
        if pai_idx >= 0:
            if not self._has_priority_over(pai_idx, start):
                self._troca(pai_idx, start)
                self._heapify_up(pai_idx)

    def _heapify_down(self, start):
        last_idx = self._get_last_idx()
        if start > last_idx:
            return

        menor = start        
        l = self._get_left(start)
        r = self._get_right(start)

        if l <= last_idx and self._has_priority_over(l, menor):
            menor = l
        if r <= last_idx and self._has_priority_over(r, menor):
            menor = r

        if menor != start:
            self._troca(start, menor)
            self._heapify_down(menor)
