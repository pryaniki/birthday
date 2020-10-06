import psycopg2
import os
from datetime import datetime, date, timedelta #working with a date
from psycopg2 import sql#import sql

def is_accessible(path, mode='r'):
    """
    Проверка, является ли файл или папка из `path`
    доступным для работы в предоставленным `mode` формате.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True

def get_setiings (fileName):
    if (is_accessible(fileName)):
        f = open(fileName, 'r')
 #       for line in f:
 #          print(line)
        f.close() 

get_setiings (os.path.abspath('settings'))
try:
    connection = psycopg2.connect(
        """
        host = 'localhost' port = '5432'
        dbname ='birthday' user = 'postgres' password = 'abc123'
        """
    )
    print("Database opened successfully")
    cursor = connection.cursor()
######## drop all table
    dropTable   = """DROP TABLE IF EXISTS phoneNumber;"""
    cursor.execute(dropTable)
    dropTable   = """DROP TABLE IF EXISTS email;"""
    cursor.execute(dropTable)
    dropTable   = """DROP TABLE IF EXISTS people;"""
    cursor.execute(dropTable)

# Query to create a table "people"
    people ="""
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
    phoneNumber ="""
    CREATE TABLE IF NOT EXISTS phoneNumber(
      id serial primary key,
      number varchar(30),
      people_id integer references people(id)
    )
    """
    cursor.execute(phoneNumber)

# Query to create a table "email"
    email ="""
    CREATE TABLE IF NOT EXISTS email(
      id serial primary key,
      email varchar(30),
      people_id integer references people(id)
    )
    """
    cursor.execute(email)
    connection.commit()

    def fill_table(csv_file, table_name):
        """
        Fills table table_name with data from file csv_file,
        where csv_file is the path to the file
        """
        f = open(csv_file, 'r')
        cursor.copy_from(f, table_name, sep=',', null='none')
        f.close()

# Filling tables with data from csv files    
    fill_table(os.path.abspath('myPeople.csv'), 'people')
    fill_table(os.path.abspath('phoneNumber.csv'), 'phoneNumber')
    fill_table(os.path.abspath('email.csv'), 'email')

# The query outputs peopl who have a birthday on the next day
    birthday_in_num_days = sql.SQL(
    """
      WITH TabNextBirthday AS(
        SELECT id,
        firstName,
        lastName,
        middleName,
        cast(birthday +
        ((extract(year from age(birthday)) + 1) *interval '1' year
        ) as date) as next_birthday,
        date_part('year',age(birthday)) as age,
        aboutPerson
        FROM people
      )
    SELECT t.firstName, t.lastName, t.age, t.next_birthday, 
      abs( date_part('day', age(t.next_birthday)) ) as daysBeforeBirthday,
      t.aboutPerson

    from TabNextBirthday as t
    where t.next_birthday <= current_date +%s 
    order by t.next_birthday;
    """
    )

    def get_date_difference(any_date):
        '''
        returns the difference between
        a date and the current day
        '''
        return any_date - date.today() 
    
    def last_day_of_week():
        '''
        Returns the last day of the week
        '''
        cur_day_week = date.today().weekday() # Monday is 0 and Sunday is 6
        return date.today() + timedelta(days= 6 - cur_day_week)
    
    def last_day_of_month():
        '''
        Returns the last day of the month
        '''
        next_month = date.today().replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)
    
    def last_day_of_year():
        '''
        Returns the last day of the year
        '''
        new_year = date(date.today().year + 1, 1, 1)
        return new_year 
    
    def get_interval(interval):
        '''
        Returns the number of days until the end of the interval
        interval = ["day", "week", "mounth", "year"]
        where 0 - "day", 3 - "year"
        '''
        if (interval == 0):
            return 1
        elif (interval == 1):
            my_date = last_day_of_week()
            return get_date_difference(my_date).days
        elif (interval == 2):
            my_date = last_day_of_month()
            return get_date_difference(my_date).days
        elif (interval == 3):
            my_date = last_day_of_year()
        
    interval = 2 #default

    cursor.execute(birthday_in_num_days,(get_interval(interval), ) )
   # cursor.execute("select * from people")
    def print_birthday_man(people):
        '''
        displays information about a person in a specific format
        '''
        print()
        if (people[0] is not None and people[1] is not None):
                print(people[0],people[1])
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
            print("Birthday before ",round(people[4])," days ")

        if (people[5] is not None):
            print(people[5])
    
    def print_table_to_file():
       pass

    while True:
        people = cursor.fetchone()
        if people == None:
              break
        print_birthday_man(people)
  
except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)
finally:
 #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


