
from collections import UserDict
from datetime import datetime, date, timedelta
import re

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
        super().__init__(value)
        self.value = value
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y")
            if date_value > datetime.now():
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
            self.value = date_value.strftime("%d.%m.%Y")
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
        birthday_str = f"Birthday: {self.birthday.value}" if self.birthday else "birthday: None"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} {birthday_str}"










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



    def get_upcoming_birthdays(self,  days=7)-> list:
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if not record.birthday:
                continue

        for user in self.data.values():
            birthday_this_year = user["birthday"].replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            birthday_this_year = self.adjust_for_weekend(birthday_this_year)

            if 0 <= (birthday_this_year - today).days <= days:

                if birthday_this_year.weekday() >= 5:
                    birthday_this_year = self.find_next_weekday(birthday_this_year, 0)

                congratulation_date_str = self.date_to_string(birthday_this_year)
                upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
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





if __name__ == "__main__":
    main()