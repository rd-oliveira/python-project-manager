# 🐍 Python Project Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-UI-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## **Description**

A simple and practical application to manage Python projects.  
It allows creating new projects, adding libraries, configuring the project path, and viewing existing projects in a modern graphical interface built with **Flet**.

---

## **Features**

- Create Python projects in a user-defined directory.
- Add libraries for automatic installation in a virtual environment (`venv`).
- View existing projects and open folders directly in the operating system.
- Configure the base project path via the settings interface.
- Visual feedback with logs and SnackBar messages.
- State management to enable/disable controls during critical operations.

---

## **Technologies Used**

- **Python 3.11+**
- **Flet** → Graphical interface (UI)
- **subprocess** → Virtual environment creation and library installation
- **pathlib** → Path manipulation
- **json** → Configuration persistence

---

## **Installation and Running**

1. Clone the repository:

```bash
git clone https://github.com/rd-oliveira/python-project-manager.git
cd project_manager
```

2.(Optional) Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3.Install dependencies:

```python
pip install flet
```

4.Run the application:

```python
python main.py #Windows
python3 main.py #Linux/macOs
```

## **Usage**

### Settings

- Click the gear icon in the header.

- Select the folder where projects will be stored.

- Click 💾 Save to save the path.

The project list will automatically update.

### Create Project

- Enter the project name.

- Add optional libraries.

- Click Create Project.

The project will be created, a virtual environment will be generated, and libraries will be installed automatically.
The library list will be cleared after project creation.

### View Projects

The project list updates automatically after creating projects or changing the path.

- Click on any project to open its folder in the operating system.

- Best Practices Applied

- Clear modularity between creation, viewing, and configuration.

- Dynamic interface updates with update() after changes.

- State management for critical operations (enable/disable controls).

- Constant visual feedback (logs and SnackBars).

- Automatic clearing of fields and lists after operations.

## **Contributing**

Contributions are welcome!
Feel free to open issues or pull requests for improvements and bug fixes.
