# produtos.py
from database import conectar
import datetime

def adicionar_produto(dados: dict) -> bool:
    """
    Recebe um dicionário com chaves:
    codigo_barras, fornecedor, nome, status, marca, preco, quantidade,
    categoria, validade, codigo_interno, observacoes
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos
            (codigo, fornecedor, nome, status, marca, preco, quantidade, categoria, validade, codigo_interno, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados.get("codigo_barras", ""),
            dados.get("fornecedor", ""),
            dados.get("nome", ""),
            dados.get("status", "Ativo"),
            dados.get("marca", ""),
            float(dados.get("preco", 0) or 0),
            int(dados.get("quantidade", 0) or 0),
            dados.get("categoria", ""),
            dados.get("validade", ""),
            dados.get("codigo_interno", ""),
            dados.get("observacoes", "")
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro adicionar_produto:", e)
        return False

def listar_produtos() -> list:
    """Retorna lista de produtos como tuplas (id, codigo, nome, fornecedor, preco, quantidade, ...)"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, fornecedor, preco, quantidade, marca, categoria, validade, codigo_interno, status FROM produtos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def buscar_por_codigo(codigo_barras: str):
    """Retorna o produto, ou None"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo, nome, fornecedor, preco, quantidade, marca, categoria, validade, codigo_interno, status FROM produtos WHERE codigo = ?", (codigo_barras,))
    row = cursor.fetchone()
    conn.close()
    return row

def atualizar_estoque(produto_id: int, nova_qtd: int) -> bool:
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd, produto_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Erro atualizar_estoque:", e)
        return False
