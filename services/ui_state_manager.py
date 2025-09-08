import flet as ft


from typing import List


class UIStateManager:
    def __init__(self):
        self.controls: List[ft.Control] = []

    def register_controls(self, controls: List[ft.Control]):
        """Registers controls for state management"""
        for c in controls:
            if c not in self.controls:
                self.controls.append(c)

    def disable_all(self):
        """Disables all registered controls"""
        for c in self.controls:
            c.disabled = True
        self._update_all()

    def enable_all(self):
        """Enables all registered controls"""
        for c in self.controls:
            if not isinstance(c, ft.ElevatedButton):
                c.disabled = False
        self._update_all()

    def _update_all(self):
        """Updates all controls that are already on the page"""
        for c in self.controls:
            if hasattr(c, "update"):
                c.update()
