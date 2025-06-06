'''
This code contains the GUI for the application. It uses tkinter to create a GUI that allows the user to
run each function inside the app.
'''
import tkinter as tk
from tkinter import ttk  # Add this import
import os
import kagglehub
from baseimport import   dload
# Ensure the Kaggle API is authenticated and the dataset is downloaded

FILE_TO_CHECK = "NYPD_Complaint_Data_Historic.csv"
FOLDER = "datasets" 

def unwriting_effect(label, text, root, on_finish, delay=16):
    if text:
        label.config(text=text)
        root.after(delay, lambda: unwriting_effect(label, text[:-1], root, on_finish, delay))
    else:
        label.config(text="")  # Ensure the label is cleared
        on_finish()

def writing_effect(label, text, root, on_finish, delay=16, start_delay=1000):
    def step(i):
        label.config(text=text[:i])
        if i <= len(text):
            root.after(delay, lambda: step(i + 1))
        else:
            on_finish()
    if start_delay > 0:
        root.after(start_delay, lambda: step(1))
    else:
        step(1)

def check_file_and_continue(root):
    file_path = os.path.join(FOLDER, FILE_TO_CHECK)
    if os.path.exists(file_path):
        structures(root)
    else:
        show_missing_file_screen(root)

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

    import threading
    def run_download():
        progress.start(10)  # Start indeterminate animation
        progress_callback(0, "Isso pode demorar um pouco, por favor, aguarde")
        dload(progress_callback)
        progress.stop()
        progress["value"] = 100
        progress_callback(100, "Download concluído!")
        root.after(0, lambda: check_file_and_continue(root))

    threading.Thread(target=run_download).start()

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
                bd=2  # border width
                )
            btn.pack(pady=20)

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
            command=lambda: unwriting_effect(label, full_text, root, lambda: root.quit()))
        btn_ok.pack(side="left")

def show_missing_file_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    full_text = "A base de dados não foi encontrada,\n gostaria de importa-la pela internet?"
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
        command=lambda: unwriting_effect(label, full_text, root, lambda: load(root))
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
        command=lambda: unwriting_effect(label, full_text, root, lambda: failscreen(root))
        )
        btn_no.pack(side="left")

def show_splash(root):
    root.configure(bg="black")
    for widget in root.winfo_children():
        widget.destroy()
    full_text = "NYCRIMINALDATA"
    label = tk.Label(root, text="", fg="white", bg="black", font=("Courier New", 64))
    label.pack(expand=True)

    def after_writing():
        root.after(1800, unwriting_effect(label, full_text, root, lambda: check_file_and_continue(root), 32))

    writing_effect(label, full_text, root, after_writing, 16)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    show_splash(root)
    root.mainloop()

if __name__ == "__main__":
    main()