from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = self.validated_phone(value)

    def validated_phone(self, phone: str) -> str:
        """
        Validates the phone number.
        Parameters:
            phone (str): The phone number to validate.
        Returns:
            str: The validated phone number.
        Raises:
            ValueError: If the phone number is not 10 digits long or 
            if it contains non-digit characters.
        """
        if not len(phone) == 10 and phone.isdigit():
            raise ValueError("Invalid phone number: {phone}. Must be 10-digits long.")
        return phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        """
        Adds a phone number to the record.
        Parameters:
            phone (str): The phone number to add.
        """
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Edits a phone number in the record.
        Parameters:
            old_phone (str): The old phone number to edit.
            new_phone (str): The new phone number.
        """
        for p in self.phones:
            if p.value == old_phone:
                p = Phone(new_phone)
                break

    def find_phone(self, phone: str):
        """
        Finds a phone number in the record.
        Parameters:
            phone (str): The phone number to find.
        Returns:
            str: The phone number if found, None otherwise.
        """
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def remove_phone(self, phone: str):
        """
        Removes a phone number from the record.
        Parameters:
            phone (str): The phone number to remove.
        Raises:
            ValueError: If the phone number is not found in the record.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found in record.")


class AddressBook(UserDict):

    def add_record(self, record: Record):
        """
        Adds a record to the address book.
        Parameters:
            record (Record): The record to add.
        Raises:
            KeyError: If a record with the same name already exists.
        """
        if record.name.value in self.data:
            raise KeyError(f"A record with name {record.name.value} already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Finds a record by name.
        Parameters:
            name (str): The name of the record to find.
        Returns:
            Record: The record with the given name.
        Raises:
            KeyError: If no record with the given name is found.
        """
        record = self.data.get(name)
        if record == None:
            raise KeyError(f"A record with name {name} not found.")
        return record

    def delete(self, name: str):
        """
        Deletes a record by name.
        Parameters:
            name (str): The name of the record to delete.
        Raises:
            KeyError: If no record with the given name is found.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"A record with name {name} not found.")


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")