import os
from customtkinter import *
from PIL import Image
from tkcalendar import DateEntry

# definindo funções e variáveis
listaTipos = ["Assalto", "Homicídio", "Sonegação", "Outro"]
listaBairros = ["Brooklyn", "Manhattan", "Bronx", "Outro"]
listaEstados = ["Tentativa", "Completado"]
listaLugares = ["Rua", "Residência", "Outro"]
def procurar():
    print("Hello World")

# setup das imagens
script_dir = os.path.dirname(os.path.abspath(__file__))
lupa_path = os.path.join(script_dir, "lupa.png")
lupa = Image.open(lupa_path)

# setup da janela
window = CTk()
window.geometry("500x400")
window.title("Página de Busca")
set_appearance_mode("dark")
icon_path = os.path.join(script_dir, "logopolicia.ico")
window.iconbitmap(icon_path)

# setup do frame
frame = CTkFrame(set_appearance_mode("dark"))
frame.pack(padx=10, pady=10)

# setando os elementos
titulo = CTkLabel(frame, text="Busca de Crimes em Nova York", font=("Arial", 25, "bold"))
textoData = CTkLabel(frame, text="Insira a data do crime:")
inserirData = CTkEntry(frame, placeholder_text="dd/mm/yyyy")
# inserirData = DateEntry(frame, date_pattern="dd/MM/yyyy")
textoTipo = CTkLabel(frame, text="Selecione o tipo do crime:")
escolherTipo = CTkComboBox(frame, values=listaTipos, state="readonly")
textoBairro = CTkLabel(frame, text="Selecione o bairro do crime:")
escolherBairro = CTkComboBox(frame, values=listaBairros, state="readonly")
textoEstado = CTkLabel(frame, text="Selecione o estado do crime:")
escolherEstado =CTkComboBox(frame, values=listaEstados, state="readonly")
textoLugar = CTkLabel(frame, text="Selecione o lugar do crime:")
escolherLugar = CTkComboBox(frame, values=listaLugares, state="readonly")
botaoProcurar = CTkButton(frame, text="Procurar", command=procurar, image=CTkImage(light_image=lupa))

# posicionando os elementos
titulo.grid(row=0, column=0, pady=10, columnspan=2, ipadx=50)
textoData.grid(row=1, column=0, pady=10, sticky="WE")
inserirData.grid(row=1, column=1, padx=10, pady=10, sticky="WE")
textoTipo.grid(row=2, column=0, pady=10, sticky="WE")
escolherTipo.grid(row=2, column=1, padx=10, pady=10, sticky="WE")
textoBairro.grid(row=3, column=0, pady=10, sticky="WE")
escolherBairro.grid(row=3, column=1, padx=10, pady=10, sticky="WE")
textoEstado.grid(row=4, column=0, pady=10, sticky="WE")
escolherEstado.grid(row=4, column=1, padx=10, pady=10, sticky="WE")
textoLugar.grid(row=5, column=0, pady=10, sticky="WE")
escolherLugar.grid(row=5, column=1, padx=10, pady=10, sticky="WE")
botaoProcurar.grid(row=100, column=0, pady=10, columnspan=2)

# rodando a janela
window.mainloop()
