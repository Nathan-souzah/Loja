import tkinter as tk
from tkinter import messagebox, ttk
from produtos import listar_produtos
from vendas import registrar_venda

def tela():
    janela = tk.Toplevel()
    janela.title("Registrar Venda")
    janela.geometry("600x500")

    # Lista de produtos (combobox)
    tk.Label(janela, text="Produto:").pack(pady=5)
    produtos = listar_produtos()
    produtos_dict = {f"{p[2]} ({p[1]})": p for p in produtos}  # nome + código de barras -> dados
    combo_produtos = ttk.Combobox(janela, values=list(produtos_dict.keys()))
    combo_produtos.pack()
    combo_produtos.current(0)

    # Quantidade
    tk.Label(janela, text="Quantidade:").pack(pady=5)
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()

    # Forma de pagamento
    tk.Label(janela, text="Forma de Pagamento:").pack(pady=5)
    pagamento = ttk.Combobox(janela, values=["Dinheiro", "Cartão", "Pix"])
    pagamento.pack()
    pagamento.current(0)

    # Carrinho de venda (Treeview)
    tk.Label(janela, text="Carrinho:").pack(pady=5)
    tree = ttk.Treeview(janela, columns=("Produto", "Qtd", "Preço", "Total"), show="headings")
    tree.heading("Produto", text="Produto")
    tree.heading("Qtd", text="Qtd")
    tree.heading("Preço", text="Preço")
    tree.heading("Total", text="Total")
    tree.pack(pady=5, fill=tk.BOTH, expand=True)

    carrinho = []

    # Adicionar produto ao carrinho
    def adicionar_produto():
        selecionado = combo_produtos.get()
        if not selecionado:
            messagebox.showwarning("Erro", "Selecione um produto.")
            return
        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto = produtos_dict[selecionado]
        produto_id, _, nome, _, preco, estoque = produto
        if qtd > estoque:
            messagebox.showwarning("Erro", "Quantidade insuficiente.")
            return

        # Adicionar ao carrinho
        carrinho.append((produto_id, nome, qtd, preco))
        total = qtd * preco
        tree.insert("", tk.END, values=(nome, qtd, f"R$ {preco:.2f}", f"R$ {total:.2f}"))

        # Limpar entrada
        entry_qtd.delete(0, tk.END)

    # Finalizar venda
    def finalizar_venda():
        if not carrinho:
            messagebox.showwarning("Erro", "O carrinho está vazio.")
            return
        forma = pagamento.get()
        erros = []
        for item in carrinho:
            produto_id, nome, qtd, preco = item
            ok = registrar_venda(produto_id, qtd, preco, forma)
            if not ok:
                erros.append(nome)

        if erros:
            messagebox.showerror("Erro", f"Não foi possível registrar os produtos: {', '.join(erros)}")
        else:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            janela.destroy()

    tk.Button(janela, text="Adicionar Produto ao Carrinho", command=adicionar_produto).pack(pady=5)
    tk.Button(janela, text="Finalizar Venda", command=finalizar_venda).pack(pady=10)
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=5)
