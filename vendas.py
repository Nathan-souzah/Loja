from database import conectar
from datetime import datetime

def registrar_venda(forma_pagamento, itens):
    """
    Registra uma venda no banco.
    itens = lista de tuplas (produto_id, quantidade, preco_unitario)
    """
    conn = conectar()
    cursor = conn.cursor()

    try:
        # Calcula total
        total = sum(qtd * preco for _, qtd, preco in itens)

        # Cabeçalho
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO venda_cabecalho (data, forma_pagamento, valor_total)
            VALUES (?, ?, ?)
        """, (data, forma_pagamento, total))
        venda_id = cursor.lastrowid

        # Itens
        for pid, qtd, preco in itens:
            cursor.execute("""
                INSERT INTO venda_itens (venda_id, produto_id, quantidade, valor_unitario, valor_total)
                VALUES (?, ?, ?, ?, ?)
            """, (venda_id, pid, qtd, preco, qtd * preco))

            # Atualiza estoque
            cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (qtd, pid))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("Erro ao registrar venda:", e)
        conn.rollback()
        conn.close()
        return False
