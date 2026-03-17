"""
Console Contact Book Application
--------------------------------
A text-based contact manager that stores contacts in a JSON file.
"""

import json
import os
import re

DATA_FILE = "contacts.json"

# -----------------------------
# File Handling Functions
# -----------------------------

def load_contacts():
    """Load contacts from JSON file. If file doesn't exist, return empty list."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
         # Open file in read mode
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    # Handle possible errors like corrupted JSON or read failure
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, start fresh
        return []


def save_contacts(contacts):
    """Save contacts list to JSON file with readable formatting."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        #Convert Python list into formatted JSON text
        json.dump(contacts, file, indent=4)


# -----------------------------
# Validation Functions
# -----------------------------

def is_valid_name(name):
    """Name must contain only letters and spaces."""
    return bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))


def is_valid_phone(phone):
    """Phone must contain digits only (no spaces or symbols)."""
    return phone.isdigit()


def is_valid_email(email):
    """Basic email validation pattern."""
    pattern = r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))


# -----------------------------
# Core Features
# -----------------------------

def add_contact(contacts):
    """Add a new contact after validating user input."""
    print("\n--- Add New Contact ---")
     # Get and validate name
    name = input("Name: ").strip()
    if not is_valid_name(name):
        print("Error: Name must contain letters and spaces only.")
        return

     # Get and validate phone number
    phone = input("Phone (digits only): ").strip()
    if not is_valid_phone(phone):
        print("Error: Phone number must contain digits only.")
        return
    # Get and validate email adress
    email = input("Email: ").strip()
    if not is_valid_email(email):
        print("Error: Invalid email format.")
        return

    address = input("Address: ").strip()

    # Store contact data in a dictionary (key-value pairs)
    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully.")



def view_contacts(contacts):
    """Display all contacts in a readable list."""
    print("\n--- Contact List ---")

     # If list is empty, inform the user
    if not contacts:
        print("No contacts found.")
        return

     # enumerate gives both index and value while looping
    for i, contact in enumerate(contacts, start=1):
        print(f"\nContact #{i}")
        print(f"Name   : {contact['name']}")
        print(f"Phone  : {contact['phone']}")
        print(f"Email  : {contact['email']}")
        print(f"Address: {contact['address']}")



def delete_contact(contacts):
    """Delete a contact by name."""
    print("\n--- Delete Contact ---")
    name = input("Enter name to delete: ").strip()

     # Loop through contact list to find a match
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            contacts.remove(contact)
            save_contacts(contacts)
            print("Contact deleted successfully.")
            return

    print("Contact not found.")



def search_contact(contacts):
    """Search for contacts by name (partial matches allowed)."""
    print("\n--- Search Contact ---")
    name = input("Enter name to search: ").strip().lower()

    # List comprehension builds a list of matching contacts
    matches = [c for c in contacts if name in c['name'].lower()]

    if not matches:
        print("No matching contacts found.")
        return

    # Display each matching contact
    for contact in matches:
        print("\nMatch Found:")
        print(f"Name   : {contact['name']}")
        print(f"Phone  : {contact['phone']}")
        print(f"Email  : {contact['email']}")
        print(f"Address: {contact['address']}")


# -----------------------------
# Menu System
# -----------------------------

def display_menu():
    """Display user options."""
    print("\n====== Contact Book Menu ======")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")


 # Load saved contacts when program starts
def main():
    """Main program loop."""
    contacts = load_contacts()
    
    # Infinite loop keeps menu running
    while True:
        display_menu()
         # Get user menu selection
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


# -----------------------------
# Program Entry Point
# -----------------------------

if __name__ == "__main__":
    main()