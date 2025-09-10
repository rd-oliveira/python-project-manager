import flet as ft


from services.ui_state_manager import UIStateManager
from services.project_creator import ProjectCreator
from services.project_viewer import ProjectViewer
from settings.configurations import Configuration
from settings.initializer import UIConfig
from pathlib import Path


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.ui_manager = UIStateManager()

        self.ui_config = UIConfig(
            project_folder_name="Python Project Manager (Projects)",
            project_folder_config="Python Project Manager (Settings)",
        )
        self.ui_config.setup()

        json_data = self.ui_config.load_json()
        self.project_path = json_data.get("project_path") if json_data else "projects"

        self.settings = Configuration(
            self.page, self.ui_config, on_path_updated=self.update_project_path
        )

        self.setup()

    def setup(self):
        self.page.title = "Project Management System"
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.maximizable = False
        self.page.window.resizable = False
        self.page.window.center()

        self.navigate_to(self._build_main_layout())

    def _build_header(self):
        self.title = ft.Text(
            value="PROJECT MANAGER", size=30, weight=ft.FontWeight.BOLD
        )

        container_dialog = ft.Container(content=self.settings, width=500, height=300)

        self.dialog = ft.AlertDialog(content=container_dialog, adaptive=True)

        self.btn_configuration = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_size=45,
            tooltip="Configuration",
            on_click=lambda e: self.page.open(self.dialog),
        )

        self.ui_manager.register_controls([self.btn_configuration])

        return ft.Container(
            content=ft.Row(
                controls=[self.title, self.btn_configuration],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
        )

    def _build_body(self):
        self.project_viewer_interface = ProjectViewer(self.project_path)
        self.project_creator_interface = ProjectCreator(
            self.project_path, self.project_viewer_interface, self.ui_manager
        )

        self.body_row = ft.Row(
            controls=[self.project_creator_interface, self.project_viewer_interface],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

        return self.body_row

    def _build_main_layout(self):
        return ft.Column(
            controls=[self._build_header(), self._build_body()], expand=True
        )

    def navigate_to(self, layout: ft.Control):
        self.page.clean()
        self.page.add(layout)
        self.page.update()

    def update_project_path(self, new_path: str):
        self.project_path = new_path
        self.project_viewer_interface.project_path = Path(new_path)
        self.project_viewer_interface.refresh()
        self.body_row.update()


def main():
    ft.app(target=App)
