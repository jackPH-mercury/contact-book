"""
Enhanced GUI Contact Book Application (Tkinter + ttk)
----------------------------------------------------

"""

import json
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Default file used to store contacts
DATA_FILE = "contacts.json"

# -----------------------------
# File Handling Functions
# -----------------------------

def load_contacts():
    """
    Load contacts from the current DATA_FILE.
    Returns an empty list if file doesn't exist or is corrupted.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def save_contacts(contacts):
    """
    Save the contact list back to the current DATA_FILE.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

# -----------------------------
# Validation Functions
# -----------------------------

def is_valid_name(name):
    """Ensure name contains only letters and spaces."""
    return bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))


def is_valid_phone(phone):
    """Ensure phone contains only digits."""
    return phone.isdigit()


def is_valid_email(email):
    """Basic email validation using regex."""
    pattern = r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

# -----------------------------
# GUI Application
# -----------------------------

class ContactApp:
    def __init__(self, root):
        """Build UI and initialize app state."""
        self.root = root
        self.root.title("Contact Book")

        # Allow window resizing
        self.root.geometry("700x450")
        self.root.minsize(600, 400)

        # Configure root grid so child frames expand
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Load contacts from default file
        self.contacts = load_contacts()

        # Track which contact is selected in the UI
        self.selected_index = None

        # Apply a nicer theme
        style = ttk.Style()
        style.theme_use("clam")

        # -----------------------------
        # Menu Bar (NEW)
        # -----------------------------
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

        # -----------------------------
        # Search Bar
        # -----------------------------
        search_frame = ttk.Frame(root)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="w")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search)

        ttk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=5)

        # -----------------------------
        # Main Layout
        # -----------------------------
        main_frame = ttk.Frame(root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Allow resizing behavior
        main_frame.columnconfigure(0, weight=3)  # list
        main_frame.columnconfigure(1, weight=2)  # form
        main_frame.rowconfigure(0, weight=1)

        # -----------------------------
        # Contact List (Treeview)
        # -----------------------------
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Phone", "Email"),
            show="headings"
        )

        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")

        self.tree.grid(row=0, column=0, sticky="nsew")

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=0, sticky="nse")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # -----------------------------
        # Form (Right Side)
        # -----------------------------
        form_frame = ttk.Frame(main_frame, padding=10)
        form_frame.grid(row=0, column=1, sticky="nsew")

        form_frame.columnconfigure(0, weight=1)

        # Name
        ttk.Label(form_frame, text="Name").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=3)

        # Phone
        ttk.Label(form_frame, text="Phone").grid(row=2, column=0, sticky="w")
        self.phone_entry = ttk.Entry(form_frame)
        self.phone_entry.grid(row=3, column=0, sticky="ew", pady=3)

        # Email
        ttk.Label(form_frame, text="Email").grid(row=4, column=0, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=5, column=0, sticky="ew", pady=3)

        # Address
        ttk.Label(form_frame, text="Address").grid(row=6, column=0, sticky="w")
        self.address_entry = ttk.Entry(form_frame)
        self.address_entry.grid(row=7, column=0, sticky="ew", pady=3)

        # -----------------------------
        # Buttons
        # -----------------------------
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, pady=10, sticky="ew")

        # Make buttons expand evenly
        for i in range(3):
            btn_frame.columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text="Add", command=self.add_contact).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="Update", command=self.update_contact).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5, sticky="ew")

        # Populate initial data
        self.refresh_list()

    # -----------------------------
    # File Dialog Feature (NEW)
    # -----------------------------

    def open_file(self):
        """
        Open a JSON file using a file dialog and load contacts from it.
        Updates the global DATA_FILE so future saves go to this file.
        """
        global DATA_FILE

        file_path = filedialog.askopenfilename(
            title="Open Contact File",
            filetypes=[("JSON Files", "*.json")]
        )

        if not file_path:
            return  # user cancelled

        DATA_FILE = file_path  # switch active file
        self.contacts = load_contacts()  # reload from new file
        self.refresh_list()  # update UI
        self.clear_form()

    # -----------------------------
    # UI Logic Methods
    # -----------------------------

    def refresh_list(self, contacts=None):
        """Refresh the list view with current or filtered contacts."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = contacts if contacts is not None else self.contacts

        for i, c in enumerate(data):
            self.tree.insert("", "end", iid=i, values=(c["phone"], c["email"]))

    def get_form_data(self):
        """Collect data from form inputs."""
        return {
            "name": self.name_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "address": self.address_entry.get().strip()
        }

    def validate(self, data):
        """Validate user input before saving."""
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
        """Reset all form fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.selected_index = None

    # -----------------------------
    # CRUD Operations
    # -----------------------------

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
        """Populate form when a contact is selected."""
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
        """Filter contacts based on search input."""
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
