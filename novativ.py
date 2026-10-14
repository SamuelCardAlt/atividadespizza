import flet as ft


def main(page: ft.Page):
    # CONFIGURACOES
    page.title = "PizzaDev"
    page.window.width = 400
    page.window.height = 760
    page.padding = 15
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK

    PRETO = "#121212"
    LARANJA = "#FF8C00"
    CINZA = "#242424"
    BRANCO = "#FFFFFF"
    VERDE = "#4CAF50"

    cardapio = {
        "Calabresa": {
            "ingredientes": "Calabresa, cebola e queijo",
            "precos": {"Pequena": 25.00, "Média": 32.00, "Grande": 42.00},
        },
        "Frango com Catupiry": {
            "ingredientes": "Frango desfiado e catupiry",
            "precos": {"Pequena": 27.00, "Média": 35.00, "Grande": 45.00},
        },
        "Mussarela": {
            "ingredientes": "Mussarela, tomate e orégano",
            "precos": {"Pequena": 23.00, "Média": 30.00, "Grande": 40.00},
        },
        "Portuguesa": {
            "ingredientes": "Presunto, ovo, cebola e queijo",
            "precos": {"Pequena": 28.00, "Média": 36.00, "Grande": 46.00},
        },
        "Chocolate": {
            "ingredientes": "Chocolate ao leite",
            "precos": {"Pequena": 25.00, "Média": 33.00, "Grande": 43.00},
        },
        "Pepperoni": {
            "ingredientes": "Pepperoni, queijo e molho",
            "precos": {"Pequena": 28.00, "Média": 36.00, "Grande": 46.00},
        },
    }

    pedidos = []
    entrega_selecionada = "Entrega em casa"
    pagamento_selecionado = "Pix"

    campo_sabor = ft.Dropdown(
        label="Escolha o sabor",
        options=[ft.DropdownOption(key=sabor, text=sabor) for sabor in cardapio],
        value="Calabresa",
        expand=True,
        border_color=LARANJA,
    )
    campo_tamanho = ft.Dropdown(
        label="Tamanho",
        options=[
            ft.DropdownOption(key="Pequena", text="Pequena"),
            ft.DropdownOption(key="Média", text="Média"),
            ft.DropdownOption(key="Grande", text="Grande"),
        ],
        value="Média",
        expand=True,
        border_color=LARANJA,
    )
    campo_quantidade = ft.Dropdown(
        label="Quantidade",
        options=[ft.DropdownOption(key=str(n), text=str(n)) for n in range(1, 11)],
        value="1",
        width=130,
        border_color=LARANJA,
    )

    mensagem = ft.Text(value="", color=VERDE, size=14)
    lista_pedidos = ft.Column(spacing=8)
    conteudo = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=12, expand=True)

    def preco(valor):
        return f"R$ {valor:.2f}".replace(".", ",")

    def titulo(texto):
        return ft.Text(texto, size=22, weight=ft.FontWeight.BOLD, color=LARANJA)

    def botao(texto, funcao, icone=None):
        return ft.Button(
            content=ft.Row(
                controls=[
                    *([ft.Icon(icone)] if icone else []),
                    ft.Text(texto),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True,
            ),
            on_click=funcao,
            style=ft.ButtonStyle(
                bgcolor=LARANJA,
                color=PRETO,
                padding=12,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

    def mostrar_mensagem(texto, cor=VERDE):
        mensagem.value = texto
        mensagem.color = cor
        page.update()

    def desenhar_pedidos():
        lista_pedidos.controls.clear()
        if not pedidos:
            lista_pedidos.controls.append(
                ft.Text("Seu carrinho está vazio.", color="#AAAAAA")
            )
        else:
            for indice, pedido in enumerate(pedidos):
                subtotal = pedido["preco"] * pedido["quantidade"]
                lista_pedidos.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.SHOPPING_CART, color=LARANJA, size=24),
                                ft.Column(
                                    controls=[
                                        ft.Text(pedido["sabor"], weight=ft.FontWeight.BOLD, color=BRANCO),
                                        ft.Text(
                                            f'{pedido["tamanho"]} | Quantidade: {pedido["quantidade"]}',
                                            size=12,
                                            color="#CCCCCC",
                                        ),
                                        ft.Text(preco(subtotal), color=LARANJA, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=3,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="#FF5252",
                                    tooltip="Excluir pedido",
                                    on_click=lambda e, idx=indice: excluir_pedido(idx),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=CINZA,
                        padding=10,
                        border_radius=10,
                    )
                )

    def abrir_cardapio(e=None):
        conteudo.controls.clear()
        conteudo.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCAL_PIZZA, color=LARANJA, size=34),
                        ft.Text("PizzaDev", size=32, weight=ft.FontWeight.BOLD, color=LARANJA),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text("Monte seu pedido com segurança!", color=BRANCO),
                ft.Divider(color=LARANJA),
                titulo("Nosso cardápio"),
            ]
        )

        for sabor, dados in cardapio.items():
            conteudo.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(sabor, size=18, weight=ft.FontWeight.BOLD, color=LARANJA),
                            ft.Text(dados["ingredientes"], size=13, color=BRANCO),
                            ft.Text(
                                f'Pequena: {preco(dados["precos"]["Pequena"])} | '
                                f'Média: {preco(dados["precos"]["Média"])} | '
                                f'Grande: {preco(dados["precos"]["Grande"])}',
                                size=12,
                                color="#CCCCCC",
                            ),
                        ],
                        spacing=5,
                    ),
                    bgcolor=CINZA,
                    padding=12,
                    border_radius=10,
                )
            )

        conteudo.controls.extend(
            [
                titulo("Monte sua pizza"),
                campo_sabor,
                campo_tamanho,
                campo_quantidade,
                botao("Adicionar ao carrinho", adicionar_pedido, ft.Icons.ADD_SHOPPING_CART),
                mensagem,
                ft.Divider(color=LARANJA),
                ft.Row(
                    controls=[
                        titulo("Seus pedidos"),
                        ft.Icon(ft.Icons.SHOPPING_CART, color=LARANJA, size=25),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                lista_pedidos,
                botao("Revisar e finalizar compra", abrir_revisao, ft.Icons.ARROW_FORWARD),
            ]
        )
        desenhar_pedidos()
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    def adicionar_pedido(e):
        sabor = campo_sabor.value
        tamanho = campo_tamanho.value
        quantidade = int(campo_quantidade.value or "1")
        if not sabor or not tamanho:
            mostrar_mensagem("Selecione o sabor e o tamanho.", "#FF5252")
            return
        pedidos.append(
            {
                "sabor": sabor,
                "tamanho": tamanho,
                "quantidade": quantidade,
                "preco": cardapio[sabor]["precos"][tamanho],
            }
        )
        desenhar_pedidos()
        mostrar_mensagem("Pizza adicionada ao carrinho!")
        page.update()

    def excluir_pedido(indice):
        if 0 <= indice < len(pedidos):
            pedidos.pop(indice)
        desenhar_pedidos()
        mostrar_mensagem("Pedido removido do carrinho.")
        page.update()

    def alterar_entrega(e):
        nonlocal entrega_selecionada
        entrega_selecionada = e.control.value

    def alterar_pagamento(e):
        nonlocal pagamento_selecionado
        pagamento_selecionado = e.control.value

    def abrir_revisao(e=None):
        if not pedidos:
            mostrar_mensagem("Adicione pelo menos uma pizza antes de continuar.", "#FFB74D")
            return

        conteudo.controls.clear()
        total = sum(p["preco"] * p["quantidade"] for p in pedidos)
        quantidade_total = sum(p["quantidade"] for p in pedidos)

        conteudo.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RECEIPT_LONG, color=LARANJA, size=30),
                        titulo("Revisão do pedido"),
                    ]
                ),
                ft.Text("Confira os itens antes de finalizar.", color="#CCCCCC"),
                ft.Divider(color=LARANJA),
            ]
        )

        for pedido in pedidos:
            subtotal = pedido["preco"] * pedido["quantidade"]
            conteudo.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(pedido["sabor"], color=BRANCO, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        f'{pedido["tamanho"]} x {pedido["quantidade"]}',
                                        color="#BBBBBB",
                                        size=13,
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Text(preco(subtotal), color=LARANJA, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    bgcolor=CINZA,
                    padding=12,
                    border_radius=8,
                )
            )

        conteudo.controls.extend(
            [
                ft.Divider(color=LARANJA),
                ft.Row(
                    controls=[
                        ft.Text("TOTAL DO PEDIDO", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(preco(total), size=20, weight=ft.FontWeight.BOLD, color=LARANJA),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                titulo("Forma de recebimento"),
                ft.Dropdown(
                    label="Como deseja receber?",
                    value=entrega_selecionada,
                    options=[
                        ft.DropdownOption(key="Entrega em casa", text="Entrega em casa"),
                        ft.DropdownOption(
                            key="Retirada no estabelecimento",
                            text="Retirada no estabelecimento",
                        ),
                    ],
                    border_color=LARANJA,
                    on_select=alterar_entrega,
                ),
                titulo("Método de pagamento"),
                ft.Dropdown(
                    label="Escolha o pagamento",
                    value=pagamento_selecionado,
                    options=[
                        ft.DropdownOption(key="Pix", text="Pix"),
                        ft.DropdownOption(key="Cartão", text="Cartão"),
                    ],
                    border_color=LARANJA,
                    on_select=alterar_pagamento,
                ),
                ft.Text(
                    "Demonstração: nenhum pagamento real será processado.",
                    color="#BBBBBB",
                    size=12,
                ),
                mensagem,
                botao("Concluir pedido", concluir_pedido, ft.Icons.CHECK_CIRCLE),
                ft.Button(
                    content="Voltar ao cardápio",
                    on_click=abrir_cardapio,
                    style=ft.ButtonStyle(color=LARANJA),
                ),
            ]
        )
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    def concluir_pedido(e):
        if not pedidos:
            abrir_cardapio()
            mostrar_mensagem("Seu carrinho está vazio.", "#FF5252")
            return

        total = sum(p["preco"] * p["quantidade"] for p in pedidos)
        quantidade_total = sum(p["quantidade"] for p in pedidos)
        entrega = entrega_selecionada
        pagamento = pagamento_selecionado
        pedidos.clear()

        conteudo.controls.clear()
        conteudo.controls.extend(
            [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=VERDE, size=75),
                            ft.Text(
                                "Pedido concluído!",
                                size=27,
                                weight=ft.FontWeight.BOLD,
                                color=VERDE,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Obrigado por escolher a PizzaDev!",
                                color=BRANCO,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    padding=20,
                    bgcolor=CINZA,
                    border_radius=15,
                ),
                ft.Divider(color=LARANJA),
                titulo("Resumo final"),
                ft.Text(f"Quantidade de pizzas: {quantidade_total}"),
                ft.Text(f"Recebimento: {entrega}"),
                ft.Text(f"Pagamento: {pagamento}"),
                ft.Text(f"Total: {preco(total)}", size=22, weight=ft.FontWeight.BOLD, color=LARANJA),
                ft.Text("Status: pedido registrado no aplicativo.", color=VERDE),
                ft.Text(
                    "Pagamento e entrega precisam ser confirmados fora do aplicativo.",
                    color="#BBBBBB",
                    size=12,
                ),
                botao("Voltar ao início", abrir_cardapio, ft.Icons.HOME),
            ]
        )
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    abrir_cardapio()


if __name__ == "__main__":
    ft.run(main)
