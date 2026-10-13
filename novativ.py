import flet as ft


def main(page: ft.Page):

    # Configurações da janela
    page.title = "PizzaDev"
    page.window.width = 400
    page.window.height = 760
    page.window.min_width = 330
    page.window.min_height = 510

    # Cores do aplicativo
    PRETO = "#121212"
    LARANJA = "#FF8C00"
    BRANCO = "#FFFFFF"

    # Configurações visuais
    page.bgcolor = PRETO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.spacing = 10
    page.scroll = ft.ScrollMode.AUTO

    # Ícone e título
    icone = ft.Text(
        "🍕",
        size=55,
        text_align=ft.TextAlign.CENTER
    )

    titulo = ft.Text(
        "PizzaDev",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=LARANJA,
        text_align=ft.TextAlign.CENTER
    )

    subtitulo = ft.Text(
        "Monte seu pedido com segurança",
        size=14,
        color=BRANCO,
        text_align=ft.TextAlign.CENTER
    )

    # Estilo dos campos de escrita
    estilo_campo = {
        "filled": True,
        "fill_color": LARANJA,
        "color": "#000000",
        "border_color": LARANJA,
        "focused_border_color": BRANCO,
        "label_style": ft.TextStyle(color="#000000"),
        "cursor_color": "#000000",
        "border_radius": 10,
    }

    # Seleção do sabor
    sabor = ft.Dropdown(
        label="Escolha o sabor",
        options=[
            ft.DropdownOption(key="Calabresa"),
            ft.DropdownOption(key="Frango"),
            ft.DropdownOption(key="Carne"),
        ],
        bgcolor=LARANJA,
        color="#FFFFFF",
        border_color=LARANJA,
        focused_border_color=BRANCO,
        border_radius=10,
        expand=True,
    )

    # Seleção do tamanho
    tamanho = ft.Dropdown(
        label="Escolha o tamanho",
        options=[
            ft.DropdownOption(key="Pequena"),
            ft.DropdownOption(key="Média"),
            ft.DropdownOption(key="Grande"),
        ],
        bgcolor=LARANJA,
        color="#FFFFFF",
        border_color=LARANJA,
        focused_border_color=BRANCO,
        border_radius=10,
        expand=True,
    )

    # Quantidade
    quantidade = ft.TextField(
        label="Digite a quantidade",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
        **estilo_campo
    )

    # Observações
    observacao = ft.TextField(
        label="Observações do pedido",
        hint_text="Ex.: Sem cebola ou borda recheada",
        multiline=True,
        min_lines=2,
        max_lines=3,
        max_length=120,
        expand=True,
        **estilo_campo
    )

    # Resultados
    resultado = ft.Text(size=16, color=BRANCO)
    total = ft.Text(
        size=18,
        weight=ft.FontWeight.BOLD,
        color=LARANJA
    )

    preco_pizza = 40.00

    # Exibe os detalhes do pedido
    def exibir_valor(e):

        if not sabor.value or not tamanho.value or not quantidade.value:
            resultado.value = (
                "Preencha o sabor, o tamanho e a quantidade!"
            )
            page.update()
            return

        try:
            qtd = int(quantidade.value)

            if qtd <= 0:
                resultado.value = (
                    "Digite uma quantidade maior que zero!"
                )
                page.update()
                return

        except ValueError:
            resultado.value = "Digite uma quantidade válida!"
            page.update()
            return

        resultado.value = (
            f"Pedido: {qtd} pizza(s) {tamanho.value} "
            f"de {sabor.value}."
        )

        obs = observacao.value.strip()

        if obs:
            resultado.value += f"\nObservação: {obs}"

        page.update()

    # Calcula o total
    def calcular_total(e):

        if not quantidade.value:
            total.value = "Informe a quantidade de pizzas."
            page.update()
            return

        try:
            qtd = int(quantidade.value)

            if qtd <= 0:
                total.value = "A quantidade deve ser maior que zero."
                page.update()
                return

        except ValueError:
            total.value = "Digite uma quantidade válida."
            page.update()
            return

        valor_total = qtd * preco_pizza

        valor_formatado = (
            f"R$ {valor_total:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        total.value = (
            f"{qtd} pizza(s) × R$ 40,00 = {valor_formatado}"
        )

        page.update()

    # Limpa os campos
    def limpar(e):

        sabor.value = None
        tamanho.value = None
        quantidade.value = ""
        observacao.value = ""
        resultado.value = ""
        total.value = ""

        page.update()

    # Estilo dos botões
    estilo_botao = ft.ButtonStyle(
        bgcolor=LARANJA,
        color="#000000",
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    # Botões
    botao = ft.Button(
        content="Adicionar",
        icon=ft.Icons.ADD_SHOPPING_CART,
        on_click=exibir_valor,
        expand=True,
        style=estilo_botao,
    )

    botao_calcular = ft.Button(
        content="Calcular Total",
        icon=ft.Icons.CALCULATE,
        on_click=calcular_total,
        expand=True,
        style=estilo_botao,
    )

    botao_limpar = ft.Button(
        content="Limpar",
        icon=ft.Icons.DELETE_OUTLINE,
        on_click=limpar,
        expand=True,
        style=estilo_botao,
    )

    # Cabeçalho
    cabecalho = ft.Column(
        controls=[
            icone,
            titulo,
            subtitulo,
        ],
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Formulário
    conteudo = ft.Column(
        controls=[
            cabecalho,
            sabor,
            tamanho,
            quantidade,
            observacao,

            ft.Column(
                controls=[
                    botao,
                    botao_calcular,
                    botao_limpar,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),

            resultado,
            total,
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    # Cartão do formulário
    layout = ft.Container(
        content=conteudo,
        width=360,
        padding=15,
        bgcolor=PRETO,
        border_radius=15,
        alignment=ft.Alignment.TOP_CENTER,
    )

    # Centraliza o aplicativo
    page.add(
        ft.Row(
            controls=[layout],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )


ft.run(main)
