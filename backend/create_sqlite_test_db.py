import sqlite3

conn = sqlite3.connect("sqlpilot_test.db")
cursor = conn.cursor()


# Remove old tables if they exist
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS customers")


# -----------------------------
# Customers
# -----------------------------

cursor.execute("""
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL
    )
""")


# -----------------------------
# Products
# -----------------------------

cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")


# -----------------------------
# Orders
# -----------------------------

cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_amount REAL NOT NULL,

        FOREIGN KEY (customer_id)
            REFERENCES customers(id),

        FOREIGN KEY (product_id)
            REFERENCES products(id)
    )
""")


# -----------------------------
# Insert customers
# -----------------------------

customers = [
    (1, "Alice", "alice@example.com", "Bengaluru"),
    (2, "Bob", "bob@example.com", "Mumbai"),
    (3, "Charlie", "charlie@example.com", "Delhi"),
    (4, "David", "david@example.com", "Bengaluru"),
    (5, "Emma", "emma@example.com", "Chennai"),
]

cursor.executemany(
    """
    INSERT INTO customers
    VALUES (?, ?, ?, ?)
    """,
    customers
)


# -----------------------------
# Insert products
# -----------------------------

products = [
    (1, "Laptop", 75000.0, 10),
    (2, "Keyboard", 2500.0, 50),
    (3, "Mouse", 1200.0, 100),
    (4, "Monitor", 18000.0, 20),
    (5, "Headphones", 3500.0, 40),
]

cursor.executemany(
    """
    INSERT INTO products
    VALUES (?, ?, ?, ?)
    """,
    products
)


# -----------------------------
# Insert orders
# -----------------------------

orders = [
    (1, 1, 1, 1, 75000.0),
    (2, 1, 3, 2, 2400.0),
    (3, 2, 2, 1, 2500.0),
    (4, 3, 4, 1, 18000.0),
    (5, 4, 5, 2, 7000.0),
    (6, 5, 3, 3, 3600.0),
]

cursor.executemany(
    """
    INSERT INTO orders
    VALUES (?, ?, ?, ?, ?)
    """,
    orders
)


conn.commit()
conn.close()

print("SQLite test database created successfully!")
print("Database: sqlpilot_test.db")