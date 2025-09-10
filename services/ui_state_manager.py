import flet as ft


from typing import List


class UIStateManager:
    def __init__(self):
        self.controls: List[ft.Control] = []

    def register_controls(self, controls: List[ft.Control]):
        for c in controls:
            if c not in self.controls:
                self.controls.append(c)

    def disable_all(self):
        for c in self.controls:
            c.disabled = True
        self._update_all()

    def enable_all(self):
        for c in self.controls:
            if not isinstance(c, ft.ElevatedButton):
                c.disabled = False
        self._update_all()

    def _update_all(self):
        for c in self.controls:
            if hasattr(c, "update"):
                c.update()
