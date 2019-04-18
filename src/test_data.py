from library_manager import *
import random
# import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="library_admin",
    passwd="readmoarbooksM8",
    database="librarymanager",
    auth_plugin='mysql_native_password'
)

names = ['jim', 'bob', 'steve', 'Alicia', 'Robbie', 'Nick', "Austen", 'Justin', 'Emily']
book_titles = ['Redwall', 'need caffeine', 'database systems', 'how 2 python', 'hitchhiker\'s guide to the galaxy',
               'moar sleep', 'pineapples', 'GIRAFFES', 'sleep is for the weak']

mycursor = mydb.cursor()

# random.seed(datetime.datetime.now())
for i in range(len(book_titles)):
    add_book_with_params(book_titles[i], names[i % len(names)], random.randint(1, 500))

for i in range(len(names)):
    birthdate = random.randint(1500, 2010) * 10000 + random.randint(1, 12) * 100 + random.randint(1, 29)
    add_user_param(names[i], names[random.randint(0, len(names) - 1)],
                   ('male' if random.randint(0, 100) > 50 else 'female'), birthdate)

mydb.commit()
