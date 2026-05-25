import datetime
from time import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_analizza(self, e):
        compagnieMin = self._view.txtNumCompagnMin.value

        if not compagnieMin.isdigit() or int(compagnieMin) < 0:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare un numero intero positivo!")
            self._view.update_page()
            return

        self._model.creaGrafo(compagnieMin)
        statistiche = self._model.getStatisticheGrafo()

        self._view.txt_result.controls.clear()

        if statistiche[0] == 0:
            self._view.create_alert("Impossibile creare grafo, numero selezionato di compagnie troppo elevato!")
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente: {statistiche[0]} nodi; {statistiche[1]} archi", color="green")
        )

        self._view.ddArrivo.disabled = False
        self._view.ddPartenza.disabled = False
        self._view.btn_connessi.disabled = False
        self._view.txtNumTratteMax.disabled = False
        self._view.btn_cerca.disabled = False


        # Pulisco le tendine prima di riempirle
        self._view.ddArrivo.options.clear()
        self._view.ddPartenza.options.clear()

        aeroporti = self._model.getNodi()
        if aeroporti:
            for a in aeroporti:
                # QUI PASSIAMO L'ID COME STRINGA
                self._view.ddArrivo.options.append(ft.dropdown.Option(key=str(a.ID), text=a.IATA_CODE))
                self._view.ddPartenza.options.append(ft.dropdown.Option(key=str(a.ID), text=a.IATA_CODE))
        else:
            self._view.create_alert("Errore nel riempimento dropdown list, ripetere operazione con valori diversi!")

        self._view.update_page()

    def handle_connessi(self, e):
        partenza_id_str = self._view.ddPartenza.value

        if not partenza_id_str:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare un aeroporto valido prima!")
            self._view.update_page()
            return

        # QUI USIAMO LA IDMAP PER RECUPERARE L'OGGETTO
        aeroporto_partenza = self._model.idMap[int(partenza_id_str)]

        lista = self._model.getConnessiNonConnessa(aeroporto_partenza)

        self._view.txt_result.controls.clear()

        if not lista:
            self._view.create_alert("L'aeroporto non ha vicini!")
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Vicini di {aeroporto_partenza.IATA_CODE} ({len(lista)} aeroporti):"
                                                      f"", color="cyan"))

        for tupla in lista:
            # tupla[0] è l'oggetto, tupla[1] è il peso. Li stampiamo belli puliti.
            self._view.txt_result.controls.append(ft.Text(f"{tupla[0].IATA_CODE} ({tupla[0].AIRPORT}) - voli (peso arco): {tupla[1]}"))

        self._view.update_page()

    def handle_cerca(self, e):
        partenza_id_str = self._view.ddPartenza.value
        arrivo_id_str = self._view.ddArrivo.value

        if not partenza_id_str:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare un aeroporto di partenza valido!")
            self._view.update_page()
            return

        if not arrivo_id_str:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Selezionare un aeroporto di arrivo valido!")
            self._view.update_page()
            return

        if arrivo_id_str == partenza_id_str:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Gli aeroporti non possono essere uguali!")
            self._view.update_page()
            return

        tratteMax = self._view.txtNumTratteMax.value
        if not tratteMax:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Inserire un numero tratte max per avviare test connessione e l'algoritmo ricorsivo!")
            self._view.update_page()
            return

        if not tratteMax.isdigit() or int(tratteMax) <= 0:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Inserire un numero tratte max intero maggiore di 0 per avviare test connessione e l'algoritmo ricorsivo!")
            self._view.update_page()
            return

        # QUI USIAMO LA IDMAP PER RECUPERARE L'OGGETTO
        aeroporto_partenza = self._model.idMap[int(partenza_id_str)]
        aeroporto_arrivo = self._model.idMap[int(arrivo_id_str)] #trasformo in int poiche il valore key salvato nel DD è str
        #per comodità anzichè aggiungere un nuovo metodo e pulsanti inutili uso il test connessione qua dentro, ci serve per la parte 2
        path = self._model.testConnessione(aeroporto_partenza, aeroporto_arrivo)
        if not path:
            self._view.txt_result.controls.clear()
            self._view.create_alert("Connessione non riuscita, provare un altra combinazione di aeroporti!")
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Connessione riuscita! Di seguito il percorso da"
                                                          f" {aeroporto_partenza.IATA_CODE} a {aeroporto_arrivo.IATA_CODE},"
                                                          f" (ignorando il peso):", color="cyan"))

        for a in path:
            self._view.txt_result.controls.append(ft.Text(a))

        self._view.txt_result.controls.append(ft.Text(f"\n\nProcedo a ricorsione cercando percorso di peso maggiore"
                                                      f"in max N = {tratteMax} tratte...\n", color="cyan"))
        #ricorsione, per ora non necessari controlli, il collegamento esiste!
        #si vuole massimizzare la somma del peso archi in max t tratte
        inizio = time()
        pathPeso, score = self._model.getCamminoOttimoXPassi(aeroporto_partenza, aeroporto_arrivo, int(tratteMax))
        fine = time()
        self._view.txt_result.controls.append(ft.Text(f"Ricorsione effettuata in {fine - inizio:.2f}s, con punteggio,"
                                                      f"di {score}, di seguito il percorso ottimo dei nodi contenuti: ", color="orange"))
        for a in pathPeso:
            self._view.txt_result.controls.append(ft.Text(a))
        self._view.update_page()
        return



