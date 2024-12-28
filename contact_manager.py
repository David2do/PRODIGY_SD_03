import json
import streamlit as st

CONTACTS_FILE = "contacts.json"

def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

def add_contact(contacts, name, phone, email):
    if name in contacts:
        st.error("Contact already exists.")
    else:
        contacts[name] = {"phone": phone, "email": email}
        save_contacts(contacts)
        st.success("Contact added successfully.")

def edit_contact(contacts, name, phone, email):
    if name in contacts:
        if phone:
            contacts[name]["phone"] = phone
        if email:
            contacts[name]["email"] = email
        save_contacts(contacts)
        st.success("Contact updated successfully.")
    else:
        st.error("Contact not found.")

def delete_contact(contacts, name):
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        st.success("Contact deleted successfully.")
    else:
        st.error("Contact not found.")

def main():
    st.set_page_config(
        page_title="Contact Manager App",  # Title of the web page
        page_icon="📇",
        layout="centered",
    )
    st.title("Contact Manager")

    contacts = load_contacts()

    menu = ["Add Contact", "View Contacts", "Edit Contact", "Delete Contact"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Contact":
        st.subheader("Add Contact")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        if st.button("Add"):
            add_contact(contacts, name, phone, email)

    elif choice == "View Contacts":
        st.subheader("View Contacts")
        if not contacts:
            st.info("No contacts found.")
        else:
            for name, info in contacts.items():
                st.write(f"**Name**: {name}")
                st.write(f"**Phone**: {info['phone']}")
                st.write(f"**Email**: {info['email']}")
                st.write("---")

    elif choice == "Edit Contact":
        st.subheader("Edit Contact")
        name = st.text_input("Enter the name of the contact to edit")
        if name in contacts:
            phone = st.text_input("New Phone", value=contacts[name]["phone"])
            email = st.text_input("New Email", value=contacts[name]["email"])
            if st.button("Update"):
                edit_contact(contacts, name, phone, email)
        else:
            st.info("Enter a valid contact name to edit.")

    elif choice == "Delete Contact":
        st.subheader("Delete Contact")
        name = st.text_input("Enter the name of the contact to delete")
        if st.button("Delete"):
            delete_contact(contacts, name)

if __name__ == "__main__":
    main()
