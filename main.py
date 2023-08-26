from collections import UserDict
from datetime import datetime

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index < len(self.data):
            keys = list(self.data.keys())
            key = keys[self._iter_index]
            self._iter_index += 1
            return self.data[key]
        else:
            raise StopIteration

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_remaining = (next_birthday - today).days
            return days_remaining
        else:
            return None
        
class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def is_valid_phone(self, value):
        # Implement your validation logic here
        return True  # Placeholder

    def __set__(self, instance, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")
        self.value = value

    def __get__(self, instance, owner):
        return self.value

class Birthday(Field):
    def is_valid_birthday(self, value):
        # Implement your validation logic here
        return True  # Placeholder

    def __set__(self, instance, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday")
        self.value = value

    def __get__(self, instance, owner):
        return self.value

address_book = AddressBook()

record1 = Record("John")
phone1 = Phone("123456789")
record1.add_phone(phone1)
birthday1 = Birthday(datetime(1990, 5, 15))
record1.birthday = birthday1

record2 = Record("Jane")
phone2 = Phone("987654321")
record2.add_phone(phone2)
birthday2 = Birthday(datetime(1985, 8, 29))
record2.birthday = birthday2

address_book.add_record(record1)
address_book.add_record(record2)

for record in address_book:
    print("Name:", record.name.value)
    print("Phones:", record.phones)
    print("Birthday:", record.birthday.value if record.birthday else "N/A")
    print("Days to Birthday:", record.days_to_birthday())
    print()
