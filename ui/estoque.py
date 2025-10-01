# ui/estoque.py
import customtkinter as ctk
from tkinter import ttk
from ui.config import criar_janela
from produtos import listar_produtos

def tela():
    janela, cfg = criar_janela("Estoque", "900x650")

    # === Frame principal ===
    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"), corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

    # === Título ===
    titulo = ctk.CTkLabel(
        frame,
        text="Estoque 🗂️",
        font=("Inter", 22, "bold"),
        text_color=cfg.get("font_color")
    )
    titulo.grid(row=0, column=0, columnspan=5, pady=(15, 20))

    # === Treeview para mostrar produtos ===
    columns = ("id", "nome", "fornecedor", "preco", "quantidade", "categoria", "status")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=120, anchor="center")
    tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=5, sticky="ns", pady=10)

    # === Preencher Treeview com produtos ===
    produtos = listar_produtos()
    tree.delete(*tree.get_children())
    for p in produtos:
        tree.insert("", "end", values=(
            p[0],      # id
            p[2],      # nome
            p[3],      # fornecedor
            f"R$ {p[4]:.2f}",  # preco
            p[5],      # quantidade
            p[6],      # categoria
            p[1]       # status
        ))

    # === Botão Fechar ===
    btn_fechar = ctk.CTkButton(
        frame,
        text="❌ Fechar",
        width=160,
        height=40,
        command=janela.destroy,
        fg_color="#EF4444",
        hover_color="#DC2626",
        font=("Inter", 14, "bold"),
        corner_radius=10
    )
    btn_fechar.grid(row=2, column=0, columnspan=5, pady=20)

    janela.mainloop()
