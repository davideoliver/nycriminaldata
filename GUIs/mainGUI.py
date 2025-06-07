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
    root.attributes('-fullscreen', True)
    #Prompt: I'd like to terminate the program if the ESC key be pressed
    root.bind("<Escape>", lambda e: root.quit())
    def delete_datasets(_event=None):
        if os.path.exists(FOLDER):
            try:
                shutil.rmtree(FOLDER)
                print(f"Deleted folder: {FOLDER}")
            except Exception as ex:
                print(f"Failed to delete folder: {ex}")  # Optionally, show a messagebox here
    root.bind("<Delete>", delete_datasets)
    show_splash(root)
    root.mainloop()

def show_splash(root):
    root.configure(bg="black")
    for widget in root.winfo_children():
        widget.destroy()
    full_text = "NYCRIMINALDATA"
    full_text2 = "Aperte ESC para sair do programa\ne DEL para excluir a base de dados\n a qualquer momento"

    # Use a frame with grid to keep label1 centered at all times
    splash_frame = tk.Frame(root, bg="black")
    splash_frame.pack(expand=True, fill="both")

    splash_frame.grid_rowconfigure(0, weight=1)
    splash_frame.grid_rowconfigure(1, weight=0)
    splash_frame.grid_rowconfigure(2, weight=1)
    splash_frame.grid_columnconfigure(0, weight=1)

    label1 = tk.Label(splash_frame, text="", fg="white", bg="black", font=("Courier New", 64))
    label1.grid(row=1, column=0, pady=(100, 10), sticky="n")

    label2 = tk.Label(splash_frame, text="", fg="white", bg="black", font=("Courier New", 24))
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
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32))
    label.pack(pady=(200, 100))  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_confirmation_buttons(root, label, full_text), 16, 500)

    def show_confirmation_buttons(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20))
    
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
        btn_yes.pack(side="left", padx=(0, 40))
    
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
        btn_no.pack(side="left")

def load(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")

    label = tk.Label(root, text="Baixando base de dados...", fg="white", bg="black", font=("Courier New", 24))
    label.pack(pady=(100, 20))
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor='white', background='black')  # Black indicator, white background

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="TProgressbar")
    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
    progress.pack(pady=(0, 20))
    status_label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 16))
    status_label.pack()

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

def failscreen(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "A base de dados não foi encontrada,\n baixe-a manualmente ou opte por Sim na tela inicial."
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32))
    label.pack(pady=(200, 100))  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_button(root, label, full_text),16, 500)

    def show_button(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20))
    
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
        btn_ok.pack(side="left")

def cut(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")

    #Prompt: The show_spalsh label last letter stays on screen while the pandas dataframe is being create
    #  for the cut function, I'd like it dissapears and a loading bar be added to this process
    # Show loading label and progress bar
    loading_label = tk.Label(root, text="Carregando dados...", fg="white", bg="black", font=("Courier New", 32))
    loading_label.pack(pady=(200, 20))
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", troughcolor='white', background='black')
    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="TProgressbar")
    progress.pack(pady=(0, 20))
    progress.start(10)

    def load_data():
        df = pd.read_csv(os.path.join(FOLDER, FILE_TO_CHECK))
        progress.stop()
        loading_label.destroy()
        progress.destroy()
        
        # Now show the next screen
        full_text = f"\nO dataset possuí {df.shape[0]} dados, muitos dados podem\ntornar processos lentos e estruturas custosas\nVocê gostaria de reduzir esses dados aleatoriamente\n para uma melhora no desempenho?"
        label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 24))
        label.pack(pady=(200, 100))
        writing_effect(label, full_text, root, lambda: show_button(root, label, full_text, df), 16, 500)

    def show_button(root, label, full_text, df):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20))

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
        btn_yes.pack(side="left", padx=(0, 40))

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
        btn_no.pack(side="left")

    # Start loading in a thread
    threading.Thread(target=load_data).start()

def reduce_data(root, df):
    # Prompt I'd like to create two widgets where the user can write a number (only numbers) to be read
    #  and used as a variable in the df.sample of reduced_data
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")

    label = tk.Label(root, text="Digite a fração (0-1) que restará e uma semente para aleatoriedade:", fg="white", bg="black", font=("Courier New", 24))
    label.pack(pady=(100, 20))

    entry_frame = tk.Frame(root, bg="black")
    entry_frame.pack(pady=(0, 20))

    # Only allow numbers and dot for fraction
    vcmd_frac = (root.register(lambda P: P == "" or (P.replace('.', '', 1).isdigit() and P.count('.') <= 1 and 0 <= float(P or 0) <= 1)), '%P')
    vcmd_seed = (root.register(lambda P: P == "" or P.isdigit()), '%P')

    tk.Label(entry_frame, text="Fração:", fg="white", bg="black", font=("Courier New", 18)).grid(row=0, column=0, padx=10)
    frac_entry = tk.Entry(entry_frame, font=("Courier New", 18), validate="key", validatecommand=vcmd_frac, width=8)
    frac_entry.insert(0, "0.5")
    frac_entry.grid(row=0, column=1, padx=10)

    tk.Label(entry_frame, text="Semente:", fg="white", bg="black", font=("Courier New", 18)).grid(row=0, column=2, padx=10)
    seed_entry = tk.Entry(entry_frame, font=("Courier New", 18), validate="key", validatecommand=vcmd_seed, width=8)
    seed_entry.insert(0, "1")
    seed_entry.grid(row=0, column=3, padx=10)

    error_label = tk.Label(root, text="", fg="red", bg="black", font=("Courier New", 16))
    error_label.pack()

    # Progress bar for sampling
    progress_label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 16))
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
    btn.pack(pady=20)
    
def optype(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "\nO que gostaria de fazer?"
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 32))
    label.pack(pady=(200, 100))  # Add top padding, small bottom padding

    writing_effect(label, full_text, root, lambda: show_button(root, label, full_text),16, 500)

    def show_button(root, label, full_text):
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=(0, 20))
    
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
        btn_yes.pack(side="left", padx=(0, 40))
    
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
        btn_no.pack(side="left")

main()