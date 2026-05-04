import csv
import json
from connect import get_connection


def setup_database():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with open("schema.sql", "r", encoding="utf-8") as file:
                    cur.execute(file.read())

                with open("procedures.sql", "r", encoding="utf-8") as file:
                    cur.execute(file.read())

            conn.commit()

        print("Database setup completed.")

    except Exception as e:
        print("Error:", e)


def get_group_id(cur, group_name):
    cur.execute(
        """
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    return cur.fetchone()[0]


def add_contact():
    username = input("Enter name: ").strip()
    email = input("Enter email: ").strip()
    birthday = input("Enter birthday YYYY-MM-DD: ").strip()
    group_name = input("Enter group Family/Work/Friend/Other: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter phone type home/work/mobile: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                group_id = get_group_id(cur, group_name)

                cur.execute(
                    """
                    INSERT INTO contacts(username, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE
                    SET email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id
                    """,
                    (username, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    """,
                    (contact_id, phone, phone_type)
                )

            conn.commit()

        print("Contact added successfully.")

    except Exception as e:
        print("Error:", e)


def show_all_contacts():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.username, c.email, c.birthday, g.name, p.phone, p.type
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    ORDER BY c.username
                    """
                )

                rows = cur.fetchall()

                if not rows:
                    print("No contacts found.")
                    return

                for row in rows:
                    print(row)

    except Exception as e:
        print("Error:", e)


def filter_by_group():
    group_name = input("Enter group name: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.username, c.email, c.birthday, g.name, p.phone, p.type
                    FROM contacts c
                    JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    WHERE g.name ILIKE %s
                    ORDER BY c.username
                    """,
                    (group_name,)
                )

                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as e:
        print("Error:", e)


def search_by_email():
    query = input("Enter email part: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT username, email, birthday
                    FROM contacts
                    WHERE email ILIKE %s
                    """,
                    (f"%{query}%",)
                )

                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as e:
        print("Error:", e)


def advanced_search():
    query = input("Search name/email/phone/group: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM search_contacts(%s)",
                    (query,)
                )

                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as e:
        print("Error:", e)


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ").strip()

    allowed = {
        "1": "username",
        "2": "birthday",
        "3": "date_added"
    }

    sort_column = allowed.get(choice)

    if not sort_column:
        print("Invalid choice.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT c.username, c.email, c.birthday, c.date_added, g.name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY {sort_column}
                    """
                )

                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as e:
        print("Error:", e)


def paginated_navigation():
    try:
        limit = int(input("Enter page size: "))
        offset = 0

        while True:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT c.username, c.email, c.birthday, g.name
                        FROM contacts c
                        LEFT JOIN groups g ON c.group_id = g.id
                        ORDER BY c.username
                        LIMIT %s OFFSET %s
                        """,
                        (limit, offset)
                    )

                    rows = cur.fetchall()

                    print("\n--- Page ---")

                    if not rows:
                        print("No records on this page.")
                    else:
                        for row in rows:
                            print(row)

            command = input("\nnext / prev / quit: ").strip().lower()

            if command == "next":
                offset += limit
            elif command == "prev":
                offset = max(0, offset - limit)
            elif command == "quit":
                break
            else:
                print("Invalid command.")

    except Exception as e:
        print("Error:", e)


def add_phone_to_contact():
    name = input("Enter contact name: ").strip()
    phone = input("Enter phone: ").strip()
    phone_type = input("Enter type home/work/mobile: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (name, phone, phone_type)
                )

            conn.commit()

        print("Phone added.")

    except Exception as e:
        print("Error:", e)


def move_contact_to_group():
    name = input("Enter contact name: ").strip()
    group_name = input("Enter new group: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL move_to_group(%s, %s)",
                    (name, group_name)
                )

            conn.commit()

        print("Contact moved to group.")

    except Exception as e:
        print("Error:", e)


def export_to_json():
    filename = input("Enter JSON filename: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT 
                        c.id,
                        c.username,
                        c.email,
                        c.birthday,
                        c.date_added,
                        g.name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    ORDER BY c.id
                    """
                )

                contacts = cur.fetchall()
                result = []

                for contact in contacts:
                    contact_id = contact[0]

                    cur.execute(
                        """
                        SELECT phone, type
                        FROM phones
                        WHERE contact_id = %s
                        """,
                        (contact_id,)
                    )

                    phones = cur.fetchall()

                    result.append({
                        "name": contact[1],
                        "email": contact[2],
                        "birthday": str(contact[3]) if contact[3] else None,
                        "date_added": str(contact[4]),
                        "group": contact[5],
                        "phones": [
                            {
                                "phone": p[0],
                                "type": p[1]
                            }
                            for p in phones
                        ]
                    })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print("Export completed.")

    except Exception as e:
        print("Error:", e)


def import_from_json():
    filename = input("Enter JSON filename: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        with get_connection() as conn:
            with conn.cursor() as cur:
                for contact in contacts:
                    name = contact["name"]

                    cur.execute(
                        "SELECT id FROM contacts WHERE username = %s",
                        (name,)
                    )

                    existing = cur.fetchone()

                    if existing:
                        answer = input(
                            f"Contact {name} already exists. skip/overwrite: "
                        ).strip().lower()

                        if answer == "skip":
                            continue

                        if answer == "overwrite":
                            cur.execute(
                                "DELETE FROM contacts WHERE username = %s",
                                (name,)
                            )

                    group_id = get_group_id(cur, contact.get("group") or "Other")

                    cur.execute(
                        """
                        INSERT INTO contacts(username, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            contact["name"],
                            contact.get("email"),
                            contact.get("birthday"),
                            group_id
                        )
                    )

                    contact_id = cur.fetchone()[0]

                    for phone in contact.get("phones", []):
                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                contact_id,
                                phone["phone"],
                                phone["type"]
                            )
                        )

            conn.commit()

        print("JSON import completed.")

    except Exception as e:
        print("Error:", e)


def import_from_csv():
    filename = input("Enter CSV filename: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        group_id = get_group_id(cur, row["group"])

                        cur.execute(
                            """
                            INSERT INTO contacts(username, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (username) DO UPDATE
                            SET email = EXCLUDED.email,
                                birthday = EXCLUDED.birthday,
                                group_id = EXCLUDED.group_id
                            RETURNING id
                            """,
                            (
                                row["name"],
                                row["email"],
                                row["birthday"],
                                group_id
                            )
                        )

                        contact_id = cur.fetchone()[0]

                        cur.execute(
                            """
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            """,
                            (
                                contact_id,
                                row["phone"],
                                row["phone_type"]
                            )
                        )

                conn.commit()

        print("CSV import completed.")

    except Exception as e:
        print("Error importing CSV:", e)


def menu():
    while True:
        print("\n===== TSIS 1 PhoneBook =====")
        print("1. Filter by group")
        print("2. Search by email")
        print("3. Sort contacts")
        print("4. Export contacts to JSON")
        print("5. Import contacts from JSON")
        print("6. Add phone")
        print("7. Move contact to group")
        print("8. Advanced search")
        print("0. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_by_email()
        elif choice == "3":
            sort_contacts()
        elif choice == "4":
            export_to_json()
        elif choice == "5":
            import_from_json()
        elif choice == "6":
            add_phone_to_contact()
        elif choice == "7":
            move_contact_to_group()
        elif choice == "8":
            advanced_search()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


print("PROGRAM STARTED")

if __name__ == "__main__":
    menu()