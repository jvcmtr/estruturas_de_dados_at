class TrieNode:
    def __init__(self, is_end=False):
        self.children = {}
        self.is_end = is_end

class BaseTrie:
    def __init__(self, words=[]):
        self.root = TrieNode()
        self._max_height = 0 # Valor maximo (não exato), desconsidera remoções.
        for w in words:
            self.insert(w)

    def insert(self, word):
        self._insert(self.root, word.lower())
        if self._max_height < len(word):
            self._max_height = len(word)

    def search(self, word):
        return self._search(self.root, word.lower())

    def list_tree(self, prefix=""):
        """
            Lista todas as palavras na Trie.
            Se um prefixo for fornescido, lista todas as palaras com aquele prefixo
        """
        if not prefix:
            return self._list(self.root, "")

        n = self._as_nodes(prefix.lower())
        if not n :
            return []
        return self._list(n[-1], prefix)

    # ==================== PRIVATE IMPLEMENTATIONS =======================


    def _list(self, node=None, prefix=""):
        """
            Procura todos os itens na subarvore começando a partir de 'node' usando DFS. 
            Retorna uma lista de palavras. Caso um prefixo seja fornescido, adiciona o prefixo a todas as palavras.
        """
        arr = []
        if node.is_end:
            arr.append(prefix)

        for key, val in node.children.items():
            rec = self._list( val, prefix+key)
            arr.extend( rec )

        return arr

    def _insert(self, node, word):
        if len(word) < 1:
            node.is_end = True
            return
        
        if not node.children.get(word[0]):
            node.children[word[0]] = TrieNode()
        
        self._insert( node.children[word[0]], word[1:])

    def _search(self, node, word):
        "Retorna se a palavra existe ou não na trie"
        if node.is_end and not word:
            return True
        
        if not word:
            return False

        if not node.children.get(word[0]):
            return False

        return self._search(node.children[word[0]], word[1:])
        
    def _as_nodes(self, word, node=None):
        """
            Retorna um array de nodes onde cada um representa um caracter da palavra fornescida. 
            Caso a palavra não seja encontrada, retorna None
        """
        node = self.root if not node else node
        if not word:
            return []

        if not node.children.get(word[0]):
            return None
        
        following = self._as_nodes(word[1:], node.children[word[0]])  
        return [ node.children[word[0]], *following ] if following is not None else None

    def print_tree(self, start=None, char="", prefix="", depth=0, last_son={0:True}, seen=[], show_word=True):
        # Metodo adaptado da classe Graph da questão 1 do TP5 de Projeto de Bloco
        # Disponivel em: https://github.com/jvcmtr/Ciencia_Comp_PB_TP5
        
        seen.append(start)
        if start == None:
            start = self.root

        child = [ (v,k) for k, v in start.children.items() if v not in seen]

        spacer = ""
        for i in range(depth):
            spacer += "    " if last_son.get(i) else "│   "

        head = "└" if last_son.get(depth) else "├" #─ 
        expand = "─" # if len(child) == 0 else "┬"
        
        if start.is_end:
            if show_word:
                tab_char = ". "
                tab =  tab_char * ((self._max_height-depth)*(4-len(tab_char))+2)
                print(f"{spacer}{head}{expand}⏵ {char.upper()} {tab}({(prefix+char).capitalize()})")
            else:
                print(f"{spacer}{head}{expand}⏵ {char.upper()}*")
        else:
            print(f"{spacer}{head}{expand}⏵ {char.upper()}")

        for e in child:
            last_son[depth+1] = (e == child[-1])
            self.print_tree(e[0], e[1], prefix+char, depth+1, last_son, seen)
