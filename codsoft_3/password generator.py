import tkinter as tk
from tkinter import messagebox
import random
import string


def check_strength(pwd):
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_symbol = any(c in string.punctuation for c in pwd)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    
    if length >= 12 and score == 4:
        return "Strong", "green"
    elif length >= 8 and score >= 3:
        return "Moderate", "orange"
    else:
        return "Weak", "red"


def generate_password():
    length = length_var.get()
    try:
        length = int(length)
        if length < 4:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number (min 4).")
        return

    chars = ''
    if use_upper.get(): chars += string.ascii_uppercase
    if use_lower.get(): chars += string.ascii_lowercase
    if use_digits.get(): chars += string.digits
    if use_symbols.get(): chars += string.punctuation

    if not chars:
        messagebox.showerror("Invalid Selection", "Please select at least one character set.")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    generated_password.set(password)
    show_strength(password, strength_label)


def show_strength(pwd, label):
    strength, color = check_strength(pwd)
    label.config(text=f"Strength: {strength}", fg=color)


def copy_to_clipboard():
    pwd = generated_password.get()
    if not pwd:
        messagebox.showwarning("No Password", "Nothing to copy.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard!")


def check_custom():
    pwd = custom_input.get()
    if not pwd:
        messagebox.showwarning("Input Required", "Please enter a password.")
        return
    show_strength(pwd, custom_strength_label)


root = tk.Tk()
root.title("Password Generator & Strength Checker")
root.geometry("450x550")
root.resizable(True, True)
root.config(bg="#f0f0f0")

length_var = tk.StringVar(value="12")
use_upper = tk.BooleanVar(value=True)
use_lower = tk.BooleanVar(value=True)
use_digits = tk.BooleanVar(value=True)
use_symbols = tk.BooleanVar(value=True)
generated_password = tk.StringVar()
custom_input = tk.StringVar()


tk.Label(root, text="🔐 Password Generator", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="Password Length:", bg="#f0f0f0").pack()
tk.Entry(root, textvariable=length_var, width=10).pack(pady=5)

tk.Checkbutton(root, text="Include Uppercase", variable=use_upper, bg="#f0f0f0").pack(anchor='w', padx=80)
tk.Checkbutton(root, text="Include Lowercase", variable=use_lower, bg="#f0f0f0").pack(anchor='w', padx=80)
tk.Checkbutton(root, text="Include Digits", variable=use_digits, bg="#f0f0f0").pack(anchor='w', padx=80)
tk.Checkbutton(root, text="Include Symbols", variable=use_symbols, bg="#f0f0f0").pack(anchor='w', padx=80)


tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", width=20).pack(pady=10)
tk.Entry(root, textvariable=generated_password, font=("Consolas", 14), width=30, justify='center').pack(pady=5)

strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12, "bold"), bg="#f0f0f0")
strength_label.pack()

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white", width=20).pack(pady=10)
tk.Label(root, text="––––––––––––––––––––––––––––––", bg="#f0f0f0").pack(pady=10)
tk.Label(root, text="🔎 Check Your Own Password", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack()

tk.Entry(root, textvariable=custom_input, font=("Consolas", 12), width=30, justify='center', show='*').pack(pady=5)

tk.Button(root, text="Check Strength", command=check_custom, bg="#9C27B0", fg="white", width=20).pack(pady=5)

custom_strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12, "bold"), bg="#f0f0f0")
custom_strength_label.pack()

root.mainloop()
