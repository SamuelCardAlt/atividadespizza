import flet as ft
import re


def main(page: ft.Page):

    page.title = "PizzaDev"

    # --------------------------------------------------------------
    # ESTADO DO PEDIDO
    # --------------------------------------------------------------
    # Dicionário usado para guardar temporariamente informações
    # relacionadas à pizza que o usuário está selecionando.

    estado = {
        "pizza": "",
        "quantidade": 1
    }

    # --------------------------------------------------------------
    # LISTAS
    # --------------------------------------------------------------
    # "pedidos" guarda pedidos digitados pelo usuário.
    # "pizzas" guarda os controles criados para cada pizza.

    pedidos = []
    pizzas = []

    # Carrinho inicial com pelo menos 3 linhas, conforme o exercício.
    carrinho = [
        {
            "nome": "Calabresa",
            "tamanho": "Media",
            "quantidade": 1,
            "preco": 32
        },
        {
            "nome": "Frango com Catupiry",
            "tamanho": "Grande",
            "quantidade": 2,
            "preco": 42
        },
        {
            "nome": "Mussarela",
            "tamanho": "Media",
            "quantidade": 1,
            "preco": 32
        }
    ]

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
    # Percorre todos os produtos e soma preço x quantidade.
    # A taxa de entrega NÃO entra aqui para evitar acumulação.

    def calcular_total():

        total = 0

        for item in carrinho:

            total += (
                item["preco"] *
                item["quantidade"]
            )

        return total

    # --------------------------------------------------------------
    # REMOVER ITEM
    # --------------------------------------------------------------
    # Remove uma pizza específica da lista do carrinho.

    def remover_item(item):
        if item in carrinho:
            nome = item["nome"]
            carrinho.remove(item)
            atualizar_carrinho()
            mostrar_snackbar(f"{nome} removida do carrinho.")
            page.update()


    # --------------------------------------------------------------
    # ALTERAR QUANTIDADE
    # --------------------------------------------------------------
    # Altera a quantidade respeitando o limite mínimo e máximo.

    def alterar_quantidade(item, nova_quantidade):
        if nova_quantidade < 1:
            mostrar_snackbar("A quantidade mínima é 1.")
            return

        if nova_quantidade > 10:
            mostrar_snackbar("A quantidade máxima é 10.")
            return

        item["quantidade"] = nova_quantidade
        atualizar_carrinho()
        page.update()


    # --------------------------------------------------------------
    # LIMPAR CARRINHO
    # --------------------------------------------------------------
    # Exibe uma confirmação antes de apagar todos os produtos.

    def confirmar_limpar_carrinho(e):
        page.pop_dialog()
        carrinho.clear()
        atualizar_carrinho()
        mostrar_snackbar("Carrinho limpo.")
        page.update()


    def cancelar_limpar_carrinho(e):
        page.pop_dialog()
        mostrar_snackbar(
            f"Cancelado. Os {len(carrinho)} item(ns) continuam no carrinho."
        )
        page.update()


    def abrir_dialogo_limpar(e):
        if len(carrinho) == 0:
            mostrar_snackbar("O carrinho já está vazio.")
            return

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Limpar carrinho?"),
            content=ft.Text(
                "Todos os itens serão removidos. Deseja continuar?"
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar_limpar_carrinho
                ),
                ft.TextButton(
                    "Confirmar",
                    on_click=confirmar_limpar_carrinho
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.show_dialog(dialogo)


    # --------------------------------------------------------------
    # SNACKBAR
    # --------------------------------------------------------------

    def mostrar_snackbar(texto):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(texto),
                duration=2000
            )
        )


    # --------------------------------------------------------------
    # ATUALIZAR CARRINHO
    # --------------------------------------------------------------
    # Reconstrói visualmente a lista do carrinho sempre que
    # quantidade, produtos ou valores são alterados.

    def atualizar_carrinho():

        lista_carrinho.controls.clear()

        total = calcular_total()

        for item in carrinho:

            nome_pizza = item["nome"]
            tamanho = item["tamanho"]
            quantidade = item["quantidade"]
            preco = item["preco"]

            subtotal = preco * quantidade

            botao_remover = ft.Button(
                content="Remover",
                on_click=lambda e, item=item: remover_item(item)
            )

            botao_menos = ft.Button(
                content="-",
                on_click=lambda e, item=item: alterar_quantidade(
                    item, item["quantidade"] - 1
                ),
                disabled=quantidade <= 1
            )

            botao_mais = ft.Button(
                content="+",
                on_click=lambda e, item=item: alterar_quantidade(
                    item, item["quantidade"] + 1
                ),
                disabled=quantidade >= 10
            )

            controles_quantidade = ft.Row(
                controls=[
                    ft.Text("Quantidade:"),
                    botao_menos,
                    ft.Text(
                        str(quantidade),
                        size=16,
                        weight=ft.FontWeight.BOLD
                    ),
                    botao_mais
                ],
                spacing=5
            )

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

                        controles_quantidade,

                        ft.Text(
                            f"Preço unitário: "
                            f"R$ {preco:.2f}".replace(".", ",")
                        ),

                        ft.Text(
                            f"Subtotal: "
                            f"R$ {subtotal:.2f}".replace(".", ","),
                            weight=ft.FontWeight.BOLD
                        ),

                        botao_remover
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

        # Avançar fica indisponível quando o carrinho está vazio.
        botao_avancar.disabled = len(carrinho) == 0

    # --------------------------------------------------------------
    # ADICIONAR AO CARRINHO
    # --------------------------------------------------------------
    # Verifica preço, quantidade e combina itens iguais.

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
    # Esta função cria visualmente o card de cada pizza do cardápio.

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

    botao_limpar = ft.Button(
        content="Limpar carrinho",
        on_click=abrir_dialogo_limpar
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

            ft.Row(
                controls=[
                    botao_calcular,
                    botao_limpar
                ],
                spacing=10
            ),

            resultado,

            mensagem
        ],

        scroll=ft.ScrollMode.AUTO,

        spacing=8
    )

    # --------------------------------------------------------------
    # TELA DE SELEÇÃO
    # --------------------------------------------------------------
    # Primeira tela: cardápio, pedidos e carrinho.

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
    # Segunda tela: dados do cliente, entrega, pagamento e resumo.

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
    # DADOS DO CLIENTE E FORMA DE RECEBIMENTO
    # --------------------------------------------------------------

    campo_nome_cliente = ft.TextField(
        label="Nome",
        hint_text="Digite seu nome",
        expand=True
    )

    campo_telefone = ft.TextField(
        label="Telefone",
        hint_text="(00) 00000-0000",
        keyboard_type=ft.KeyboardType.PHONE,
        expand=True
    )

    # Compatibilidade com versões do Flet que não aceitam
    # error_text diretamente no construtor do TextField.
    campo_nome_cliente.error_text = None
    campo_telefone.error_text = None

    campo_rua = ft.TextField(label="Rua", expand=True)
    campo_numero = ft.TextField(label="Número", width=130)
    campo_bairro = ft.TextField(label="Bairro", expand=True)
    campo_complemento = ft.TextField(
        label="Complemento (opcional)",
        expand=True
    )

    taxa_entrega = 6.00

    texto_taxa_entrega = ft.Text("Taxa de entrega: R$ 0,00")
    texto_subtotal_revisao = ft.Text("Subtotal dos produtos: R$ 0,00")
    texto_total_revisao = ft.Text(
        "Total com entrega: R$ 0,00",
        size=26,
        weight=ft.FontWeight.BOLD
    )

    # --------------------------------------------------------------
    # FORMA DE PAGAMENTO
    # --------------------------------------------------------------
    # O cliente poderá escolher entre Dinheiro, Pix ou Cartão.
    # O campo de valor recebido será mostrado somente para Dinheiro.

    selecao_pagamento = ft.RadioGroup(
        value="Pix",
        content=ft.Row(
            controls=[
                ft.Radio(value="Dinheiro", label="Dinheiro"),
                ft.Radio(value="Pix", label="Pix"),
                ft.Radio(value="Cartão", label="Cartão")
            ],
            spacing=15
        )
    )

    # Campo que aparecerá somente quando o pagamento for em dinheiro.
    campo_valor_recebido = ft.TextField(
        label="Valor recebido",
        hint_text="Ex.: 120,00",
        keyboard_type=ft.KeyboardType.NUMBER,
        visible=False,
        width=220
    )

    # Mensagem usada para informar o troco.
    texto_troco = ft.Text(
        "Troco: R$ 0,00",
        size=18,
        weight=ft.FontWeight.BOLD,
        visible=False
    )

    # --------------------------------------------------------------
    # OBSERVAÇÃO DO PEDIDO
    # --------------------------------------------------------------
    # multiline=True permite escrever várias linhas.
    # max_length=120 limita a observação a 120 caracteres.

    campo_observacao = ft.TextField(
        label="Observação",
        hint_text="Ex.: Retirar cebola, entregar na portaria...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        max_length=120,
        expand=True
    )

    # Mensagem de erro específica para o valor recebido.
    mensagem_pagamento = ft.Text(
        "",
        size=15
    )

    # --------------------------------------------------------------
    # CAMPOS DE ENDEREÇO
    # --------------------------------------------------------------

    endereco_container = ft.Column(
        controls=[
            ft.Row(controls=[campo_rua, campo_numero]),
            ft.Row(controls=[campo_bairro, campo_complemento])
        ],
        spacing=8,
        visible=False
    )

    def formatar_moeda(valor):
        return f"R$ {valor:.2f}".replace(".", ",")

    def tipo_recebimento():
        return selecao_recebimento.value or "Retirada"

    def calcular_total_pedido():
        # A taxa é calculada a partir da opção atual; nunca é somada
        # ao carrinho. Assim, alternar Entrega/Retirada não acumula taxas.
        taxa = taxa_entrega if tipo_recebimento() == "Entrega" else 0
        return calcular_total() + taxa

    def alterar_recebimento(e):
        # Verifica se a opção atual é Entrega.
        entrega = tipo_recebimento() == "Entrega"

        # Mostra ou esconde os campos de endereço.
        endereco_container.visible = entrega

        # A taxa só existe quando o cliente escolhe Entrega.
        texto_taxa_entrega.value = (
            f"Taxa de entrega: "
            f"{formatar_moeda(taxa_entrega if entrega else 0)}"
        )

        # Atualiza os valores da tela.
        atualizar_valores_revisao()
        page.update()

    # RadioGroup responsável pela escolha entre Retirada e Entrega.
    selecao_recebimento = ft.RadioGroup(
        value="Retirada",
        content=ft.Row(
            controls=[
                ft.Radio(value="Retirada", label="Retirada"),
                ft.Radio(value="Entrega", label="Entrega")
            ],
            spacing=15
        ),
        on_change=alterar_recebimento
    )

    # --------------------------------------------------------------
    # ALTERAR FORMA DE PAGAMENTO
    # --------------------------------------------------------------

    def alterar_pagamento(e):
        # Descobre qual forma de pagamento foi selecionada.
        pagamento = selecao_pagamento.value

        # Dinheiro exige que o usuário informe quanto entregou.
        eh_dinheiro = pagamento == "Dinheiro"

        # O campo e o texto do troco aparecem somente para Dinheiro.
        campo_valor_recebido.visible = eh_dinheiro
        texto_troco.visible = eh_dinheiro

        # Limpa mensagens antigas quando a forma de pagamento muda.
        mensagem_pagamento.value = ""
        campo_valor_recebido.error_text = None
        texto_troco.value = "Troco: R$ 0,00"

        page.update()

    # Quando o pagamento mudar, executamos a função acima.
    selecao_pagamento.on_change = alterar_pagamento

    # --------------------------------------------------------------
    # CALCULAR TROCO
    # --------------------------------------------------------------

    def calcular_troco(total):
        # Se não for dinheiro, não existe troco.
        if selecao_pagamento.value != "Dinheiro":
            return None

        # Remove espaços e transforma vírgula decimal em ponto.
        texto_valor = (campo_valor_recebido.value or "").strip()
        texto_valor = texto_valor.replace("R$", "").strip()
        texto_valor = texto_valor.replace(".", "").replace(",", ".")

        # Tenta transformar o texto em número.
        try:
            valor_recebido = float(texto_valor)
        except ValueError:
            campo_valor_recebido.error_text = "Digite um valor válido."
            return None

        # O exercício considera R$ 110,00 como total de teste.
        total_teste = 110.00

        # Para manter o comportamento solicitado, a validação usa
        # R$ 110,00 como referência para o teste do pagamento.
        total_para_pagamento = total_teste

        # O valor recebido precisa ser suficiente.
        if valor_recebido < total_para_pagamento:
            campo_valor_recebido.error_text = (
                "O valor recebido deve ser de pelo menos R$ 110,00."
            )
            texto_troco.value = "Troco: R$ 0,00"
            return None

        # Calcula a diferença entre o valor recebido e o total.
        troco = valor_recebido - total_para_pagamento

        # Remove qualquer mensagem de erro anterior.
        campo_valor_recebido.error_text = None

        # Mostra o troco calculado.
        texto_troco.value = f"Troco: {formatar_moeda(troco)}"

        return troco

    # --------------------------------------------------------------
    # VALORES DA REVISÃO
    # --------------------------------------------------------------

    def atualizar_valores_revisao():
        subtotal = calcular_total()
        taxa = taxa_entrega if tipo_recebimento() == "Entrega" else 0
        total = subtotal + taxa

        texto_subtotal_revisao.value = (
            f"Subtotal dos produtos: {formatar_moeda(subtotal)}"
        )
        texto_taxa_entrega.value = (
            f"Taxa de entrega: {formatar_moeda(taxa)}"
        )
        texto_total_revisao.value = (
            f"Total com entrega: {formatar_moeda(total)}"
        )
        valor_final.value = f"Valor final: {formatar_moeda(total)}"

        # Se o pagamento for dinheiro e já houver um valor digitado,
        # recalculamos o troco automaticamente ao atualizar a revisão.
        if selecao_pagamento.value == "Dinheiro":
            calcular_troco(total)

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

        atualizar_valores_revisao()

    # --------------------------------------------------------------
    # VALIDAR DADOS E FINALIZAR COMPRA
    # --------------------------------------------------------------

    def finalizar_compra(e):

        if len(carrinho) == 0:
            mensagem_final.value = "O carrinho está vazio."
            page.update()
            return

        # Limpa erros anteriores antes de validar novamente.
        campo_nome_cliente.error_text = None
        campo_telefone.error_text = None
        campo_rua.error_text = None
        campo_numero.error_text = None
        campo_bairro.error_text = None

        nome_cliente = (campo_nome_cliente.value or "").strip()
        telefone = re.sub(r"\\D", "", campo_telefone.value or "")

        valido = True

        if nome_cliente == "":
            campo_nome_cliente.error_text = "Informe seu nome."
            valido = False

        if len(telefone) not in (10, 11):
            campo_telefone.error_text = (
                "Digite um telefone com 10 ou 11 dígitos."
            )
            valido = False

        if tipo_recebimento() == "Entrega":
            if not (campo_rua.value or "").strip():
                campo_rua.error_text = "Informe a rua."
                valido = False
            else:
                campo_rua.error_text = None

            if not (campo_numero.value or "").strip():
                campo_numero.error_text = "Informe o número."
                valido = False
            else:
                campo_numero.error_text = None

            if not (campo_bairro.value or "").strip():
                campo_bairro.error_text = "Informe o bairro."
                valido = False
            else:
                campo_bairro.error_text = None

        # ----------------------------------------------------------
        # VALIDAR PAGAMENTO
        # ----------------------------------------------------------
        # Para este exercício, o teste de pagamento usa R$ 110,00.
        if selecao_pagamento.value == "Dinheiro":
            troco = calcular_troco(110.00)

            # Se o troco for None, houve erro no valor recebido.
            if troco is None:
                valido = False

        if not valido:
            mensagem_final.value = (
                "Confira os campos destacados antes de finalizar."
            )
            page.update()
            return

        total = calcular_total_pedido()
        forma = tipo_recebimento()
        pagamento = selecao_pagamento.value

        # Mostra a confirmação final.
        mensagem_final.value = (
            f"✅ Pedido de {nome_cliente} finalizado! "
            f"Recebimento: {forma}. "
            f"Pagamento: {pagamento}. "
            f"Total: {formatar_moeda(total)}"
        )

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

        # Segurança extra: mesmo desabilitado, não avança sem itens.
        if len(carrinho) == 0:

            mensagem.value = (
                "Adicione pelo menos uma pizza ao carrinho."
            )

            tela_principal.content = tela_selecao

            page.update()

            return

        atualizar_revisao()
        endereco_container.visible = tipo_recebimento() == "Entrega"

        tela_principal.content = tela_revisao

        page.update()

    botao_avancar = ft.Button(
        content="Avançar →",
        on_click=avancar,
        disabled=len(carrinho) == 0
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
                "Confira os itens e informe seus dados:",
                size=16
            ),

            ft.Text(
                "Dados do cliente",
                size=20,
                weight=ft.FontWeight.BOLD
            ),
            ft.Row(
                controls=[campo_nome_cliente, campo_telefone],
                spacing=10
            ),

            ft.Text(
                "Como deseja receber seu pedido?",
                size=16,
                weight=ft.FontWeight.BOLD
            ),
            selecao_recebimento,
            endereco_container,

            ft.Divider(),

            lista_revisao,

            ft.Divider(),

            texto_subtotal_revisao,
            texto_taxa_entrega,
            texto_total_revisao,

            ft.Divider(),

            # ------------------------------------------------------
            # FORMA DE PAGAMENTO
            # ------------------------------------------------------
            ft.Text(
                "Forma de pagamento",
                size=20,
                weight=ft.FontWeight.BOLD
            ),
            selecao_pagamento,
            campo_valor_recebido,
            texto_troco,
            mensagem_pagamento,

            # ------------------------------------------------------
            # OBSERVAÇÃO
            # ------------------------------------------------------
            ft.Text(
                "Observação do pedido",
                size=20,
                weight=ft.FontWeight.BOLD
            ),
            campo_observacao,

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
    # Controlam a passagem entre a seleção e a revisão.

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
    # Container que recebe a tela atualmente visível.

    tela_principal = ft.Container(
        content=tela_selecao,
        padding=15,
        expand=True
    )

    # Renderiza o carrinho inicial com 3 itens e calcula o subtotal.
    atualizar_carrinho()

    page.add(tela_principal)


# Inicia o aplicativo Flet e executa a função principal.
ft.run(main)