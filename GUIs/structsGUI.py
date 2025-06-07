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
        for i, text in enumerate(btn_texts):
            btn = tk.Button(
                root,
                text=text,
                font=("Courier New", 24),
                width=50,
                height=1,
                bg="black",
                fg="white",
                activebackground="black",
                activeforeground="white",
                highlightbackground="white",  # border color on some platforms
                highlightcolor="white",
                bd=2,  # border width
                command=lambda t=text: unwriting_effect(label, full_text, root, lambda: structure(root, t))
                )
            btn.pack(pady=20)

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

    def show_next_screen():
        for widget in root.winfo_children():
            widget.destroy()
        full_text = "Estrutura Escolhida: " + structure_name + "\n\nO que deseja fazer?"
        label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 28))
        label.pack(pady=(50, 50))
        writing_effect(label, full_text, root, lambda: show_buttons(root), 16, 500)

        def show_buttons(root):
            btn_texts = ["Inserir", "Remover", "Buscar", "Filtrar e Ordenar", "Cálculo Estátístico", "Simulação"]
            for i, text in enumerate(btn_texts):
                btn = tk.Button(
                    root,
                    text=text,
                    font=("Courier New", 24),
                    width=50,
                    height=1,
                    bg="black",
                    fg="white",
                    activebackground="black",
                    activeforeground="white",
                    highlightbackground="white",
                    highlightcolor="white",
                    bd=2,
                    command=lambda t=text: lambda: [disable_all_buttons(root), unwriting_effect(label, full_text, root, lambda: structure(root, t))]
                )
                btn.pack(pady=20)

    if structure_name == "Lista Duplamente Encadeada":
        loading_label = tk.Label(root, text="Carregando...", fg="white", bg="black", font=("Courier New", 32))
        loading_label.pack(pady=(100, 100))
        threading.Thread(target=run_cpp_and_show_result, daemon=True).start()
    else:
        show_next_screen()