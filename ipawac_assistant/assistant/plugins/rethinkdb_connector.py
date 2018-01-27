import rethinkdb
from assistant.plugins.utilities import paths
import pexpect
import abc


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class rethinkDBConnection(abc.ABCMeta, metaclass=Singleton):
    connection = rethinkdb.connect("localhost", 28015, db='Jasper')


def instantiate_if_not_exists():
    conn = rethinkDBConnection.connection
    rethinkdb.db_create("Jasper").run(conn)
    rethinkdb.db('Jasper').table_create(
        'Contacts', primary_key='serial_number').run(conn)
    rethinkdb.table("Contacts").index_create("first_name").run(conn)
    rethinkdb.table("Contacts").index_create("last_name").run(conn)
    rethinkdb.table("Contacts").index_wait("first_name").run(conn)
    rethinkdb.table("Contacts").index_wait("last_name").run(conn)
    try:
        rethinkdb.table("Contacts").index_create(
            "fullname", [rethinkdb.row["first_name"], rethinkdb.row["last_name"]]).run(conn)
        rethinkdb.table("Contacts").index_wait("fullname").run(conn)
    except BaseException:
        pass


def list_of_all_contacts():
    db_count = rethinkdb.table("Contacts").count().run(connection)
    i = 1
    names = []
    while i <= db_count:
        full_name = rethinkdb.table("Contacts").get(
            i).get_field('full_name').run(connection)
        names.append(full_name)
        i = i + 1
    return names


def birthday_list(
    day=rethinkdb.now().day().run(
        rethinkDBConnection.connection),
        month=rethinkdb.now().month().run(
            rethinkDBConnection.connection)):
    # parameters (day,month)
        # day: integer between 0 to 31
        # month: integer between 0 and 12
        # default parameter : today
    blist = []
    i = 1
    db_count = rethinkdb.table("Contacts").count().run(connection)
    dobstmt = rethinkdb.table("Contacts").get(
        i)['PersonalInfo']['date_of_birth']
    while i <= db_count:
        try:
            if(dobstmt.month().run(rethinkDBConnection.connection) == month and dobstmt.day().run(connection) == day):
                birthday_contact = rethinkdb.table("Contacts").get(i)[
                    'full_name'].run(connection)
                blist.append(birthday_contact)

        except BaseException:
            pass

        i = i + 1
    return blist


def list_all_contact_values(contact_parameter='email_id'):
    mylist_of_all_contacts = []
    mylist_of_all_contacts = list_of_all_contacts()
    i = 0
    for i in range(len(mylist_of_all_contacts)):
        contact_name = mylist_of_all_contacts[i]
        first_name, last_name = contact_name.split(" ")
        i = i + 1
        if contact_parameter == 'email_id':
            group_name = 'Email'

        elif contact_parameter == 'phone_number':
            group_name = 'Contact'

        elif contact_parameter == 'date_of_birth':
            group_name = 'PersonalInfo'

        contact_attribute_value = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
            group_name].get_field(contact_parameter)[0].run(connection)
        contact_attribute_list = []
        contact_attribute_list.append(contact_attribute_value)
        return contact_attribute_list


def getChoice():
    print("ENTER YOUR CHOICE")
    choice = input()
    return int(choice)


def get_contact(contact_list):
    if len(contact_list) > 1:
        for i in range(len(contact_list)):
            print(str(int(i + 1)) + " " +
                  contact_list[i]['first_name'] + " " + contact_list[i]['last_name'])
        choice = getChoice()
        return contact_list[int(choice) - 1]
    elif len(contact_list) == 1:
        return contact_list[0]


def get_contact_value(first_name, contact_parameter='email_id'):
    result = rethinkdb.table("Contacts").filter(
        lambda user: user["first_name"].match(
            "(?i)^" +
            first_name +
            "$")).run(
        rethinkDBConnection.connection)
    mylist_of_contacts = list(result)
    contact = get_contact(mylist_of_contacts)

    if contact_parameter == 'email_id':
        group_name = "Email"
    if contact_parameter == 'phone_number':
        group_name = "Contact"
        contact_parameter = "phone_number"
    if contact_parameter == 'date_of_birth':
        group_name = "PersonalInfo"

    try:
        return (contact[group_name][contact_parameter])
    except BaseException:
        return -1


def insert_into_contacts(my_connections):
    i = 0
    while(i < len(my_connections) - 1):
        if(my_connections[i].get('name')):
            name = (my_connections[i].get('name'))
            name_list = name.split()
            first_name = name_list[0]
            if (len(name_list) > 2):
                last_name = name_list[1] + " " + name_list[2]
            elif (len(name_list) == 2):
                last_name = name_list[1]
            else:
                last_name = " "

        full_name = first_name + " " + last_name
        db_count = rethinkdb.table("Contacts").get_all(
            [first_name, last_name], index="fullname").count().run(rethinkDBConnection.connection)
        if (db_count == 0):
            count = rethinkdb.table("Contacts").count().run(
                rethinkDBConnection.connection)
            count += 1
            rethinkdb.table("Contacts").insert(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    'full_name': full_name,
                    'serial_number': count}).run(
                rethinkDBConnection.connection)
        if(my_connections[i].get('birthdate')):
            date_of_birth = (my_connections[i].get('birthdate'))
            if date_of_birth.get('year'):
                year = date_of_birth['year']
            if date_of_birth.get('month'):
                month = date_of_birth['month']
            if date_of_birth.get('day'):
                day = date_of_birth['day']
            if (day and month and year):
                if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                        {'Contact': {'date_of_birth': True}}).is_empty().run(rethinkDBConnection.connection)):
                    age = rethinkdb.now().year().run(rethinkDBConnection.connection) - year
                    rethinkdb.table("Contacts").get_all(
                        [
                            first_name,
                            last_name],
                        index="fullname").update(
                        {
                            "PersonalInfo": {
                                'date_of_birth': rethinkdb.time(
                                    year,
                                    month,
                                    day,
                                    'Z').run(
                                    rethinkDBConnection.connection),
                                'age': age}}).run(
                        rethinkDBConnection.connection)
                db_date = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                    'PersonalInfo'].get_field('date_of_birth')[0].run(rethinkDBConnection.connection)
                if (db_date.date().year != year or db_date.date().month !=
                        month or db_date.date().day != day):
                    age = rethinkdb.now().year().run(rethinkDBConnection.connection) - year
                    rethinkdb.table("Contacts").get_all(
                        [
                            first_name,
                            last_name],
                        index="fullname").update(
                        {
                            "PersonalInfo": {
                                'date_of_birth': rethinkdb.time(
                                    year,
                                    month,
                                    day,
                                    'Z').run(
                                    rethinkDBConnection.connection),
                                'age': age}}).run(
                        rethinkDBConnection.connection)

        if(my_connections[i].get('numbers')):
            numbers = my_connections[i].get('numbers')
            # Add function for numbers using for
            if (len(numbers) >= 1):
                phone_number = numbers[0]
                if (phone_number):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Contact': {'phone_number': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number': phone_number}}).run(rethinkDBConnection.connection)
                    db_phone_number = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Contact'].get_field('phone_number')[0].run(rethinkDBConnection.connection)
                    if db_phone_number != phone_number:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number': phone_number}}).run(rethinkDBConnection.connection)
            if (len(numbers) == 2):
                phone_number1 = numbers[1]
                if (phone_number1):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Contact': {'phone_number1': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number1': phone_number1}}).run(rethinkDBConnection.connection)
                    db_phone_number = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Contact'].get_field('phone_number1')[0].run(rethinkDBConnection.connection)
                    if db_phone_number != phone_number1:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number1': phone_number1}}).run(rethinkDBConnection.connection)
            if (len(numbers) > 2):
                phone_number2 = numbers[2]
                if (phone_number2):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Contact': {'phone_number2': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number2': phone_number2}}).run(rethinkDBConnection.connection)
                    db_phone_number = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Contact'].get_field('phone_number2')[0].run(rethinkDBConnection.connection)
                    if db_phone_number != phone_number2:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Contact": {'phone_number2': phone_number2}}).run(rethinkDBConnection.connection)
        if(my_connections[i].get('emails')):
            emails = my_connections[i].get('emails')

            if (len(emails) >= 1):
                email_id = emails[0]
                if (email_id):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Email': {'email_id': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id': email_id}}).run(rethinkDBConnection.connection)
                    db_email_id = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Email'].get_field('email_id')[0].run(rethinkDBConnection.connection)
                    if db_email_id != email_id:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id': email_id}}).run(rethinkDBConnection.connection)
            if (len(emails) == 2):
                email_id1 = emails[1]
                if (email_id1):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Email': {'email_id1': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id1': email_id1}}).run(rethinkDBConnection.connection)
                    db_email_id = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Email'].get_field('email_id1')[0].run(rethinkDBConnection.connection)
                    if db_email_id != email_id1:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id1': email_id1}}).run(rethinkDBConnection.connection)

            if (len(emails) > 2):
                email_id2 = emails[2]
                if (email_id2):
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Email': {'email_id2': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id2': email_id2}}).run(rethinkDBConnection.connection)
                    db_email_id = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Email'].get_field('email_id2')[0].run(rethinkDBConnection.connection)
                    if db_email_id != email_id2:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Email": {'email_id2': email_id2}}).run(rethinkDBConnection.connection)

        if (my_connections[i].get('address')):
            address = my_connections[i].get('address')
            if address['formattedValue'] is not None:
                str_address = address['formattedValue']
                if str_address:
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Address': {'address': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'address': str_address}}).run(rethinkDBConnection.connection)
                    db_address = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Address'].get_field('address')[0].run(rethinkDBConnection.connection)
                    if db_address != str_address:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'address': str_address}}).run(rethinkDBConnection.connection)
            if address['city'] is not None:
                city = address['city']
                if city:
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Address': {'address': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'city': city}}).run(rethinkDBConnection.connection)
                    db_address = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Address'].get_field('city').run(rethinkDBConnection.connection)
                    if db_address != city:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'city': city}}).run(rethinkDBConnection.connection)
            if address['country'] is not None:
                country = address['country']
                if country:
                    if (rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").has_fields(
                            {'Address': {'country': True}}).is_empty().run(rethinkDBConnection.connection)):
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'country': country}}).run(rethinkDBConnection.connection)
                    db_address = rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname")[
                        'Address'].get_field('country')[0].run(rethinkDBConnection.connection)
                    if db_address != country:
                        rethinkdb.table("Contacts").get_all([first_name, last_name], index="fullname").update(
                            {"Address": {'country': country}}).run(rethinkDBConnection.connection)

        i += 1


def main():
    rethinkdbprocess = pexpect.spawn(
        "rethinkdb -d {} --bind 127.0.0.1".format(jasperpath.RETHINKDB_DATA_PATH,))
    rethinkdbprocess.expect(
        'Listening on http addresses: 127.0.0.1, ::1',
        timeout=None)
    rethinkdb.connect("localhost", 28015).repl()
    try:
        rethinkdb.db_drop("test").run()
        rethinkdb.db_create("Jasper").run()
    except BaseException:
        pass
    rethinkdb.connect("localhost", 28015, db='Jasper').repl()
    birthday_list()
# main()
