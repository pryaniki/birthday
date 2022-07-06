import psycopg2
import subprocess
import os
import sys
from datetime import date, timedelta, datetime  # working with a date
from psycopg2 import sql, Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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


def connect_to_db(command, data_for_request):
    def get_birthday_people_from_table_people(cursor, interval):
        interval = interval[0]
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
                       birthday,
                       aboutPerson
                       FROM people
                     )

                   SELECT t.firstName, t.lastName,
                   CASE
                       WHEN  t.next_birthday = current_date + interval '1' year
                           THEN date_part('year',age(t.birthday))
                       ELSE date_part('year',age(t.birthday)) +1
                   END  as age,
                   t.next_birthday, 
                   CASE
                       WHEN  t.next_birthday = current_date + interval '1' year
                           THEN 0
                       ELSE abs(extract(day from (now() - next_birthday)))::int+1
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
            elif interval in (1, 2, 3):
                get_last_day = {
                    1: last_day_of_week,
                    2: last_day_of_month,
                    3: last_day_of_year,
                }
                my_date = get_last_day[interval](date.today())
                return get_date_difference(my_date).days
            else:
                print('не правильное значение интервала')

        cursor.execute(birthday_in_num_days, (get_interval(interval),))

    def get_all_data_from_table_people(cursor, data):
        birthday_in_num_days = sql.SQL(
            """
                SELECT * from people ORDER BY id
            """
        )
        cursor.execute(birthday_in_num_days)

    def insert_to_table_people(cursor, data):
        data_people = data[0]

        data_people = [(data_people[0], data_people[1], data_people[2], data_people[3], data_people[4], data_people[5])]

        request = sql.SQL(
            'INSERT INTO people (firstName, lastName, middleName, birthday, sex, aboutPerson) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, data_people))
        )
        cursor.execute(request)

        return 0

    def import_data_from_file(cursor, f_name):
        f_name = f_name[0]
        create_tables(cursor)

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

        fill_table_people(os.path.abspath(f_name))

    def get_person(cursor, person_id):
        person_id = person_id[0]
        request = sql.SQL(
            """
               SELECT * 
               from people as p
               where p.id = %s
            """
        )

        cursor.execute(request, (person_id,))

    def update_person(cursor, data):
        person_id = data[0]
        person_data = data[1]
        print(data)
        print(person_id)
        print(person_data)
        request = sql.SQL(
            """
            UPDATE people 
                SET firstName = %s,
                    lastName = %s, 
                    middleName = %s, 
                    birthday = %s, 
                    sex = %s, 
                    aboutPerson = %s
            WHERE id = %s
            """
        )
        record_to_insert = (person_data[0], person_data[1], person_data[2], person_data[3], person_data[4],
                            person_data[5], person_id)
        cursor.execute(request, record_to_insert)

    def execute_command(cursor, request: str, data: list):
        commands = {
            'get_birthdays_from_people': get_birthday_people_from_table_people,
            'get_people': get_all_data_from_table_people,
            'insert_to_people': insert_to_table_people,
            'import_data': import_data_from_file,
            'get_person_by_id': get_person,
            'update_people': update_person,
        }
        try:
            commands[request](cursor, data)
        except KeyError:
            print(f'команды {request} нет')
        finally:
            if request in ('get_birthdays_from_people', 'get_people', 'get_person_by_id'):
                table = []
                while True:
                    people = cursor.fetchone()
                    if people is None:
                        break
                    table.append(people)
                return table

    def connect(com: str, data_for_request: list):
        db_name = 'birthday2'
        is_exist_db = False
        try:  # создать БД
            connection = psycopg2.connect(user="postgres",
                                          password="admin",
                                          host="127.0.0.1",
                                          port="5432")
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = connection.cursor()
            sql_create_database = 'select * from pg_database'
            cursor.execute(sql_create_database)
            while True:
                db = cursor.fetchone()
                if db is None:
                    break
                if db[1] == db_name:
                    is_exist_db = True
            if not is_exist_db:
                sql_create_database = f'create database {db_name}'
                cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

        try:
            connection = psycopg2.connect(user="postgres", password="admin", database=db_name, host="localhost",
                                          port="5432")
            connection.autocommit = True
            with connection:
                with connection.cursor() as cursor:
                    table = execute_command(cursor, com, data_for_request)
                    return table
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    PGRE_EXE = f'PostgreSQLPortable{os.path.sep}PostgreSQLPortable.exe'

    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def start_pgre():
        pgre_path = os.path.join(resource_path("."), PGRE_EXE)
        print(pgre_path)
        p = subprocess.Popen(
            [pgre_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print(stdout)
        print(stderr)

    start_pgre()
    return connect(command, data_for_request)
