import customtkinter as ctk
from tkinter import ttk, messagebox
from produtos import listar_produtos
from vendas import registrar_venda
from ui.config import criar_janela

def tela():
    janela, cfg = criar_janela("Registrar Venda", "800x600")
    carrinho = []

    # Código de barras
    ctk.CTkLabel(janela, text="Código de Barras:", text_color=cfg.get("font_color")).pack(pady=5)
    entry_codigo = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_codigo.pack()

    ctk.CTkLabel(janela, text="Quantidade:", text_color=cfg.get("font_color")).pack(pady=5)
    entry_qtd = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_qtd.pack()

    # Lista do carrinho
    tree = ttk.Treeview(janela, columns=("produto","qtd","preco","subtotal"), show="headings")
    tree.heading("produto", text="Produto")
    tree.heading("qtd", text="Qtd")
    tree.heading("preco", text="Preço")
    tree.heading("subtotal", text="Subtotal")
    tree.pack(fill="both", expand=True, pady=10)

    lbl_total = ctk.CTkLabel(janela, text="Total: R$ 0.00", font=(cfg.get("font"), 14, "bold"), text_color=cfg.get("font_color"))
    lbl_total.pack(pady=10)

    # Forma de pagamento
    ctk.CTkLabel(janela, text="Forma de Pagamento:", text_color=cfg.get("font_color")).pack(pady=5)
    pagamento = ttk.Combobox(janela, values=["Dinheiro", "Pix", "Cartão"])
    pagamento.pack()
    pagamento.current(0)

    sub_pagamento = ttk.Combobox(janela, values=["Crédito", "Débito", "Alimentação"])
    sub_pagamento.pack_forget()

    def update_sub_pagamento(event):
        if pagamento.get() == "Cartão":
            sub_pagamento.pack()
        else:
            sub_pagamento.pack_forget()
    pagamento.bind("<<ComboboxSelected>>", update_sub_pagamento)

    # Funções
    def adicionar_produto():
        codigo = entry_codigo.get().strip()
        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produtos = listar_produtos()
        produto = next((p for p in produtos if p[1]==codigo), None)
        if not produto:
            messagebox.showwarning("Erro", "Produto não encontrado.")
            return

        produto_id, _, nome, _, preco, estoque = produto
        if qtd > estoque:
            messagebox.showwarning("Erro", "Estoque insuficiente.")
            return

        subtotal = preco * qtd
        carrinho.append((produto_id, nome, qtd, preco, subtotal))
        tree.insert("", "end", values=(nome, qtd, f"R$ {preco:.2f}", f"R$ {subtotal:.2f}"))
        atualizar_total()

    def atualizar_total():
        total = sum(item[4] for item in carrinho)
        lbl_total.configure(text=f"Total: R$ {total:.2f}")

    def remover_item():
        selected = tree.selection()
        if not selected: return
        index = tree.index(selected[0])
        tree.delete(selected[0])
        carrinho.pop(index)
        atualizar_total()

    def finalizar_venda():
        if not carrinho:
            messagebox.showerror("Erro", "Carrinho vazio.")
            return
        forma = pagamento.get()
        if forma=="Cartão": forma += " - " + sub_pagamento.get()

        sucesso = True
        for produto_id, nome, qtd, preco, subtotal in carrinho:
            ok = registrar_venda(produto_id, qtd, preco, forma)
            if not ok: sucesso = False

        if sucesso:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Ocorreu um problema ao registrar a venda.")

    # Botões
    ctk.CTkButton(janela, text="Adicionar Produto", fg_color=cfg.get("button_color"), command=adicionar_produto).pack(pady=5)
    ctk.CTkButton(janela, text="Remover Produto", fg_color=cfg.get("button_color"), command=remover_item).pack(pady=5)
    ctk.CTkButton(janela, text="Finalizar Venda", fg_color=cfg.get("button_color"), command=finalizar_venda).pack(pady=10)
    ctk.CTkButton(janela, text="Fechar", fg_color=cfg.get("button_color"), command=janela.destroy).pack(pady=5)
