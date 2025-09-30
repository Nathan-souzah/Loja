from database import conectar

def adicionar_produto(codigo, fornecedor, nome, status, marca, preco, quantidade, categoria, validade, codigo_interno, observacoes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (codigo, fornecedor, nome, status, marca, preco, quantidade, categoria, validade, codigo_interno, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (codigo, fornecedor, nome, status, marca, preco, quantidade, categoria, validade, codigo_interno, observacoes))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos
