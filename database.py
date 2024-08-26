import utils


def connect(name='database'):                                        #connection
    import sqlite3
    return sqlite3.connect(name,check_same_thread=False)

def user_tb(connection):                                              #user table
    cursor = connection.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            creditCard INTEGER,
            photo TEXT,
            balance INTEGER
        )
    ''')
    connection.commit()


def add_user(connection,username,password,credit_card,photo,balance):          #add user
    cursor= connection.cursor()
    hashed_pass = utils.hash_password(password)
    query=''' insert into users (username,password, creditCard ,photo,balance) values (? , ?, ? , ? , ?)'''
    cursor.execute(query,(username,hashed_pass,credit_card,photo,balance))
    connection.commit()


def delete_user(connection,username):                                 #delete user
    cursor=connection.cursor()
    query=''' delete from users where username = ? '''
    cursor.execute(query,(username,))
    connection.commit() 

def get_user(connection , username ) :                                 #get user
    cursor = connection.cursor()
    query = ''' select * 
                from users
                where username = ?    '''
    cursor.execute(query, (username,))
    return cursor.fetchone()

def product_tb(connection):                                             #products table
    cursor = connection.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL PRIMARY KEY,
            price INTEGER,
            quantity INTEGER,
            photo TEXT
        )
    ''')
    connection.commit()

def add_product(connection,product_name,price,quantity,photo):         #add product
    cursor= connection.cursor()
    query=''' insert into products (product_name,price,quantity,photo) values (? , ? , ?, ? )'''
    cursor.execute(query,(product_name,price,quantity,photo))
    connection.commit()

def get_product(connection,product_name):                       #show specific product
    cursor= connection.cursor()
    query = ''' select * 
                from products
                where product_name = ?    '''
    cursor.execute(query,(product_name,))
    return cursor.fetchone()


def get_all_products(connection):                       # show all products
    cursor = connection.cursor()
    query = ''' select * from products'''
    cursor.execute(query)
    return cursor.fetchall()


def delete_product(connection,product_name):                    # delete product
    cursor=connection.cursor()
    query=''' delete from products where product_name = ? '''
    cursor.execute(query,(product_name,))
    connection.commit() 

def search_product(connection,product_name):                    # search product
    cursor=connection.cursor()
    query= f''' select * from products where product_name LIKE '%{ product_name }%' '''
    cursor.execute(query)
    return cursor.fetchall()
 

def comment_tb(connection):                      # comment table
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT ,
            commento TEXT NOT NULL,
            product_name TEXT ,
            FOREIGN KEY (product_name) REFERENCES products(product_name))
    ''')
    connection.commit()

def add_comment(connection,comment): #add comment
    cursor = connection.cursor()
    query ='''insert into comment (commento) values(?) '''
    cursor.execute(query,(comment,))
    connection.commit()

def show_comment(connection,product_name):               #show comment
    cursor = connection.cursor()
    query = ''' select comment from comment where product_name = ? '''
    cursor.execute(query,(product_name,))
    return cursor.fetchall()

def clear_comment(connection,product_name):                           # clear comment when we delete product
    cursor = connection.cursor()
    query = ''' Delete from comment where product_name = ?'''
    query.execute(query,(product_name,))
    connection.commit()

def update_user(connection , username , current_balance):
    cursor = connection.cursor()
    query = ''' UPDATE users set balance = ?  WHERE username = ? '''
    cursor.execute(query,(current_balance,username))
    connection.commit() 

def show_all_comments(connection):               #show all_comments
    cursor = connection.cursor()
    query = ''' select commento from comment  '''
    cursor.execute(query)
    return cursor.fetchall()