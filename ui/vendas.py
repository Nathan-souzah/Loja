import customtkinter as ctk
from tkinter import ttk, messagebox
from produtos import listar_produtos
from vendas import registrar_venda
from ui.config import criar_janela

def tela():
    janela, cfg = criar_janela("PDV Profissional", "900x700")
    carrinho = []

    # ---------- PRODUTOS DO BANCO ----------
    produtos = listar_produtos()
    produtos_dict = {p[2]: p for p in produtos}  # {nome: produto_tuple}
    nomes_produtos = list(produtos_dict.keys())

    # ---------- FRAME DE ENTRADA ----------
    frame_input = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_input.pack(pady=10, fill="x", padx=20)

    # Produto
    ctk.CTkLabel(frame_input, text="Produto:", text_color=cfg.get("font_color")).grid(row=0, column=0, padx=5, pady=5)
    combo_produto = ttk.Combobox(frame_input, values=nomes_produtos, state="readonly", width=30)
    combo_produto.grid(row=0, column=1, padx=5, pady=5)
    if nomes_produtos:
        combo_produto.current(0)

    # Quantidade
    ctk.CTkLabel(frame_input, text="Qtd:", text_color=cfg.get("font_color")).grid(row=0, column=2, padx=5, pady=5)
    entry_qtd = ctk.CTkEntry(frame_input, fg_color="#FFFFFF", text_color=cfg.get("font_color"), width=5)
    entry_qtd.grid(row=0, column=3, padx=5, pady=5)

    # Botão Adicionar
    def adicionar_produto():
        nome_produto = combo_produto.get()
        if not nome_produto or nome_produto not in produtos_dict:
            messagebox.showwarning("Erro", "Produto inválido.")
            return
        produto = produtos_dict[nome_produto]

        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto_id, codigo, nome, marca, preco, estoque = produto
        if qtd > estoque:
            messagebox.showwarning("Erro", "Estoque insuficiente.")
            return

        subtotal = preco * qtd
        carrinho.append((produto_id, nome, qtd, preco, subtotal))
        tree.insert("", "end", values=(nome, qtd, f"R$ {preco:.2f}", f"R$ {subtotal:.2f}"))
        atualizar_total()

    ctk.CTkButton(frame_input, text="Adicionar", fg_color=cfg.get("button_color"), width=120, height=35,
                  command=adicionar_produto).grid(row=0, column=4, padx=10)

    # ---------- FRAME PAGAMENTO ----------
    frame_pagamento = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_pagamento.pack(pady=10, fill="x", padx=20)

    ctk.CTkLabel(frame_pagamento, text="Pagamento:", text_color=cfg.get("font_color")).grid(row=0, column=0, padx=5)
    pagamento = ttk.Combobox(frame_pagamento, values=["Dinheiro", "Pix", "Cartão"], width=12)
    pagamento.grid(row=0, column=1, padx=5)
    pagamento.current(0)

    sub_pagamento = ttk.Combobox(frame_pagamento, values=["Crédito", "Débito", "Alimentação"], width=12)
    sub_pagamento.grid(row=0, column=2, padx=5)
    sub_pagamento.grid_remove()  # inicialmente escondido

    def update_sub_pagamento(event):
        if pagamento.get() == "Cartão":
            sub_pagamento.grid()
        else:
            sub_pagamento.grid_remove()
    pagamento.bind("<<ComboboxSelected>>", update_sub_pagamento)

    # ---------- CARRINHO ----------
    tree = ttk.Treeview(janela, columns=("produto","qtd","preco","subtotal"), show="headings", height=15)
    tree.heading("produto", text="Produto")
    tree.heading("qtd", text="Qtd")
    tree.heading("preco", text="Preço")
    tree.heading("subtotal", text="Subtotal")
    tree.pack(fill="both", expand=True, pady=10, padx=20)

    lbl_total = ctk.CTkLabel(janela, text="Total: R$ 0.00", font=(cfg.get("font"), 16, "bold"), text_color=cfg.get("font_color"))
    lbl_total.pack(pady=10)

    # ---------- FUNÇÕES ----------
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

    # ---------- BOTOES ----------
    frame_botoes = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_botoes.pack(pady=20)

    botoes = [
        ("Remover Item", remover_item),
        ("Finalizar Venda", finalizar_venda),
        ("Fechar", janela.destroy)
    ]

    for index, (texto, comando) in enumerate(botoes):
        ctk.CTkButton(frame_botoes, text=texto, fg_color=cfg.get("button_color"),
                      width=180, height=50, command=comando).grid(row=0, column=index, padx=10, pady=5)

    janela.mainloop()


if __name__ == "__main__":
    tela()

