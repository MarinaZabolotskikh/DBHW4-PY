import psycopg2

def del_number_phone_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE client_number_phones;
                """)

def del_client_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE clients;
                """)

def create_client_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    surname VARCHAR(50) NOT NULL,
                    email VARCHAR(40) NOT NULL
                    );
                """)

def create_number_phone_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS client_number_phones (
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(20),
                    clients_id INTEGER NOT NULL REFERENCES clients(id)
                    );
                """)

def add_new_client(conn, id, name, surname, email):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO clients (id, name, surname, email) VALUES (%s, %s, %s, %s) RETURNING id;
                """, (id, name, surname, email))
        cur.fetchone()
        print("Новый клиент добавлен")

def add_phone_client(conn, id, phone, clients_id):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO client_number_phones (id, phone, clients_id) VALUES (%s, %s, %s) RETURNING id;
                """, (id, phone, clients_id))
        cur.fetchone()
        print(f"Телефон клиента с номером id: {clients_id} добавлен")

def data_change_name(conn, new_name, id):
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE clients
                    SET name = %s
                    WHERE id = %s;
                """, (new_name, id))
        print(f"Имя клиента с номером id: {id} изменено на {new_name}")

def data_change_surname(conn, new_surname, id):
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE clients
                    SET surname = %s
                    WHERE id = %s;
                """, (new_surname, id))
        print(f"Фамилия клиента с номером id: {id} изменена на {new_surname}")

def data_change_email(conn, new_email, id):
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE clients
                    SET email = %s
                    WHERE id = %s;
                """, (new_email, id))
        print(f"Адрес почты клиента с номером id: {id} изменентна {new_email}")

def data_change_phone(conn, new_phone, clients_id):
    with conn.cursor() as cur:
        cur.execute("""
                UPDATE client_number_phones
                    SET phone = %s
                    WHERE clients_id = %s;
                """, (new_phone, clients_id))
        print(f"Номер телефона клиента с номером id: {clients_id} изменен на {new_phone}")

def del_phone_client(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client_number_phones
                    WHERE phone = %s;
                """, (phone,))
        print(f"{phone} удален")

def del_all_phones_client(conn, clients_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client_number_phones
                    WHERE clients_id = %s;
                """, (clients_id,))

def del_client(conn, clients_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM client
                    WHERE id = %s;
                """, (clients_id,))

def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT * FROM clients c
                    JOIN client_number_phones cn ON c.id = cn.clients_id
                    WHERE name = %s OR surname = %s OR email = %s OR phone = %s;
                """, (name, surname, email, phone))
        print(cur.fetchall())

with psycopg2.connect(database="DB-clients", user="postgres", password="") as conn:
    # del_number_phone_table(conn)
    # del_client_table(conn)
    create_client_table(conn)
    create_number_phone_table(conn)
    # add_new_client(conn, 1, "Ivan", "Petrov", "ivanpetrov@mail.ru")
    # add_new_client(conn, 2, "Petr", "Ivanov", "petrivanov@mail.ru")
    # add_new_client(conn, 3, "Maria", "Sidorova", "mariasid@mail.ru")
    # add_new_client(conn, 4, "Anna", "Fedorova", "annaf@mail.ru")
    # add_new_client(conn, 5, "Inna", "Golubeva", "innag@mail.ru")
    # add_phone_client(conn, 1, 89219212121, 1)
    # add_phone_client(conn, 2, 89219212123, 1)
    # add_phone_client(conn, 3, 89119895231, 2)
    # add_phone_client(conn, 4, 89239212151, 3)
    # add_phone_client(conn, 1, 89219212121, 1)
    # add_phone_client(conn, 5, 89216312121, 3)
    # add_phone_client(conn, 6, 89116312121, 5)
    # del_phone_client(conn, "89119895231")
    # del_all_phones_client(conn, 1)
    # del_client(conn, clients_id)
    # find_client(conn, "Ivan", surname=None, email=None, phone=None)
    # find_client(conn, name=None, surname="Ivanov", email=None, phone=None)
    # find_client(conn, name=None, surname=None, email="mariasid@mail.ru", phone=None)
    # data_change_name(conn, "Natalia", 5)
    # data_change_surname(conn, "Kozlov", 1)
    # data_change_email(conn, "nata@mail", 5)
    # data_change_phone(conn, "89826547893", 1)
    conn.commit()
conn.close()

