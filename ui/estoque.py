import customtkinter as ctk
from tkinter import ttk
from ui.config import criar_janela
from produtos import listar_produtos

def tela():
    janela, cfg = criar_janela("Estoque - PDV", "1400x800")

    # ---------- FRAME CENTRAL ----------
    frame_central = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_central.pack(pady=10, padx=20, fill="both", expand=True)

    # ---------- PESQUISA ----------
    frame_pesquisa = ctk.CTkFrame(frame_central, fg_color=cfg.get("bg_color"))
    frame_pesquisa.pack(pady=5, fill="x")

    ctk.CTkLabel(frame_pesquisa, text="Pesquisar:", text_color=cfg.get("font_color")).pack(side="left", padx=5)
    entry_pesquisa = ctk.CTkEntry(frame_pesquisa, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    entry_pesquisa.pack(side="left", fill="x", expand=True, padx=5)

    # ---------- TREEVIEW DE ESTOQUE ----------
    colunas = ("Código", "Nome", "Categoria", "Preço", "Estoque")
    tree = ttk.Treeview(frame_central, columns=colunas, show="headings", height=20)
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True, pady=10)

    # Preencher Treeview
    produtos = listar_produtos()
    for p in produtos:
        tree.insert("", "end", values=(p[0], p[2], p[3], f"R$ {p[4]:.2f}", p[5]))

    # Função de filtro
    def filtrar_produtos(event=None):
        termo = entry_pesquisa.get().lower()
        tree.delete(*tree.get_children())
        for p in produtos:
            if termo in str(p[0]).lower() or termo in p[2].lower():
                tree.insert("", "end", values=(p[0], p[2], p[3], f"R$ {p[4]:.2f}", p[5]))

    entry_pesquisa.bind("<KeyRelease>", filtrar_produtos)

    # ---------- BOTOES ----------
    frame_botoes = ctk.CTkFrame(frame_central, fg_color=cfg.get("bg_color"))
    frame_botoes.pack(pady=10)

    botoes = [
        ("Atualizar", lambda: filtrar_produtos()),
        ("Fechar", janela.destroy)
    ]

    for index, (texto, comando) in enumerate(botoes):
        ctk.CTkButton(frame_botoes, text=texto, fg_color=cfg.get("button_color"),
                      width=160, height=50, command=comando).grid(row=0, column=index, padx=10)

    janela.mainloop()


if __name__ == "__main__":
    tela()
