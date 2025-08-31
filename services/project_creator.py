import flet as ft


class ProjectCreator(ft.Column):
    def __init__(self):
        super().__init__(expand=True)

        # Textfields
        self.txt_project_name = ft.TextField(
            label="Project Name", on_change=self.check_project_name
        )
        self.txt_library_name = ft.TextField(label="Library Name", expand=True)

        # Buttons
        self.btn_add_library = ft.IconButton(
            icon=ft.Icons.ADD,
            on_click=self.add_library,
            tooltip="Add library",
        )

        self.btn_create_project = ft.ElevatedButton(
            text="Create Project",
            height=64,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            ),
            on_click=self.create_project,
            disabled=True,
            expand=True,
        )

        # List of added libraries
        self.library_list = ft.ListView(
            spacing=10,
            padding=20,
            auto_scroll=True,
            expand=1,
        )

        # Information log
        self.information_log = ft.Text(value="", color="#36da6a")

        # Rows
        row_library = ft.Row(controls=[self.txt_library_name, self.btn_add_library])

        row_information_log = ft.Row(
            controls=[self.information_log],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        row_btn_create_project = ft.Row(controls=[self.btn_create_project])

        # Containers
        container_library_list = ft.Container(
            content=self.library_list,
            bgcolor="#f0f0f0",
            expand=1,
        )

        container_information_log = ft.Container(
            content=row_information_log,
            bgcolor="#303030",
        )

        self.controls.extend(
            [
                self.txt_project_name,
                row_library,
                container_library_list,
                row_btn_create_project,
                container_information_log,
            ]
        )

    def check_project_name(self, e):
        self.btn_create_project.disabled = not bool(self.txt_project_name.value)
        self.btn_create_project.update()

    def create_project(self, e):
        pass

    def add_library(self, e):
        library = self.txt_library_name.value.strip()

        # Extrai nomes das bibliotecas já adicionadas
        library_names = [
            row.controls[0].value
            for row in self.library_list.controls
            if isinstance(row, ft.Row) and isinstance(row.controls[0], ft.Text)
        ]

        if not library:
            return

        if library in library_names:
            self.show_information_log("-- library already added --")
        else:
            # Cria Text do nome da biblioteca
            txt = ft.Text(value=library)

            # Define função de remoção vinculada a este item
            def remove_library(ev):
                self.library_list.controls.remove(row)
                self.library_list.update()
                self.show_information_log(f"-- Removed library '{library}' --")

            # Cria Row com botão de deletar
            row = ft.Row(
                controls=[
                    txt,
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_size=15,
                        tooltip="Remove library",
                        on_click=remove_library,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

            self.library_list.controls.append(row)
            self.library_list.update()
            self.show_information_log(f"-- Add library '{library}' --")

        self.txt_library_name.value = ""
        self.txt_library_name.update()

    def show_information_log(self, message: str):
        """Shows information about what is happening in the interactivity and creation of the project.

        Args:
            message (str): message that will be displayed in the information field.
        """
        self.information_log.value = message
        self.information_log.update()
        print(message)
