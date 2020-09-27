import psycopg2
import os
from psycopg2 import sql#import sql
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
    fill_table(os.path.abspath('people.csv'), 'people')
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
        date_part('year',age(birthday)) as age
        FROM people
      )
    SELECT t.id, t.next_birthday
    from TabNextBirthday as t
    where t.next_birthday <= current_date +%s 
    order by t.next_birthday;
    """
    )
    num = (200, )

    cursor.execute(birthday_in_num_days, num)
   # cursor.execute("select * from people")
    people = cursor.fetchall()

    for user in people:
        print(user)

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)
finally:
 #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

