import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        #definizione grafo
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

    def buildGraph(self):
        #aggiungere i nodi (prendiamo dal DAO)
        self._graph.add_nodes_from(self._nodes)

        #aggiungere gli archi (prendiamo dal DAO)
        self.addEdgesV2()

    #PESATI MA DOPPIO CICLO FOR NON VA BENE TROPPO LENTO, FACIO VERSIONE 2
    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u,v, weight = peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)


    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len (self._graph.edges)

    #ora dobbiamo lavorare sul grafo per la componente connessa a cui passiamo un id oggetto che chiediamo nell'interf grafica
    #cercare la componente connessa che contiene id oggetto
    #si puo utilizzare DEPTH FIRST SEARCH per profondità
    #ci sono tre modi per farlo
    #1. fare un dfs tree e contare il numero di nodi dell'albero
        #faccio una ricerca in profondita, mi prendo l'albero e tutti i nodi e li conto
    #2. usare un metodo che esplora albero di visita che restituisce successori e predecessori
        #prendere predecessori di algoritmo dfs
        #restituisce dizionario con chiave = il nodo e valore = il nodo da cui sono arrivata secondo la ricerca depth
        #quindi conto i valori del dizionario cioè tutti i predecessori = nodi presenti nella comp connessa
        #avrò un valore decrementato di uno per il nodo source
    #3. usiamo metodi della galleria
        #prende come argomento un grafo e il source
        #conto la lunghezza
    def getInfoCompConnessa(self, id_oggetto):

        #uso has node per vedere se id oggetto è contenuto nel grafo e se ha senso cercare la comp conn con quell'id
        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        #STRATEGIA 1.
        dfsTree = nx.dfs_tree(self._graph, source)
        print("size connessa con dfs_tree", len(dfsTree.nodes()))

        #STRATEGIA 2.
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print("size connessa con dfs_precesseros", len(dfsPred.values()))

        #STRATEGIA 3.
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_component", len(conn))

        return len(conn)



    #metodo per verificare che l'id oggetto che passo è contenuto nel grafo (se è contenuto nell'idmap lo è anche nel grafo)
    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO
