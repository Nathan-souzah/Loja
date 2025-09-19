from database import conectar

def registrar_venda(produto_id: int, quantidade: int, preco: float, forma_pagamento: str):
    conn = conectar()
    cursor = conn.cursor()
    
    # Buscar estoque atual
    cursor.execute("SELECT quantidade FROM produtos WHERE id=?", (produto_id,))
    estoque = cursor.fetchone()[0]
    
    if quantidade > estoque:
        conn.close()
        return False  # estoque insuficiente

    # Atualizar estoque
    novo_estoque = estoque - quantidade
    total = quantidade * preco
    cursor.execute("UPDATE produtos SET quantidade=? WHERE id=?", (novo_estoque, produto_id))
    
    # Registrar venda com forma de pagamento
    cursor.execute(
        "INSERT INTO vendas (produto_id, quantidade, total, forma_pagamento) VALUES (?, ?, ?, ?)",
        (produto_id, quantidade, total, forma_pagamento)
    )
    
    conn.commit()
    conn.close()
    return True
