import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment(e):
        counter.data += 1
        counter.value = str(counter.data)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment
    )
    page.add(
        ft.Container(
            content=counter,
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
    )


ft.run(main)