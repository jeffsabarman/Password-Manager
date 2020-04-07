#Import the packages
import sqlite3
import string
import random
from getpass import getpass

#Connect to the sqlite3
conn = sqlite3.connect('my_password.sqlite') #Any file name
cursor = conn.cursor()

#The admin password for opening the program
admin_password = '123123'

#getpass module so the password doesn't show when input
user = getpass('What is the password?\n')

while user != admin_password:
    user = getpass("What is your password? \n")
    if user == 'q':
        break

#try and except function for create the table
#The table name here is password
#Service and password is the name of the column
try:
    cursor.execute(''' CREATE TABLE PASSWORD 
        (SERVICE TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL);''')
    print('YOUR SAFE HAS BEEN CREATED!')
except :
    print("You have a safe!")

#new_password function for inserting password that already exist
def new_password(service, password):
    params = (service,password)
    cursor.execute("INSERT INTO PASSWORD (SERVICE, PASSWORD) "
                   "VALUES (?, ?)",params); #You have to use params because you have excute the code that sqllite understand
    #The '?' will be filled with the value in params
    conn.commit() #You have to commit everytime you change your database

#show_all function for showing all of the service and password in your database
def show_all():
    for row in cursor.execute("SELECT service,password from PASSWORD"):
        print('Service = ',row[0])
        print('Password = ',row[1])
        print('')

#upadate_password function for update exsisting password service
def update_password(service,new_password):
    params = (new_password,service)
    conn.execute("UPDATE PASSWORD set password = ? "
                 "where SERVICE = ? ",params)
    conn.commit()

#show_password function for look at a specific service password
def show_password(service):
    for row in cursor.execute("SELECT service,password from PASSWORD"):
        if row[0] == service:
            print('Password : ', row[1])

#delete_service function for deleting a service and the password
def delete_service(service):
    sql_delete_query = """ DELETE from PASSWORD where SERVICE = ?"""
    cursor.execute(sql_delete_query, (service, ))
    conn.commit()

#password_generator function for give you a completely random and safe password
def password_generator(length):
    n_letter = length/2
    n_digits = length-n_letter
    password_list = []
    password = ''
    num1 = 0
    while num1 != n_letter:
        letter = random.choice(string.ascii_letters)
        password_list.append(letter)
        num1 +=1
    num2 = 0
    while num2 != n_digits:
        digit = random.choice(string.digits)
        password_list.append(digit)
        num2 +=1
    random.shuffle(password_list)
    return password.join(password_list)

#The overall program
if user == admin_password:
    while True:
        print("\n" + "*"*15)
        print('Commands :')
        print('ip = insert password')
        print('ss = show all service')
        print('sp = Show service password')
        print('up = upadate password')
        print('ds = delete service')
        print('pg = password generator')
        print('q = quit program')
        print("\n"+"*"*15)
        input_ = input('What do you like to do? \n')
        if input_.lower() == 'q':
            conn.close()
            break
        elif input_.lower() == 'ip':
            ser = input('What is the service?\n')
            pas = input('What is the password?\n')
            new_password(ser, pas)
            print('Your data entry is succesfull')
        elif input_.lower() == 'ss':
            show_all()
        elif input_.lower() == 'up':
            ser = input('What password service do you want to update?\n')
            new = input("What's the new password for " +  ser + '\n')
            update_password(ser, new)
            print('Your update is succesful')
        elif input_.lower() == 'sp':
            ser = input('What password service do you want to see?\n')
            show_password(ser)
        elif input_.lower() == 'ds':
            ser = input('What service do you want to delete?\n')
            delete_service(ser)
            print('The service has been deleted')
        elif input_.lower() == 'pg':
            ans = int(input('How many length do you want for your password?\n'))
            while ans<6:
                ans = int(input('How many length do you want for your password?\n'))
            print("Here's your password : ", password_generator(ans))
