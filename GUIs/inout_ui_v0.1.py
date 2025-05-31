import os
from customtkinter import *
from PIL import Image
from tkcalendar import DateEntry

def inout_ui(t):
    typ = t

    # definindo funções e variáveis
    listTypes = ["Assalto", "Homicídio", "Sonegação", "Outro"]
    listBoroughs = ["Brooklyn", "Manhattan", "Bronx", "Outro"]
    listStates = ["Tentativa", "Completado"]
    listPlaces = ["Rua", "Residência", "Outro"]
    def Search():
        print("Hello World")

    # setup das imagens
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lupa_path = os.path.join(script_dir, "lupa.png")
    lupa = Image.open(lupa_path)

    # setup da janela
    window = CTk()
    window.geometry("500x400")
    window.title("Página de %s", typ)
    set_appearance_mode("dark")
    icon_path = os.path.join(script_dir, "logopolicia.ico")
    window.iconbitmap(icon_path)

    # setup do frame
    frame = CTkFrame(set_appearance_mode("dark"))
    frame.pack(padx=10, pady=10)

    # setando os elementos
    title = CTkLabel(frame, text=typ + " de Registros", font=("Arial", 25, "bold"))
    textDate = CTkLabel(frame, text="Insira a data do crime:")
    inserirDate = CTkEntry(frame, placeholder_text="dd/mm/yyyy")
    # inserirData = DateEntry(frame, date_pattern="dd/MM/yyyy")
    textType = CTkLabel(frame, text="Selecione o tipo do crime:")
    choiceType = CTkComboBox(frame, values=listTypes, state="readonly")
    textBorough = CTkLabel(frame, text="Selecione o bairro do crime:")
    choiceBorough = CTkComboBox(frame, values=listBoroughs, state="readonly")
    textState = CTkLabel(frame, text="Selecione o estado do crime:")
    choiceState =CTkComboBox(frame, values=listStates, state="readonly")
    textPlace = CTkLabel(frame, text="Selecione o lugar do crime:")
    choicePlace = CTkComboBox(frame, values=listPlaces, state="readonly")
    buttonSearch = CTkButton(frame, text="Procurar", command=Search, image=CTkImage(light_image=lupa))

    # posicionando os elementos
    title.grid(row=0, column=0, pady=10, columnspan=2, ipadx=50)
    textDate.grid(row=1, column=0, pady=10, sticky="WE")
    inserirDate.grid(row=1, column=1, padx=10, pady=10, sticky="WE")
    textType.grid(row=2, column=0, pady=10, sticky="WE")
    choiceType.grid(row=2, column=1, padx=10, pady=10, sticky="WE")
    textBorough.grid(row=3, column=0, pady=10, sticky="WE")
    choiceBorough.grid(row=3, column=1, padx=10, pady=10, sticky="WE")
    textState.grid(row=4, column=0, pady=10, sticky="WE")
    choiceState.grid(row=4, column=1, padx=10, pady=10, sticky="WE")
    textPlace.grid(row=5, column=0, pady=10, sticky="WE")
    choicePlace.grid(row=5, column=1, padx=10, pady=10, sticky="WE")
    buttonSearch.grid(row=100, column=0, pady=10, columnspan=2)

    # rodando a janela
    window.mainloop()
