import os
import threading
import subprocess
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from effects import writing_effect, unwriting_effect, disable_all_buttons

def structures(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "Escolha a estrutura de dados que deseja utilizar:"
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32))
    label.pack(pady=(50, 50))  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_buttons(root), 16, 500)

    def show_buttons(root):
        btn_texts = ["Lista Duplamente Encadeada", "Árvore B", "Tabela Hash", "Skip List", "Árvore Prefixada", "Extra - Fila com Prioridade"]
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(expand=True, fill="both")
        for i, text in enumerate(btn_texts):
            btn_frame.rowconfigure(i, weight=1)
        btn_frame.columnconfigure(0, weight=1)
        for i, text in enumerate(btn_texts):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Courier New", 24),
                bg="black",
                fg="white",
                activebackground="black",
                activeforeground="white",
                highlightbackground="white",
                highlightcolor="white",
                bd=2,
                command=lambda t=text: unwriting_effect(label, full_text, root, lambda: structure(root, t))
                )
            btn.grid(row=i, column=0, pady=10, sticky="nsew")

    def update_fonts(event=None):
        w, h = root.winfo_width(), root.winfo_height()
        base = min(w, h)
        big = max(12, int(base * 0.05))
        med = max(10, int(base * 0.03))
        # Button height: at least 1.5x font size, minimum 2
        btn_height = max(2, int(med * 1.5 // 10))
        wrap = max(200, int(w * 0.95))
        for widget in root.winfo_children():
            set_widget_font(widget, big, med, btn_height, wrap)
    def set_widget_font(widget, big, med, btn_height, wrap):
        if isinstance(widget, tk.Label):
            widget.config(font=("Courier New", big), wraplength=wrap)
        elif isinstance(widget, tk.Button):
            widget.config(font=("Courier New", med), height=btn_height)
        elif isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                set_widget_font(child, big, med, btn_height, wrap)
    root.bind("<Configure>", update_fonts)
    root.after(0, update_fonts)

def structure(root, structure_name):
    #Prompt: I'd like to create a condition, where if the structure_name is "Lista Duplamente Encadeada",
    #it will run a C++ code.
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")

    def run_cpp_and_show_result():
        exe_path = os.path.abspath(os.path.join("out", "build", "GCC", "nycd.exe"))
        if not os.path.exists(exe_path):
            root.after(0, lambda: messagebox.showerror("Erro", f"Executável não encontrado: {exe_path}"))
            return
        try:
            result = subprocess.run([exe_path], capture_output=True, text=True)
            root.after(0, lambda: messagebox.showinfo("Saída do C++", result.stdout))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao executar o código C++: {e}"))
        # After showing result, continue to next screen
        root.after(0, lambda: show_next_screen())

    def update_fonts(event=None):
        w, h = root.winfo_width(), root.winfo_height()
        base = min(w, h)
        big = max(12, int(base * 0.05))
        med = max(10, int(base * 0.03))
        btn_height = max(2, int(med * 1.5 // 10))
        wrap = max(200, int(w * 0.95))
        for widget in root.winfo_children():
            set_widget_font(widget, big, med, btn_height, wrap)

    def set_widget_font(widget, big, med, btn_height, wrap):
        if isinstance(widget, tk.Label):
            widget.config(font=("Courier New", big), wraplength=wrap)
        elif isinstance(widget, tk.Button):
            widget.config(font=("Courier New", med), height=btn_height)
        elif isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                set_widget_font(child, big, med, btn_height, wrap)

    def show_next_screen():
        for widget in root.winfo_children():
            widget.destroy()
        full_text = "Estrutura Escolhida: " + structure_name + "\n\nO que deseja fazer?"
        label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 28))
        label.pack(pady=(50, 50), expand=True, fill="both")
        writing_effect(label, full_text, root, lambda: show_buttons(root), 16, 500)

        def show_buttons(root):
            btn_texts = ["Inserir", "Remover", "Buscar", "Filtrar e Ordenar", "Cálculo Estátistico", "Simulação"]
            btn_frame = tk.Frame(root, bg="black")
            btn_frame.pack(expand=True, fill="both")
            for i, text in enumerate(btn_texts):
                btn_frame.rowconfigure(i, weight=1)
            btn_frame.columnconfigure(0, weight=1)
            for i, text in enumerate(btn_texts):
                btn = tk.Button(
                    btn_frame,
                    text=text,
                    font=("Courier New", 24),
                    bg="black",
                    fg="white",
                    activebackground="black",
                    activeforeground="white",
                    highlightbackground="white",
                    highlightcolor="white",
                    bd=2,
                    command=lambda t=text: lambda: [disable_all_buttons(root), unwriting_effect(label, full_text, root, lambda: structure(root, t))]
                )
                btn.grid(row=i, column=0, pady=10, sticky="nsew")
        root.bind("<Configure>", update_fonts)

    if structure_name == "Lista Duplamente Encadeada":
        loading_label = tk.Label(root, text="Carregando...", fg="white", bg="black", font=("Courier New", 32))
        loading_label.pack(pady=(100, 100), expand=True, fill="both")
        threading.Thread(target=run_cpp_and_show_result, daemon=True).start()
        root.after(0, update_fonts)
    else:
        show_next_screen()
        root.after(0, update_fonts)