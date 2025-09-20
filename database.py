import sqlite3
from datetime import datetime

DB_FILE = "loja.db"

def conectar():
    """
    Cria a conexão com o banco e retorna o objeto conexão.
    Cria as tabelas caso não existam.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 🔹 Tabela de produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nome TEXT NOT NULL,
        marca TEXT,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    """)

    # 🔹 Tabela de vendas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        total REAL,
        forma_pagamento TEXT,
        data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    conn.commit()
    return conn

def popular_dados_teste():
    """
    Insere dados de teste para produtos e vendas.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Produtos de exemplo
    produtos_exemplo = [
        ("7891234567890", "Coca-Cola 2L", "Coca-Cola", 9.99, 50),
        ("7899876543210", "Arroz 5kg", "Tio João", 25.90, 30),
        ("7895554443332", "Feijão Carioca 1kg", "Kicaldo", 8.50, 40),
        ("7891112223334", "Detergente Neutro 500ml", "Ypê", 2.80, 100),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO produtos (codigo, nome, marca, preco, quantidade)
    VALUES (?, ?, ?, ?, ?)
    """, produtos_exemplo)

    # Vendas de exemplo
    vendas_exemplo = [
        (1, 2, 19.98, "Dinheiro", datetime(2025, 9, 18, 14, 30)),
        (2, 1, 25.90, "Cartão", datetime(2025, 9, 19, 10, 15)),
        (3, 3, 25.50, "Pix", datetime(2025, 9, 20, 9, 5)),
    ]

    cursor.executemany("""
    INSERT INTO vendas (produto_id, quantidade, total, forma_pagamento, data)
    VALUES (?, ?, ?, ?, ?)
    """, vendas_exemplo)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    popular_dados_teste()
    print("✅ Banco de dados 'loja.db' criado e populado com dados de teste!")
