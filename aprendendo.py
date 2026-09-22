import flet as ft


def main(page: ft.Page):

    # =========================================================
    # CONFIGURAÇÕES DA PÁGINA
    # =========================================================

    page.title = "PizzaDev"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = "#000000"

    # =========================================================
    # CORES
    # =========================================================

    LARANJA = "#FF8C00"
    LARANJA_CLARO = "#FFA500"
    PRETO = "#000000"
    CINZA = "#1A1A1A"
    BRANCO = "#FFFFFF"
    VERMELHO = "#FF3333"
    VERDE = "#00CC66"

    # =========================================================
    # LISTA DE PEDIDOS
    # =========================================================

    pedidos = []

    # Variável que informa se estamos editando um pedido
    pedido_editando = None

    # =========================================================
    # TÍTULO
    # =========================================================

    titulo = ft.Text(
        "PizzaDev",
        size=34,
        weight=ft.FontWeight.BOLD,
        color=LARANJA
    )

    subtitulo = ft.Text(
        "Monte seu pedido com segurança",
        size=16,
        color=BRANCO
    )

    # =========================================================
    # CAMPOS
    # =========================================================

    campo_nome = ft.TextField(
    label="Nome do cliente",
    width=450,
    color=BRANCO,
    label_style=ft.TextStyle(
        color=LARANJA
    ),
    border=ft.OutlineInputBorder(
        border_radius=8,
        side=ft.BorderSide(
            width=2,
            color=LARANJA
        )
    ),
    cursor_color=LARANJA,
    filled=True,
    fill_color="#1A1A1A"
)

    campo_pizza = ft.TextField(
    label="Sabor da pizza",
    width=450,
    color=BRANCO,
    label_style=ft.TextStyle(color=LARANJA),
    border=ft.OutlineInputBorder(
        border_radius=8,
        side=ft.BorderSide(
            width=2,
            color=LARANJA
        )
    ),
    cursor_color=LARANJA,
    filled=True,
    fill_color=CINZA
)

    campo_telefone = ft.TextField(
    label="Telefone",
    width=450,
    color=BRANCO,
    label_style=ft.TextStyle(color=LARANJA),
    border=ft.OutlineInputBorder(
        border_radius=8,
        side=ft.BorderSide(
            width=2,
            color=LARANJA
        )
    ),
    cursor_color=LARANJA,
    filled=True,
    fill_color=CINZA
)

    campo_busca = ft.TextField(
    label="Digite o nome do cliente",
    width=450,
    color=BRANCO,
    label_style=ft.TextStyle(color=LARANJA),
    border=ft.OutlineInputBorder(
        border_radius=8,
        side=ft.BorderSide(
            width=2,
            color=LARANJA
        )
    ),
    cursor_color=LARANJA,
    filled=True,
    fill_color=CINZA
)

    # =========================================================
    # ÁREA DE PEDIDOS
    # =========================================================

    lista_pedidos = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    mensagem = ft.Text(
        "",
        size=16
    )

    # =========================================================
    # FUNÇÃO PARA MOSTRAR MENSAGEM
    # =========================================================

    def mostrar_mensagem(texto, cor):

        mensagem.value = texto
        mensagem.color = cor

        page.update()

    # =========================================================
    # LIMPAR CAMPOS
    # =========================================================

    def limpar_campos():

        campo_nome.value = ""
        campo_pizza.value = ""
        campo_telefone.value = ""

        page.update()

    # =========================================================
    # NORMALIZAR TEXTO
    # =========================================================

    def normalizar(texto):

        return texto.strip().lower()

    # =========================================================
    # CANCELAR EDIÇÃO
    # =========================================================

    def cancelar_edicao(e=None):

        nonlocal pedido_editando

        pedido_editando = None

        limpar_campos()

        mostrar_mensagem(
            "Edição cancelada.",
            BRANCO
        )

        tela_cadastro()

    # =========================================================
    # CADASTRAR PEDIDO
    # =========================================================

    def cadastrar_pedido(e):

        nome = campo_nome.value.strip()
        pizza = campo_pizza.value.strip()
        telefone = campo_telefone.value.strip()

        # -----------------------------------------
        # VERIFICAÇÕES
        # -----------------------------------------

        if nome == "":
            mostrar_mensagem(
                "Digite o nome do cliente.",
                VERMELHO
            )
            return

        if pizza == "":
            mostrar_mensagem(
                "Digite o sabor da pizza.",
                VERMELHO
            )
            return

        if telefone == "":
            mostrar_mensagem(
                "Digite o telefone.",
                VERMELHO
            )
            return

        # -----------------------------------------
        # VERIFICAR CLIENTE DUPLICADO
        # -----------------------------------------

        for pedido in pedidos:

            if normalizar(pedido["nome"]) == normalizar(nome):

                mostrar_mensagem(
                    "Já existe um pedido para esse cliente.",
                    VERMELHO
                )

                return

        # -----------------------------------------
        # CRIAR PEDIDO
        # -----------------------------------------

        pedido = {
            "nome": nome,
            "pizza": pizza,
            "telefone": telefone
        }

        pedidos.append(pedido)

        limpar_campos()

        mostrar_mensagem(
            "Pedido cadastrado com sucesso!",
            VERDE
        )

        listar_pedidos()

    # =========================================================
    # SALVAR EDIÇÃO
    # =========================================================

    def salvar_edicao(e):

        nonlocal pedido_editando

        if pedido_editando is None:
            return

        nome = campo_nome.value.strip()
        pizza = campo_pizza.value.strip()
        telefone = campo_telefone.value.strip()

        # -----------------------------------------
        # VERIFICAÇÕES
        # -----------------------------------------

        if nome == "":
            mostrar_mensagem(
                "Digite o nome do cliente.",
                VERMELHO
            )
            return

        if pizza == "":
            mostrar_mensagem(
                "Digite o sabor da pizza.",
                VERMELHO
            )
            return

        if telefone == "":
            mostrar_mensagem(
                "Digite o telefone.",
                VERMELHO
            )
            return

        # -----------------------------------------
        # ATUALIZAR PEDIDO
        # -----------------------------------------

        pedido_editando["nome"] = nome
        pedido_editando["pizza"] = pizza
        pedido_editando["telefone"] = telefone

        pedido_editando = None

        limpar_campos()

        mostrar_mensagem(
            "Pedido atualizado com sucesso!",
            VERDE
        )

        tela_lista()

    # =========================================================
    # EDITAR PEDIDO
    # =========================================================

    def editar_pedido(pedido):

        nonlocal pedido_editando

        pedido_editando = pedido

        campo_nome.value = pedido["nome"]
        campo_pizza.value = pedido["pizza"]
        campo_telefone.value = pedido["telefone"]

        campo_busca.visible = False

        conteudo.controls.clear()

        conteudo.controls.extend([

            ft.Text(
                "Editar Pedido",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=LARANJA
            ),

            campo_nome,
            campo_pizza,
            campo_telefone,

            ft.Row([

                ft.Button(
                    content="Salvar Alterações",
                    icon=ft.Icons.SAVE,
                    on_click=salvar_edicao
                ),

                ft.Button(
                    content="Cancelar",
                    icon=ft.Icons.CANCEL,
                    on_click=cancelar_edicao
                )

            ]),

            mensagem
        ])

        page.update()

    # =========================================================
    # EXCLUIR PEDIDO
    # =========================================================

    def excluir_pedido(pedido):

        if pedido in pedidos:

            pedidos.remove(pedido)

            mostrar_mensagem(
                "Pedido excluído com sucesso!",
                VERDE
            )

            listar_pedidos()

    # =========================================================
    # CRIAR CARD DO PEDIDO
    # =========================================================

    def criar_card(pedido, numero):

        return ft.Container(

            bgcolor=CINZA,

            border=ft.Border.all(
                1,
                LARANJA
            ),

            border_radius=10,

            padding=15,

            content=ft.Column([

                ft.Text(
                    f"Pedido {numero}",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=LARANJA
                ),

                ft.Text(
                    f"Cliente: {pedido['nome']}",
                    color=BRANCO
                ),

                ft.Text(
                    f"Pizza: {pedido['pizza']}",
                    color=BRANCO
                ),

                ft.Text(
                    f"Telefone: {pedido['telefone']}",
                    color=BRANCO
                ),

                ft.Row([

                    ft.Button(
                        content="Editar",
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, p=pedido: editar_pedido(p)
                    ),

                    ft.Button(
                        content="Excluir",
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, p=pedido: excluir_pedido(p)
                    )

                ])

            ])
        )

    # =========================================================
    # LISTAR PEDIDOS
    # =========================================================

    def listar_pedidos(e=None):

        lista_pedidos.controls.clear()

        if len(pedidos) == 0:

            lista_pedidos.controls.append(

                ft.Text(
                    "Nenhum pedido cadastrado.",
                    size=18,
                    color=BRANCO
                )

            )

        else:

            for i, pedido in enumerate(pedidos):

                lista_pedidos.controls.append(
                    criar_card(
                        pedido,
                        i + 1
                    )
                )

        page.update()

    # =========================================================
    # BUSCAR PEDIDO
    # =========================================================

    def buscar_pedido(e):

        nome_busca = normalizar(
            campo_busca.value
        )

        lista_pedidos.controls.clear()

        if nome_busca == "":

            mostrar_mensagem(
                "Digite um nome para buscar.",
                VERMELHO
            )

            return

        encontrados = []

        # -----------------------------------------
        # BUSCA IGNORANDO MAIÚSCULAS
        # -----------------------------------------

        for pedido in pedidos:

            if nome_busca in normalizar(
                pedido["nome"]
            ):

                encontrados.append(pedido)

        # -----------------------------------------
        # RESULTADOS
        # -----------------------------------------

        if len(encontrados) == 0:

            lista_pedidos.controls.append(

                ft.Text(
                    "Nenhum pedido encontrado.",
                    size=18,
                    color=VERMELHO
                )

            )

        else:

            mostrar_mensagem(
                f"{len(encontrados)} pedido(s) encontrado(s).",
                VERDE
            )

            for i, pedido in enumerate(encontrados):

                lista_pedidos.controls.append(
                    criar_card(
                        pedido,
                        i + 1
                    )
                )

        page.update()

    # =========================================================
    # TELA DE CADASTRO
    # =========================================================

    def tela_cadastro(e=None):

        campo_busca.visible = False

        lista_pedidos.controls.clear()

        mensagem.value = ""

        conteudo.controls.clear()

        conteudo.controls.extend([

            ft.Text(
                "Novo Pedido",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=LARANJA
            ),

            campo_nome,

            campo_pizza,

            campo_telefone,

            ft.Button(
                content="Cadastrar Pedido",
                icon=ft.Icons.ADD,
                on_click=cadastrar_pedido
            ),

            mensagem

        ])

        page.update()

    # =========================================================
    # TELA DE LISTA
    # =========================================================

    def tela_lista(e=None):

        campo_busca.visible = False

        conteudo.controls.clear()

        conteudo.controls.extend([

            ft.Text(
                "Pedidos Cadastrados",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=LARANJA
            ),

            ft.Button(
                content="Atualizar Lista",
                icon=ft.Icons.REFRESH,
                on_click=listar_pedidos
            ),

            lista_pedidos

        ])

        listar_pedidos()

    # =========================================================
    # TELA DE BUSCA
    # =========================================================

    def tela_busca(e=None):

        campo_busca.visible = True

        lista_pedidos.controls.clear()

        conteudo.controls.clear()

        conteudo.controls.extend([

            ft.Text(
                "Buscar Pedido",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=LARANJA
            ),

            campo_busca,

            ft.Button(
                content="Buscar",
                icon=ft.Icons.SEARCH,
                on_click=buscar_pedido
            ),

            lista_pedidos

        ])

        page.update()

    # =========================================================
    # MENU LATERAL
    # =========================================================

    menu = ft.NavigationRail(
    selected_index=0,

    label_type=ft.NavigationRailLabelType.ALL,

    bgcolor="#FF8C00",

    indicator_color="#1A1A1A",

    destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            selected_icon=ft.Icons.ADD_CIRCLE,
            label="Novo Pedido"
        ),

        ft.NavigationRailDestination(
            icon=ft.Icons.LIST_ALT_OUTLINED,
            selected_icon=ft.Icons.LIST_ALT,
            label="Listar"
        ),

        ft.NavigationRailDestination(
            icon=ft.Icons.SEARCH,
            selected_icon=ft.Icons.SEARCH,
            label="Buscar"
        )
    ]
)

    # =========================================================
    # MUDAR OPÇÃO DO MENU
    # =========================================================

    def mudar_menu(e):

        if e.control.selected_index == 0:

            tela_cadastro()

        elif e.control.selected_index == 1:

            tela_lista()

        elif e.control.selected_index == 2:

            tela_busca()

    menu.on_change = mudar_menu

    # =========================================================
    # CONTEÚDO PRINCIPAL
    # =========================================================

    conteudo = ft.Column(

        expand=True,

        scroll=ft.ScrollMode.AUTO

    )

    # =========================================================
    # CABEÇALHO
    # =========================================================

    cabecalho = ft.Column([

        titulo,

        subtitulo

    ])

    # =========================================================
    # LAYOUT
    # =========================================================

    page.add(

        cabecalho,

        ft.Divider(
            color=LARANJA
        ),

        ft.Row([

            menu,

            ft.VerticalDivider(
                width=1,
                color=LARANJA
            ),

            conteudo

        ],

        expand=True)

    )

    # =========================================================
    # ABRIR TELA INICIAL
    # =========================================================

    tela_cadastro()


# =============================================================
# INICIAR PROGRAMA
# =============================================================

ft.run(main)