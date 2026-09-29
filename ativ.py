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
    carrinho = []

    # --------------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------------

    titulo = ft.Text(
        "PizzaDev",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text("Monte seu pedido com segurança")
    nome = ft.Text("Seu nome é Simba")
    slogan = ft.Text("Coma Pizza")
    instrucao = ft.Text("Selecione os sabores que deseja adicionar ao carrinho temporario e prossiga.")

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
                    size=16
                ),
                padding=8
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
        size=26,
        weight=ft.FontWeight.BOLD
    )

    # --------------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------------

    resultado = ft.Text(
        "Subtotal: R$ 0,00",
        size=22,
        weight=ft.FontWeight.BOLD
    )

    mensagem = ft.Text(
        "",
        size=15
    )

    # --------------------------------------------------------------
    # CARRINHO
    # --------------------------------------------------------------

    carrinho_titulo = ft.Text(
        "🛒 CARRINHO",
        size=26,
        weight=ft.FontWeight.BOLD
    )

    lista_carrinho = ft.ListView(
        spacing=8,
        height=280
    )

    subtotal_carrinho = ft.Text(
        "Subtotal: R$ 0,00",
        size=22,
        weight=ft.FontWeight.BOLD
    )

    # --------------------------------------------------------------
    # ESTADO
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
    # PREÇO
    # --------------------------------------------------------------

    def pegar_preco(tamanho):

        if tamanho == "Media":
            return 32

        elif tamanho == "Grande":
            return 42

        else:
            return None

    # --------------------------------------------------------------
    # CALCULAR TOTAL DO CARRINHO
    # --------------------------------------------------------------

    def calcular_total():

        total = 0

        for item in carrinho:

            total += (
                item["preco"] *
                item["quantidade"]
            )

        return total

    # --------------------------------------------------------------
    # ATUALIZAR CARRINHO
    # --------------------------------------------------------------

    def atualizar_carrinho():

        lista_carrinho.controls.clear()

        total = calcular_total()

        for item in carrinho:

            nome_pizza = item["nome"]
            tamanho = item["tamanho"]
            quantidade = item["quantidade"]
            preco = item["preco"]

            subtotal = preco * quantidade

            card = ft.Container(

                content=ft.Column(
                    controls=[

                        ft.Text(
                            f"🍕 {nome_pizza}",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            f"Tamanho: {tamanho}"
                        ),

                        ft.Text(
                            f"Quantidade: {quantidade}"
                        ),

                        ft.Text(
                            f"Preço unitário: "
                            f"R$ {preco:.2f}".replace(
                                ".", ","
                            )
                        ),

                        ft.Text(
                            f"Subtotal: "
                            f"R$ {subtotal:.2f}".replace(
                                ".", ","
                            ),
                            weight=ft.FontWeight.BOLD
                        )
                    ],
                    spacing=4
                ),

                padding=10,

                border=ft.Border.all(
                    1,
                    "orange"
                ),

                width=400
            )

            lista_carrinho.controls.append(card)

        subtotal_carrinho.value = (
            f"Subtotal: R$ {total:.2f}"
        ).replace(".", ",")

        resultado.value = (
            f"Subtotal: R$ {total:.2f}"
        ).replace(".", ",")

    # --------------------------------------------------------------
    # ADICIONAR AO CARRINHO
    # --------------------------------------------------------------

    def adicionar_ao_carrinho(
        nome_pizza,
        tamanho,
        quantidade
    ):

        preco = pegar_preco(tamanho)

        if preco is None:

            mensagem.value = (
                f"A pizza {nome_pizza} está no tamanho Pequena, "
                "mas o preço desse tamanho ainda não foi cadastrado."
            )

            page.update()

            return

        # ----------------------------------------------------------
        # PROCURA MESMA PIZZA + MESMO TAMANHO
        # ----------------------------------------------------------

        for item in carrinho:

            if (
                item["nome"] == nome_pizza
                and item["tamanho"] == tamanho
            ):

                nova_quantidade = (
                    item["quantidade"] + quantidade
                )

                # Máximo de 10
                if nova_quantidade > 10:

                    mensagem.value = (
                        f"Não é possível adicionar mais "
                        f"{nome_pizza} tamanho {tamanho}. "
                        f"A quantidade máxima é 10."
                    )

                    page.update()

                    return

                item["quantidade"] = nova_quantidade

                mensagem.value = (
                    f"{nome_pizza} adicionada ao carrinho! "
                    f"Quantidade total: {nova_quantidade}"
                )

                atualizar_carrinho()

                page.update()

                return

        # ----------------------------------------------------------
        # NOVA COMBINAÇÃO
        # ----------------------------------------------------------

        carrinho.append(
            {
                "nome": nome_pizza,
                "tamanho": tamanho,
                "quantidade": quantidade,
                "preco": preco
            }
        )

        mensagem.value = (
            f"{nome_pizza} adicionada ao carrinho! 🛒"
        )

        atualizar_carrinho()

        page.update()

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
                ],

                spacing=5
            )
        )

    # --------------------------------------------------------------
    # QUANTIDADE
    # --------------------------------------------------------------

    def campo_quantidade():

        return ft.TextField(
            label="Quantidade (1 a 10)",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            value="1"
        )

    # --------------------------------------------------------------
    # CRIAR PIZZA
    # --------------------------------------------------------------

    def criar_pizza(nome_pizza, ingredientes):

        tamanho = escolher_tamanho()

        quantidade = campo_quantidade()

        # ----------------------------------------------------------
        # SELECIONAR
        # ----------------------------------------------------------

        def selecionar(e):

            if tamanho.value is None:

                mensagem.value = (
                    f"Escolha o tamanho da pizza {nome_pizza}."
                )

                page.update()

                return

            try:

                qtd = int(quantidade.value)

            except ValueError:

                mensagem.value = (
                    "Digite uma quantidade válida."
                )

                page.update()

                return

            if qtd < 1 or qtd > 10:

                mensagem.value = (
                    "A quantidade deve estar entre 1 e 10."
                )

                page.update()

                return

            estado["pizza"] = nome_pizza
            estado["quantidade"] = qtd

            atualizar_estado()

            adicionar_ao_carrinho(
                nome_pizza,
                tamanho.value,
                qtd
            )

        botao_selecionar = ft.Button(
            content="Selecionar",
            on_click=selecionar
        )

        # ----------------------------------------------------------
        # CARD DA PIZZA
        # ----------------------------------------------------------

        pizza = ft.Container(

            content=ft.Column(
                controls=[

                    ft.Text(
                        f"🍕 {nome_pizza}",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        f"Ingredientes: {ingredientes}",
                        size=13
                    ),

                    ft.Text(
                        "Escolha o tamanho:",
                        size=14,
                        weight=ft.FontWeight.BOLD
                    ),

                    tamanho,

                    quantidade,

                    botao_selecionar
                ],
                spacing=6
            ),

            padding=10,

            border=ft.Border.all(
                1,
                "orange"
            ),

            width=400
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

        total = calcular_total()

        resultado.value = (
            f"Subtotal: R$ {total:.2f}"
        ).replace(".", ",")

        subtotal_carrinho.value = (
            f"Subtotal: R$ {total:.2f}"
        ).replace(".", ",")

        mensagem.value = (
            "Carrinho calculado com sucesso!"
        )

        page.update()

    botao_calcular = ft.Button(
        content="Calcular",
        on_click=calcular
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
                ],
                spacing=10
            ),

            ft.Row(
                controls=[
                    pizza_mussarela,
                    pizza_portuguesa
                ],
                spacing=10
            ),

            ft.Row(
                controls=[
                    pizza_chocolate,
                    pizza_pepperoni
                ],
                spacing=10
            ),

            ft.Divider(),

            # ------------------------------------------------------
            # CARRINHO
            # ------------------------------------------------------

            carrinho_titulo,

            lista_carrinho,

            subtotal_carrinho,

            botao_calcular,

            resultado,

            mensagem
        ],

        scroll=ft.ScrollMode.AUTO,

        spacing=8
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
                size=20,
                weight=ft.FontWeight.BOLD
            ),

            lista_pedidos,

            ft.Divider(),

            cardapio
        ],

        spacing=8,

        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # TELA DE REVISÃO
    # --------------------------------------------------------------

    resumo_titulo = ft.Text(
        "📋 Revisão da compra",
        size=28,
        weight=ft.FontWeight.BOLD
    )

    lista_revisao = ft.ListView(
        spacing=8,
        height=350
    )

    valor_final = ft.Text(
        "Valor final: R$ 0,00",
        size=26,
        weight=ft.FontWeight.BOLD
    )

    mensagem_final = ft.Text(
        "",
        size=18
    )

    # --------------------------------------------------------------
    # ATUALIZAR REVISÃO
    # --------------------------------------------------------------

    def atualizar_revisao():

        lista_revisao.controls.clear()

        total = calcular_total()

        # ----------------------------------------------------------
        # MOSTRA OS ITENS DO CARRINHO
        # ----------------------------------------------------------

        for item in carrinho:

            nome_pizza = item["nome"]
            tamanho = item["tamanho"]
            quantidade = item["quantidade"]
            preco = item["preco"]

            subtotal = (
                preco *
                quantidade
            )

            item_revisao = ft.Container(

                content=ft.Column(
                    controls=[

                        ft.Text(
                            f"🍕 {nome_pizza}",
                            size=19,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            f"Tamanho: {tamanho}"
                        ),

                        ft.Text(
                            f"Quantidade: {quantidade}"
                        ),

                        ft.Text(
                            f"Subtotal: "
                            f"R$ {subtotal:.2f}".replace(
                                ".", ","
                            ),
                            weight=ft.FontWeight.BOLD
                        )
                    ],

                    spacing=4
                ),

                padding=10,

                border=ft.Border.all(
                    1,
                    "orange"
                )
            )

            lista_revisao.controls.append(
                item_revisao
            )

        # ----------------------------------------------------------
        # VALOR FINAL
        # ----------------------------------------------------------

        valor_final.value = (
            f"Valor final: R$ {total:.2f}"
        ).replace(".", ",")

    # --------------------------------------------------------------
    # FINALIZAR COMPRA
    # --------------------------------------------------------------

    def finalizar_compra(e):

        if len(carrinho) == 0:

            mensagem_final.value = (
                "O carrinho está vazio."
            )

            page.update()

            return

        total = calcular_total()

        mensagem_final.value = (
            f"✅ Compra finalizada com sucesso! "
            f"Total: R$ {total:.2f}"
        ).replace(".", ",")

        page.update()

    botao_finalizar = ft.Button(
        content="Finalizar Compra",
        on_click=finalizar_compra
    )

    # --------------------------------------------------------------
    # BOTÃO VOLTAR
    # --------------------------------------------------------------

    def voltar_para_selecao(e):

        atualizar_estado()

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

        if len(carrinho) == 0:

            mensagem.value = (
                "Adicione pelo menos uma pizza ao carrinho."
            )

            tela_principal.content = tela_selecao

            page.update()

            return

        atualizar_revisao()

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

            resumo_titulo,

            ft.Text(
                "Confira os itens antes de finalizar:",
                size=16
            ),

            lista_revisao,

            ft.Divider(),

            valor_final,

            mensagem_final,

            ft.Row(
                controls=[

                    botao_voltar,

                    botao_finalizar
                ],

                spacing=10
            )
        ],

        spacing=10,

        scroll=ft.ScrollMode.AUTO
    )

    # --------------------------------------------------------------
    # BOTÕES DE NAVEGAÇÃO
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
        padding=15,
        expand=True
    )

    page.add(tela_principal)


ft.run(main)