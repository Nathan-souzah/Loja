# ui/vendas.py
import customtkinter as ctk
from tkinter import messagebox, ttk
from produtos import listar_produtos, buscar_produto_estoque
from vendas import registrar_venda
from ui.config import criar_janela

def tela():
    # === Janela ===
    janela, cfg = criar_janela("Registrar Venda", "1200x700")

    # === Frame Principal ===
    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"), corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

    # === Título ===
    titulo = ctk.CTkLabel(frame, text="Registrar Venda 🛒", font=("Inter", 22, "bold"), text_color=cfg.get("font_color"))
    titulo.grid(row=0, column=0, columnspan=6, pady=(15,25))

    # === Produtos ===
    produtos = listar_produtos()
    items = [f"{p[0]} - {p[2]} (Estoque: {p[5]})" for p in produtos]

    # === Campo Código de Barras ===
    ctk.CTkLabel(frame, text="Código de Barras:", font=("Inter", 14), text_color=cfg.get("font_color")).grid(row=1, column=0, sticky="e", padx=10)
    entry_codigo = ctk.CTkEntry(frame, fg_color="#1E293B", text_color=cfg.get("font_color"), border_color="#475569", corner_radius=8, height=32)
    entry_codigo.grid(row=1, column=1, padx=5, sticky="we")

    # === Treeview para carrinho ===
    columns = ("id", "nome", "quantidade", "preco_unit")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=180, anchor="center")
    tree.grid(row=3, column=0, columnspan=6, pady=15, sticky="nsew")

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=3, column=6, sticky="ns")

    # === Total ===
    ctk.CTkLabel(frame, text="Total:", font=("Inter", 16, "bold"), text_color=cfg.get("font_color")).grid(row=4, column=4, sticky="e")
    total_entry = ctk.CTkEntry(frame, width=100, font=("Inter", 16, "bold"), justify="center")
    total_entry.grid(row=4, column=5, sticky="w")
    total_entry.configure(state="readonly")

    # === Funções ===
    def atualizar_total():
        total = 0.0
        for child in tree.get_children():
            values = tree.item(child, "values")
            try:
                qtd = int(values[2])
                preco = float(values[3])
            except (IndexError, ValueError):
                qtd = 0
                preco = 0
            total += qtd * preco
        total_entry.configure(state="normal")
        total_entry.delete(0, "end")
        total_entry.insert(0, str(total))
        total_entry.configure(state="readonly")

    def adicionar_produto_codigo():
        codigo = entry_codigo.get().strip()
        if not codigo:
            return
        produto = buscar_produto_estoque(codigo)
        if not produto:
            messagebox.showinfo("Não encontrado", "Produto não encontrado no estoque.")
            return
        produto_id = produto["id"]
        nome = produto["nome"]
        preco_unit = float(produto["preco"])
        qtd = 1
        tree.insert("", "end", values=(produto_id, nome, qtd, preco_unit))
        atualizar_total()
        entry_codigo.delete(0, "end")

    # === Bind Enter para código de barras ===
    entry_codigo.bind("<Return>", lambda event: adicionar_produto_codigo())

    # === Combobox de produtos ===
    ctk.CTkLabel(frame, text="Produto:", font=("Inter", 14), text_color=cfg.get("font_color")).grid(row=2, column=0, sticky="e", padx=10)
    comb_prod = ttk.Combobox(frame, values=items, state="readonly", width=50)
    comb_prod.grid(row=2, column=1, columnspan=2, padx=10, pady=8, sticky="we")

    ctk.CTkLabel(frame, text="Quantidade:", font=("Inter", 14), text_color=cfg.get("font_color")).grid(row=2, column=3, sticky="e")
    entry_qtd = ctk.CTkEntry(frame, fg_color="#1E293B", text_color=cfg.get("font_color"), border_color="#475569", corner_radius=8, height=32)
    entry_qtd.grid(row=2, column=4, padx=5, sticky="we")

    ctk.CTkLabel(frame, text="Forma de Pagamento:", font=("Inter", 14), text_color=cfg.get("font_color")).grid(row=5, column=0, sticky="e", padx=10)
    formas = ["💵 Dinheiro", "💳 Débito", "💳 Crédito", "💠 Pix"]
    comb_forma = ttk.Combobox(frame, values=formas, state="readonly", width=20)
    comb_forma.grid(row=5, column=1, padx=10, pady=8, sticky="w")
    comb_forma.set(formas[0])

    # === Adicionar pelo combobox ===
    def adicionar_produto():
        sel = comb_prod.get()
        if not sel:
            messagebox.showerror("Erro", "Selecione um produto.")
            return
        produto_id = int(sel.split(" - ")[0])
        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return
        prod = next((p for p in produtos if p[0] == produto_id), None)
        if not prod:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return
        preco_unit = float(prod[4])
        tree.insert("", "end", values=(produto_id, prod[2], qtd, preco_unit))
        atualizar_total()

    def remover_produto():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Erro", "Selecione um produto para remover.")
            return
        for item in sel:
            tree.delete(item)
        atualizar_total()

    def finalizar_venda():
        if not tree.get_children():
            messagebox.showerror("Erro", "Nenhum produto no carrinho.")
            return
        forma_pagamento = comb_forma.get()
        sucesso = True
        for item in tree.get_children():
            pid, nome, qtd, preco_unit = tree.item(item, "values")
            ok = registrar_venda(int(pid), int(qtd), float(preco_unit), forma_pagamento)
            if not ok:
                sucesso = False
        if sucesso:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao registrar alguma venda.")

    # === Botões ===
    btn_add_prod = ctk.CTkButton(frame, text="➕ Adicionar Produto", width=180, height=40, command=adicionar_produto, fg_color=cfg.get("button_color"))
    btn_add_prod.grid(row=2, column=5, padx=10, pady=10)

    btn_remove_prod = ctk.CTkButton(frame, text="🗑️ Remover Produto", width=180, height=40, command=remover_produto, fg_color="#EF4444")
    btn_remove_prod.grid(row=2, column=6, padx=10, pady=10)

    btn_finalizar = ctk.CTkButton(frame, text="💳 Finalizar Venda", width=200, height=40, command=finalizar_venda, fg_color="#10B981")
    btn_finalizar.grid(row=6, column=0, columnspan=6, pady=20)

    atualizar_total()
    janela.mainloop()
