import flet as ft


from controllers.env_project_manager import EnvProjectManager
from services.project_viewer import ProjectViewer
from services.ui_state_manager import UIStateManager


class ProjectCreator(ft.Column):
    def __init__(
        self,
        project_path: str,
        project_viewer: ProjectViewer,
        ui_manager: UIStateManager,
    ):
        super().__init__(expand=True)
        self.project_path = project_path
        self.project_viewer = project_viewer
        self.ui_manager = ui_manager

        self.saved_libraries = []
        self.saved_libraries_set = set()

        # TextFields
        self.txt_project_name = ft.TextField(
            label="Project Name",
            on_change=self.check_project_name,
            on_submit=self.create_project,
        )
        self.txt_library_name = ft.TextField(
            label="Library Name", expand=True, on_submit=self.add_library
        )

        # Buttons
        self.btn_add_library = ft.IconButton(
            icon=ft.Icons.ADD, on_click=self.add_library, tooltip="Add library"
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

        # Library list
        self.library_list = ft.ListView(
            spacing=10, padding=20, auto_scroll=True, expand=1
        )

        # Log
        self.information_log = ft.Text(value="", color="#36da6a")

        # Layout
        row_library = ft.Row(controls=[self.txt_library_name, self.btn_add_library])
        row_information_log = ft.Row(
            controls=[self.information_log],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        row_btn_create_project = ft.Row(controls=[self.btn_create_project])
        container_library_list = ft.Container(
            content=self.library_list, bgcolor="#f0f0f0", expand=1
        )
        container_information_log = ft.Container(
            content=row_information_log, bgcolor="#303030"
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

        # Register controls with UI manager
        self.ui_manager.register_controls(
            [
                self.txt_project_name,
                self.txt_library_name,
                self.btn_add_library,
                self.btn_create_project,
                self.library_list,
            ]
        )

    def check_project_name(self, e):
        self.btn_create_project.disabled = not bool(self.txt_project_name.value)
        self.update()

    def create_project(self, e):
        project = EnvProjectManager(
            self.txt_project_name.value.strip(), self.project_path, self.saved_libraries
        )
        try:
            self.ui_manager.disable_all()
            self.show_information_log("Creating project...", "yellow")
            project.setup_project()
            self.show_information_log("Project created successfully!", "green")

            # Refresh project viewer
            self.project_viewer.refresh()

        except Exception as error:
            self.show_information_log(f"Error: {error}", "red")
        finally:
            self.ui_manager.enable_all()
            self.txt_update_field(self.txt_project_name)
            self.txt_update_field(self.txt_library_name)

    def add_library(self, e):
        library_name = self.txt_library_name.value.strip()
        if not library_name:
            return

        if library_name in self.saved_libraries_set:
            self.show_information_log(
                f"Library '{library_name}' already added!", "yellow"
            )
            self.txt_update_field(self.txt_library_name)
            return

        # UI line
        line = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        library_text = ft.Text(value=library_name)
        btn_delete_library = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_size=15,
            on_click=lambda e, row=line: self.delete_library(row),
        )
        line.controls.extend([library_text, btn_delete_library])

        self.library_list.controls.append(line)
        self.saved_libraries.append(library_name)
        self.saved_libraries_set.add(library_name)

        self.show_information_log(f"Added library '{library_name}'", "green")
        self.txt_update_field(self.txt_library_name)
        self.update()

    def delete_library(self, row):
        library_name = row.controls[0].value
        self.library_list.controls.remove(row)
        self.saved_libraries.remove(library_name)
        self.saved_libraries_set.remove(library_name)
        self.show_information_log(f"Removed library '{library_name}'", "yellow")
        self.update()

    def txt_update_field(self, field):
        field.value = ""
        field.update()

    def show_information_log(self, message: str, color: str = "green"):
        self.information_log.value = message
        self.information_log.color = color
        self.information_log.update()
