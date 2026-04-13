import psycopg2
import csv
from config import load_config

def get_connection():
    config = load_config()
    return psycopg2.connect(**config)

def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("Table created successfully.")

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    sql = "INSERT INTO phonebook (username, phone) VALUES (%s, %s)"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (username, phone))
        conn.commit()
    print("Contact added successfully.")

def insert_from_csv(filename):
    sql = "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING"
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        cur.execute(sql, (row[0], row[1]))
        conn.commit()
    print("CSV data imported successfully.")

def update_contact():
    choice = input("Update by (1) username or (2) phone? ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                old_username = input("Enter current username: ")
                new_username = input("Enter new username: ")
                cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_username, old_username))
            elif choice == "2":
                old_phone = input("Enter current phone: ")
                new_phone = input("Enter new phone: ")
                cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
        conn.commit()
    print("Contact updated successfully.")

def query_contacts():
    print("1 - Show all contacts")
    print("2 - Search by username")
    print("3 - Search by phone prefix")
    choice = input("Choose filter: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                cur.execute("SELECT * FROM phonebook ORDER BY id")
            elif choice == "2":
                name = input("Enter username: ")
                cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s", (f"%{name}%",))
            elif choice == "3":
                prefix = input("Enter phone prefix: ")
                cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f"{prefix}%",))
            rows = cur.fetchall()
            for row in rows:
                print(row)

def delete_contact():
    choice = input("Delete by (1) username or (2) phone? ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == "1":
                username = input("Enter username to delete: ")
                cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))
            elif choice == "2":
                phone = input("Enter phone to delete: ")
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        conn.commit()
    print("Contact deleted successfully.")

def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update contact")
        print("5. Query contacts")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()