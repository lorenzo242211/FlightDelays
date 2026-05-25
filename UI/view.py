import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txtNumCompagnMin = None
        self.btn_analizza = None
        self.ddPartenza = None
        self.ddArrivo = None
        self.txtNumTratteMax = None
        self.btn_cerca = None
        self.btn_connessi = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # Title
        self._title = ft.Text("Flight Delays", color="cyan", size=24)
        self._page.controls.append(self._title)

        # Row 1: txtNumCompagn + bottone analizza aeroporti
        self.txtNumCompagnMin = ft.TextField(
            label="Numero minimo compagnie",
            width=610,
            hint_text="Inserisci numero minimo compagnie",
            color="cyan",
            border_color="cyan"
        )
        self.btn_analizza = ft.ElevatedButton(
            text="Analizza aeroporti",
            on_click=self._controller.handle_analizza,
            bgcolor="cyan",
            color="white"
        )
        row1 = ft.Row([self.txtNumCompagnMin, self.btn_analizza], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Row 2: dropdown aeroporto partenza + aeroporto destinazione + pulsante aeroporti connessi
        self.ddPartenza = ft.Dropdown(label="Aeroporto partenza", border_color = "cyan", color = "cyan", disabled=True)
        self.ddArrivo = ft.Dropdown(label="Aeroporto Arrivo" , border_color = "cyan", color="cyan", disabled=True)
        self.btn_connessi = ft.ElevatedButton(
            text="Connessa Partenza",
            on_click=self._controller.handle_connessi,  # Cambiato nome per non sovrapporlo!
            bgcolor="cyan",
            color="white", disabled=True
        )
        row2 = ft.Row([self.ddPartenza, self.ddArrivo, self.btn_connessi], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # Row 3: txt num tratte massimo + pulsante cerca itinerario
        self.txtNumTratteMax = ft.TextField(
            label="Numero tratte massimo",
            width=610,
            hint_text="Inserisci numero tratte massimo",
            color="cyan",
            border_color="cyan", disabled=True
        )
        self.btn_cerca = ft.ElevatedButton(
            text="Cerca itinerario (ricorsione)",
            on_click=self._controller.handle_cerca,  # Cambiato nome per non sovrapporlo!
            bgcolor="cyan",
            color="white", disabled=True
        )
        # Qui c'era l'errore: stavi appendendo row2 di nuovo invece di row3!
        row3 = ft.Row([self.txtNumTratteMax, self.btn_cerca], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed (Console dei risultati)
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
