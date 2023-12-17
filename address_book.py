from collections import UserDict
from datetime import datetime, timedelta
from collections import defaultdict


class InvalidPhoneNumber(Exception):
    pass


class InvalidBirthDate(Exception):
    pass


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if isinstance(value, str) and len(value) == 10:
            super().__init__(value)
        else:
            raise InvalidPhoneNumber


class Birthday(Field):
    DATEFORMAT = '%d.%m.%Y'

    def __init__(self, value):
        try:
            self._value = datetime.strptime(value, Birthday.DATEFORMAT).date()
        except ValueError:
            raise InvalidBirthDate


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = None
        self.birthday = None

    def add_phone(self, value):
        self.phone = Phone(value)

    def edit_phone(self, value):
        self.phone = Phone(value)

    def add_birthday(self, birthday_date):
        self.birthday = Birthday(birthday_date)

    def __str__(self):
        return f"Contact name: {self.name}, phone: {self.phone}"


class AddressBook(UserDict):
    WEEKEND_DAYS = {5, 6}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def get_birthdays_per_week(self):
        birthdays_dict = defaultdict(list)
        today = datetime.today().date()

        for user in self.data.values():
            if not user.birthday:
                continue

            birthday = user.birthday.value.replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=birthday.year + 1)

            delta_days = (birthday - today).days

            if delta_days > 7 or delta_days == 0:
                continue

            if birthday.weekday() in AddressBook.WEEKEND_DAYS:
                days_until_next_monday = (7 - birthday.weekday()) % 7
                birthday = birthday + timedelta(days=days_until_next_monday)

            birthdays_dict[birthday].append(user.name.value)

        return '\n'.join([f"{date.strftime('%A')}: {', '.join(names)}"
                          for date, names in sorted(birthdays_dict.items())])
