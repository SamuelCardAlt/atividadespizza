import flet as ft


def main(page: ft.Page):
    page.title = "PizzaDev"

    # Lista para guardar os pedidos
    pedidos = []

    # --------------------------------------------------------------
    # TITULO
    # --------------------------------------------------------------

    titulo = ft.Text(
        "PizzaDev",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text("Monte seu pedido com segurança")
    nome = ft.Text("Seu nome é Pizzaiolo")
    slogan = ft.Text("Piza nhamenhame")
    instrucao = ft.Text("Corta e depois come")

    # --------------------------------------------------------------
    # PEDIDOS
    # --------------------------------------------------------------

    campo_pedido = ft.TextField(
        label="Digite seu pedido",
        expand=True
    )

    lista_pedidos = ft.Column(
        scroll=ft.ScrollMode.AUTO
    )

    def adicionar_pedido(e):
        pedido = campo_pedido.value.strip()

        if pedido == "":
            return

        pedidos.append(pedido)

        lista_pedidos.controls.append(
            ft.Container(
                content=ft.Text(
                    f"🍕 {pedido}",
                    size=18
                ),
                padding=10
            )
        )

        campo_pedido.value = ""
        page.update()

    # Botão para adicionar os pedidos
    botao_adicionar = ft.Button(
        content="Adicionar Pedido",
        on_click=adicionar_pedido
    )

    linha_pedido = ft.Row(
        controls=[
            campo_pedido,
            botao_adicionar
        ]
    )

    # --------------------------------------------------------------
    # CARDAPIO
    # --------------------------------------------------------------

    cardapio_titulo = ft.Text(
        "🍕 CARDÁPIO",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    # --------------------------------------------------------------
    # FUNÇÃO PARA CRIAR AS OPÇÕES DE TAMANHO
    # --------------------------------------------------------------

    def escolher_tamanho():
        return ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(
                        value="Pequena",
                        label="Pequena"
                    ),
                    ft.Radio(
                        value="Media",
                        label="Média - R$ 32,00"
                    ),
                    ft.Radio(
                        value="Grande",
                        label="Grande - R$ 42,00"
                    )
                ]
            )
        )

    # --------------------------------------------------------------
    # FUNÇÃO PARA CRIAR CAMPO DE QUANTIDADE
    # --------------------------------------------------------------

    def campo_quantidade():
        return ft.TextField(
            label="Quantidade (1 a 10)",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER
        )

    # --------------------------------------------------------------
    # PIZZA DE CALABRESA
    # --------------------------------------------------------------

    tamanho_calabresa = escolher_tamanho()
    quantidade_calabresa = campo_quantidade()

    pizza_calabresa = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Calabresa",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: calabresa, queijo, cebola e molho de tomate."
                ),
                ft.Text(
                    "Escolha o tamanho:",
                    weight=ft.FontWeight.BOLD
                ),
                tamanho_calabresa,
                quantidade_calabresa
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # --------------------------------------------------------------
    # PIZZA DE FRANGO
    # --------------------------------------------------------------

    tamanho_frango = escolher_tamanho()
    quantidade_frango = campo_quantidade()

    pizza_frango = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Frango com Catupiry",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: frango desfiado, catupiry, queijo e molho de tomate."
                ),
                ft.Text(
                    "Escolha o tamanho:",
                    weight=ft.FontWeight.BOLD
                ),
                tamanho_frango,
                quantidade_frango
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # --------------------------------------------------------------
    # PIZZA DE MUSSARELA
    # --------------------------------------------------------------

    tamanho_mussarela = escolher_tamanho()
    quantidade_mussarela = campo_quantidade()

    pizza_mussarela = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Mussarela",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: queijo mussarela, tomate, orégano e molho de tomate."
                ),
                ft.Text(
                    "Escolha o tamanho:",
                    weight=ft.FontWeight.BOLD
                ),
                tamanho_mussarela,
                quantidade_mussarela
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # --------------------------------------------------------------
    # PIZZA PORTUGUESA
    # --------------------------------------------------------------

    tamanho_portuguesa = escolher_tamanho()
    quantidade_portuguesa = campo_quantidade()

    pizza_portuguesa = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Portuguesa",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: presunto, queijo, ovo, cebola, tomate e azeitona."
                ),
                ft.Text(
                    "Escolha o tamanho:",
                    weight=ft.FontWeight.BOLD
                ),
                tamanho_portuguesa,
                quantidade_portuguesa
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # --------------------------------------------------------------
    # PIZZA DE CHOCOLATE
    # --------------------------------------------------------------

    tamanho_chocolate = escolher_tamanho()
    quantidade_chocolate = campo_quantidade()

    pizza_chocolate = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍫 Chocolate",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: chocolate, leite condensado e granulado."
                ),
                ft.Text(
                    "Escolha o tamanho:",
                    weight=ft.FontWeight.BOLD
                ),
                tamanho_chocolate,
                quantidade_chocolate
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # --------------------------------------------------------------
    # RESULTADO DO CALCULO
    # --------------------------------------------------------------

    resultado = ft.Text(
        "Parcial: R$ 0,00",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    mensagem = ft.Text(
        "",
        size=16
    )

    # --------------------------------------------------------------
    # FUNÇÃO PARA CALCULAR O PARCIAL
    # --------------------------------------------------------------

    def calcular(e):

        total = 0

        # Lista com todas as pizzas
        pizzas = [
            ("Calabresa", tamanho_calabresa, quantidade_calabresa),
            ("Frango com Catupiry", tamanho_frango, quantidade_frango),
            ("Mussarela", tamanho_mussarela, quantidade_mussarela),
            ("Portuguesa", tamanho_portuguesa, quantidade_portuguesa),
            ("Chocolate", tamanho_chocolate, quantidade_chocolate)
        ]

        for nome_pizza, tamanho, quantidade in pizzas:

            # Se não informou quantidade, ignora essa pizza
            if quantidade.value.strip() == "":
                continue

            try:
                qtd = int(quantidade.value)

            except ValueError:
                mensagem.value = (
                    f"A quantidade da pizza {nome_pizza} deve ser um número."
                )
                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            # Validação da quantidade
            if qtd < 1 or qtd > 10:
                mensagem.value = (
                    f"A quantidade da pizza {nome_pizza} "
                    f"deve estar entre 1 e 10."
                )
                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            # Verifica se escolheu o tamanho
            if tamanho.value is None:
                mensagem.value = (
                    f"Escolha o tamanho da pizza {nome_pizza}."
                )
                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            # Define o preço
            if tamanho.value == "Media":
                preco = 32

            elif tamanho.value == "Grande":
                preco = 42

            else:
                mensagem.value = (
                    f"A pizza {nome_pizza} está no tamanho Pequena, "
                    f"mas o preço desse tamanho ainda não foi cadastrado."
                )
                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            # Calcula
            total += preco * qtd

        # Mostra o resultado
        resultado.value = f"Parcial: R$ {total:.2f}".replace(".", ",")
        mensagem.value = "Pedido calculado com sucesso!"

        page.update()

    # --------------------------------------------------------------
    # BOTÃO CALCULAR
    # --------------------------------------------------------------

    botao_calcular = ft.Button(
        content="Calcular",
        on_click=calcular
    )

    # --------------------------------------------------------------
    # COLUNA DO CARDAPIO
    # --------------------------------------------------------------

    cardapio = ft.Column(
        controls=[
            cardapio_titulo,

            ft.Row(
                controls=[
                    pizza_calabresa,
                    pizza_frango
                ]
            ),

            ft.Row(
                controls=[
                    pizza_mussarela,
                    pizza_portuguesa
                ]
            ),

            ft.Row(
                controls=[
                    pizza_chocolate
                ]
            ),

            ft.Divider(),

            botao_calcular,

            resultado,

            mensagem
        ],
        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # CONTEUDO PRINCIPAL
    # --------------------------------------------------------------

    conteudo = ft.Column(
        controls=[
            titulo,
            subtitulo,
            nome,
            instrucao,
            slogan,

            ft.Divider(),

            linha_pedido,

            ft.Text(
                "Pedidos adicionados:",
                size=22,
                weight=ft.FontWeight.BOLD
            ),

            lista_pedidos,

            ft.Divider(),

            # Cardápio separado
            cardapio
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # CONTAINER PRINCIPAL
    # --------------------------------------------------------------

    tela = ft.Container(
        content=conteudo,
        padding=20,
        expand=True
    )

    page.add(tela)


ft.run(main)
