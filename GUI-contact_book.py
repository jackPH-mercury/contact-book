"""
Enhanced GUI Contact Book Application (Tkinter + ttk)
----------------------------------------------------
Adds:
- Editable contact form (no popups)
- Modernized UI using ttk
- Inline search bar
- Cleaner layout
"""

import json
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "contacts.json"

# -----------------------------
# File Handling Functions
# -----------------------------

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

# -----------------------------
# Validation Functions
# -----------------------------

def is_valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))


def is_valid_phone(phone):
    return phone.isdigit()


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

# -----------------------------
# GUI Application
# -----------------------------

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("700x450")

        self.contacts = load_contacts()
        self.selected_index = None

        style = ttk.Style()
        style.theme_use("clam")

        # Search bar
        search_frame = ttk.Frame(root)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=5)

        # Main layout
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Contact list
        self.tree = ttk.Treeview(main_frame, columns=("Phone", "Email"), show="headings")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(side="right", fill="y", padx=10)

        ttk.Label(form_frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=0, pady=5)

        ttk.Label(form_frame, text="Phone").grid(row=2, column=0, sticky="w")
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=3, column=0, pady=5)

        ttk.Label(form_frame, text="Email").grid(row=4, column=0, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=5, column=0, pady=5)

        ttk.Label(form_frame, text="Address").grid(row=6, column=0, sticky="w")
        self.address_entry = ttk.Entry(form_frame)
        self.address_entry.grid(row=7, column=0, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, pady=10)

        ttk.Button(btn_frame, text="Add New", command=self.add_contact).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_contact).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5)

        self.refresh_list()

    def refresh_list(self, contacts=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = contacts if contacts is not None else self.contacts
        for i, c in enumerate(data):
            self.tree.insert("", "end", iid=i, values=(c["phone"], c["email"]), text=c["name"])

    def get_form_data(self):
        return {
            "name": self.name_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "address": self.address_entry.get().strip()
        }

    def validate(self, data):
        if not is_valid_name(data["name"]):
            messagebox.showerror("Error", "Invalid name")
            return False
        if not is_valid_phone(data["phone"]):
            messagebox.showerror("Error", "Invalid phone")
            return False
        if not is_valid_email(data["email"]):
            messagebox.showerror("Error", "Invalid email")
            return False
        return True

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.selected_index = None

    def add_contact(self):
        data = self.get_form_data()
        if not self.validate(data):
            return

        self.contacts.append(data)
        save_contacts(self.contacts)
        self.refresh_list()
        self.clear_form()

    def update_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Select a contact first")
            return

        data = self.get_form_data()
        if not self.validate(data):
            return

        self.contacts[self.selected_index] = data
        save_contacts(self.contacts)
        self.refresh_list()

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Select a contact first")
            return

        self.contacts.pop(self.selected_index)
        save_contacts(self.contacts)
        self.refresh_list()
        self.clear_form()

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = int(selected[0])
        self.selected_index = index
        contact = self.contacts[index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, contact["name"])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, contact["phone"])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, contact["email"])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, contact["address"])

    def update_search(self, *args):
        query = self.search_var.get().lower()
        filtered = [c for c in self.contacts if query in c["name"].lower()]
        self.refresh_list(filtered)

# -----------------------------
# Entry Point
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
