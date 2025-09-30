from database import conectar

def registrar_venda(produto_id, quantidade, preco, forma_pagamento):
    total = quantidade * preco
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vendas (produto_id, quantidade, preco, total, forma_pagamento)
            VALUES (?, ?, ?, ?, ?)
        """, (produto_id, quantidade, preco, total, forma_pagamento))

        # Atualiza estoque
        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()
