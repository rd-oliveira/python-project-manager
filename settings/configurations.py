import flet as ft


class Configuration(ft.Column):
    def __init__(self, page: ft.Page, on_return, config):
        super().__init__(expand=True)

        self.on_return_callback = on_return
        self.config = config
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

        self.page = page
        self.path = None

        file_dialog = ft.FilePicker(on_result=self.search_directory)
        self.page.overlay.append(file_dialog)

        # Title
        title = ft.Text(
            value="Settings Page",
            size=40,
            weight=ft.FontWeight.BOLD,
        )

        # Entries
        self.txt_path_project = ft.TextField(
            value=self.config,
            label="project path",
            disabled=True,
        )

        # Buttons
        btn_folder = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_size=30,
            on_click=lambda _: file_dialog.get_directory_path(
                dialog_title="Choose a folder"
            ),
        )
        btn_return = ft.ElevatedButton(
            text="← Back",
            height=64,
            width=150,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(
                    size=20,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            on_click=self.on_return,
        )

        row = ft.Row(
            controls=[self.txt_path_project, btn_folder],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        column = ft.Column(
            controls=[title, row, btn_return],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )

        self.controls.extend([column])

    def search_directory(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.path = e.path
            self.txt_path_project.value = self.path
            self.txt_path_project.update()

    def on_return(self, e):
        if self.on_return_callback:
            self.on_return_callback()
