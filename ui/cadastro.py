import customtkinter as ctk
from tkinter import messagebox
from produtos import adicionar_produto
from api import buscar_internet
from ui.config import criar_janela

def tela():
    janela, cfg = criar_janela("Cadastro de Produto", "800x600")

    # Código de barras
    ctk.CTkLabel(janela, text="Código de Barras:", text_color=cfg.get("font_color")).pack(pady=(10,0))
    entry_codigo = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_codigo.pack(pady=(0,10))

    # Nome
    ctk.CTkLabel(janela, text="Nome:", text_color=cfg.get("font_color")).pack(pady=(10,0))
    entry_nome = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_nome.pack(pady=(0,10))

    # Marca
    ctk.CTkLabel(janela, text="Marca:", text_color=cfg.get("font_color")).pack(pady=(10,0))
    entry_marca = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_marca.pack(pady=(0,10))

    # Preço
    ctk.CTkLabel(janela, text="Preço:", text_color=cfg.get("font_color")).pack(pady=(10,0))
    entry_preco = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_preco.pack(pady=(0,10))

    # Quantidade
    ctk.CTkLabel(janela, text="Quantidade:", text_color=cfg.get("font_color")).pack(pady=(10,0))
    entry_qtd = ctk.CTkEntry(janela, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_qtd.pack(pady=(0,10))

    # Funções internas
    def buscar():
        dados = buscar_internet(entry_codigo.get())
        if dados:
            entry_nome.delete(0, "end")
            entry_nome.insert(0, dados.get("nome", ""))
            entry_marca.delete(0, "end")
            entry_marca.insert(0, dados.get("marca", ""))
        else:
            messagebox.showinfo("Info", "Produto não encontrado na internet.")

    def salvar():
        try:
            adicionar_produto(
                entry_codigo.get(),
                entry_nome.get(),
                entry_marca.get(),
                float(entry_preco.get()),
                int(entry_qtd.get())
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Preço ou quantidade inválidos!")

    # Botões
    ctk.CTkButton(janela, text="Buscar na Internet", fg_color=cfg.get("button_color"), command=buscar).pack(pady=5)
    ctk.CTkButton(janela, text="Salvar", fg_color=cfg.get("button_color"), command=salvar).pack(pady=5)
    ctk.CTkButton(janela, text="Cancelar", fg_color=cfg.get("button_color"), command=janela.destroy).pack(pady=5)
