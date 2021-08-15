import psycopg2
import os
from datetime import date, timedelta, datetime  # working with a date
from psycopg2 import sql  # import sql


def create_tables(cursor):
    ######## drop all table
    dropTable = """DROP TABLE IF EXISTS phoneNumber;"""
    cursor.execute(dropTable)
    dropTable = """DROP TABLE IF EXISTS email;"""
    cursor.execute(dropTable)
    dropTable = """DROP TABLE IF EXISTS people;"""
    cursor.execute(dropTable)

    # Query to create a table "people"
    people = """
           CREATE TABLE IF NOT EXISTS people (
             id serial primary key,
             firstName varchar(30),
             lastName varchar(30),
             middleName varchar(30),
             birthday date,
             sex char(6),
             aboutPerson varchar
           )
           """
    cursor.execute(people)

    # Query to create a table "phoneNumber"
    phoneNumber = """
           CREATE TABLE IF NOT EXISTS phoneNumber(
             id serial primary key,
             number varchar(30),
             people_id integer references people(id)
           )
           """
    cursor.execute(phoneNumber)

    # Query to create a table "email"
    email = """
           CREATE TABLE IF NOT EXISTS email(
             id serial primary key,
             email varchar(30),
             people_id integer references people(id)
           )
           """
    cursor.execute(email)


def print_to_console_birthday_man(people):
    """
    displays information about a person in a specific format
    """
    print()
    if (people[0] is not None and people[1] is not None):
        print(people[0], people[1])
    elif (people[0] is not None):
        print(people[0])
    elif (people[1] is not None):
        print(people[1])

    print("Current age: ", round(people[2]))
    if (people[4] == 0):
        print("Birthday today")
    elif (people[4] == 1):
        print("Birthday tomorrow")
    elif (people[4] > 1):
        print("Birthday before ", round(people[4]), " days ")

    if (people[5] is not None):
        print(people[5])


def print_birthday_to_console(cursor):
    ### Красивый вывод в консоль
    while True:
        people = cursor.fetchone()
        if people is None:
            break
        print_to_console_birthday_man(people)


def get_all_data_from_table():
    try:
        connection = psycopg2.connect(user="postgres", password="admin", database='birthday', host="localhost",
                                      port="5432")

        cursor = connection.cursor()
        create_tables(cursor)
        connection.commit()

        def fill_table_people(csv_file):
            """
            Fills table table_name with data from file csv_file,
            where csv_file is the path to the file
            """
            import csv
            with open(csv_file, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    cursor.execute('INSERT INTO people (firstName, lastName, middleName, birthday, sex, aboutPerson) '
                                   'VALUES (%s, %s, %s, %s, %s, %s)',
                                   (row[0], row[1], row[2], row[3], row[4], row[5]))

        # Filling tables with data from csv files
        fill_table_people(os.path.abspath('people.csv'))

        birthday_in_num_days = sql.SQL(
            """
                SELECT * from people 
            """
        )

        cursor.execute(birthday_in_num_days)

        birthdays = []

        while True:
            people = cursor.fetchone()
            if people is None:
                break
            birthdays.append(people)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")
        return birthdays


def connect_to_db(flag):
    try:
        connection = psycopg2.connect(user="postgres", password="admin", database='birthday', host="localhost",
                                      port="5432")

        #print("Database opened successfully")

        cursor = connection.cursor()
        create_tables(cursor)
        connection.commit()
        ''''''
        def fill_table_people(csv_file):
            """
            Fills table table_name with data from file csv_file,
            where csv_file is the path to the file
            """
            import csv
            with open(csv_file, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    cursor.execute('INSERT INTO people (firstName, lastName, middleName, birthday, sex, aboutPerson) '
                                   'VALUES (%s, %s, %s, %s, %s, %s)',
                                   (row[0], row[1], row[2], row[3], row[4], row[5]))

        # Filling tables with data from csv files
        fill_table_people(os.path.abspath('people.csv'))

        # The query outputs people who have a birthday on the next day
        birthday_in_num_days = sql.SQL(
            """

                     WITH TabNextBirthday AS(
                       SELECT id,
                       firstName,
                       lastName,
                       middleName,
                       cast(birthday +
                       ((extract(year from age(birthday)) + 1) * interval '1' year) as date) as next_birthday,
                       (date_part('year',age(birthday)) + 1) as age,
                       birthday,
                       aboutPerson
                       FROM people
                     )

                   SELECT t.firstName, t.lastName, t.age, t.next_birthday, 
                   CASE
                       WHEN  t.next_birthday = current_date + interval '1' year
                           THEN 0
                       ELSE abs(extract(day from (now() - next_birthday)))::int + 1
                   END  as daysBeforeBirthday,
                     t.birthday,
                     t.aboutPerson

                   from TabNextBirthday as t
                   where (t.next_birthday <= current_date +%s) or  ( t.next_birthday = current_date + interval '1' year)
                   order by t.next_birthday;
                   """
        )

        def get_date_difference(any_date):
            """
            returns the difference between
            a date and the current day
            """
            #print(f'{any_date} - {date.today()} = {(any_date - date.today()).days}')
            return any_date - date.today()

        def last_day_of_week(any_day):
            """
            Returns the last day of the week
            """
            cur_day_week = date.today().weekday()  # Monday is 0 and Sunday is 6
            return date.today() + timedelta(days=6 - cur_day_week)

        def last_day_of_month(any_day):
            """
            Returns the last day of the month
            """
            next_month = any_day.replace(day=28) + timedelta(days=4)
            return next_month - timedelta(days=next_month.day)

        def last_day_of_year(any_day):
            """
            Returns the last day of the year
            """
            year = any_day.year
            return last_day_of_month(date(year, 12, 1))


        def get_interval(interval):
            """
            Returns the number of days until the end of the interval
            interval = ["day", "week", "month", "year"]
            where 0 - "day", 3 - "year"
            """
            if interval == 0:
                return 1
            elif interval == 1:
                my_date = last_day_of_week(date.today())
                return get_date_difference(my_date).days
            elif interval == 2:
                my_date = last_day_of_month(date.today())
                return get_date_difference(my_date).days
            elif interval == 3:
                my_date = last_day_of_year(date.today())
                return get_date_difference(my_date).days

        interval = flag

        cursor.execute(birthday_in_num_days, (get_interval(interval),))

        #print(cursor.execute(birthday_in_num_days, (get_interval(interval),)))
        birthdays = []

        while True:
            people = cursor.fetchone()
            if people is None:
                break
            birthdays.append(people)
            #print(people)

        #print_birthday_to_console(cursor)
        ''''''

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")
        return birthdays


def test(command, data_for_request):

    def get_birthday_people_from_table_people(cursor, interval, table):
        # The query all_dataoutputs people who have a birthday on the next day
        birthday_in_num_days = sql.SQL(
            """

                     WITH TabNextBirthday AS(
                       SELECT id,
                       firstName,
                       lastName,
                       middleName,
                       cast(birthday +
                       ((extract(year from age(birthday)) + 1) * interval '1' year) as date) as next_birthday,
                       (date_part('year',age(birthday)) + 1) as age,
                       birthday,
                       aboutPerson
                       FROM people
                     )

                   SELECT t.firstName, t.lastName, t.age, t.next_birthday, 
                   CASE
                       WHEN  t.next_birthday = current_date + interval '1' year
                           THEN 0
                       ELSE abs(extract(day from (now() - next_birthday)))::int + 1
                   END  as daysBeforeBirthday,
                     t.birthday,
                     t.aboutPerson

                   from TabNextBirthday as t
                   where (t.next_birthday <= current_date +%s) or  ( t.next_birthday = current_date + interval '1' year)
                   order by t.next_birthday;
                   """
        )

        def get_date_difference(any_date):
            """
            returns the difference between
            a date and the current day
            """
            # print(f'{any_date} - {date.today()} = {(any_date - date.today()).days}')
            return any_date - date.today()

        def last_day_of_week(any_day):
            """
            Returns the last day of the week
            """
            cur_day_week = any_day.weekday()  # Monday is 0 and Sunday is 6
            return date.today() + timedelta(days=6 - cur_day_week)

        def last_day_of_month(any_day):
            """
            Returns the last day of the month
            """
            next_month = any_day.replace(day=28) + timedelta(days=4)
            return next_month - timedelta(days=next_month.day)

        def last_day_of_year(any_day):
            """
            Returns the last day of the year
            """
            year = any_day.year
            return last_day_of_month(date(year, 12, 1))

        def get_interval(interval):
            """
            Returns the number of days until the end of the interval
            interval = ["day", "week", "month", "year"]
            where 0 - "day", 3 - "year"
            """
            if interval == 0:
                return 1
            elif interval == 1:
                my_date = last_day_of_week(date.today())
                return get_date_difference(my_date).days
            elif interval == 2:
                my_date = last_day_of_month(date.today())
                return get_date_difference(my_date).days
            elif interval == 3:
                my_date = last_day_of_year(date.today())
                return get_date_difference(my_date).days

        cursor.execute(birthday_in_num_days, (get_interval(interval),))

        # print(cursor.execute(birthday_in_num_days, (get_interval(interval),)))

        while True:
            people = cursor.fetchone()
            if people is None:
                break
            table.append(people)

        # print_birthday_to_console(cursor)

    def get_all_data_from_table_people(cursor, table):
        birthday_in_num_days = sql.SQL(
            """
                SELECT * from people 
            """
        )

        table = cursor.execute(birthday_in_num_days)

    def insert_to_table_people(cursor, data_people):
        cursor.execute('INSERT INTO people (firstName, lastName, middleName, birthday, sex, aboutPerson) '
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (data_people[0], data_people[1], data_people[2], data_people[3], data_people[4], data_people[5]))

    def execute_command(cursor, command: str, data_for_request: list, table):
        if command == 'get_birthdays_from_people':
            return get_birthday_people_from_table_people(cursor, data_for_request[0], data_for_request[1])
        elif command == 'get_people':
            return get_all_data_from_table_people(cursor, table)
        elif command == 'insert_to_people':
            return insert_to_table_people(cursor, data_for_request)
        else:
            print(f'команды {command} нет')

    def connect_to_db(command: str, data_for_request: list):
        try:
            connection = psycopg2.connect(user="postgres", password="admin", database='birthday', host="localhost",
                                          port="5432")

            cursor = connection.cursor()
            create_tables(cursor)
            connection.commit()

            def fill_table_people(csv_file):
                """
                Fills table table_name with data from file csv_file,
                where csv_file is the path to the file
                """
                import csv
                with open(csv_file, newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        cursor.execute(
                            'INSERT INTO people (firstName, lastName, middleName, birthday, sex, aboutPerson) '
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (row[0], row[1], row[2], row[3], row[4], row[5]))

                # Filling tables with data from csv files

            fill_table_people(os.path.abspath('people.csv'))

            table = []

            execute_command(cursor, command, data_for_request, table)

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                # print("PostgreSQL connection is closed")
            return table

    connect_to_db(command, data_for_request)






