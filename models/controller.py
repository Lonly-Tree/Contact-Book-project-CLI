from sql.db_manager import Manger_data_base, initialize_database
from models.person import person_data


initialize_database()


class ContactController:
    def __init__(self):
        self.db = Manger_data_base()

    def add_contact(self, name, phone, categories=None):
        person = person_data(name=name, phone=phone)
        success = self.db.add_person(data=person)
        if success:
            result = self.db.search_by_data_for_person(person=person, field="phone")
            if result:
                person.id = result[0].id
                for category in categories:
                    self.db.add_relationship(person=person, relation=category)

            return True
        return False

    def get_all_contacts(self):
        return self.db.get_all_data_from_contacts()

    def get_person(self, id):
        person = self.db.search_by_data_for_person(field="id", id=id)
        if person:
            return person[0]
        return False

    def delete_contact_by_name(self, name):
        search_result = self.db.search_by_data_for_person(
            person=person_data(name=name), field="name"
        )
        if search_result:
            for person in search_result:
                self.db.delete_person(person)
            return True
        return False

    def delete_contact_by_phone(self, phone):
        search_result = self.db.search_by_data_for_person(
            person=person_data(phone=phone), field="phone"
        )
        if search_result:
            for person in search_result:
                self.db.delete_person(person)
            return True
        return False

    def delete_contact_by_id(self, id):
        search_result = self.db.search_by_data_for_person(field="id", id=id)
        if search_result:
            for person in search_result:
                self.db.delete_person(person)
            return True
        return False

    def search_by_name(self, name):
        return self.db.search_by_data_for_person(
            person=person_data(name=name), field="name"
        )

    def search_by_phone(self, phone):
        return self.db.search_by_data_for_person(
            person=person_data(phone=phone), field="phone"
        )

    def search_by_id(self, id):
        return self.db.search_by_data_for_person(field="id", id=id)

    def search_by_category(self, category):
        return self.db.search_By_category(type=category)

    def update_contact(self, id, new_name=None, new_phone=None):
        person = person_data()
        person.id = id
        return self.db.update_person(person=person, name=new_name, phone=new_phone)

    def add_relation(self, Person_id, relation: str):

        result = self.db.search_by_data_for_person(field="id", id=Person_id)

        if result:
            result_person = result[0]
            done = self.db.add_relationship(person=result_person, relation=relation)

            if not done:
                return False
            return True
        return False

    def update_relation(self, relation_name, person_id, new_relation):
        result = self.db.search_by_data_for_person(field="id", id=person_id)

        if result:
            result_person = result[0]
            done = self.db.update_relationship(
                person=result_person,
                relation_name=relation_name,
                new_relation=new_relation,
            )
            if not done:
                return False
            return True
        return False

    def delete_relation(self, relation_name, person_id):
        result = self.db.search_by_data_for_person(field="id", id=person_id)

        if result:
            result_person = result[0]
            done = self.db.delete_relation(
                person=result_person, relation_name=relation_name
            )
            if not done:
                return False
            return True
        return False
