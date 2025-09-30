import sqlite3
import os

DB_FILE = "loja.db"

def conectar():
    """Conecta ao banco de dados loja.db e cria o arquivo se não existir"""
    conn = sqlite3.connect(DB_FILE)
    return conn

def criar_tabelas():
    """Cria as tabelas produtos e vendas se não existirem"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT,
        nome TEXT,
        preco REAL,
        quantidade INTEGER,
        marca TEXT,
        categoria TEXT,
        validade TEXT,
        codigo_interno TEXT,
        status TEXT,
        observacoes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        valor_total REAL,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

# Chamar criar_tabelas() automaticamente quando o módulo for importado
if not os.path.exists(DB_FILE):
    criar_tabelas()
