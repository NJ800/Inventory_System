import sqlite3
import hashlib
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DatabaseManager:
    def __init__(self):
        db_path = resource_path('inventory.db')
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.create_default_users()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Operators (
                operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductMasterList (
                barcode TEXT PRIMARY KEY,
                sku_id TEXT,
                category TEXT,
                subcategory TEXT,
                product_images TEXT,
                product_name TEXT,
                description TEXT,
                tax REAL,
                price REAL,
                default_unit TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS GoodsReceiving (
                grn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_barcode TEXT,
                supplier_name TEXT,
                supplier_address TEXT,
                quantity REAL,
                unit TEXT,
                rate REAL,
                total REAL,
                tax REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_barcode) REFERENCES ProductMasterList(barcode)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SalesForm (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_barcode TEXT,
                customer_name TEXT,
                customer_address TEXT,
                quantity REAL,
                unit TEXT,
                rate REAL,
                total REAL,
                tax REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_barcode) REFERENCES ProductMasterList(barcode)
            )
        ''')
        self.conn.commit()

    def create_default_users(self):
        cursor = self.conn.cursor()
        users = [
            ('operator1', hashlib.sha256('password1'.encode()).hexdigest()),
            ('operator2', hashlib.sha256('password2'.encode()).hexdigest())
        ]
        cursor.executemany(
            'INSERT OR IGNORE INTO Operators (username, password) VALUES (?, ?)', users
        )
        self.conn.commit()

    def get_connection(self):
        return self.conn

# Test block to verify the class works when run directly
if __name__ == "__main__":
    db = DatabaseManager()
    print("DatabaseManager initialized successfully!")
