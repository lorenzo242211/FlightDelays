import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        for a in DAO.getAllAirports():
            self.idMap[a.ID] = a
        self.bestCammino = []
        self.bestScore = 0


    def getCamminoOttimoXPassi(self, a0, a1, tratte):
        self.bestCammino = []
        self.bestScore = 0

        parziale = [a0]
        self.ricorsione(parziale, a1, tratte)
        return self.bestCammino, self.bestScore


    def ricorsione(self, parziale, a1, tratte):
        #verifico se parziale è una soluzione valida, in caso, la salvo
        #1) condizioni di ottimalità
        if parziale[-1] == a1: #è potenzialmente una soluzione accettabile
            if self.getScore(parziale) > self.bestScore: #se calcolo punteggio attuale migliore di quello registrato allora
                self.bestCammino = list(parziale)
                self.bestScore = self.getScore(parziale)
        #verifica se ha senso aggiungere elementi al parizale o esco
        #2) condizione di terminazione
        if len(parziale) == tratte + 1: #nMax tratte raggiunto!
            return
        #3) espansione 'albero' + backtracking
        for a in self.grafo.neighbors(parziale[-1]):
            if a not in parziale:
                parziale.append(a)
                self.ricorsione(parziale, a1, tratte)
                parziale.pop()

#o
    def getScore(self, parziale):
        #somma pesi archi
        somma = 0
        for i in range(0, len(parziale) - 1):
            somma += self.grafo[parziale[i]][parziale[i+1]]["weight"] #grafo[nodo partenza][nodo arrivo][peso]
        return somma





    def creaGrafo(self, numCompagnie):
        self.grafo.clear()

        # 1. Aggiungo i nodi
        listaNodi = DAO.getNodi(numCompagnie)
        for id in listaNodi:
            self.grafo.add_node(self.idMap[id])

            # 2. Aggiungo gli archi (INDENTAZIONE CORRETTA: fuori dal ciclo dei nodi)
        for rotta in DAO.getArchiPesati():
            p = self.idMap[rotta[0]]
            a = self.idMap[rotta[1]]
            peso = rotta[2]

            if p in self.grafo and a in self.grafo:
                if self.grafo.has_edge(p, a):
                    self.grafo[p][a]["weight"] += peso
                else:
                    self.grafo.add_edge(p, a, weight=peso)

    def getNodi(self):
        return list(self.grafo.nodes())

    def getStatisticheGrafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def getConnessiNonConnessa(self, oggettoAeroportoSource): #restituisce tutti i vicini di source
        listaVicini = self.grafo.neighbors(oggettoAeroportoSource)
        listaTupleViciniPesata = []
        #oppure self.grafo.neighbors(source)
        for v in listaVicini:
            listaTupleViciniPesata.append((v,self.grafo[oggettoAeroportoSource][v]["weight"]))
        listaTupleViciniPesata.sort(key = lambda x: x[1], reverse = True)
        return listaTupleViciniPesata

    def testConnessione(self, oggettoAeroPartenza, oggettoAeroArrivo):
        try:
            percorso = nx.dijkstra_path(self.grafo, oggettoAeroPartenza, oggettoAeroArrivo, weight=None)
            return percorso
        except nx.NetworkXNoPath:
            # Se NetworkX non trova strade, restituiamo None (così il tuo Controller fa scattare l'alert!)
            return None