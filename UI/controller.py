import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi"))


        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        #ATTIVO I BOTTONI SOLO DOPO AVER CLICCATO IL BOTTONE ANALIZZA OGGETTI
        self._view.update_page()


    #determinare la componente connessa del grafo e stampare la componente connessa del grafo che contiene il
    #vertice selezionato precedentemente e stampare il numero di vertici che la compongono
    def handleCompConnessa(self,e):

        #recupero l'input dell'utente
        txtIdOggetto = self._view._txtIdOggetto.value

        #faccio le provo, se è vuoto rimprovero
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text( f'Attenzione inserire un valore nel campo id_oggetto',color = "red"))
            self._view.update_page()
            return

        #se non è un numero riprovero
        try:
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f'Attenzione inserire un valore numerico nel campo id_oggetto', color="red"))
            self._view.update_page()
            return

        #se è un numero ma che non corrisponde all'oggetto (avevo fatto il metodo nel model per verificare)
        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f'Attenzione id_oggetto inserito non è presente nel grafo', color="red"))
            self._view.update_page()
            return

        sizeCompConnessa = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contente oggetto con l'id oggetto {idOggetto} è composta di {sizeCompConnessa} nodi. ", color="green"))
        self._view.update_page()







