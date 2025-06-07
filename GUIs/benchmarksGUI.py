def benchmarks(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")