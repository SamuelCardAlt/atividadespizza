import flet as ft

def main(page: ft.Page):
    page.title = "PizzaDev"
    
    titulo = ft.Text("PizzaDev",size=32,weight=ft.FontWeight.BOLD)
    nome= ft.Text("Seu nome é Pizzaiolo ")
    slogan= ft.Text("Pizza nhamenhame ")
    Instrução = ft.Text("Corta e depois come")
    subtitulo = ft.Text("Monte seu pedido com segurança ")

    page.add(titulo,subtitulo,nome,Instrução,slogan)
ft.run(main)