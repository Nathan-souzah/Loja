# database.py
import sqlite3
import os

DB_FILE = "loja.db"

def conectar():
    """Retorna uma conexão sqlite3 para loja.db"""
    # usa check_same_thread=False para maior flexibilidade se precisar de threads (opcional)
    conn = sqlite3.connect(DB_FILE, timeout=10)
    return conn

def criar_tabelas():
    """Cria as tabelas básicas se não existirem"""
    conn = conectar()
    cursor = conn.cursor()

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        valor_unitario REAL,
        valor_total REAL,
        forma_pagamento TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

# garante criação do banco/tabelas ao importar
if not os.path.exists(DB_FILE):
    criar_tabelas()
else:
    # caso haja arquivo, ainda garantimos as tabelas
    try:
        criar_tabelas()
    except Exception:
        pass
