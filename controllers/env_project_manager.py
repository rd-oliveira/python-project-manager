import shutil
import subprocess
import platform
import sys
from pathlib import Path


class EnvProjectManager:
    """
    Python project manager that creates folders, virtual environments,
    and automatically installs dependencies.

    Attributes:
        project_name (str): Project folder name.
        base_path (Path): Base directory where the project will be created.
        project_path (Path): Full project path.
        library_list (list): List of libraries to be installed in venv.
    """

    def __init__(self, project_name: str, base_path: str, library_list: list = None):
        self.project_name = project_name.lower()
        self.base_path = Path(base_path)
        self.project_path = self.base_path / self.project_name
        self.library_list = library_list

    def setup_project(self):
        folder_msg = self.create_project_folder()
        venv_msg = self.create_virtual_environment()
        libs_msg = self.install_libraries()

        results = [folder_msg, venv_msg] + libs_msg

        return results

    def create_project_folder(self):
        """
        Creates the project folder if it doesn't exist.

        Returns:
            str: Message indicating whether the folder was created or already exists.
        """
        if self.project_path.exists():
            return f"Project already exists in {self.project_path}"
        self.project_path.mkdir(parents=True, exist_ok=True)

        return f"Project created in {self.project_path}"

    def list_projects(self):
        return [p.name for p in self.base_path.iterdir() if p.is_dir()]

    def delete_project_folder(self):
        if self.project_path.exists():
            shutil.rmtree(path=self.project_path)
            return f"Project removed: {self.project_path}"
        return "Project not found"

    def create_virtual_environment(self):
        """Creates a virtual environment inside the project folder."""
        venv_path = self.project_path.joinpath(".venv")

        if venv_path.exists():
            return f"Virtual environment already exists at {venv_path}"

        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            return f"Virtual environment created in '{venv_path}'"

        except subprocess.CalledProcessError as erro:
            return f"Não foi possível criar o virtual environment. Error: {erro}"

    def install_libraries(self):
        library_list = self.library_list

        results = []

        if library_list is None:
            results.append("No libraries were installed")
            return results

        try:
            for library in library_list:
                if platform.system() == "Windows":
                    python_exec = self.project_path / ".venv/Scripts/python.exe"
                else:
                    python_exec = self.project_path / ".venv/bin/python"

                result = subprocess.run(
                    [str(python_exec), "-m", "pip", "install", library],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    results.append(f"{library} installed successfully.")
                else:
                    results.append(f"Error when installing {library}: {result.stderr}")

        except Exception as erro:
            return [f"Unable to install dependencies... {erro}"]

        return results
