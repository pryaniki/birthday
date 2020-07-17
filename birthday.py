import psycopg2
from psycopg2 import sql#import sql
try:
    connection = psycopg2.connect("""host='localhost' port='5432'
                                  dbname='birthday' user='postgres'
                                  password='abc123'""")
    print("Database opened successfully")
    cursor = connection.cursor()
######## drop all table
    dropTable   = """DROP TABLE IF EXISTS phoneNumber;"""
    cursor.execute(dropTable)
    dropTable   = """DROP TABLE IF EXISTS email;"""
    cursor.execute(dropTable)
    dropTable   = """DROP TABLE IF EXISTS people;"""
    cursor.execute(dropTable)

#######PEAPLE
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

#######PHONENUMBER_ID
    phoneNumber= """
    CREATE TABLE IF NOT EXISTS phoneNumber(
      id serial primary key,
      number varchar(30),
      people_id integer references people(id)
    )
    """
    cursor.execute(phoneNumber)

#######EMAIL
    email= """
    CREATE TABLE IF NOT EXISTS email(
      id serial primary key,
      email varchar(30),
      people_id integer references people(id)
    )
    """
    cursor.execute(email)
    connection.commit()


#FILLING TABLES
#filling people
    f = open(r'/home/maks/project/birthday/people.csv', 'r')
    cursor.copy_from(f,"people",sep=',',null='none')
    f.close()

#filling people
    f = open(r'/home/maks/project/birthday/phoneNumber.csv', 'r')
    cursor.copy_from(f,"phoneNumber",sep=',',null='none')
    f.close()
#filling email
    f = open(r'/home/maks/project/birthday/email.csv', 'r')
    cursor.copy_from(f,"email",sep=',',null='none')
    f.close()

# The query outputs peopl who have a birthday on the next day
    birthday_in_num_days = sql.SQL("""
    WITH next_birthday AS(
      SELECT id,
        cast(birthday +((extract(year from age(birthday)) + 1) *
             interval '1' year) as date)
      FROM people
    )
    SELECT * from next_birthday
    /*WHERE date = now()*/
    WHERE extract(month from date) = extract(month from now()) and
          extract(day from date) = extract(day from now())+%s
    """)
    num = (2,)


    cursor.execute(birthday_in_num_days,num)
    cursor.execute("select * from people")
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




    # The query outputs people who have a birthday on the next day
   ## cursor.execute("""
   ## WITH next_birthday AS(
   ##   SELECT id,
   ##     cast(birthday +((extract(year from age(birthday)) + 1) *
   ##          interval '1' year) as date)
   ##   FROM people
   ## )
   ## SELECT * from next_birthday
   ## /*WHERE date = now()*/
   ## WHERE extract(month from date) = extract(month from now()) and
   ##       extract(day from date) = extract(day from now())
   ## """)
