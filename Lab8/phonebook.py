import psycopg2
from config import load_config


def get_connection():
    config = load_config()
    return psycopg2.connect(**config)


def upsert_contact():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
            conn.commit()
        print("Upsert completed.")
    except Exception as error:
        print("Error:", error)


def search_contacts():
    pattern = input("Enter search pattern: ")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
    except Exception as error:
        print("Error:", error)


def insert_many_users():
    usernames = input("Enter usernames separated by comma: ").split(",")
    phones = input("Enter phones separated by comma: ").split(",")

    usernames = [u.strip() for u in usernames]
    phones = [p.strip() for p in phones]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
            conn.commit()
        print("Bulk insert completed.")
    except Exception as error:
        print("Error:", error)


def get_paginated_contacts():
    limit_value = int(input("Enter limit: "))
    offset_value = int(input("Enter offset: "))

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s)",
                    (limit_value, offset_value)
                )
                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")
    except Exception as error:
        print("Error:", error)


def delete_contact():
    value = input("Enter username or phone to delete: ")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (value,))
            conn.commit()
        print("Delete completed.")
    except Exception as error:
        print("Error:", error)


def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1. Upsert contact")
        print("2. Search contacts by pattern")
        print("3. Insert many users")
        print("4. Get contacts with pagination")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            upsert_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            insert_many_users()
        elif choice == "4":
            get_paginated_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()