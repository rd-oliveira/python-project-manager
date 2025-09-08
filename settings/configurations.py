import flet as ft
import json


class Configuration(ft.Column):
    def __init__(self, page: ft.Page, on_return, config):
        super().__init__(expand=True)

        # Props
        self.page = page
        self.config = config  # Instance of UIConfig
        self.on_return_callback = on_return
        self.path = None

        # Layout config
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20

        # File picker
        self.file_dialog = ft.FilePicker(on_result=self.search_directory)
        self.page.overlay.append(self.file_dialog)

        # Title
        title = ft.Text(
            value="Settings Page",
            size=40,
            weight=ft.FontWeight.BOLD,
        )

        # Project path field (disabled, updated via file picker)
        self.txt_path_project = ft.TextField(
            value="",
            label="Project Path",
            disabled=True,
            width=400,
        )

        # Buttons
        btn_folder = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_size=30,
            tooltip="Select project folder",
            on_click=self.file_dialog.get_directory_path,
        )

        btn_save = ft.ElevatedButton(
            text="💾 Save",
            height=48,
            width=150,
            on_click=self.save_path,
        )

        btn_return = ft.ElevatedButton(
            text="← Back",
            height=48,
            width=150,
            on_click=self.on_return,
        )

        # Row for field + folder button
        row = ft.Row(
            controls=[self.txt_path_project, btn_folder],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Main layout
        content = ft.Column(
            controls=[title, row, btn_save, btn_return],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )

        self.controls.append(content)

    def did_mount(self):
        """Runs after the control is added to the page (safe to call update)."""
        self.load_current_config()

    def load_current_config(self):
        """Loads existing project path from settings.json (if any)."""
        settings = self.config.load_json()
        if settings:
            self.path = settings.get("project_path", "")
            self.txt_path_project.value = self.path
            self.txt_path_project.update()

    def search_directory(self, e: ft.FilePickerResultEvent):
        """When user selects a directory from the file picker."""
        if e.path:
            self.path = e.path
            self.txt_path_project.value = self.path
            self.txt_path_project.update()

    def save_path(self, e):
        """Saves selected path to settings.json."""
        if not self.path:
            self.show_snack_bar("⚠️ No path selected.")
            return

        data = self.config.load_json() or {}
        data["project_path"] = self.path

        try:
            with self.config.json_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.show_snack_bar("✅ Settings saved.")
        except Exception as ex:
            self.show_snack_bar(f"❌ Error saving: {ex}")

    def on_return(self, e):
        """Calls back to return to the main screen."""
        if self.on_return_callback:
            self.on_return_callback()

    def show_snack_bar(self, message: str):
        """Displays a temporary notification message."""
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
