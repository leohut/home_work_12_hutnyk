import pickle
from collections import UserDict
from datetime import datetime

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def save_to_disk(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def search(self, query):
        results = []
        for record in self.data.values():
            if (
                query.lower() in record.name.value.lower()
                or any(query in phone for phone in record.phones)
            ):
                results.append(record)
        return results  
    
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

address_book.save_to_disk("address_book.pkl")

address_book.load_from_disk("address_book.pkl")

search_query = input("Enter search query: ")
results = address_book.search(search_query)

if results:
    print("Search results:")
    for record in results:
        print("Name:", record.name.value)
        print("Phones:", record.phones)
        print("Birthday:", record.birthday.value if record.birthday else "N/A")
        print("Days to Birthday:", record.days_to_birthday())
        print()
else:
    print("No results found.")