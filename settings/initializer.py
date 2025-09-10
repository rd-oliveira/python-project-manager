import os
import platform
import json
import logging


from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")


class UIConfig:
    def __init__(self, project_folder_name: str, project_folder_config: str):
        self.project_folder_name = project_folder_name
        self.project_folder_config = project_folder_config

        self.system_base_path, self.documents_path = self.check_operating_system()

        self.full_project_path = self.documents_path / self.project_folder_name
        self.full_settings_path = self.system_base_path / self.project_folder_config
        self.json_path = self.full_settings_path / "settings.json"

    def check_operating_system(self):
        os_name = platform.system()
        if os_name == "Windows":
            return (
                Path(os.getenv("APPDATA")) / "PythonProjectManager",
                Path.home() / "Documents",
            )
        elif os_name in ["Linux", "Darwin"]:
            return (Path.home(), Path.home() / "Documents")
        raise EnvironmentError("Unsupported operating system.")

    def create_project_folder(self) -> Path | None:
        try:
            self.full_project_path.mkdir(parents=True, exist_ok=True)
            return self.full_project_path
        except Exception as e:
            logging.error(f"Error creating project folder: {e}")
            return None

    def create_settings_folder(self) -> Path | None:
        try:
            self.full_settings_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Settings folder: {self.full_settings_path}")
            return self.full_settings_path
        except Exception as e:
            logging.error(f"Error creating settings folder: {e}")
            return None

    def create_json(self) -> Path | None:
        if self.json_path.exists():
            logging.info("JSON file already exists. Skipping creation.")
            return self.json_path

        data = {"project_path": str(self.full_project_path)}

        try:
            with self.json_path.open(mode="w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                logging.info(f"JSON file created at: {self.json_path}")
                return self.json_path
        except Exception as e:
            logging.error(f"Error creating JSON file: {e}")
            return None

    def load_json(self) -> dict | None:
        try:
            if self.json_path.exists():
                with self.json_path.open("r", encoding="utf-8") as file:
                    return json.load(file)
            else:
                logging.warning("JSON file not found.")
        except Exception as e:
            logging.error(f"Error reading JSON file: {e}")
        return None

    def setup(self):
        self.create_settings_folder()
        self.create_project_folder()
        if not self.json_path.exists():
            self.create_json()
