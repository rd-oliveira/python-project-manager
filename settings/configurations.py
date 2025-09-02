import flet as ft


class Configuration(ft.Column):
    def __init__(self, on_return):
        super().__init__(expand=True)

        self.on_return_callback = on_return
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

        # Title
        title = ft.Text(
            value="⚙️ Settings Page",
            size=40,
            weight=ft.FontWeight.BOLD,
        )

        # Entries
        txt_path = ft.TextField(label="project path")

        # Buttons
        btn_folder = ft.IconButton(
            icon=ft.Icons.FOLDER, icon_size=30, on_click=self.search_directory
        )
        btn_return = ft.ElevatedButton(text="← Back", on_click=self.on_return)

        row = ft.Row(
            controls=[txt_path, btn_folder],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        column = ft.Column(
            controls=[title, row, btn_return],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )

        self.controls.extend([column])

    def search_directory(self, e):
        pass

    def on_return(self, e):
        if self.on_return_callback:
            self.on_return_callback()
