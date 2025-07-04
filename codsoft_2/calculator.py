import tkinter as tk
from tkinter import messagebox

def press(symbol):
    current = entry_var.get()
    entry_var.set(current + str(symbol))

def calculate():
    try:
        result = str(eval(entry_var.get()))
        entry_var.set(result)
    except ZeroDivisionError:
        messagebox.showerror("Error", "Division by zero is not allowed.")
    except:
        messagebox.showerror("Error", "Invalid expression.")


def clear():
    entry_var.set("")


def backspace():
    entry_var.set(entry_var.get()[:-1])


root = tk.Tk()
root.title("Simple Calculator")
root.geometry("400x650")
root.resizable(False, False)
root.configure(bg="#2d2d2d")

entry_var = tk.StringVar()


entry = tk.Entry(root, textvariable=entry_var, font=('Arial', 24), bd=10, insertwidth=2,
                 width=14, borderwidth=4, relief='sunken', justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20)


buttons = [
    ('C', 1, 0, clear, "#d9534f"),
    ('←', 1, 1, backspace, "#f0ad4e"),
    ('%', 1, 2, lambda: press('%'), "#5bc0de"),
    ('/', 1, 3, lambda: press('/'), "#0275d8"),

    ('7', 2, 0, lambda: press('7')),
    ('8', 2, 1, lambda: press('8')),
    ('9', 2, 2, lambda: press('9')),
    ('*', 2, 3, lambda: press('*'), "#0275d8"),

    ('4', 3, 0, lambda: press('4')),
    ('5', 3, 1, lambda: press('5')),
    ('6', 3, 2, lambda: press('6')),
    ('-', 3, 3, lambda: press('-'), "#0275d8"),

    ('1', 4, 0, lambda: press('1')),
    ('2', 4, 1, lambda: press('2')),
    ('3', 4, 2, lambda: press('3')),
    ('+', 4, 3, lambda: press('+'), "#0275d8"),

    ('0', 5, 0, lambda: press('0')),
    ('.', 5, 1, lambda: press('.')),
    ('=', 5, 2, calculate, "#5cb85c"),
]


for (text, row, col, command, *color) in buttons:
    btn_color = color[0] if color else "#f7f7f7"
    tk.Button(
        root, text=text, padx=20, pady=20, bd=4, fg="black", bg=btn_color,
        font=('Arial', 18), command=command
    ).grid(row=row, column=col, padx=5, pady=5)


tk.Button(root, text='=', padx=20, pady=20, bd=4, fg="white", bg="#5cb85c",
          font=('Arial', 18), command=calculate).grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky='we')


root.mainloop()
