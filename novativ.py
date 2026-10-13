import flet as ft


def main(page: ft.Page):

    # Lista para guardar os pedidos
    lista_pedidos = []

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

    # Preço de cada pizza
    preco_pizza = 40.00

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

    # Estilo dos campos
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
            ft.DropdownOption(key="Portuguesa"),
            ft.DropdownOption(key="Marguerita"),
            ft.DropdownOption(key="Quatro Queijos"),
            ft.DropdownOption(key="Bacon"),
        ],
        bgcolor=LARANJA,
        color=BRANCO,
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
        color=BRANCO,
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

    # Lista visual dos pedidos
    lista_visual = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    mensagem_lista = ft.Text(
        "Nenhum pedido adicionado ainda.",
        color=BRANCO,
        size=14,
    )

    # Formata valores em reais
    def formatar_moeda(valor):
        return (
            f"R$ {valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # Atualiza a lista de pedidos na tela
    def atualizar_lista():
        lista_visual.controls.clear()

        if not lista_pedidos:
            lista_visual.controls.append(
                ft.Text(
                    "Nenhum pedido adicionado ainda.",
                    color=BRANCO,
                )
            )
        else:
            for i, pedido in enumerate(lista_pedidos):
                cartao = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"🍕 Pedido {i + 1}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=LARANJA,
                            ),
                            ft.Text(
                                f"Sabor: {pedido['sabor']}",
                                color=BRANCO,
                            ),
                            ft.Text(
                                f"Tamanho: {pedido['tamanho']}",
                                color=BRANCO,
                            ),
                            ft.Text(
                                f"Quantidade: {pedido['quantidade']}",
                                color=BRANCO,
                            ),
                            ft.Text(
                                f"Observação: "
                                f"{pedido['observacao'] or 'Nenhuma'}",
                                color=BRANCO,
                            ),
                            ft.Text(
                                f"Subtotal: "
                                f"{formatar_moeda(pedido['subtotal'])}",
                                color=LARANJA,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    bgcolor="#242424",
                    padding=12,
                    border_radius=10,
                    border=ft.Border.all(1, LARANJA),
                )

                lista_visual.controls.append(cartao)

        page.update()

    # Adiciona um pedido à lista
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

        # Calcula o subtotal
        subtotal = qtd * preco_pizza

        # Salva o pedido na lista
        pedido = {
            "sabor": sabor.value,
            "tamanho": tamanho.value,
            "quantidade": qtd,
            "observacao": observacao.value.strip(),
            "subtotal": subtotal,
        }

        lista_pedidos.append(pedido)

        resultado.value = (
            f"Pedido de {sabor.value} adicionado com sucesso!"
        )

        # Atualiza a lista na tela
        atualizar_lista()

        # Limpa os campos para o próximo pedido
        sabor.value = None
        tamanho.value = None
        quantidade.value = ""
        observacao.value = ""

    # Calcula o total de todos os pedidos
    def calcular_total(e):

        if not lista_pedidos:
            total.value = "Adicione pelo menos uma pizza."
            page.update()
            return

        valor_total = sum(
            pedido["subtotal"] for pedido in lista_pedidos
        )

        quantidade_total = sum(
            pedido["quantidade"] for pedido in lista_pedidos
        )

        total.value = (
            f"{quantidade_total} pizza(s) × "
            f"{formatar_moeda(preco_pizza)}\n"
            f"Total do pedido: {formatar_moeda(valor_total)}"
        )

        page.update()

    # Limpa somente o formulário
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
        content="Adicionar pedido",
        icon=ft.Icons.ADD_SHOPPING_CART,
        on_click=exibir_valor,
        expand=True,
        style=estilo_botao,
    )

    botao_calcular = ft.Button(
        content="Calcular total",
        icon=ft.Icons.CALCULATE,
        on_click=calcular_total,
        expand=True,
        style=estilo_botao,
    )

    botao_limpar = ft.Button(
        content="Limpar formulário",
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

            ft.Text(
                "Monte sua pizza",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=LARANJA,
            ),

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

            ft.Divider(color=LARANJA),

            ft.Text(
                "Lista de pedidos",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=LARANJA,
            ),

            ft.Text(
                f"Preço por pizza: {formatar_moeda(preco_pizza)}",
                color=BRANCO,
            ),

            lista_visual,
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    # Cartão principal
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

    # Exibe a mensagem inicial da lista
    atualizar_lista()


ft.run(main)
