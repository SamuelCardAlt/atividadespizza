import flet as ft


# FUNÇÃO PRINCIPAL: inicia e configura o aplicativo PizzaDev.
# O parâmetro page representa a janela e os elementos da interface.
def main(page: ft.Page):

    # CONFIGURAÇÕES DA JANELA
    page.title = "PizzaDev"  # Define o título da janela.
    page.window.width = 400  # Define a largura inicial.
    page.window.height = 760  # Define a altura inicial.
    page.padding = 15  # Define o espaçamento interno da página.
    page.bgcolor = "#121212"  # Define o fundo preto.
    page.theme_mode = ft.ThemeMode.DARK  # Ativa o tema escuro.

    # CONSTANTES DE CORES: facilitam a personalização visual.
    PRETO = "#121212"
    LARANJA = "#FF8C00"
    CINZA = "#242424"
    BRANCO = "#FFFFFF"
    VERDE = "#4CAF50"

    # CARDÁPIO: dicionário que armazena sabores, ingredientes e preços.
    # Cada sabor possui outro dicionário com os tamanhos e seus valores.
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

    # ESTADOS DO APLICATIVO: guardam os pedidos e as escolhas do cliente.
    pedidos = []  # Lista que armazena as pizzas adicionadas ao carrinho.
    entrega_selecionada = "Entrega em casa"  # Opção inicial de recebimento.
    pagamento_selecionado = "Pix"  # Opção inicial de pagamento.

    # CAMPO DE SABOR: cria uma lista suspensa com os sabores disponíveis.
    # As opções são geradas automaticamente a partir das chaves do cardápio.
    campo_sabor = ft.Dropdown(
        label="Escolha o sabor",
        options=[ft.DropdownOption(key=sabor, text=sabor) for sabor in cardapio],
        value="Calabresa",
        expand=True,
        border_color=LARANJA,
    )

    # CAMPO DE TAMANHO: permite escolher entre pequena, média e grande.
    # O valor selecionado será utilizado para consultar o preço da pizza.
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

    # CAMPO DE QUANTIDADE: permite escolher de 1 a 10 unidades.
    # O valor é armazenado como texto e convertido para inteiro ao adicionar.
    campo_quantidade = ft.Dropdown(
        label="Quantidade",
        options=[ft.DropdownOption(key=str(n), text=str(n)) for n in range(1, 11)],
        value="1",
        width=130,
        border_color=LARANJA,
    )

    # COMPONENTES REUTILIZÁVEIS: exibem mensagens e os itens do carrinho.
    mensagem = ft.Text(value="", color=VERDE, size=14)
    lista_pedidos = ft.Column(spacing=8)

    # COLUNA PRINCIPAL: recebe os conteúdos das telas e permite rolagem.
    conteudo = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=12, expand=True)

    # FUNÇÃO DE FORMATAÇÃO: transforma números em valores monetários brasileiros.
    # Exemplo: 32.00 passa a ser exibido como R$ 32,00.
    def preco(valor):
        return f"R$ {valor:.2f}".replace(".", ",")

    # FUNÇÃO DE TÍTULO: cria textos padronizados para as seções do aplicativo.
    # Recebe o texto desejado e devolve um componente com destaque em laranja.
    def titulo(texto):
        return ft.Text(texto, size=22, weight=ft.FontWeight.BOLD, color=LARANJA)

    # FUNÇÃO DE BOTÃO: cria botões padronizados com texto e ícone opcional.
    # Recebe o texto, a função executada no clique e, opcionalmente, um ícone.
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

    # FUNÇÃO DE MENSAGEM: atualiza o texto e a cor da mensagem na tela.
    # O parâmetro cor possui verde como padrão, mas pode receber outra cor.
    def mostrar_mensagem(texto, cor=VERDE):
        mensagem.value = texto
        mensagem.color = cor
        page.update()  # Atualiza a interface para exibir a mensagem.

    # FUNÇÃO DE DESENHO DO CARRINHO: atualiza visualmente os pedidos.
    # Limpa os componentes anteriores e recria a lista com os dados atuais.
    def desenhar_pedidos():
        lista_pedidos.controls.clear()

        # Se a lista estiver vazia, informa que não existem itens no carrinho.
        if not pedidos:
            lista_pedidos.controls.append(
                ft.Text("Seu carrinho está vazio.", color="#AAAAAA")
            )

        # Caso contrário, percorre a lista e cria um cartão para cada pedido.
        else:
            for indice, pedido in enumerate(pedidos):

                # Calcula o subtotal multiplicando o preço pela quantidade.
                subtotal = pedido["preco"] * pedido["quantidade"]

                # Cria o cartão visual com informações e botão de exclusão.
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

                                # O lambda guarda o índice correto para excluir o item clicado.
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

    # FUNÇÃO DE ABERTURA DO CARDÁPIO: monta a tela inicial do aplicativo.
    # Também apresenta as pizzas, os campos de seleção e o carrinho.
    def abrir_cardapio(e=None):

        # Remove os componentes da tela anterior antes de montar a nova.
        conteudo.controls.clear()

        # Adiciona o cabeçalho, a descrição e o título do cardápio.
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

        # Percorre o dicionário e cria um cartão para cada sabor disponível.
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

        # Adiciona os campos de seleção, o botão de adicionar e a lista de pedidos.
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

        # Atualiza o carrinho e coloca a tela inicial na janela.
        desenhar_pedidos()
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    # FUNÇÃO DE ADIÇÃO: registra uma nova pizza na lista de pedidos.
    # Lê as seleções, valida os campos e calcula o preço unitário pelo cardápio.
    def adicionar_pedido(e):

        # Obtém os valores escolhidos pelo cliente nos campos.
        sabor = campo_sabor.value
        tamanho = campo_tamanho.value
        quantidade = int(campo_quantidade.value or "1")

        # Impede a adição se o sabor ou o tamanho não estiver selecionado.
        if not sabor or not tamanho:
            mostrar_mensagem("Selecione o sabor e o tamanho.", "#FF5252")
            return

        # Adiciona um dicionário com os dados da pizza à lista do carrinho.
        pedidos.append(
            {
                "sabor": sabor,
                "tamanho": tamanho,
                "quantidade": quantidade,
                "preco": cardapio[sabor]["precos"][tamanho],
            }
        )

        # Redesenha o carrinho e informa que o item foi adicionado.
        desenhar_pedidos()
        mostrar_mensagem("Pizza adicionada ao carrinho!")
        page.update()

    # FUNÇÃO DE EXCLUSÃO: remove um item do carrinho usando seu índice.
    # Depois da remoção, atualiza a lista e mostra uma mensagem ao cliente.
    def excluir_pedido(indice):
        if 0 <= indice < len(pedidos):
            pedidos.pop(indice)

        desenhar_pedidos()
        mostrar_mensagem("Pedido removido do carrinho.")
        page.update()

    # FUNÇÃO DE ENTREGA: guarda a forma de recebimento escolhida.
    # O nonlocal permite alterar a variável criada dentro de main().
    def alterar_entrega(e):
        nonlocal entrega_selecionada
        entrega_selecionada = e.control.value

    # FUNÇÃO DE PAGAMENTO: guarda o método de pagamento selecionado.
    # A escolha é mantida na variável para ser usada na finalização.
    def alterar_pagamento(e):
        nonlocal pagamento_selecionado
        pagamento_selecionado = e.control.value

    # FUNÇÃO DE REVISÃO: apresenta os itens e os valores antes da conclusão.
    # Impede o avanço quando o carrinho está vazio e calcula o total da compra.
    def abrir_revisao(e=None):

        # Verifica se existe pelo menos uma pizza no carrinho.
        if not pedidos:
            mostrar_mensagem("Adicione pelo menos uma pizza antes de continuar.", "#FFB74D")
            return

        # Limpa a tela anterior e calcula os totais da compra.
        conteudo.controls.clear()
        total = sum(p["preco"] * p["quantidade"] for p in pedidos)
        quantidade_total = sum(p["quantidade"] for p in pedidos)

        # Monta o cabeçalho da revisão do pedido.
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

        # Percorre o carrinho e mostra o sabor, o tamanho e o subtotal de cada item.
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

        # Adiciona o total, as opções de recebimento e as formas de pagamento.
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

                # Dropdown para escolher entrega em casa ou retirada no local.
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

                # Dropdown para selecionar Pix ou cartão.
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

                # Informa que o aplicativo não realiza transações financeiras reais.
                ft.Text(
                    "Demonstração: nenhum pagamento real será processado.",
                    color="#BBBBBB",
                    size=12,
                ),
                mensagem,

                # Botão para concluir a compra ou retornar ao cardápio.
                botao("Concluir pedido", concluir_pedido, ft.Icons.CHECK_CIRCLE),
                ft.Button(
                    content="Voltar ao cardápio",
                    on_click=abrir_cardapio,
                    style=ft.ButtonStyle(color=LARANJA),
                ),
            ]
        )

        # Exibe a tela de revisão na janela do aplicativo.
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    # FUNÇÃO DE FINALIZAÇÃO: registra a conclusão e mostra o resumo da compra.
    # Calcula os totais, guarda as escolhas e limpa o carrinho após a conclusão.
    def concluir_pedido(e):

        # Se o carrinho estiver vazio, retorna ao início e informa o problema.
        if not pedidos:
            abrir_cardapio()
            mostrar_mensagem("Seu carrinho está vazio.", "#FF5252")
            return

        # Calcula o valor total e a quantidade de pizzas antes de limpar a lista.
        total = sum(p["preco"] * p["quantidade"] for p in pedidos)
        quantidade_total = sum(p["quantidade"] for p in pedidos)

        # Guarda as escolhas para exibi-las no resumo final.
        entrega = entrega_selecionada
        pagamento = pagamento_selecionado

        # Limpa os pedidos do carrinho após a conclusão da compra.
        pedidos.clear()

        # Monta a tela de confirmação e agradecimento.
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

                # Exibe um resumo com quantidade, recebimento, pagamento e total.
                ft.Divider(color=LARANJA),
                titulo("Resumo final"),
                ft.Text(f"Quantidade de pizzas: {quantidade_total}"),
                ft.Text(f"Recebimento: {entrega}"),
                ft.Text(f"Pagamento: {pagamento}"),
                ft.Text(f"Total: {preco(total)}", size=22, weight=ft.FontWeight.BOLD, color=LARANJA),
                ft.Text("Status: pedido registrado no aplicativo.", color=VERDE),

                # Esclarece que o pagamento e a entrega são confirmados externamente.
                ft.Text(
                    "Pagamento e entrega precisam ser confirmados fora do aplicativo.",
                    color="#BBBBBB",
                    size=12,
                ),

                # Permite voltar à tela inicial para iniciar um novo pedido.
                botao("Voltar ao início", abrir_cardapio, ft.Icons.HOME),
            ]
        )

        # Atualiza a janela para apresentar a confirmação da compra.
        page.controls.clear()
        page.add(ft.SafeArea(content=conteudo, expand=True))
        page.update()

    # INICIALIZAÇÃO: abre o cardápio assim que o aplicativo é executado.
    abrir_cardapio()


# PONTO DE ENTRADA: executa main() quando este arquivo é iniciado diretamente.
# O ft.run cria e inicia a aplicação usando a função principal.
if __name__ == "__main__":
    ft.run(main)