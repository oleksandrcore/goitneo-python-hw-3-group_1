from address_book import (AddressBook, Record,
                          InvalidPhoneNumber, InvalidBirthDate)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except InvalidPhoneNumber:
            return 'Give me valid phone plase'
        except InvalidBirthDate:
            return 'Give me valid birth date'

    return inner


def non_existing_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Give me existing name."
        except TypeError:
            return 'Provide me only one name'

    return inner


def start():
    return 'How can I help you?'


@input_error
@non_existing_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    record.edit_phone(phone)
    return "Contact updated."


@non_existing_error
def show_phone(name, book):
    return book.find(name)


def show_all(book):
    return '\n'.join([f"{record.name} - {record.phone}"
                      for record in book.values()])


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


def finish():
    return 'Good bye!'


@non_existing_error
@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@non_existing_error
def show_birthday(name, book):
    return book.find(name).birthday


def show_all_birthdays(book):
    return book.get_birthdays_per_week()


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(finish())
            break
        elif command == "hello":
            print(start())
        elif command == "add":
            print(add_contact(args, book))
        elif command == 'phone':
            print(show_phone(*args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'add-birthday':
            print(add_birthday(args, book))
        elif command == 'show-birthday':
            print(show_birthday(*args, book))
        elif command == 'birthdays':
            print(show_all_birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
