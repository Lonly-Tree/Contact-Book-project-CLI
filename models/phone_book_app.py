from models.controller import ContactController


class ContactAppCLI:
    def __init__(self):
        self.controller = ContactController()
        self.options = {
            "1": "work",
            "2": "friend",
            "3": "family",
            "4": "gym_rat",
            "5": "others",
        }

    def get_choice(self):
        choice = input("Choose an option: ").strip()
        return choice

    # ^ menu
    def show_search_menu(self):
        print(
            """
[1] search by name
[2] search by phone number
[3] search by id
[4] search by category
[0] Exit
"""
        )
        options = {
            "1": self.search_by_name,
            "2": self.search_by_phone,
            "3": self.search_by_id,
            "4": self.search_by_category,
        }
        choice = self.get_choice()

        if choice == "0":
            return
        elif choice in options:
            options[choice]()  # Call the selected method
        else:
            print("❌ Invalid choice. Please try again.")

    def show_main_menu(self):
        print(
            """
[1] Add Contact
[2] Show All Contacts
[3] Search
[4] Delete
[5] Update Contact
[0] Exit
"""
        )
        options = {
            "1": self.add_contact,
            "2": self.show_all_contacts,
            "3": self.show_search_menu,
            "4": self.show_delete_menu,
            "5": self.edit_menu,
        }
        choice = self.get_choice()

        if choice == "0":
            return -1000
        elif choice in options:
            options[choice]()  # Call the selected method
        else:
            print("❌ Invalid choice. Please try again.")

    def show_delete_menu(self):
        print(
            """
[1] delete by name
[2] delete by phone number
[3] delete by id 
[0] Exit
"""
        )
        options = {
            "1": self.delete_by_name,
            "2": self.delete_by_phone,
            "3": self.delete_by_id,
        }
        choice = self.get_choice()

        if choice == "0":
            return
        elif choice in options:
            options[choice]()  # Call the selected method
        else:
            print("❌ Invalid choice. Please try again.")

    def delete_menu(self, id=None):
        print("[1]- delete user ")
        print("[2]- delete  relation")
        print("[0]- go to main menu")

        choice = self.get_choice()
        if choice == "0":
            return
        elif choice == "1":
            self.delete_by_id(id=id)
        elif choice == "2":
            self.delete_relation(id=id)

    def edit_menu(self, id=None):
        print("[1]- edit data")
        print("[2]- edit relation")
        print("[3]- add relation")
        print("[0]- go to main menu")

        choice = self.get_choice()
        if choice == "0":
            return
        elif choice == "1":
            self.update_contact(id=id)
        elif choice == "2":
            self.updata_relation(id=id)
        elif choice == "3":
            self.add_relation(id=id)

    # ^ add user

    def add_contact(self):
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        selected_category = self.choose_categories()
        success = self.controller.add_contact(name, phone, selected_category)
        print("Contact added!" if success else "Failed to add contact.")

    # ^ add relation
    def add_relation(self, id=None):
        contact_id = id if id else input("Enter contact ID to update: ").strip()

        if not str(contact_id).isdigit():
            print("❌ ID must be a number.")
            return

        person = self.controller.get_person(id=int(contact_id))

        if not person:
            print("❌ Person not found.")
            return

        print(f"Name  : {person.name}")
        print(f"Phone : {person.phone}")
        print("Current Relations:")

        # علاقات الشخص الحالية
        existing_keys = []
        for relation in person.category:
            for key, value in self.options.items():
                if relation == value.upper():
                    print(f" - {relation}")
                    existing_keys.append(key)
                    break

        print("\nAvailable Relations to Add:")
        available_options = {
            k: v for k, v in self.options.items() if k not in existing_keys
        }

        if not available_options:
            print("⚠️ All possible relations are already assigned.")
            return

        for key, value in available_options.items():
            print(f"[{key}] - {value}")

        choice = self.get_choice()

        if not choice.isdigit():
            print("❌ ID must be a number.")
            return

        if choice not in available_options:
            print("❌ Invalid choice or relation already exists.")
            return

        # add new relation
        success = self.controller.add_relation(
            Person_id=person.id, relation=available_options[choice]
        )

        print("✅ Relation added." if success else "❌ Failed to add relation.")

    def show_all_contacts(self):
        contacts = self.controller.get_all_contacts()

        if not contacts:
            print("There are no users yet.")
            return

        self._show_data(contacts)

        print("\nEnter the user ID to access their profile")
        print("or type '0' to return to the main menu.")
        choice = self.get_choice()

        if choice == "0":
            return

        if not choice.isdigit():
            print("Invalid input. ID must be a number.")
            return

        person = self.search_by_id(id=choice, edit=True)

        if not person:
            print("User not found.")
            return

        self._show_data(results=person)

        print("\n[1] Edit user")
        print("[2] Delete user")
        print("[0] Return to main menu")

        choice = self.get_choice()
        person = person[0]
        if choice == "1":
            self.edit_menu(id=person.id)

        elif choice == "2":
            self.delete_menu(id=person.id)

        elif choice == "0":
            return

        else:
            print("Invalid choice.")

    def _show_person(
        self,
        results: list,
    ):
        if not results:
            print("No results found")
            return

        print("-" * 50)

        for person in results:
            print(f"ID       : {person.id}")
            print(f"Name     : {person.name}")
            print(f"Phone    : {person.phone}")
            print("Categories:")

            there_is_relation = False

            for relation in person.category:

                for key, value in self.options.items():

                    if relation == value.upper():

                        print(f"  > [{key}] {value.lower()}")
                        there_is_relation = True
                        break

            if not there_is_relation:
                print("there is no relation")

            print("-" * 50)

    def _show_data(self, results: list):
        if not results:
            print("No results found")
            return
        for person in results:
            print(person)

    # ^search for data
    def search_by_name(self):
        name = input("Enter name to search: ").strip()
        results = self.controller.search_by_name(name)
        self._show_person(results)

    def search_by_phone(self):
        phone = input("Enter phone to search: ").strip()
        results = self.controller.search_by_phone(phone)
        self._show_person(results)

    def search_by_id(self, id=None, edit=False):

        if not id:
            id = input("Enter id to search: ").strip()

        results = self.controller.search_by_id(id)
        if not edit:

            self._show_person(results)

            return

        return results

    def search_by_category(self):
        for key, value in self.options.items():
            print(f"[{key}]- {value}")

        category_id = input("Enter category id to search: ").strip()

        if not category_id.isdigit():
            print("ID must be a number.")
            return

        elif category_id in self.options:
            category = self.options[category_id]
            results = self.controller.search_by_category(category)
            self._show_person(results)
        else:
            print("invalid category ID")

    # ^ delete data
    def delete_by_name(self):
        name = input("Enter name to delete: ").strip()
        success = self.controller.delete_contact_by_name(name)
        print("Contact deleted." if success else "Contact not found.")

    def delete_by_phone(self):
        phone = input("Enter phone to delete: ").strip()
        success = self.controller.delete_contact_by_phone(phone=phone)
        print("Contact deleted." if success else "Contact not found.")

    def delete_by_id(self, id=None):
        contact_id = id
        if not id:
            contact_id = input("Enter contact ID to update: ").strip()
        if not str(contact_id).isdigit():
            print("id must be a number.")
            return
        success = self.controller.delete_contact_by_id(id=int(contact_id))
        print("Contact deleted." if success else "Contact not found.")

    def delete_relation(self, id=None):
        contact_id = id
        if not id:
            contact_id = input("Enter contact ID to update: ").strip()
        if not str(contact_id).isdigit():
            print("id must be a number.")
            return
        print(contact_id)
        print(type(contact_id))

        person = self.controller.get_person(id=int(contact_id))
        print(person.id)
        if not person:
            print("person not found")
            return

        print(f"Name  : {person.name}")
        print(f"Phone : {person.phone}")
        print("Categories:")

        keys_list = []
        user_relation = {}  # لربط relation name بالـ key

        for relation in person.category:
            for key, value in self.options.items():
                if relation == value.upper():
                    print(f"Relation ID: [{key}], Relation Value: '{relation}'")
                    keys_list.append(key)
                    user_relation[key] = relation
                    break

        if not keys_list:
            print("⚠️ No relations to delete.")
            return

        choice = self.get_choice()

        if not choice.isdigit():
            print("❌ ID must be a number.")
            return

        if choice not in keys_list:
            print("❌ Invalid input.")
            return

        category = user_relation[choice]
        success = self.controller.delete_relation(
            person_id=person.id, relation_name=category
        )

        if success:
            print("relation deleted.")
        else:
            print("failed to delete relation.")

        # ^ updata data

    def update_contact(self, id=None):

        contact_id: str = id
        if not id:
            contact_id = input("Enter contact ID to update: ").strip()
        if not str(contact_id).isdigit():
            print("id must be a number.")
            return
        person = self.search_by_id(id=contact_id, edit=True)
        person = person[0]
        name = input(f"New name (leave blank to keep {person.name}): ").strip()
        phone = input(f"New phone (leave blank to keep {person.phone}): ").strip()

        if not name and not phone:
            print("No changes entered.")
            return

        updated = self.controller.update_contact(
            id=int(contact_id), new_name=name or None, new_phone=phone or None
        )

        print("✅ Contact updated." if updated else "❌ Update failed.")

    def updata_relation(self, id=None):
        contact_id = id
        if not id:
            contact_id = input("Enter contact ID to update: ").strip()

        if not str(contact_id).isdigit():
            print("ID must be a number.")
            return
        there_is_relation = False
        person = self.controller.get_person(id=int(contact_id))

        if person:
            print(f"Name     : {person.name}")
            print(f"Phone    : {person.phone}")
            print("Categories:")
            keys_list = []
            for relation in person.category:
                for key, value in self.options.items():
                    # print(f"{value}  {relation}")
                    if relation == value.upper():
                        # print("yes")
                        print(f"Relation ID: [{key}], Relation Value: '{relation}'")
                        there_is_relation = True
                        keys_list.append(key)
                        break

            if there_is_relation:
                choice = self.get_choice()
                if not choice.isdigit():
                    print("ID must be a number.")
                    return
                elif choice in keys_list:
                    category = self.options[choice]
                    for key, value in self.options.items():
                        print(f"[{key}] {value}")
                    new_relation = input("enter the relation id : ").strip()
                    if not new_relation.isdigit():
                        print("must be digits")
                        return
                    options = [str(i) for i in range(1, 7)]
                    if new_relation in options:
                        updated_relation = self.controller.update_relation(
                            person_id=person.id,
                            relation_name=category,
                            new_relation=self.options[new_relation],
                        )
                    else:
                        print(options)
                        print("pls enter a number between (1 - 6)")
                        updated_relation = False
                    if updated_relation:
                        print("relation updated")
                    else:
                        print("can't update this relation")
                else:
                    print("invalid input!")
        else:
            print("❌ Person not found.")

    def choose_categories(self):

        print("Choose categories by number (comma-separated):")
        for key, value in self.options.items():
            print(f"[{key}] {value}")

        raw_input = input("Your choice(s): ").strip()
        chosen_numbers = [num.strip() for num in raw_input.split(",")]
        selected_categories = [
            self.options[num] for num in chosen_numbers if num in self.options
        ]

        return selected_categories

    def run(self):
        Turn_on = True
        while Turn_on:
            if self.show_main_menu() == -1000:
                print("good bye!")
                Turn_on = False
