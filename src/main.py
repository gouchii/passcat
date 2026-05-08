import flet as ft

from breach_checker import is_pwned
from generator import generate_password
from storage import retrieve_passwords, save_password
from validator import check_strength


async def main(page: ft.Page):
    page.title = "PassCat - Password Generator & Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 600
    page.window.height = 800
    page.padding = 20

    clipboard = ft.Clipboard()

    length_input = ft.TextField(
        label="Length",
        value="16",
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    cb_upper = ft.Checkbox(label="Uppercase (A-Z)", value=True)
    cb_lower = ft.Checkbox(label="Lowercase (a-z)", value=True)
    cb_numbers = ft.Checkbox(label="Numbers (0-9)", value=True)
    cb_symbols = ft.Checkbox(label="Symbols (!@#)", value=True)

    result_text = ft.Text(
        size=24,
        weight=ft.FontWeight.BOLD,
        selectable=True,
        text_align=ft.TextAlign.CENTER,
    )
    strength_text = ft.Text(size=16)
    pwned_text = ft.Text(size=16)

    service_input = ft.TextField(label="Service Name (e.g., Netflix)", expand=True)
    username_input = ft.TextField(label="Username / Email", expand=True)
    save_pwd_input = ft.TextField(
        label="Password",
        expand=True,
        password=True,
        can_reveal_password=True,
    )
    passwords_list_view = ft.ListView(expand=True, spacing=10)

    def show_snackbar(message: str) -> None:
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    async def copy_to_clipboard(password: str) -> None:
        try:
            await clipboard.set(password)
            show_snackbar("Password copied to clipboard.")
        except Exception:
            show_snackbar("Could not copy password.")

    def load_saved_passwords() -> None:
        passwords_list_view.controls.clear()
        saved = retrieve_passwords() or []

        if not saved:
            passwords_list_view.controls.append(
                ft.Text("No saved passwords found.", color=ft.Colors.GREY_400)
            )
        else:
            for item in saved:
                async def on_copy_click(e, pwd=item["password"]):
                    await copy_to_clipboard(pwd)

                passwords_list_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SECURITY),
                        title=ft.Text(f"{item['service']} ({item['username']})"),
                        subtitle=ft.Text("********"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.COPY,
                            tooltip="Copy Password",
                            on_click=on_copy_click,
                        ),
                    )
                )

        page.update()

    def on_generate(e):
        try:
            length = int(length_input.value)
            if length <= 0:
                raise ValueError("Length must be a positive number.")

            pwd = generate_password(
                length,
                cb_upper.value,
                cb_lower.value,
                cb_numbers.value,
                cb_symbols.value,
            )
            result_text.value = pwd

            strength = check_strength(pwd)
            strength_text.value = f"Strength: {strength}"
            strength_text.color = (
                ft.Colors.GREEN
                if strength == "Strong"
                else ft.Colors.YELLOW
                if strength == "Medium"
                else ft.Colors.RED
            )

            pwned_text.value = "Checking breach status..."
            pwned_text.color = ft.Colors.WHITE
            page.update()

            breaches = is_pwned(pwd)
            if breaches == -1:
                pwned_text.value = "API unreachable. Could not check breach status."
                pwned_text.color = ft.Colors.ORANGE
            elif breaches > 0:
                pwned_text.value = (
                    f"WARNING: This password has been seen in {breaches} data breaches!"
                )
                pwned_text.color = ft.Colors.RED
            else:
                pwned_text.value = "Safe: not found in any known data breaches."
                pwned_text.color = ft.Colors.GREEN

        except ValueError as ex:
            result_text.value = str(ex)
            strength_text.value = ""
            pwned_text.value = ""
            strength_text.color = None
            pwned_text.color = None

        page.update()

    def on_save_click(e):
        if not (service_input.value and username_input.value and save_pwd_input.value):
            show_snackbar("Fill in service, username, and password first.")
            return

        save_password(service_input.value, username_input.value, save_pwd_input.value)
        service_input.value = ""
        username_input.value = ""
        save_pwd_input.value = ""
        load_saved_passwords()
        show_snackbar("Password safely encrypted and stored!")
        page.update()

    generator_tab = ft.Column(
        controls=[
            ft.Text("Customize Password", size=20, weight=ft.FontWeight.W_600),
            ft.Row([length_input]),
            cb_upper,
            cb_lower,
            cb_numbers,
            cb_symbols,
            ft.Button(
                content="Generate Password",
                on_click=on_generate,
                icon=ft.Icons.RESTART_ALT,
            ),
            ft.Divider(height=40),
            ft.Container(
                content=result_text,
                padding=20,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=10,
                alignment=ft.Alignment.CENTER,
            ),
            strength_text,
            pwned_text,
        ],
        spacing=10,
        expand=True,
    )

    manager_tab = ft.Column(
        controls=[
            ft.Text("Save a New Password", size=20, weight=ft.FontWeight.W_600),
            service_input,
            username_input,
            ft.Row(
                [
                    save_pwd_input,
                    ft.Button(
                        content="Save",
                        on_click=on_save_click,
                        icon=ft.Icons.SAVE,
                    ),
                ]
            ),
            ft.Divider(height=40),
            ft.Text("Your Vault", size=20, weight=ft.FontWeight.W_600),
            passwords_list_view,
        ],
        spacing=10,
        expand=True,
    )

    tabs = ft.Tabs(
        length=2,
        selected_index=0,
        animation_duration=300,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Generator"),
                        ft.Tab(label="Manager"),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(content=generator_tab, padding=20),
                        ft.Container(content=manager_tab, padding=20),
                    ],
                ),
            ],
        ),
        on_change=lambda e: load_saved_passwords()
        if e.control.selected_index == 1
        else None,
    )

    page.add(tabs)
    on_generate(None)
    load_saved_passwords()


if __name__ == "__main__":
    ft.run(main)

