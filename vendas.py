from database import conectar
from datetime import datetime

def listar_vendas():
    """
    Retorna todas as vendas do banco.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    conn.close()
    return vendas

def registrar_venda(produto_id, quantidade, preco, forma_pagamento):
    """
    Registra uma venda e atualiza o estoque do produto.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        total = preco * quantidade
        data_venda = datetime.now()

        # Inserir venda
        cursor.execute("""
        INSERT INTO vendas (produto_id, quantidade, total, forma_pagamento, data)
        VALUES (?, ?, ?, ?, ?)
        """, (produto_id, quantidade, total, forma_pagamento, data_venda))

        # Atualizar estoque
        cursor.execute("""
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        """, (quantidade, produto_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro ao registrar venda:", e)
        return False
