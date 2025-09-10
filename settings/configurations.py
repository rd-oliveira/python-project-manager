import flet as ft
import json


class Configuration(ft.Column):
    def __init__(self, page: ft.Page, config, on_path_updated=None):
        super().__init__(expand=True)
        self.page = page
        self.config = config
        self.on_path_updated = on_path_updated
        self.path = None

        self.file_dialog = ft.FilePicker(on_result=self.search_directory)
        self.page.overlay.append(self.file_dialog)

        title = ft.Text(value="Settings Page", size=40, weight=ft.FontWeight.BOLD)

        self.txt_path_project = ft.TextField(
            value="", label="Project Path", disabled=True, width=400
        )

        btn_folder = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_size=30,
            tooltip="Select project folder",
            on_click=lambda e: self.file_dialog.get_directory_path(),
        )

        btn_save = ft.ElevatedButton(
            text="💾 Save",
            height=48,
            width=150,
            on_click=self.save_path,
        )

        row = ft.Row(
            controls=[self.txt_path_project, btn_folder],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.controls.append(
            ft.Column(
                controls=[title, row, btn_save],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            )
        )

    def did_mount(self):
        self.load_current_config()

    def load_current_config(self):
        settings = self.config.load_json()
        if settings:
            self.path = settings.get("project_path", "")
            self.txt_path_project.value = self.path
            self.txt_path_project.update()

    def search_directory(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.path = e.path
            self.txt_path_project.value = self.path
            self.txt_path_project.update()

    def save_path(self, e):
        if not self.path:
            self.show_snack_bar("⚠️ No path selected.")
            return

        data = self.config.load_json() or {}
        data["project_path"] = self.path

        try:
            with self.config.json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.show_snack_bar("✅ Settings saved.")

            if self.on_path_updated:
                self.on_path_updated(self.path)
        except Exception as ex:
            self.show_snack_bar(f"❌ Error saving: {ex}")

    def show_snack_bar(self, message: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
