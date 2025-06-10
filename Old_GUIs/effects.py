import tkinter as tk


# Prompt: I'd like the label, vanish with a effect of unwriting it
def unwriting_effect(label, text, root, on_finish, delay=8):
    if text:
        label.config(text=text)
        root.after(delay, lambda: unwriting_effect(label, text[:-1], root, on_finish, delay))
    else:
        label.config(text="")  # Ensure the label is cleared
        on_finish()

# Prompt: I'd like a similar function of unwriting, but it actually write the labels
# + I'd like a delay be added before each writing effect
def writing_effect(label, text, root, on_finish, delay=16, start_delay=500):
    def step(i):
        label.config(text=text[:i])
        if i <= len(text):
            root.after(delay, lambda: step(i + 1))
        else:
            if on_finish:
                on_finish()
    if start_delay > 0:
        root.after(start_delay, lambda: step(1))
    else:
        step(1)


# Prompt: I'd like any button can be clicked just one time in this code
def disable_all_buttons(root):
    for widget in root.winfo_children():
        # Prompt: I'd like the disable_all_buttons, also works on tk.Entry
        if isinstance(widget, (tk.Button, tk.Entry)):
            widget.config(state="disabled")
        elif isinstance(widget, tk.Frame):
            disable_all_buttons(widget)