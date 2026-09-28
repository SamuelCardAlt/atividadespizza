import flet as ft

def main(page: ft.Page):
    page.title = "PizzaDev"
    # --------------------------------------------------------------
    # ESTADO DO PEDIDO
    # --------------------------------------------------------------

    estado = {
        "pizza": "",
        "quantidade": 1
    }

    # --------------------------------------------------------------
    # LISTAS
    # --------------------------------------------------------------

    pedidos = []
    pizzas = []

    # --------------------------------------------------------------
    # TÍTULO
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
    # LINHA DO ESTADO
    # --------------------------------------------------------------

    pedido_edicao = ft.Text(
        "Pedido em edição: Nenhuma pizza selecionada",
        size=14,
        italic=True
    )

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
    # CARDÁPIO
    # --------------------------------------------------------------

    cardapio_titulo = ft.Text(
        "🍕 CARDÁPIO",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    # --------------------------------------------------------------
    # RESULTADO
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
    # FUNÇÃO PARA ATUALIZAR O ESTADO NO TOPO
    # --------------------------------------------------------------

    def atualizar_estado():
        if estado["pizza"] == "":
            pedido_edicao.value = (
                "Pedido em edição: Nenhuma pizza selecionada"
            )
        else:
            pedido_edicao.value = (
                f"Pedido em edição: "
                f"{estado['pizza']} - "
                f"Quantidade: {estado['quantidade']}"
            )

    # --------------------------------------------------------------
    # TAMANHO
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
    # QUANTIDADE
    # --------------------------------------------------------------

    def campo_quantidade():
        return ft.TextField(
            label="Quantidade (1 a 10)",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="1"
        )

    # --------------------------------------------------------------
    # CRIAR PIZZA
    # --------------------------------------------------------------

    def criar_pizza(nome_pizza, ingredientes):

        tamanho = escolher_tamanho()
        quantidade = campo_quantidade()

        def selecionar(e):

            # Guarda o nome da pizza no estado
            estado["pizza"] = nome_pizza

            # Guarda a quantidade no estado
            try:
                qtd = int(quantidade.value)

                if qtd < 1 or qtd > 10:
                    mensagem.value = (
                        "A quantidade deve estar entre 1 e 10."
                    )
                    page.update()
                    return

                estado["quantidade"] = qtd

            except ValueError:
                mensagem.value = (
                    "Digite uma quantidade válida."
                )
                page.update()
                return

            atualizar_estado()

            mensagem.value = (
                f"Pizza selecionada: {nome_pizza} 🍕"
            )

            page.update()

        botao_selecionar = ft.Button(
            content="Selecionar",
            on_click=selecionar
        )

        pizza = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"🍕 {nome_pizza}",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        f"Ingredientes: {ingredientes}"
                    ),

                    ft.Text(
                        "Escolha o tamanho:",
                        weight=ft.FontWeight.BOLD
                    ),

                    tamanho,

                    quantidade,

                    botao_selecionar
                ]
            ),
            padding=15,
            border=ft.Border.all(1, "orange"),
            width=450
        )

        pizzas.append(
            {
                "nome": nome_pizza,
                "tamanho": tamanho,
                "quantidade": quantidade
            }
        )

        return pizza

    # --------------------------------------------------------------
    # PIZZAS
    # --------------------------------------------------------------

    pizza_calabresa = criar_pizza(
        "Calabresa",
        "calabresa, queijo, cebola e molho de tomate."
    )

    pizza_frango = criar_pizza(
        "Frango com Catupiry",
        "frango desfiado, catupiry, queijo e molho de tomate."
    )

    pizza_mussarela = criar_pizza(
        "Mussarela",
        "queijo mussarela, tomate, orégano e molho de tomate."
    )

    pizza_portuguesa = criar_pizza(
        "Portuguesa",
        "presunto, queijo, ovo, cebola, tomate e azeitona."
    )

    pizza_chocolate = criar_pizza(
        "Chocolate",
        "chocolate, leite condensado e granulado."
    )

    pizza_pepperoni = criar_pizza(
        "Pepperoni",
        "pepperoni, queijo, molho de tomate e orégano."
    )

    # --------------------------------------------------------------
    # CALCULAR
    # --------------------------------------------------------------

    def calcular(e):

        total = 0

        for pizza in pizzas:

            nome_pizza = pizza["nome"]
            tamanho = pizza["tamanho"]
            quantidade = pizza["quantidade"]

            if quantidade.value.strip() == "":
                continue

            try:
                qtd = int(quantidade.value)

            except ValueError:

                mensagem.value = (
                    f"A quantidade da pizza {nome_pizza} "
                    f"deve ser um número."
                )

                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            if qtd < 1 or qtd > 10:

                mensagem.value = (
                    f"A quantidade da pizza {nome_pizza} "
                    f"deve estar entre 1 e 10."
                )

                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

            if tamanho.value is None:

                mensagem.value = (
                    f"Escolha o tamanho da pizza {nome_pizza}."
                )

                resultado.value = "Parcial: R$ 0,00"
                page.update()
                return

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

            total += preco * qtd

        resultado.value = (
            f"Parcial: R$ {total:.2f}"
        ).replace(".", ",")

        mensagem.value = "Pedido calculado com sucesso!"

        page.update()

    botao_calcular = ft.Button(
        content="Calcular",
        on_click=calcular
    )

    # --------------------------------------------------------------
    # PIZZA TEMPORÁRIA
    # --------------------------------------------------------------

    def adicionar_pizza_temporaria(e):

        nova_pizza = criar_pizza(
            "Pizza Temporária",
            "queijo, molho de tomate e ingredientes especiais."
        )

        cardapio.controls.insert(
            len(cardapio.controls) - 4,
            nova_pizza
        )

        mensagem.value = (
            "Pizza temporária adicionada ao cardápio! 🍕"
        )

        page.update()

    botao_pizza_temporaria = ft.Button(
        content="Adicionar Pizza Temporária",
        on_click=adicionar_pizza_temporaria
    )

    # --------------------------------------------------------------
    # CARDÁPIO
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
                    pizza_chocolate,
                    pizza_pepperoni
                ]
            ),

            ft.Divider(),

            botao_pizza_temporaria,

            botao_calcular,

            resultado,

            mensagem
        ],
        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # TELA DE SELEÇÃO
    # --------------------------------------------------------------

    tela_selecao = ft.Column(
        controls=[
            titulo,
            subtitulo,
            pedido_edicao,

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

            cardapio
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # TELA DE REVISÃO
    # --------------------------------------------------------------

    resumo_pizza = ft.Text(
        "Nenhuma pizza selecionada",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    resumo_quantidade = ft.Text(
        "Quantidade: 0",
        size=20
    )

    def atualizar_resumo():

        if estado["pizza"] == "":
            resumo_pizza.value = "Nenhuma pizza selecionada"
            resumo_quantidade.value = "Quantidade: 0"

        else:
            resumo_pizza.value = (
                f"🍕 Pizza: {estado['pizza']}"
            )

            resumo_quantidade.value = (
                f"🔢 Quantidade: {estado['quantidade']}"
            )

    # --------------------------------------------------------------
    # BOTÃO VOLTAR
    # --------------------------------------------------------------

    def voltar_para_selecao(e):

        atualizar_estado()

        # Volta para a tela de seleção
        tela_principal.content = tela_selecao

        page.update()

    botao_voltar = ft.Button(
        content="← Voltar",
        on_click=voltar_para_selecao
    )

    # --------------------------------------------------------------
    # BOTÃO AVANÇAR
    # --------------------------------------------------------------

    def avancar(e):

        if estado["pizza"] == "":
            mensagem.value = (
                "Selecione uma pizza antes de avançar."
            )

            tela_principal.content = tela_selecao

            page.update()
            return

        atualizar_resumo()

        tela_principal.content = tela_revisao

        page.update()

    botao_avancar = ft.Button(
        content="Avançar →",
        on_click=avancar
    )

    # --------------------------------------------------------------
    # TELA DE REVISÃO
    # --------------------------------------------------------------

    tela_revisao = ft.Column(
        controls=[
            titulo,

            pedido_edicao,

            ft.Divider(),

            ft.Text(
                "📋 Revisão do pedido",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            resumo_pizza,

            resumo_quantidade,

            ft.Divider(),

            ft.Row(
                controls=[
                    botao_voltar,
                    botao_avancar
                ]
            )
        ],
        spacing=15
    )

    # --------------------------------------------------------------
    # BOTÕES DA TELA DE SELEÇÃO
    # --------------------------------------------------------------

    botoes_navegacao = ft.Row(
        controls=[
            botao_avancar
        ]
    )

    tela_selecao.controls.append(
        ft.Divider()
    )

    tela_selecao.controls.append(
        botoes_navegacao
    )

    # --------------------------------------------------------------
    # CONTAINER PRINCIPAL
    # --------------------------------------------------------------

    tela_principal = ft.Container(
        content=tela_selecao,
        padding=20,
        expand=True
    )

    page.add(tela_principal)

ft.run(main)