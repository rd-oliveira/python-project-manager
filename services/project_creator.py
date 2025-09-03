import flet as ft

from controllers.env_project_manager import EnvProjectManager


class ProjectCreator(ft.Column):
    def __init__(self):
        super().__init__(expand=True)

        self.saved_libraries = []

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

        self.interactive_controls = [
            self.txt_project_name,
            self.txt_library_name,
            self.btn_add_library,
            self.btn_create_project,
            self.library_list,
        ]

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
        project = EnvProjectManager(
            self.txt_project_name.value,
            "C:/new folder",
            self.saved_libraries,
        )

        try:
            self.disable_ui()
            self.show_information_log("-- Please wait, project is being created --")
            project.setup_project()
            self.show_information_log(" -- project created successfully --")
            self.enable_ui()
        except Exception as erro:
            self.show_information_log(f"{erro}")

        finally:
            self.txt_update_field(self.txt_project_name)
            self.txt_update_field(self.txt_library_name)

    def add_library(self, e):
        nome = self.txt_library_name.value.strip()

        # Check if the name is empty
        if not nome:
            return

        library = ft.Text(value=nome)
        line = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        btn_delete_library = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_size=15,
            on_click=lambda e, row=line: self.delete_library(row),
        )

        line.controls.extend([library, btn_delete_library])

        # Checks if the name already exists in the list
        for item in self.library_list.controls:
            for sub_item in item.controls:
                if isinstance(sub_item, ft.Text) and sub_item.value.strip() == nome:
                    self.txt_update_field(self.txt_library_name)
                    self.show_information_log("-- library already added --")
                    return

        self.library_list.controls.append(line)
        self.saved_libraries.append(nome)

        self.txt_update_field(self.txt_library_name)
        self.show_information_log(f"-- Add library '{library.value}' --")

        self.library_list.update()

    def delete_library(self, row):
        item_removed = row.controls[0].value

        self.library_list.controls.remove(row)
        self.saved_libraries.remove(item_removed)

        self.show_information_log(f"-- Removed library '{item_removed}' --")

        self.library_list.update()

    def txt_update_field(self, field):
        field.value = ""
        field.update()

    def list_update(self):
        self.library_list.clean()
        self.library_list.update()

    def show_information_log(self, message: str):
        """Shows information about what is happening in the interactivity and creation of the project.

        Args:
            message (str): message that will be displayed in the information field.
        """
        self.information_log.value = message
        self.information_log.update()

    def disable_ui(self):
        for item in self.interactive_controls:
            item.disabled = True
            item.update()

    def enable_ui(self):
        for item in self.interactive_controls:
            if item != self.btn_create_project:
                item.disabled = False
                item.update()

        self.list_update()
