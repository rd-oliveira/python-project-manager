import flet as ft


class ProjectViewer(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=0,
            expand=True,
        )

        # Title
        self.title = ft.Text(
            value="PROJECTS",
            color="#f0f0f0",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        # List containing the directories of each project
        self.project_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True,
        )

        row = ft.Row(
            controls=[self.title],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Containers
        container_title = ft.Container(
            content=row,
            bgcolor="#909090",
            padding=10,
        )

        container_project_list = ft.Container(
            content=self.project_list,
            bgcolor="#f0f0f0",
            expand=1,
        )

        self.controls.extend([container_title, container_project_list])
