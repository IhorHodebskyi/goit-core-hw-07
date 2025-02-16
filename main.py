
from collections import UserDict
from datetime import datetime, date, timedelta
import re
import unittest
def input_error(func: callable)-> callable:
    """Декоратор для обробки помилок."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid input. Please provide the correct number of arguments."
    return wrapper






class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name is required.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)



class Birthday(Field):
    def __init__(self, value: str):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y")
            if date_value > datetime.now():
                raise ValueError("Birthday cannot be in the future.")
            super().__init__(date_value.strftime("%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

            



class Record:
    name = None

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = str(Phone(new_phone))
                return
        raise ValueError("Phone number not found.")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return ("Phone number remove")
        raise ValueError("Phone number not found.")


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    
    def sow_birthday(self):
        return str(self.birthday) if self.birthday else "Birthday: None"
    

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"










class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address book is empty."

        result = ["Address Book:"]
        for record in self.data.values():
            result.append(str(record))

        return "\n".join(result)

    @staticmethod
    def date_to_string(date: date)-> str:
        return date.strftime("%Y.%m.%d")




    @staticmethod
    def find_next_weekday(start_date: date, weekday: int) -> date:
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def adjust_for_weekend(birthday: date) -> date:
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7) -> list:
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_this_year = datetime.strptime(record.birthday.value, "%d.%m.%Y").date().replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            birthday_this_year = self.adjust_for_weekend(birthday_this_year)

            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date_str = self.date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date_str})

        return upcoming_birthdays


def parse_input(user_input: str)-> tuple:
    parts = user_input.strip().split(" ")
    command = parts[0].lower()
    args = parts[1:]
    return command, args

@input_error
def add_contact(args: list, book: AddressBook)-> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone_number(args, book: AddressBook)-> str:
    if len(args) != 3:
        return "Invalid input. Please provide name, old phone, and new phone."

    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    try:
        record.edit_phone(old_phone, new_phone)
        return "Phone number changed successfully."
    except ValueError:
        return "Old phone number not found in contact."



@input_error
def show_all_contacts(book: AddressBook)-> str:
    return str(book)

@input_error
def sow_contact_by_name(args: list, book: AddressBook)-> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return str(record)


@input_error
def add_birthday(args: list, book: AddressBook)-> str:
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added successfully."


@input_error
def show_birthday(args: list, book: AddressBook)-> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.sow_birthday()


@input_error
def show_birthdays(book: AddressBook)-> str:
    return str(book.get_upcoming_birthdays())

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            result = add_contact(args, book)
            print(result)

        elif command == "change":
            result = change_phone_number(args, book)
            print(result)

        elif command == "phone":
            result = sow_contact_by_name(args, book)
            print(result)

        elif command == "all":
            result = show_all_contacts(book)
            print(result)

        elif command == "add-birthday":
            result = add_birthday(args, book)
            print(result)

        elif command == "show-birthday":
            result = show_birthday(args, book)
            print(result)

        elif command == "birthdays":
            result = show_birthdays(book)
            print(result)

        else:
            print("Invalid command.")





class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.book.add_record(Record("Alice"))
        self.book.add_record(Record("Bob"))

    def test_add_contact(self):
        result = add_contact(["Charlie", "1234567890"], self.book)
        self.assertEqual(result, "Contact added.")
        self.assertIsNotNone(self.book.find("Charlie"))

    def test_change_phone_number(self):
        self.book.find("Alice").add_phone("1234567890")
        result = change_phone_number(["Alice", "1234567890", "0987654321"], self.book)
        self.assertEqual(result, "Phone number changed successfully.")
        self.assertEqual(self.book.find("Alice").phones[0].value, "0987654321")

    def test_sow_contact_by_name(self):
        self.book.find("Alice").add_phone("1234567890")
        result = sow_contact_by_name(["Alice"], self.book)
        self.assertIn("Alice", result)
        self.assertIn("1234567890", result)

    def test_add_birthday(self):
        result = add_birthday(["Alice", "01.01.2000"], self.book)
        self.assertEqual(result, "Birthday added successfully.")
        self.assertEqual(self.book.find("Alice").birthday.value, "01.01.2000")

    def test_show_birthday(self):
        self.book.find("Alice").add_birthday("01.01.2000")
        result = show_birthday(["Alice"], self.book)
        self.assertEqual(result, "01.01.2000")

    def test_show_birthdays(self):
        self.book.find("Alice").add_birthday("01.01.2000")
        self.assertIsInstance(show_birthdays(self.book), str)

    def test_remove_phone(self):
        self.book.find("Alice").add_phone("1234567890")
        self.assertEqual(self.book.find("Alice").remove_phone("1234567890"), "Phone number remove")
        self.assertEqual(len(self.book.find("Alice").phones), 0)

    def test_delete_contact(self):
        self.book.delete("Alice")
        self.assertIsNone(self.book.find("Alice"))




if __name__ == "__main__":
    unittest.main()
    main()