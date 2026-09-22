import flet as ft 

def main(page:ft.Page): 
    page.title="PizzaDev"
#Lista para guardar os pedidos
    pedidos = []
#--------------------------------------------------------------
#TITULO
#--------------------------------------------------------------

    titulo=ft.Text(
        "PizzaDev",
        size=32,
        weight=ft.FontWeight.BOLD
    )

    subtitulo = ft.Text("Monte seu pedido com segurança")
    nome = ft.Text("Seu nome é Pizzaiolo")
    slogan = ft.Text("Piza nhamenhame")
    instrucao = ft.Text("Corta e depois come")

#--------------------------------------------------------------
#PEDIDOS
#--------------------------------------------------------------

    campo_pedido = ft.TextField(label="Digite seu pedido",
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
#botão para adicionar os pedidos.
    botao_adicionar = ft.Button(
        content="Adicionar Pedido ",
        on_click=adicionar_pedido
    )
    linha_pedido = ft.Row(
        controls=[
            campo_pedido,
            botao_adicionar
        ]
    )
#--------------------------------------------------------------
#CARDAPIO 
#--------------------------------------------------------------
    cardapio_titulo = ft.Text(
         "🍕 CARDÁPIO",
         size=28,
         weight=ft.FontWeight.BOLD

    )
#Pizza de calabresa
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
            )
        ]
    ),
    padding=15,
    border=ft.Border.all(1, "orange")
)
     # Pizza de Frango
    pizza_frango = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Frango com Catupiry",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: frango desfiado, catupiry, queijo e molho de tomate"
                )
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )
 # Pizza de Mussarela
    pizza_mussarela = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Mussarela",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: queijo mussarela, tomate, orégano e molho de tomate"
                )
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # Pizza Portuguesa
    pizza_portuguesa = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍕 Portuguesa",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: presunto, queijo, ovo, cebola, tomate e azeitona"
                )
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    # Pizza de Chocolate
    pizza_chocolate = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🍫 Chocolate",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Text(
                    "Ingredientes: chocolate, leite condensado e granulado"
                )
            ]
        ),
        padding=15,
        border=ft.Border.all(1, "orange")
    )

    #Coluna do cardapio
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
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )

#--------------------------------------------------------------
#CONTEUDO PRINCIPAL
#--------------------------------------------------------------
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
                size = 22,
                weight=ft.FontWeight.BOLD
            ),
            lista_pedidos,

            ft.Divider(),
#cardapio separado
            cardapio


        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    #container principal
    tela= ft.Container(
        content = conteudo,
        padding=20,
        expand=True

    )

    page.add(tela)
ft.run(main)
