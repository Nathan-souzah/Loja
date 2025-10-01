# vendas.py
from database import conectar
from produtos import buscar_por_codigo, atualizar_estoque
import datetime

def registrar_venda(produto_id: int, quantidade: int, valor_unitario: float, forma_pagamento: str) -> bool:
    """
    Registra uma venda e atualiza estoque.
    produto_id: id do produto (INTEGER)
    quantidade: quantidade vendida (INTEGER)
    valor_unitario: preço por unidade
    forma_pagamento: texto (ex: 'Dinheiro', 'Cartão - Crédito')
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # verifica estoque atual
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        estoque_atual = row[0]
        if quantidade > estoque_atual:
            conn.close()
            return False

        valor_total = float(valor_unitario) * int(quantidade)
        data = datetime.datetime.now().isoformat(timespec='seconds')

        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, valor_unitario, valor_total, forma_pagamento, data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produto_id, quantidade, valor_unitario, valor_total, forma_pagamento, data))

        # atualiza estoque
        novo_estoque = estoque_atual - quantidade
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_estoque, produto_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro registrar_venda:", e)
        return False
