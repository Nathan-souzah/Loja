import tkinter as tk
from tkinter import messagebox, ttk
from produtos import listar_produtos
from vendas import registrar_venda

def tela():
    janela = tk.Toplevel()
    janela.title("Registrar Venda")
    janela.geometry("400x300")

    tk.Label(janela, text="Código de Barras:").pack(pady=5)
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()

    tk.Label(janela, text="Quantidade:").pack(pady=5)
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()

    tk.Label(janela, text="Forma de Pagamento:").pack(pady=5)
    pagamento = ttk.Combobox(janela, values=["Dinheiro", "Cartão", "Pix"])
    pagamento.pack()
    pagamento.current(0)

    def vender():
        codigo = entry_codigo.get().strip()
        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        forma = pagamento.get()
        produtos = listar_produtos()
        produto_encontrado = None

        for p in produtos:
            if p[1] == codigo:  # p[1] = código de barras
                produto_encontrado = p
                break

        if not produto_encontrado:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return

        produto_id, _, nome, _, preco, estoque = produto_encontrado
        if qtd > estoque:
            messagebox.showwarning("Erro", "Quantidade insuficiente.")
            return

        ok = registrar_venda(produto_id, qtd, preco, forma)
        if ok:
            messagebox.showinfo("Sucesso", f"Venda de {qtd}x {nome} registrada!\nPagamento: {forma}")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível registrar a venda.")

    tk.Button(janela, text="Registrar Venda", command=vender).pack(pady=10)
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=5)
