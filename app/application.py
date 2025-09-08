import flet as ft


from services.project_creator import ProjectCreator
from services.project_viewer import ProjectViewer
from settings.configurations import Configuration
from settings.initializer import UIConfig


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup()

    def setup(self):
        self.configure_window()
        self.build_interface()

    def configure_window(self):
        # Application window settings
        self.page.title = "Project Management System"
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.maximizable = False
        self.page.window.resizable = False
        self.page.window.center()

        self.initializer = UIConfig(
            f"{self.page.title} (Projects)",
            f"{self.page.title} settings",
        )
        self.initializer.setup()

    def build_interface(self):
        header = self._build_header()
        body = self._build_body()

        layout = ft.Column(
            controls=[header, ft.Container(content=body, expand=True)], expand=True
        )

        self.navigate_to(layout)

    def _build_header(self):
        self.title = ft.Text(
            value="Project Manager".upper(),
            size=30,
            weight=ft.FontWeight.BOLD,
        )

        self.btn_configuration = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_size=45,
            tooltip="Configuration",
            on_click=self.settings,
        )

        container = ft.Container(
            content=ft.Row(
                controls=[self.title, self.btn_configuration],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
        )

        return container

    def _build_body(self):
        project_creator_interface = ProjectCreator()
        project_viewer_interface = ProjectViewer()

        return ft.Row(
            controls=[project_creator_interface, project_viewer_interface],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

    def settings(self, e):
        self.navigate_to(
            Configuration(
                self.page,
                on_return=lambda: self.navigate_to(self.get_main_interface()),
                config=self.initializer,
            )
        )

    def get_main_interface(self):
        """Returns to the main screen and rebuilds the interface"""
        header = self._build_header()
        body = self._build_body()

        return ft.Column(
            controls=[header, body],
            expand=True,
        )

    def navigate_to(self, component: ft.Control):
        self.page.clean()
        self.page.add(component)
        self.page.update()


def main():
    ft.app(target=App)
