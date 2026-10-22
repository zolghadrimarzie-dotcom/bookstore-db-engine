import sqlite3
import os
connection=sqlite3.connect('book_inventory.db')
cursor=connection.cursor()
print('sqlite is connected to the database successfully')

cursor.execute(""
               "CREATE TABLE IF NOT EXISTS categories("
               "category_id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "category_name TEXT NOT NULL)"
               "")
cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL,
                        category_id INTEGER,
                        FOREIGN KEY(category_id) REFERENCES categories(category_id))
                """)
cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
             customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
             full_name TEXT NOT NULL,
             email TEXT UNIQUE)
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
               order_id INTEGER PRIMARY KEY AUTOINCREMENT,
               customer_id INTEGER,
               book_id INTEGER,
               quantity INTEGER NOT NULL,
               order_date TEXT DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY(customer_id) REFERENCES customers(Customer_id),
               FOREIGN KEY(book_id) REFERENCES books(book_id))
               """)
connection.commit()
print('your tables were added successfully')

categories_info=[
    ("AI and programming",),
    ("novels and literature",),
    ("psychology",)
                ]
cursor.executemany("INSERT OR IGNORE into categories(category_name) VALUES(?);", categories_info)

books_info=[
    ("Advanced Python Teaching","Sara Ahmadi",350000,12,1),
    ("The Death of Ivan Illich","Leo Tolstoy",500000,20,2),
    ("The Compound Effect","Darren Hardy", 450000,40,3)
        ]
cursor.executemany("INSERT OR IGNORE INTO books(title,author,price,stock,category_id) VALUES(?,?,?,?,?);", books_info)

customers_info=[
    ("Marzieh Zolghadri","zolghadrimarzie@gmail.com"),("Carol Davidson","davidson@yahoo.com")
              ]
cursor.executemany('INSERT OR IGNORE INTO customers(full_name,email)VALUES(?,?);',customers_info)

orders_info=[(1,1,4),(2,3,2)]
cursor.executemany('INSERT OR IGNORE INTO orders(customer_id,book_id,quantity) VALUES(?,?,?);',orders_info)
connection.commit()

print("The first report:A list of books characteristics including title,author and category, which needs the join of books and categories tables:")
query="""SELECT books.title,books.author,categories.category_name FROM books 
        JOIN categories ON books.category_id = categories.category_id;"""
books_attributes=cursor.execute(query).fetchall()
for attribute in books_attributes:
    print(f"book title:{books_attributes[0]}\nauthor:{books_attributes[1]}\n book category:{books_attributes[2]}")

print("\nThe second report:The total price of the whole books in the book inventory:")
print(cursor.execute("""SELECT SUM(price*stock) FROM books;""").fetchone()[0])

print("\nThe third report:A list of orders that are submitted by customers:")
cursor.execute("""
                    SELECT customers.full_name,books.title,orders.quantity,orders.order_date FROM orders 
                                JOIN customers ON orders.customer_id=customers.customer_id
                                JOIN books ON orders.book_id=books.book_id;
                                """)
orders_lines=cursor.fetchall()
for line in orders_lines:
    print(f"\ncustomer:{line[0]}****The bought book:{line[1]}*****number:{line[2]}*****date of purchase:{line[2]}")

connection.close()
print("the database was closed successfully")