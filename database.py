import sqlite3
import os

DB_FILE = "loja.db"

def conectar():
    """Retorna uma conexão sqlite3 para loja.db"""
    conn = sqlite3.connect(DB_FILE, timeout=10)
    return conn

def criar_tabelas():
    """Cria as tabelas básicas se não existirem"""
    conn = conectar()
    cursor = conn.cursor()

    # Produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        fornecedor TEXT,
        nome TEXT,
        status TEXT,
        marca TEXT,
        preco REAL,
        quantidade INTEGER,
        categoria TEXT,
        validade TEXT,
        codigo_interno TEXT,
        observacoes TEXT
    )
    """)

    # Cabeçalho da venda
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venda_cabecalho (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        forma_pagamento TEXT,
        valor_total REAL
    )
    """)

    # Itens da venda
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venda_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER,
        produto_id INTEGER,
        quantidade INTEGER,
        valor_unitario REAL,
        valor_total REAL,
        FOREIGN KEY (venda_id) REFERENCES venda_cabecalho(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    """)

    conn.commit()
    conn.close()

# Garante criação ao importar
if not os.path.exists(DB_FILE):
    criar_tabelas()
else:
    try:
        criar_tabelas()
    except Exception:
        pass
