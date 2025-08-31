import flet as ft


from services.project_creator import ProjectCreator
from services.project_viewer import ProjectViewer


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
        self.page.window.maximizable = False,
        self.page.window.resizable = False,
        self.page.window.center()

    def build_interface(self):
        header = self._build_header()
        body = self._build_body()
        column = ft.Column(
            controls=[body],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.page.add(header, column)

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


def main():
    ft.app(target=App)
