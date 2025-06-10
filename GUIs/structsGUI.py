import os
from textwrap import wrap
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
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
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
            widget.config(font=("Courier New", big), wraplength=wrap, justify="center")
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

    def exCstructure(structure_type):
        # Write the structure_type number to communication.data
        comm_file = "datasets/communication.data"
        try:
            with open(comm_file, "w") as f:
                f.write(str(structure_type))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao escrever em {comm_file}: {e}"))
            return
        exe_path = os.path.abspath(os.path.join("out", "build", "GCC", "nycd.exe"))
        if not os.path.exists(exe_path):
            root.after(0, lambda: messagebox.showerror("Erro", f"Executável não encontrado: {exe_path}"))
            return
        def run_and_wait_for_signal():
            import time
            # Start the C++ process (non-blocking)
            proc = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            comm_file = "datasets/communication.data"
            expected_value = "0"
            for _ in range(300):  # Wait up to 60 seconds (300 * 0.2)
                try:
                    with open(comm_file, "r") as f:
                        content = f.read()
                    if content.strip() == expected_value:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                        root.after(0, show_next_screen(structure_type))
=======
                        root.after(0, show_next_screen)
>>>>>>> Stashed changes
=======
                        root.after(0, show_next_screen)
>>>>>>> Stashed changes
=======
                        root.after(0, show_next_screen)
>>>>>>> Stashed changes
                        return
                except Exception:
                    pass
                # Do NOT terminate the process, just check if it exited
                time.sleep(0.2)
            # If not detected after timeout, still proceed (fail-safe)
            root.after(0, show_next_screen)

        threading.Thread(target=run_and_wait_for_signal, daemon=True).start()

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
            widget.config(font=("Courier New", big), wraplength=wrap, justify="center")
        elif isinstance(widget, tk.Button):
            widget.config(font=("Courier New", med), height=btn_height)
        elif isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                set_widget_font(child, big, med, btn_height, wrap)

    def show_next_screen(structure_code):
        for widget in root.winfo_children():
            widget.destroy()
        full_text = "Estrutura Escolhida: " + structure_name + "\n\nO que deseja fazer?"
        wrap = max(200, int(root.winfo_width() * 0.95))
        label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 28), wraplength=wrap, justify="center")
        label.pack(pady=(50, 50), expand=True, fill="both")

        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(expand=True, fill="both")

        def show_buttons(root):
            btn_texts = ["Inserir", "Remover", "Buscar", "Filtrar e Ordenar", "Cálculo Estátistico", "Simulação"]
            for i, text in enumerate(btn_texts):
                btn_frame.rowconfigure(i, weight=1)
                btn_frame.columnconfigure(0, weight=1)
            for i, text in enumerate(btn_texts):
                def on_button_click(t=text, idx=i):
                    # Write structure_code + (idx+1) to communication.data
                    comm_file = "datasets/communication.data"
                    try:
                        with open(comm_file, "w") as f:
                            f.write(str(structure_code) + str(idx + 1))
                    except Exception as e:
                        root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao escrever em {comm_file}: {e}"))
                        return
                    disable_all_buttons(root)
                    unwriting_effect(label, full_text, root, lambda: structure(root, t))
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
                    command=on_button_click
                )
                btn.grid(row=i, column=0, pady=10, sticky="nsew")
        # Prompt: I'd like the pady between the label and buttons be dinamic resized with the window
        def update_dynamic_pady(event=None):
            h = root.winfo_height()
            # Calculate dynamic pady as a fraction of window height, min 20, max 150
            pady = max(20, min(150, int(h * 0.08)))
            label.pack_configure(pady=(pady, pady))

        writing_effect(label, full_text, root, lambda: show_buttons(root), 16, 500)
        root.bind("<Configure>", update_fonts)
        root.bind("<Configure>", update_dynamic_pady)
        root.after(0, update_dynamic_pady)

    structure_map = {
        "Lista Duplamente Encadeada": 1,
        "Árvore B": 2,
        "Tabela Hash": 3,
        "Skip List": 4,
        "Árvore Prefixada": 5,
        "Extra - Fila com Prioridade": 6
    }
    if structure_name in structure_map:
        wrap = max(200, int(root.winfo_width() * 0.95))
        loading_label = tk.Label(root, text="Carregando...", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
        loading_label.pack(pady=(100, 100), expand=True, fill="both")
        threading.Thread(target=lambda: exCstructure(structure_map[structure_name]), daemon=True).start()
        root.after(0, update_fonts)