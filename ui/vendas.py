import customtkinter as ctk
from tkinter import ttk, messagebox
from produtos import listar_produtos
from vendas import registrar_venda
from ui.config import criar_janela

def tela():
    janela, cfg = criar_janela("Registrar Venda", "800x650")
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

    # Frame para os botões
    frame_botoes = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_botoes.pack(pady=20)

    botoes = [
        ("Adicionar Produto", adicionar_produto),
        ("Remover Produto", remover_item),
        ("Finalizar Venda", finalizar_venda),
    ]

    # Primeira linha: 3 botões
    for index, (texto, comando) in enumerate(botoes):
        ctk.CTkButton(frame_botoes, text=texto, fg_color=cfg.get("button_color"),
                      width=180, height=50, command=comando).grid(row=0, column=index, padx=10, pady=5)

    # Segunda linha: Fechar centralizado
    ctk.CTkButton(frame_botoes, text="Fechar", fg_color=cfg.get("button_color"),
                  width=180, height=50, command=janela.destroy).grid(row=1, column=0, columnspan=3, pady=5)
