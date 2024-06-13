import sqlite3
from tabulate import tabulate

def create_tables():
    connection = sqlite3.connect('dealership.db')
    cursor = connection.cursor()
    
    # Drop and create tables to ensure correct schema
    cursor.execute('DROP TABLE IF EXISTS customers')
    cursor.execute('DROP TABLE IF EXISTS vehicles')
    cursor.execute('DROP TABLE IF EXISTS sales_persons')
    cursor.execute('DROP TABLE IF EXISTS invoice')
    
    # Customers table with added salesperson_id column
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   phone_number TEXT NOT NULL,
                   salesperson_id INTEGER,
                   FOREIGN KEY (salesperson_id) REFERENCES sales_persons(id)
    )''')
    
    # Vehicles table
    cursor.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   make TEXT NOT NULL,
                   model TEXT NOT NULL,
                   color TEXT NOT NULL,
                   customer_id INTEGER,
                   FOREIGN KEY (customer_id) REFERENCES customers(id)
    )''')
    
    # Sales Persons table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales_persons(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL
    )''')
    
    # Invoice table
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoice(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_id INTEGER,
                   salesperson_id INTEGER,
                   vehicle_id INTEGER,
                   FOREIGN KEY (customer_id) REFERENCES customers(id),
                   FOREIGN KEY (salesperson_id) REFERENCES sales_persons(id),
                   FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
    )''')
    
    connection.commit()
    connection.close()

create_tables()

class DealershipDB:
    def __init__(self):
        self.connection = sqlite3.connect('dealership.db')
        self.cursor = self.connection.cursor()

    # Adding a salesperson
    def add_salesperson(self, first_name, last_name):
        self.cursor.execute('INSERT INTO sales_persons (first_name, last_name) VALUES (?, ?)', (first_name, last_name))
        self.connection.commit()

    # Adding a customer
    def add_customer(self, first_name, last_name, phone_number):
        self.cursor.execute('INSERT INTO customers (first_name, last_name, phone_number) VALUES (?, ?, ?)', (first_name, last_name, phone_number))
        self.connection.commit()

    # Adding a vehicle
    def add_vehicle(self, make, model, color, customer_id):
        self.cursor.execute('INSERT INTO vehicles (make, model, color, customer_id) VALUES (?, ?, ?, ?)', (make, model, color, customer_id))
        self.connection.commit()

    # Check if salesperson exists
    def salesperson_exists(self, salesperson_id):
        self.cursor.execute('SELECT * FROM sales_persons WHERE id = ?', (salesperson_id,))
        return self.cursor.fetchone() is not None

    # Assign a salesperson to a customer
    def assign_salesperson_to_customer(self, customer_id, salesperson_id):
        if self.salesperson_exists(salesperson_id):
            self.cursor.execute('UPDATE customers SET salesperson_id = ? WHERE id = ?', (salesperson_id, customer_id))
            self.connection.commit()
            print(f"Sales Person {salesperson_id} assigned to Customer {customer_id}.")
        else:
            print(f"Sales Person with ID {salesperson_id} does not exist.")

    # List all salespersons
    def list_salespersons(self):
        self.cursor.execute("SELECT * FROM sales_persons")
        sales_persons = self.cursor.fetchall()
        headers = ["ID", "First Name", "Last Name"]
        print(tabulate(sales_persons, headers, tablefmt="grid"))

    # List all customers
    def list_customers(self):
        query = '''
            SELECT customers.id, customers.first_name, customers.last_name, customers.phone_number, sales_persons.id,
            sales_persons.first_name, sales_persons.last_name
            FROM customers
            LEFT JOIN sales_persons ON customers.salesperson_id = sales_persons.id
        '''
        self.cursor.execute(query)
        customers = self.cursor.fetchall()
        headers = ["Customer ID", "First Name", "Last Name", "Phone Number", "Sales Person ID", "Sales Person First Name", "Sales Person Last Name"]
        print(tabulate(customers, headers, tablefmt="grid"))

    # List all vehicles
    def list_vehicles(self):
        query = '''
            SELECT vehicles.id, vehicles.make, vehicles.model, vehicles.color, customers.id, customers.first_name, customers.last_name
            FROM vehicles
            LEFT JOIN customers ON vehicles.customer_id = customers.id
        '''
        self.cursor.execute(query)
        vehicles = self.cursor.fetchall()
        headers = ["Vehicle ID", "Make", "Model", "Color", "Customer ID", "Customer First Name", "Customer Last Name"]
        print(tabulate(vehicles, headers, tablefmt="grid"))

    def close(self):
        self.connection.close()

def main():
    db = DealershipDB()

    while True:
        print("\n1. Add Sales Person")
        print("2. Add Customer")
        print("3. Add Vehicle")
        print("4. Assign Sales Person to Customer")
        print("5. List Sales Persons")
        print("6. List Customers")
        print("7. List Vehicles")
        print("8. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            first_name = input("Enter Sales Person First Name: ")
            last_name = input("Enter Sales Person Last Name: ")
            db.add_salesperson(first_name, last_name)

        elif choice == '2':
            first_name = input("Enter Customer's First Name: ")
            last_name = input("Enter Customer's Last Name: ")
            phone_number = input("Enter Customer's phone number: ")
            db.add_customer(first_name, last_name, phone_number)

        elif choice == '3':
            make = input("Enter Vehicle Make: ")
            model = input("Enter Vehicle Model: ")
            color = input("Enter Vehicle Color: ")
            customer_id = int(input("Enter Customer's ID: "))
            db.add_vehicle(make, model, color, customer_id)

        elif choice == '4':
            customer_id = int(input("Enter Customer's ID: "))
            salesperson_id = int(input("Enter Sales Person's ID: "))
            db.assign_salesperson_to_customer(customer_id, salesperson_id)

        elif choice == '5':
            db.list_salespersons()

        elif choice == '6':
            db.list_customers()

        elif choice == '7':
            db.list_vehicles()

        elif choice == '8':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == '__main__':
    main()
