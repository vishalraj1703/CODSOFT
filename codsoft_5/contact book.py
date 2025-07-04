import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("contacts.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT
)''')
conn.commit()

# --- GUI Setup ---
root = tk.Tk()
root.title("Contact Book")
root.geometry("700x500")
root.configure(bg="#e6f2ff")

HEADER_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 12)

# --- Frames ---
main_frame = tk.Frame(root, bg="#e6f2ff")
main_frame.pack(fill="both", expand=True)

# --- Functions ---
def show_frame(frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    frame()

def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()
    address = address_var.get()

    if name and phone:
        c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                  (name, phone, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully")
        show_frame(home_screen)
    else:
        messagebox.showerror("Error", "Name and Phone are required")

def view_contacts():
    show_frame(display_contacts)

def delete_contact():
    selected = contact_list.selection()
    if selected:
        contact_id = contact_list.item(selected[0])['values'][0]
        c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Contact deleted")
        display_contacts()

def load_contacts():
    contact_list.delete(*contact_list.get_children())
    for row in c.execute("SELECT * FROM contacts"):
        contact_list.insert("", "end", values=row)

def update_contact():
    selected = contact_list.selection()
    if selected:
        global update_id
        update_id = contact_list.item(selected[0])['values'][0]
        row = c.execute("SELECT * FROM contacts WHERE id=?", (update_id,)).fetchone()
        show_frame(update_screen)
        name_var.set(row[1])
        phone_var.set(row[2])
        email_var.set(row[3])
        address_var.set(row[4])

def save_update():
    c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
              (name_var.get(), phone_var.get(), email_var.get(), address_var.get(), update_id))
    conn.commit()
    messagebox.showinfo("Updated", "Contact updated successfully")
    show_frame(display_contacts)

def search_contacts():
    keyword = search_var.get()
    query = f"SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?"
    results = c.execute(query, (f"%{keyword}%", f"%{keyword}%")).fetchall()
    contact_list.delete(*contact_list.get_children())
    for row in results:
        contact_list.insert("", "end", values=row)

# --- Screens ---
def home_screen():
    tk.Label(main_frame, text="Contact Book", font=HEADER_FONT, bg="#e6f2ff", fg="#003366").pack(pady=20)
    
    tk.Button(main_frame, text="Add Contact", font=LABEL_FONT, bg="#99ccff", width=20, command=lambda: show_frame(add_screen)).pack(pady=10)
    tk.Button(main_frame, text="View Contacts", font=LABEL_FONT, bg="#99ccff", width=20, command=view_contacts).pack(pady=10)
    tk.Button(main_frame, text="Search Contact", font=LABEL_FONT, bg="#99ccff", width=20, command=lambda: show_frame(search_screen)).pack(pady=10)
    tk.Button(main_frame, text="Exit", font=LABEL_FONT, bg="#ff6666", width=20, command=root.destroy).pack(pady=20)

def add_screen():
    tk.Label(main_frame, text="Add New Contact", font=HEADER_FONT, bg="#e6f2ff").pack(pady=10)
    
    form_frame = tk.Frame(main_frame, bg="#e6f2ff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:", font=LABEL_FONT, bg="#e6f2ff").grid(row=0, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=name_var).grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Phone:", font=LABEL_FONT, bg="#e6f2ff").grid(row=1, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=phone_var).grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Email:", font=LABEL_FONT, bg="#e6f2ff").grid(row=2, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=email_var).grid(row=2, column=1, pady=5)

    tk.Label(form_frame, text="Address:", font=LABEL_FONT, bg="#e6f2ff").grid(row=3, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=address_var).grid(row=3, column=1, pady=5)

    tk.Button(main_frame, text="Save", bg="#66cc66", command=add_contact).pack(pady=10)
    tk.Button(main_frame, text="Back to Home", command=lambda: show_frame(home_screen)).pack()

def display_contacts():
    tk.Label(main_frame, text="All Contacts", font=HEADER_FONT, bg="#e6f2ff").pack(pady=10)

    global contact_list
    contact_list = ttk.Treeview(main_frame, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
    contact_list.heading("ID", text="ID")
    contact_list.heading("Name", text="Name")
    contact_list.heading("Phone", text="Phone")
    contact_list.heading("Email", text="Email")
    contact_list.heading("Address", text="Address")
    contact_list.pack(fill="both", expand=True)
    load_contacts()

    tk.Button(main_frame, text="Update", bg="#ffff66", command=update_contact).pack(pady=5)
    tk.Button(main_frame, text="Delete", bg="#ff6666", command=delete_contact).pack(pady=5)
    tk.Button(main_frame, text="Back to Home", command=lambda: show_frame(home_screen)).pack(pady=10)

def update_screen():
    tk.Label(main_frame, text="Update Contact", font=HEADER_FONT, bg="#e6f2ff").pack(pady=10)

    form_frame = tk.Frame(main_frame, bg="#e6f2ff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:", font=LABEL_FONT, bg="#e6f2ff").grid(row=0, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=name_var).grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Phone:", font=LABEL_FONT, bg="#e6f2ff").grid(row=1, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=phone_var).grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Email:", font=LABEL_FONT, bg="#e6f2ff").grid(row=2, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=email_var).grid(row=2, column=1, pady=5)

    tk.Label(form_frame, text="Address:", font=LABEL_FONT, bg="#e6f2ff").grid(row=3, column=0, sticky="e")
    tk.Entry(form_frame, textvariable=address_var).grid(row=3, column=1, pady=5)

    tk.Button(main_frame, text="Save Changes", bg="#66cc66", command=save_update).pack(pady=10)
    tk.Button(main_frame, text="Back to Home", command=lambda: show_frame(home_screen)).pack()

def search_screen():
    tk.Label(main_frame, text="Search Contacts", font=HEADER_FONT, bg="#e6f2ff").pack(pady=10)
    
    tk.Entry(main_frame, textvariable=search_var, width=40).pack(pady=5)
    tk.Button(main_frame, text="Search", bg="#99ccff", command=search_contacts).pack(pady=5)

    global contact_list
    contact_list = ttk.Treeview(main_frame, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
    contact_list.heading("ID", text="ID")
    contact_list.heading("Name", text="Name")
    contact_list.heading("Phone", text="Phone")
    contact_list.heading("Email", text="Email")
    contact_list.heading("Address", text="Address")
    contact_list.pack(fill="both", expand=True)

    tk.Button(main_frame, text="Back to Home", command=lambda: show_frame(home_screen)).pack(pady=10)


name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()
search_var = tk.StringVar()


show_frame(home_screen)
root.mainloop()
conn.close()
