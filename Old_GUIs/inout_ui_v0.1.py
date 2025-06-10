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
    frame.pack(padx=10, pady=10, expand=True, fill="both")
    for i in range(7):  # include row for button
        frame.grid_rowconfigure(i, weight=1)
    frame.grid_rowconfigure(100, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)

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
    title.grid(row=0, column=0, pady=10, columnspan=2, ipadx=50, sticky="nsew")
    textDate.grid(row=1, column=0, pady=10, sticky="nsew")
    inserirDate.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    textType.grid(row=2, column=0, pady=10, sticky="nsew")
    choiceType.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
    textBorough.grid(row=3, column=0, pady=10, sticky="nsew")
    choiceBorough.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
    textState.grid(row=4, column=0, pady=10, sticky="nsew")
    choiceState.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
    textPlace.grid(row=5, column=0, pady=10, sticky="nsew")
    choicePlace.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")
    buttonSearch.grid(row=100, column=0, pady=10, columnspan=2, sticky="nsew")

    # Dynamic font and widget resizing
    def resize_fonts(event=None):
        w, h = window.winfo_width(), window.winfo_height()
        base = min(w, h)
        title_font_size = max(12, int(base * 0.05))
        label_font_size = max(10, int(base * 0.025))
        entry_font_size = max(10, int(base * 0.025))
        button_font_size = max(10, int(base * 0.03))
        entry_height = max(28, int(base * 0.06))
        # Button height: at least 1.5x font size, minimum 32
        button_height = max(32, int(button_font_size * 1.5))
        wrap = max(200, int(w * 0.95))
        title.configure(font=("Arial", title_font_size, "bold"), wraplength=wrap)
        textDate.configure(font=("Arial", label_font_size), wraplength=wrap)
        inserirDate.configure(font=("Arial", entry_font_size))
        inserirDate.configure(height=entry_height)
        textType.configure(font=("Arial", label_font_size), wraplength=wrap)
        choiceType.configure(font=("Arial", entry_font_size))
        choiceType.configure(height=entry_height)
        textBorough.configure(font=("Arial", label_font_size), wraplength=wrap)
        choiceBorough.configure(font=("Arial", entry_font_size))
        choiceBorough.configure(height=entry_height)
        textState.configure(font=("Arial", label_font_size), wraplength=wrap)
        choiceState.configure(font=("Arial", entry_font_size))
        choiceState.configure(height=entry_height)
        textPlace.configure(font=("Arial", label_font_size), wraplength=wrap)
        choicePlace.configure(font=("Arial", entry_font_size))
        choicePlace.configure(height=entry_height)
        buttonSearch.configure(font=("Arial", button_font_size, "bold"))
        buttonSearch.configure(height=button_height)

    window.bind("<Configure>", resize_fonts)
    resize_fonts()

    # rodando a janela
    window.mainloop()
