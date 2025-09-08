# app.py
import flet as ft


from services.project_creator import ProjectCreator
from services.project_viewer import ProjectViewer
from settings.configurations import Configuration
from settings.initializer import UIConfig


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.initializer: UIConfig | None = None
        self.setup()

    def setup(self):
        self._configure_window()
        self._configure_initializer()
        self.navigate_to(self._build_main_layout())

    def _configure_window(self):
        """Configures the main window"""
        self.page.title = "Project Management System"
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.maximizable = False
        self.page.window.resizable = False
        self.page.window.center()

    def _configure_initializer(self):
        """Initializes system settings"""
        self.initializer = UIConfig(
            f"{self.page.title} (Projects)",
            f"{self.page.title} settings",
        )
        self.initializer.setup()

    def _build_header(self):
        """Builds the header"""
        title = ft.Text(
            value="PROJECT MANAGER",
            size=30,
            weight=ft.FontWeight.BOLD,
        )

        btn_configuration = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            icon_size=45,
            tooltip="Configurações",
            on_click=self.settings,
        )

        return ft.Container(
            content=ft.Row(
                controls=[title, btn_configuration],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
        )

    def _build_body(self):
        """Builds the main body"""
        project_creator_interface = ProjectCreator()

        config = self.initializer.load_json()
        project_path = config.get("project_path", "")

        project_viewer_interface = ProjectViewer(project_path)

        return ft.Row(
            controls=[project_creator_interface, project_viewer_interface],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

    def _build_main_layout(self):
        """Returns the main layout (header + body)"""
        return ft.Column(
            controls=[
                self._build_header(),
                ft.Container(content=self._build_body(), expand=True),
            ],
            expand=True,
        )

    def settings(self, e):
        """Navigates to the Settings screen"""
        self.navigate_to(
            Configuration(
                self.page,
                on_return=lambda: self.navigate_to(self._build_main_layout()),
                config=self.initializer,
            )
        )

    def navigate_to(self, component: ft.Control):
        """Clears the screen and displays the specified component"""
        self.page.clean()
        self.page.add(component)
        self.page.update()


def main():
    ft.app(target=lambda page: App(page))
