import flet as ft


def main(page: ft.Page):

    # Configurações da janela em formato mobile
    page.title = "PizzaDev"

    page.window.width = 400
    page.window.height = 760

    page.window.min_width = 330
    page.window.min_height = 510

    page.padding = 15
    page.spacing = 10
    page.scroll = ft.ScrollMode.AUTO
    
    # Título
    titulo = ft.Text(
        "PizzaDev",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    # Dropdown do sabor
    sabor = ft.Dropdown(
        label="Escolha o sabor",
        options=[
            ft.DropdownOption(key="Calabresa"),
            ft.DropdownOption(key="Frango"),
            ft.DropdownOption(key="Carne")
        ],
        expand=True
    )

    # Dropdown do tamanho
    tamanho = ft.Dropdown(
        label="Escolha o tamanho",
        options=[
            ft.DropdownOption(key="Pequena"),
            ft.DropdownOption(key="Média"),
            ft.DropdownOption(key="Grande")
        ],
        expand=True
    )

    # Quantidade de pizzas
    quantidade = ft.TextField(
        label="Digite a quantidade",
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True
    )

    # Observações do pedido
    observacao = ft.TextField(
        label="Observações do pedido",
        hint_text="Ex.: Sem cebola ou borda recheada",
        multiline=True,
        min_lines=2,
        max_lines=4,
        max_length=120,
        expand=True
    )

    # Resultados
    resultado = ft.Text(size=16)
    total = ft.Text(size=18, weight=ft.FontWeight.BOLD)

    # Preço fixo por pizza
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

        # Adiciona a observação se estiver preenchida
        obs = observacao.value.strip()

        if obs:
            resultado.value += f"\nObservação: {obs}"

        page.update()

    # Calcula o valor total
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

        # Formatação monetária brasileira
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

    # Botões com largura disponível
    botao = ft.Button(
        content="Adicionar",
        on_click=exibir_valor,
        expand=True
    )

    botao_calcular = ft.Button(
        content="Calcular Total",
        on_click=calcular_total,
        expand=True
    )

    botao_limpar = ft.Button(
        content="Limpar",
        on_click=limpar,
        expand=True
    )

    # Coluna principal responsiva
    conteudo = ft.Column(
        controls=[
            titulo,
            sabor,
            tamanho,
            quantidade,
            observacao,

            # Botões organizados verticalmente
            ft.Column(
                controls=[
                    botao,
                    botao_calcular,
                    botao_limpar
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            ),

            resultado,
            total
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True
    )

    # Limita a largura em telas grandes e permite
    # que o conteúdo se ajuste em telas pequenas.
    layout = ft.Container(
    content=conteudo,
    width=360,
    alignment=ft.Alignment.TOP_CENTER
    )

    # Centraliza o formulário e permite rolagem
    page.add(
        ft.Row(
            controls=[layout],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )


ft.run(main)