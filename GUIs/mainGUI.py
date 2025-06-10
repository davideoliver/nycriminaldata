'''
This code contains the GUI for the application. It uses tkinter to create a GUI that allows the user to
run each of the other function inside the app.
'''
import os
import shutil
import threading
import pandas as pd
import tkinter as tk
from tkinter import ttk 
from baseimport import dload
from benchmarksGUI import benchmarks
from structsGUI import structures, structure 
from effects import writing_effect, unwriting_effect, disable_all_buttons

# Constants for file checking
FILE_TO_CHECK = "NYPD_Complaint_Data_Historic.csv"
FOLDER = "datasets" 

"""
Prompt for buttons customization:
I'd like all the buttons have a black colored background
with their text color being white as well as their borders
"""

def main():
    root = tk.Tk()
    root.title("NYCRIMINALDATA")
    root.geometry("1280x800")
    root.minsize(600, 400)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # Prompt: I'd like to terminate the program if the ESC key be pressed
    root.bind("<Escape>", lambda e: root.quit())
    def delete_datasets(_event=None):
        if os.path.exists(FOLDER):
            try:
                shutil.rmtree(FOLDER)
                print(f"Deleted folder: {FOLDER}")
            except Exception as ex:
                print(f"Failed to delete folder: {ex}")  # Optionally, show a messagebox here
    root.bind("<Delete>", delete_datasets)

    def update_fonts(event=None):
        w, h = root.winfo_width(), root.winfo_height()
        base = min(w, h)
        big = max(12, int(base * 0.05))
        med = max(10, int(base * 0.03))
        small = max(8, int(base * 0.02))
        btn_height = max(2, int(med * 1.5 // 10))
        entry_height = max(1, int(base * 0.012))
        bar_length = max(200, int(w * 0.4))
        wrap = max(200, int(w * 0.95))  # Use wrap for label wraplength
        # Dynamic vertical padding for cut/optype screens
        root.dynamic_pady_label = int(h * 0.18)
        root.dynamic_pady_btn = int(h * 0.05)
        for widget in root.winfo_children():
            set_widget_font(widget, big, med, small, btn_height, entry_height, bar_length, wrap)

    def set_widget_font(widget, big, med, small, btn_height, entry_height, bar_length, wrap):
        if isinstance(widget, tk.Label):
            text = widget.cget("text")
            if len(text) > 30:
                widget.config(font=("Courier New", med), wraplength=wrap, justify="center")
            elif len(text) > 10:
                widget.config(font=("Courier New", big), wraplength=wrap, justify="center")
            else:
                widget.config(font=("Courier New", big, "bold"), wraplength=wrap, justify="center")
        elif isinstance(widget, tk.Button):
            widget.config(font=("Courier New", med), height=btn_height)
        elif isinstance(widget, tk.Entry):
            widget.config(font=("Courier New", med))
            try:
                widget.config(height=entry_height)
            except Exception:
                pass
        elif isinstance(widget, ttk.Progressbar):
            widget.config(length=bar_length)
        elif isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                set_widget_font(child, big, med, small, btn_height, entry_height, bar_length, wrap)

    root.bind("<Configure>", update_fonts)
    show_splash(root)
    root.mainloop()

def show_splash(root):
    root.configure(bg="black")
    for widget in root.winfo_children():
        widget.destroy()
    full_text = "NYCRIMINALDATA"
    full_text2 = "Aperte ESC para sair do programa\ne DEL para excluir a base de dados\n a qualquer momento"

    splash_frame = tk.Frame(root, bg="black")
    splash_frame.pack(expand=True, fill="both")

    splash_frame.grid_rowconfigure(0, weight=1)
    splash_frame.grid_rowconfigure(1, weight=0)
    splash_frame.grid_rowconfigure(2, weight=1)
    splash_frame.grid_columnconfigure(0, weight=1)

    # Set wraplength to 95% of window width
    wrap = max(200, int(root.winfo_width() * 0.95))
    label1 = tk.Label(splash_frame, text="", fg="white", bg="black", font=("Courier New", 64), wraplength=wrap, justify="center")
    label1.grid(row=1, column=0, pady=(100, 10), sticky="n")

    label2 = tk.Label(splash_frame, text="", fg="white", bg="black", font=("Courier New", 24), wraplength=wrap, justify="center")
    label2.grid(row=2, column=0, pady=(0, 100), sticky="n")

    def after_label1():
        writing_effect(label2, full_text2, root, after_label2, 16, 500)

    def after_label2():
        # Wait a moment, then unwriting effect for label2 first
        root.after(1500, lambda: unwriting_effect(
            label2, full_text2, root,
            lambda: (
                label2.grid_remove(),
                unwriting_effect(label1, full_text, root, lambda: (label1.grid_remove(), splash_frame.destroy(), check_file_and_continue(root)), 8)
            ),
            8
        ))

    writing_effect(label1, full_text, root, after_label1, 16, 500)
    root.after(0, root.event_generate, "<<UpdateFonts>>")  # trigger font update

def check_file_and_continue(root):
    file_path = os.path.join(FOLDER, FILE_TO_CHECK)
    if os.path.exists(file_path):
        cut(root)
    else:
        show_missing_file_screen(root)

def show_missing_file_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "A base de dados não foi encontrada,\n gostaria de baixa-la pela internet?"
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
    label.pack(pady=(200, 100), expand=True, fill="both")  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_confirmation_buttons(root, label, full_text), 16, 500)

    def show_confirmation_buttons(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20), expand=True, fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_yes = tk.Button(
            btn_frame,
            text="Sim",
            font=("Courier New", 24),
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="white",
            bd=2,
            command=lambda: [disable_all_buttons(root),unwriting_effect(label, full_text, root, lambda: load(root))]
        )
        btn_yes.grid(row=0, column=0, padx=(0, 40), sticky="nsew")
    
        btn_no = tk.Button(
            btn_frame,
            text="Não",
            font=("Courier New", 24),
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="white",
            bd=2,
            command=lambda: [disable_all_buttons(root),unwriting_effect(label, full_text, root, lambda: failscreen(root))]
        )
        btn_no.grid(row=0, column=1, sticky="nsew")

    root.event_generate("<<UpdateFonts>>")

def load(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="Baixando base de dados...", fg="white", bg="black", font=("Courier New", 24), wraplength=wrap, justify="center")
    label.pack(pady=(100, 20), expand=True, fill="both")
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor='white', background='black')  # Black indicator, white background

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="TProgressbar")
    progress.pack(pady=(0, 20), expand=True, fill="x")
    status_label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 16), wraplength=wrap, justify="center")
    status_label.pack(expand=True, fill="both")

    def progress_callback(percent, message):
        root.after(0, lambda: status_label.config(text=message))
        root.update_idletasks()
    def run_download():
        progress.start(10)  # Start indeterminate animation
        progress_callback(0, "Isso pode demorar um pouco, por favor, aguarde")
        dload(progress_callback)
        progress.stop()
        progress["value"] = 100
        progress_callback(100, "Download concluído!")
        root.after(0, lambda: check_file_and_continue(root))

    threading.Thread(target=run_download).start()
    root.event_generate("<<UpdateFonts>>")

def failscreen(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "A base de dados não foi encontrada,\n baixe-a manualmente ou opte por Sim na tela inicial."
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
    label.pack(pady=(200, 100), expand=True, fill="both")  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_button(root, label, full_text),16, 500)

    def show_button(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20), expand=True, fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_ok = tk.Button(btn_frame,
            text="OK",
            font=("Courier New", 24),
            width=20,
            height=2,
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            highlightbackground="white",  # border color on some platforms
            highlightcolor="white",
            bd=2,  # border width
            command=lambda: [disable_all_buttons(root),unwriting_effect(label, full_text, root, lambda: root.quit())]
            )
        btn_ok.grid(row=0, column=0, sticky="nsew")

    root.event_generate("<<UpdateFonts>>")

def cut(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    wrap = max(200, int(root.winfo_width() * 0.95))
    loading_label = tk.Label(root, text="Carregando dados...", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
    loading_label.pack(pady=(root.dynamic_pady_label if hasattr(root, "dynamic_pady_label") else 200, 20), expand=True, fill="both")
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor='white', background='black')
    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="TProgressbar")
    progress.pack(pady=(0, 20), expand=True, fill="x")
    progress.start(10)

    def load_data():
        df = pd.read_csv(os.path.join(FOLDER, FILE_TO_CHECK))
        progress.stop()
        loading_label.destroy()
        progress.destroy()
        
        # Now show the next screen
        full_text = f"\nO dataset possuí {df.shape[0]} dados, muitos dados podem\ntornar processos lentos e estruturas custosas\nVocê gostaria de reduzir esses dados aleatoriamente\n para uma melhora no desempenho?"
        label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 24), wraplength=wrap, justify="center")
        label.pack(pady=(root.dynamic_pady_label if hasattr(root, "dynamic_pady_label") else 200, root.dynamic_pady_btn if hasattr(root, "dynamic_pady_btn") else 100), expand=True, fill="both")
        writing_effect(label, full_text, root, lambda: show_button(root, label, full_text, df), 16, 500)

    def show_button(root, label, full_text, df):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, root.dynamic_pady_btn if hasattr(root, "dynamic_pady_btn") else 20), expand=True, fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_yes = tk.Button(
            btn_frame,
            text="Sim",
            font=("Courier New", 24),
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="white",
            bd=2,
            command=lambda: [disable_all_buttons(root),unwriting_effect(label, full_text, root, lambda: reduce_data(root, df))]
        )
        btn_yes.grid(row=0, column=0, padx=(0, 40), sticky="nsew")

        btn_no = tk.Button(
            btn_frame,
            text="Não",
            font=("Courier New", 24),
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            highlightbackground="white",
            highlightcolor="white",
            bd=2,
            command=lambda: [disable_all_buttons(root),unwriting_effect(label, full_text, root, lambda: optype(root), 4)]
        )
        btn_no.grid(row=0, column=1, sticky="nsew")

    # Start loading in a thread
    threading.Thread(target=load_data).start()
    root.event_generate("<<UpdateFonts>>")

def reduce_data(root, df):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="Digite a fração (0-1) que restará e uma semente para aleatoriedade:", fg="white", bg="black", font=("Courier New", 24), wraplength=wrap, justify="center")
    label.pack(pady=(100, 20), expand=True, fill="both")

    entry_frame = tk.Frame(root, bg="black")
    entry_frame.pack(pady=(0, 20), expand=True, fill="x")
    entry_frame.columnconfigure(1, weight=1)
    entry_frame.columnconfigure(3, weight=1)

    # Only allow numbers and dot for fraction
    vcmd_frac = (root.register(lambda P: P == "" or (P.replace('.', '', 1).isdigit() and P.count('.') <= 1 and 0 <= float(P or 0) <= 1)), '%P')
    vcmd_seed = (root.register(lambda P: P == "" or P.isdigit()), '%P')

    tk.Label(entry_frame, text="Fração:", fg="white", bg="black", font=("Courier New", 18)).grid(row=0, column=0, padx=10)
    frac_entry = tk.Entry(entry_frame, font=("Courier New", 18), validate="key", validatecommand=vcmd_frac, width=8)
    frac_entry.insert(0, "0.5")
    frac_entry.grid(row=0, column=1, padx=10, sticky="ew")

    tk.Label(entry_frame, text="Semente:", fg="white", bg="black", font=("Courier New", 18)).grid(row=0, column=2, padx=10)
    seed_entry = tk.Entry(entry_frame, font=("Courier New", 18), validate="key", validatecommand=vcmd_seed, width=8)
    seed_entry.insert(0, "1")
    seed_entry.grid(row=0, column=3, padx=10, sticky="ew")

    error_label = tk.Label(root, text="", fg="red", bg="black", font=("Courier New", 16), wraplength=wrap, justify="center")
    error_label.pack(expand=True, fill="both")

    # Progress bar for sampling
    progress_label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 16), wraplength=wrap, justify="center")
    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="TProgressbar")

    def on_reduce():
        try:
            frac = float(frac_entry.get())
            seed = int(seed_entry.get())
            if not (0 < frac <= 1):
                raise ValueError
        except ValueError:
            error_label.config(text="Insira uma fração entre 0 e 1 e uma semente válida.")
            return

        # Prompt: I'd like to hide the label, buttom and entries before the progress bar
        # Hide input widgets before showing progress bar
        label.pack_forget()
        entry_frame.pack_forget()
        error_label.pack_forget()
        btn.pack_forget()

        # Show progress bar and label
        progress_label.config(text="Reduzindo dados, por favor aguarde...")
        progress_label.pack(pady=(10, 0))
        progress.pack(pady=(0, 20))
        progress.start(10)

        def do_sample():
            reduced_df = df.sample(frac=frac, random_state=seed)
            reduced_df.to_csv(os.path.join(FOLDER, FILE_TO_CHECK), index=False)
            progress.stop()
            progress.pack_forget()
            progress_label.pack_forget()
            root.after(0, lambda: optype(root))

        threading.Thread(target=do_sample).start()

    btn = tk.Button(root,
        text="Reduzir",
        font=("Courier New", 20),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        bd=2,
        command=lambda: [disable_all_buttons(root),on_reduce()]
    )
    btn.pack(pady=20, expand=True, fill="x")
    root.event_generate("<<UpdateFonts>>")
    
def optype(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "\nO que gostaria de fazer?"
    wrap = max(200, int(root.winfo_width() * 0.95))
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32), wraplength=wrap, justify="center")
    label.pack(pady=(root.dynamic_pady_label if hasattr(root, "dynamic_pady_label") else 200, root.dynamic_pady_btn if hasattr(root, "dynamic_pady_btn") else 100), expand=True, fill="both")  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_button(root, label, full_text),16, 500)

    def show_button(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, root.dynamic_pady_btn if hasattr(root, "dynamic_pady_btn") else 20), expand=True, fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_yes = tk.Button(
        btn_frame,
        text="Operações Individuais",
        font=("Courier New", 24),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        highlightbackground="white", 
        highlightcolor="white",
        bd=2,
        command=lambda: [disable_all_buttons(root), unwriting_effect(label, full_text, root, lambda: structures(root))]
        )
        btn_yes.grid(row=0, column=0, padx=(0, 40), sticky="nsew")
    
        btn_no = tk.Button(
        btn_frame,
        text="Testes de Benchmark",
        font=("Courier New", 24),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        bd=2,
        command=lambda: [disable_all_buttons(root), unwriting_effect(label, full_text, root, lambda: benchmarks(root))]
        )
        btn_no.grid(row=0, column=1, sticky="nsew")

    root.event_generate("<<UpdateFonts>>")

main()