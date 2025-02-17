import unittest
from main import AddressBook, Record, add_contact,change_phone_number, sow_contact_by_name,add_birthday,show_birthday,show_birthdays


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