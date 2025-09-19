import sqlite3

def conectar():
    conn = sqlite3.connect("loja.db", timeout=10)  # timeout evita database is locked
    cursor = conn.cursor()

    # Tabela produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nome TEXT NOT NULL,
        marca TEXT,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    """)

    # Tabela vendas com forma_pagamento
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        total REAL,
        forma_pagamento TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    conn.commit()
    return conn
