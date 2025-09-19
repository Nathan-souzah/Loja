import sqlite3

def conectar ():
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nome TEXT NOT NULL,
        marca TEXT,
        preco Real NOT NULL,
        quantidade INTEGER NOT NULL
        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id TEXT,
        quantidade INTEGER,
        total REAL,
        FOREIGN KEY (produto_id) REFERENCES produtos(ID)
        )""")
    conn.commit()
    return conn
    