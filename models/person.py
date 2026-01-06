class person_data:
    def __init__(self, name="", phone="", category=None):
        self.id = None
        self.name = name
        self.phone = phone
        self.category = category if category is not None else []

    def __str__(self):
        return (
            ("---" * 50)
            + f"\nid: {self.id}\nname: {self.name}\nphone number: ({self.phone})\nCategories: {', '.join(self.category) or 'None'}\n\n"
            + ("---" * 50)
        )
