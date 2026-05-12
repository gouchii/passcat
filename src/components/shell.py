import flet as ft


class AppShell(ft.Container):
    def __init__(self, sidebar, content_area):

        self.row: ft.Row = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar,
                content_area,
            ],
        )

        super().__init__(
            expand=True,
            content=self.row,
        )