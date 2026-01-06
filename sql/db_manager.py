import sqlite3
from models.person import person_data
from pathlib import Path


def initialize_database():
    global DB_PATH
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "data" / "data_base.db"
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    cr = db.cursor()

    cr.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT  NOT NULL,
            phone TEXT UNIQUE NOT NULL
        )
        """
    )

    cr.execute(
        """
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
        UNIQUE(contact_id, type)
    )
        """
    )

    db.commit()
    cr.close()
    db.close()


initialize_database()


def connection_toDatabase(func):
    def wrapper(self, *args, **kwargs):
        try:
            db_path = DB_PATH
            connection = sqlite3.connect(db_path)
            connection.execute("PRAGMA foreign_keys = ON")
            cursor = connection.cursor()

            result = func(self, cursor, *args, **kwargs)

            connection.commit()

            # ⛔ تأكد إنك خلصت من استخدام الكورسر قبل القفل
            return result

        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            return None

        finally:
            try:
                cursor.close()
            except:
                pass
            try:
                connection.close()
            except:
                pass

    return wrapper


class Manger_data_base:
    def __init__(self):
        pass

    @connection_toDatabase
    def add_person(self, cr, data: person_data) -> bool:
        try:
            cr.execute(
                """
                INSERT INTO contacts(name, phone) VALUES (?, ?)
                    
            """,
                (
                    data.name.upper(),
                    data.phone,
                ),
            )
            return True  # "added a new person!"
        except sqlite3.IntegrityError as _:
            print("this phone number is already in use")
            return False

    @connection_toDatabase
    def add_relationship(self, cr, person: person_data, relation="others") -> bool:
        try:
            cr.execute(
                """
                    INSERT INTO relationships (contact_id, type) VALUES (?, ?)
                """,
                (
                    person.id,
                    relation.upper(),
                ),
            )
            return True  # "relationship added"

        except Exception as e:
            print(f"[!] unexcepted error  {e}")
            return False

    @connection_toDatabase
    def update_person(self, cr, person: person_data, name=None, phone=None) -> bool:
        try:
            if name == None:
                cr.execute(
                    """
                        UPDATE contacts SET phone = ? WHERE id = ?

                    """,
                    (
                        phone,
                        person.id,
                    ),
                )
            elif phone == None:
                cr.execute(
                    """
                        UPDATE contacts SET name = ? WHERE id = ?

                    """,
                    (
                        name.upper(),
                        person.id,
                    ),
                )
            else:
                cr.execute(
                    """
                        UPDATE contacts SET name = ?, phone = ? WHERE id = ?

                    """,
                    (
                        name.upper(),
                        phone,
                        person.id,
                    ),
                )
            return True
        except Exception as e:
            print(f"we got and error : {e}")
            return False

    @connection_toDatabase
    def update_relationship(
        self, cr, person: person_data, relation_name, new_relation
    ) -> bool:
        try:
            cr.execute(
                "UPDATE relationships SET type = ? WHERE type = ? AND contact_id = ?",
                (
                    new_relation.upper(),
                    relation_name.upper(),
                    person.id,
                ),
            )
            return True
        except Exception as e:
            print(f"error happened :{e}")
            return False

    #

    #

    @connection_toDatabase
    def delete_person(self, cr, person: person_data) -> bool:
        try:
            cr.execute("DELETE FROM contacts WHERE id = ?", (person.id,))
            return True  # True
        except Exception as e:
            print("can't delete this user")
            return False

    @connection_toDatabase
    def delete_relation(self, cr, person: person_data, relation_name) -> bool:
        try:
            cr.execute(
                "DELETE FROM relationships WHERE type = ? AND contact_id = ?",
                (
                    relation_name.upper(),
                    person.id,
                ),
            )
            return True
        except Exception as e:
            print(f"error happened :{e}")
            return False

    #

    # ^ get all data

    @connection_toDatabase
    def get_all_data_from_relationships(self, cr, data):
        for x in data:

            cr.execute("SELECT * FROM relationships WHERE contact_id = ? ", (x.id,))
            type_data = cr.fetchall()

            for i in type_data:
                x.category.append(i[2])
        return data

    @connection_toDatabase
    def get_all_data_from_contacts(self, cr):
        try:

            cr.execute("SELECT * FROM contacts ")
            data = cr.fetchall()

            if not data:
                print("⚠️ There are no contacts in the database yet.")
                return None

            result = []
            for row in data:
                ob = person_data(name=row[1], phone=row[2])
                ob.id = row[0]

                result.append(ob)
            return self.get_all_data_from_relationships(result)

        except Exception as e:
            print(f"there is no data yet : {e}")

    # ^ search

    @connection_toDatabase
    def search_by_data_for_person(
        self, cr, person: person_data = None, field="name", id=None
    ):
        try:
            if field == "name" and person is not None:
                cr.execute(
                    "SELECT * FROM contacts WHERE name = ?", (person.name.upper(),)
                )

            elif field == "phone" and person is not None:
                cr.execute("SELECT * FROM contacts WHERE phone = ?", (person.phone,))

            elif field == "id":
                cr.execute("SELECT * FROM contacts WHERE id = ?", (id,))

            else:
                print("❌ Unsupported search field.")
                return None

            data = cr.fetchall()
            if not data:
                print("⚠️ No match found.")
                return None

            result = []
            for row in data:
                ob = person_data(name=row[1], phone=row[2])
                ob.id = row[0]
                result.append(ob)

            return self.get_all_data_from_relationships(result)
        except Exception as e:
            print(e)

    @connection_toDatabase
    def search_By_category(self, cr, type: str):
        try:
            cr.execute(
                "SELECT contact_id FROM relationships WHERE type = ?", (type.upper(),)
            )
            data = cr.fetchall()
            result = []
            for person in data:
                p = self.search_by_data_for_person(field="id", id=person[0])
                if p is not None:
                    result.extend(p)  # عشان search_by_data بيرجع list
            return result
        except Exception as e:
            print(e)
            return []
