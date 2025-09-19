from database import conectar

def registrar_venda(produto_id, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id))
    estoque = cursor.fetchone()[0]
    
    if quantidade > estoque:
        conn.close()
        return False
    
    novo_estoque = estoque - quantidade
    total = quantidade * preco

    cursor.execute("UPDATE produtos SET quantidade =? WHERE id=?", (novo_estoque, produto_id)) 
    cursor.ececute("INSERT INTO vendas ( produto_id, quantidade, total) VALUES (?, ?, ?)", 
                   (produto_id, quantidade, total))
    conn.commit()
    conn.close()
    return True