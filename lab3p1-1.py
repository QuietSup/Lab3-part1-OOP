import json
import os
import datetime


class Ticket:
    """Base class contains ticket and person info, and serialization for .json file.

    Base class contains first name, last name, patronymic, age, ticket type and event info."""
    def __init__(self, f_name, l_name, patronymic, age, ticket_type, event):
        self.__f_name = f_name
        self.__l_name = l_name
        self.__patronymic = patronymic
        self.__age = age
        self.__ticket_type = ticket_type
        self.__price = event.price
        self.__date = datetime.date.today()
        self.__event = event

    def serialization(self):
        """Serialization of .json file. Checks if it is empty and if it exists"""
        file_name = f'{self.event.name}.json'
        data = {
            0: {
                "first name": self.f_name,
                "last name": self.l_name,
                "patronymic": self.patronymic,
                "ticket type": self.ticket_type,
                "price": self.price,
                "date bought": self.date,
                "event name": self.event.name,
                "event date": self.event.date
            }
        }

        if not os.path.exists(file_name):
            with open(file_name, 'w'):
                pass

        if os.path.getsize(file_name):
            with open(file_name, "r") as read_file:
                n = json.load(read_file)

            if len(n) == self.event.tickets_num:
                raise IndexError('No more ticket left')

            n.append(data)
            n[-1][len(n) - 1] = n[-1].pop(0)

            with open(file_name, "w") as write_file:
                json.dump(n, write_file, indent=4, default=str)

        else:
            with open(file_name, "w") as write_file:
                json.dump([data], write_file, indent=4, default=str)

    @property
    def price(self):
        return self.__price

    @property
    def f_name(self):
        return self.__f_name

    @property
    def l_name(self):
        return self.__l_name

    @property
    def patronymic(self):
        return self.__patronymic

    @property
    def age(self):
        return self.__age

    @property
    def ticket_type(self):
        return self.__ticket_type

    @property
    def date(self):
        return self.__date

    @property
    def event(self):
        return self.__event

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Price must be int/float')
        self.__price = value

    @f_name.setter
    def f_name(self, value):
        if not isinstance(value, str):
            raise TypeError('First name must be str')
        self.__f_name = value

    @l_name.setter
    def l_name(self, value):
        if not isinstance(value, str):
            raise TypeError('last name must be str')
        self.__l_name = value

    @patronymic.setter
    def patronymic(self, value):
        if not isinstance(value, str):
            raise TypeError('Patronymic must be str')
        self.__patronymic = value

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError('Age must be int')
        self.__age = value

    @ticket_type.setter
    def ticket_type(self, value):
        if not isinstance(value, str):
            raise TypeError('Ticket type must be str')
        self.__ticket_type = value

    @date.setter
    def date(self, value):
        self.__date = value

    @event.setter
    def event(self, value):
        self.__event = value


class Regular(Ticket):
    """Information about regular ticket and gives info about ticket type to base class"""
    def __init__(self, f_name, l_name, patronymic, age, event):
        super().__init__(f_name, l_name, patronymic, age, 'regular', event)
        self.serialization()


class Advance(Ticket):
    """Information about advance ticket with discount and gives info about ticket type to base class"""
    def __init__(self, f_name, l_name, patronymic, age, event):
        super().__init__(f_name, l_name, patronymic, age, 'advance', event)
        self.price *= 0.6
        self.serialization()


class Student(Ticket):
    """Information about student ticket and gives info about ticket type to base class"""
    def __init__(self, f_name, l_name, patronymic, age, event):
        super().__init__(f_name, l_name, patronymic, age, 'student', event)
        self.price *= 0.5
        self.serialization()


class Late(Ticket):
    """Information about Late ticket and gives info about ticket type to base class"""
    def __init__(self, f_name, l_name, patronymic, age, event):
        super().__init__(f_name, l_name, patronymic, age, 'late', event)
        self.price *= 1.1
        self.serialization()


def identify(f_name, l_name, patronymic, age, student, event):
    """Selects which ticket type to sell"""
    if student:
        Student(f_name, l_name, patronymic, age, event)
    elif event.date - datetime.date.today() < datetime.timedelta(days=10):
        Late(f_name, l_name, patronymic, age, event)
    elif event.date - datetime.date.today() > datetime.timedelta(days=60):
        Advance(f_name, l_name, patronymic, age, event)
    else:
        Regular(f_name, l_name, patronymic, age, event)


class Event:
    """Contains info about event: name, total tickets number and holding date"""
    def __init__(self, name, tickets_num, price, date):
        self.__name = name
        self.__date = date
        self.__tickets_num = tickets_num
        self.__price = price

    def __str__(self):
        return f'Name: {self.__name}\nEvent date: {self.__date}\n' \
               + f'Number of tickets: {self.__tickets_num}\nStart price: {self.__price}'

    def deserialization(self):
        """Deserialization of .json file"""
        file_name = f'{self.name}.json'
        if not os.path.exists(file_name):
            raise OSError(f'path/directory {file_name} doesn\'t exist')

        if os.path.getsize(file_name):
            with open(file_name, "r") as write_file:
                return json.load(write_file)
        else:
            raise ValueError(f'{file_name} is empty')

    def find(self, ticket_id):
        """Find a ticket info with id"""
        file_name = f'{self.name}.json'
        if not os.path.exists(file_name):
            raise OSError(f'path/directory {file_name} doesn\'t exist')

        if os.path.getsize(file_name):
            with open(file_name, "r") as write_file:
                all_data = json.load(write_file)
                if ticket_id >= len(all_data) or ticket_id <= 0:
                    raise IndexError(f'id must be in range [0; {len(all_data)}]')
                return all_data[ticket_id]
        else:
            raise OSError(f'{file_name} is empty')

    @property
    def name(self):
        return self.__name

    @property
    def date(self):
        return self.__date

    @property
    def tickets_num(self):
        return self.__tickets_num

    @property
    def price(self):
        return self.__price

    @name.setter
    def name(self, value):
        self.__name = value

    @date.setter
    def date(self, value):
        self.__date = value

    @tickets_num.setter
    def tickets_num(self, value):
        self.__tickets_num = value

    @price.setter
    def price(self, value):
        self.__price = value


night = Event('night', 225, 1000, datetime.date(2022, 12, 30))
identify('Fintan', 'Redmond', 'Ihorovych', 26, False, night)

print(night)
print(night.deserialization())
print(night.find(2))
