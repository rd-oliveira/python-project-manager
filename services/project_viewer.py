import os
import platform
import subprocess
import flet as ft


from pathlib import Path


class ProjectViewer(ft.Column):
    def __init__(self, project_path: str):
        super().__init__(spacing=0, expand=True)
        self.project_path = Path(project_path) if project_path else None

        # Title
        self.title = ft.Text(
            value="PROJECTS",
            color="#f0f0f0",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        # Project list
        self.project_list = ft.ListView(
            expand=1, spacing=10, padding=20, auto_scroll=True
        )

        # Build containers
        self.controls.extend([self._build_title(), self._build_project_list()])

        # Load projects
        self.refresh()

    def _build_title(self):
        return ft.Container(
            content=ft.Row(
                controls=[self.title],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#909090",
            padding=10,
        )

    def _build_project_list(self):
        return ft.Container(
            content=self.project_list,
            bgcolor="#f0f0f0",
            expand=1,
        )

    def refresh(self):
        """Reload the project list."""
        self.project_list.controls.clear()
        if not self.project_path or not self.project_path.exists():
            self.project_list.controls.append(ft.Text("No projects found", color="red"))
        else:
            for project in self.project_path.iterdir():
                if project.is_dir():
                    self.project_list.controls.append(
                        ft.ListTile(
                            title=ft.Text(project.name),
                            leading=ft.Icon(ft.Icons.FOLDER),
                            on_click=lambda e, p=project: self._on_project_click(p),
                        )
                    )
        if self.project_list.page:
            self.project_list.update()

    def _on_project_click(self, project: Path):
        project_path = project

        if not os.path.exists(project_path):
            raise FileNotFoundError(f"project_path not found: {project_path}")

        operational_system = platform.system()

        if operational_system == "Windows":
            os.startfile(project_path)
        elif operational_system == "Darwin":
            subprocess.run(["open", project_path])
        elif operational_system == "Linux":
            subprocess.run(["xdg-open", project_path])
        else:
            raise OSError(f"Unsupported operating system: {operational_system}")
