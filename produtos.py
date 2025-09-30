from database import conectar

def adicionar_produto(codigo, nome, marca, preco, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (codigo, nome, marca, preco, quantidade) Values (?, ?, ?, ?, ?)", 
                   (codigo, nome, marca, preco, quantidade))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    return dados

def remover_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    
    