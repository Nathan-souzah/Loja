import customtkinter as ctk
from tkinter import messagebox
from produtos import adicionar_produto  # sua função que grava no banco
from api import buscar_internet
from ui.config import criar_janela

def tela():
    janela, cfg = criar_janela("Cadastro de Produto - PDV Compacto", "1000x600")

    # ---------- CENTRALIZAÇÃO ----------
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_rowconfigure(2, weight=1)
    janela.grid_columnconfigure(0, weight=1)
    janela.grid_columnconfigure(2, weight=1)

    frame_central = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_central.grid(row=1, column=1, padx=20, pady=10)

    for i in range(5):
        frame_central.grid_rowconfigure(i, weight=1)
    for j in range(6):
        frame_central.grid_columnconfigure(j, weight=1, uniform="col")

    # ---------- CAMPOS ----------
    # Linha 1
    ctk.CTkLabel(frame_central, text="Código de Barras:", text_color=cfg.get("font_color")).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_codigo = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_codigo.grid(row=0, column=1, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Fornecedor:", text_color=cfg.get("font_color")).grid(row=0, column=2, sticky="e", padx=5, pady=5)
    entry_fornecedor = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_fornecedor.grid(row=0, column=3, sticky="we", padx=5, pady=5)

    # Linha 2
    ctk.CTkLabel(frame_central, text="Nome:", text_color=cfg.get("font_color")).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_nome = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_nome.grid(row=1, column=1, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Status:", text_color=cfg.get("font_color")).grid(row=1, column=2, sticky="e", padx=5, pady=5)
    combobox_status = ctk.CTkComboBox(frame_central, values=["Ativo", "Inativo"], fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    combobox_status.set("Ativo")
    combobox_status.grid(row=1, column=3, sticky="we", padx=5, pady=5)

    # Linha 3
    ctk.CTkLabel(frame_central, text="Marca:", text_color=cfg.get("font_color")).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_marca = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_marca.grid(row=2, column=1, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Preço:", text_color=cfg.get("font_color")).grid(row=2, column=2, sticky="e", padx=5, pady=5)
    entry_preco = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_preco.grid(row=2, column=3, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Quantidade:", text_color=cfg.get("font_color")).grid(row=2, column=4, sticky="e", padx=5, pady=5)
    entry_qtd = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_qtd.grid(row=2, column=5, sticky="we", padx=5, pady=5)

    # Linha 4
    ctk.CTkLabel(frame_central, text="Categoria:", text_color=cfg.get("font_color")).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    categorias = ["Alimentício", "Eletrônico", "Higiene", "Vestuário", "Outros"]
    combobox_categoria = ctk.CTkComboBox(frame_central, values=categorias, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    combobox_categoria.set("Selecione a categoria")
    combobox_categoria.grid(row=3, column=1, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Data Validade:", text_color=cfg.get("font_color")).grid(row=3, column=2, sticky="e", padx=5, pady=5)
    entry_validade = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_validade.grid(row=3, column=3, sticky="we", padx=5, pady=5)

    ctk.CTkLabel(frame_central, text="Código Interno:", text_color=cfg.get("font_color")).grid(row=3, column=4, sticky="e", padx=5, pady=5)
    entry_codigo_interno = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_codigo_interno.grid(row=3, column=5, sticky="we", padx=5, pady=5)

    # Linha 5
    ctk.CTkLabel(frame_central, text="Observações:", text_color=cfg.get("font_color")).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entrada_observacoes = ctk.CTkEntry(frame_central, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entrada_observacoes.grid(row=4, column=1, columnspan=5, sticky="we", padx=5, pady=5)

    # ---------- FUNÇÃO SALVAR ----------
    def salvar_produto():
        try:
            dados = {
                "codigo_barras": entry_codigo.get().strip(),
                "fornecedor": entry_fornecedor.get().strip(),
                "nome": entry_nome.get().strip(),
                "status": combobox_status.get(),
                "marca": entry_marca.get().strip(),
                "preco": float(entry_preco.get()),
                "quantidade": int(entry_qtd.get()),
                "categoria": combobox_categoria.get(),
                "validade": entry_validade.get().strip(),
                "codigo_interno": entry_codigo_interno.get().strip(),
                "observacoes": entrada_observacoes.get().strip()
            }
        except ValueError:
            messagebox.showerror("Erro", "Preço ou quantidade inválidos.")
            return

        # Chama sua função de adicionar no banco
        sucesso = adicionar_produto(loja.db)
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto cadastrado!")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar o produto.")

    # ---------- BOTOES ----------
    frame_botoes = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_botoes.grid(row=2, column=1, pady=20)

    botoes = [
        ("Buscar na Internet", lambda: buscar_internet(entry_codigo.get())),
        ("Salvar", salvar_produto),
        ("Limpar Campos", lambda: [entry.delete(0,"end") for entry in [
            entry_codigo, entry_fornecedor, entry_nome, entry_marca, entry_preco, entry_qtd,
            entry_validade, entry_codigo_interno, entrada_observacoes
        ]]),
        ("Cancelar", janela.destroy)
    ]

    for index, (texto, comando) in enumerate(botoes):
        ctk.CTkButton(frame_botoes, text=texto, fg_color=cfg.get("button_color"),
                      width=160, height=50, command=comando).grid(row=0, column=index, padx=10)

    janela.mainloop()

if __name__ == "__main__":
    tela()
