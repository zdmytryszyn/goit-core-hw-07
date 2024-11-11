from collections.abc import Iterator
from typing import Callable

from home_work import AddressBook, Record, PhoneVerificationError


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "There is no such contact. Add contact"
        except ValueError as e:
            return e
            # or "Enter the argument for the command | Invalid date format. Use DD.MM.YYYY"
        except IndexError:
            return "Name of contact wasn't given in the argument.\
            Input the name of the contact"
        except PhoneVerificationError as e:
            return e
    return inner


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    username, phone, *_ = args
    record = book.find(username)
    message = "Contact updated."
    if record is None:
        record = Record(username)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    username, old_phone, new_phone, *_ = args
    record = book.find(username)
    if record:
        record.edit_phone(old_phone=old_phone, new_phone=new_phone)
        return "Contact updated."
    return "Name is not in contacts. Add new contact"


@input_error
def show_phone(args: str, book: AddressBook) -> str:
    username = args[0]
    record = book.find(username)
    return record.__str__()


@input_error
def add_birthday(args: str, book: AddressBook) -> str:
    username, birthday, *_ = args
    record = book.find(username)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "No such contact"


@input_error
def show_birthday(args: str, book: AddressBook) -> str:
    username, *_ = args
    record = book.find(username)
    if record:
        return f"Birthday of contact '{record.name}': {record.birthday.value.date()}"
    return "No such contact"


@input_error
def birthdays(book: AddressBook) -> str:
    return (
            'Upcoming birthdays:\n'
            + '\n'.join(f"{record['name']}: {record['birthday']}" for record in book.get_upcoming_birthdays())
    )


def show_all(book: AddressBook) -> Iterator:
    return (f"{value.__str__()}" for value in book.values())


def main() -> None:
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            for contact in show_all(book):
                print(contact)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
