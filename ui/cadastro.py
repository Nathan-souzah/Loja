# ui/cadastro.py
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import re
from produtos import adicionar_produto
from ui.config import criar_janela


def tela():
    janela, cfg = criar_janela("Cadastro de Produto", "950x650")

    # === Frame Principal ===
    frame = ctk.CTkFrame(
        janela,
        fg_color=cfg.get("bg_color"),
        corner_radius=12
    )
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

    titulo = ctk.CTkLabel(
        frame,
        text="Cadastro de Produto",
        font=("Inter", 22, "bold"),
        text_color=cfg.get("font_color")
    )
    titulo.grid(row=0, column=0, columnspan=6, pady=(15, 25))

    # === Campos ===
    entries = {}
    labels = [
        ("Código de Barras", "codigo_barras"),
        ("Fornecedor", "fornecedor"),
        ("Nome", "nome"),
        ("Status", "status"),
        ("Marca", "marca"),
        ("Preço", "preco"),
        ("Quantidade", "quantidade"),
        ("Categoria", "categoria"),
        ("Validade (DD-MM-AAAA)", "validade"),
        ("Código Interno", "codigo_interno"),
        ("Observações", "observacoes"),
    ]

    # Opções para comboboxes
    status_opcoes = ["Ativo", "Inativo", "Descontinuado"]
    categoria_opcoes = ["Eletrônicos", "Roupas", "Calçados", "Alimentos", "Outros"]

    # 6 colunas (label + entry em 2 colunas)
    for i in range(6):
        frame.grid_columnconfigure(i, weight=1, uniform="col")

    # Distribui labels + inputs
    for idx, (label_text, key) in enumerate(labels, start=1):
        row = (idx - 1) // 2 + 1
        col_base = ((idx - 1) % 2) * 3  # 0 ou 3

        lbl = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Inter", 13),
            text_color=cfg.get("font_color"),
            anchor="e"
        )
        lbl.grid(row=row, column=col_base, padx=8, pady=8, sticky="e")

        # === Entrada específica para campos especiais ===
        if key == "status":
            ent = ctk.CTkComboBox(frame, values=status_opcoes, font=("Inter", 12))
            ent.set(status_opcoes[0])
        elif key == "categoria":
            ent = ctk.CTkComboBox(frame, values=categoria_opcoes, font=("Inter", 12))
            ent.set(categoria_opcoes[0])
        elif key == "observacoes":
            ent = ctk.CTkTextbox(frame, height=80, fg_color="#1E293B", text_color=cfg.get("font_color"))
        else:
            ent = ctk.CTkEntry(
                frame,
                placeholder_text=f"Digite {label_text.lower()}",
                fg_color="#1E293B",
                text_color=cfg.get("font_color"),
                border_color="#475569",
                corner_radius=8,
                height=32
            )
            # Máscara de preço
            if key == "preco":
                def formatar_preco(event, entry=ent):
                    texto = re.sub(r"[^\d]", "", entry.get())
                    if texto == "":
                        entry.delete(0, "end")
                        return
                    valor = int(texto)
                    entry.delete(0, "end")
                    entry.insert(0, f"R$ {valor/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                ent.bind("<KeyRelease>", formatar_preco)
            # Máscara de data
            if key == "validade":
                def formatar_data(event, entry=ent):
                    texto = re.sub(r"[^0-9]", "", entry.get())
                    if len(texto) > 8:
                        texto = texto[:8]
                    formatted = ""
                    if len(texto) >= 2:
                        formatted += texto[:2] + "-"
                        if len(texto) >= 4:
                            formatted += texto[2:4] + "-"
                            formatted += texto[4:]
                        else:
                            formatted += texto[2:]
                    else:
                        formatted += texto
                    entry.delete(0, "end")
                    entry.insert(0, formatted)
                ent.bind("<KeyRelease>", formatar_data)

        if key != "observacoes":
            ent.grid(row=row, column=col_base + 1, columnspan=2, padx=8, pady=8, sticky="we")
        else:
            ent.grid(row=row, column=col_base + 1, columnspan=2, padx=8, pady=8, sticky="we")

        entries[key] = ent

    # === Função de salvar ===
    def salvar_produto():
        dados = {}
        for k, v in entries.items():
            if k == "observacoes":
                dados[k] = v.get("1.0", "end").strip()
            elif k == "preco":
                preco_texto = v.get().replace("R$", "").replace(".", "").replace(",", ".").strip()
                try:
                    dados[k] = float(preco_texto)
                except:
                    messagebox.showerror("Erro", "Preço inválido.")
                    return
            else:
                dados[k] = v.get().strip()

        if not dados["nome"] or not dados["preco"]:
            messagebox.showerror("Erro", "Nome e Preço são obrigatórios.")
            return

        # Valida quantidade
        try:
            dados["quantidade"] = int(dados["quantidade"]) if dados["quantidade"] else 0
        except:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        sucesso = adicionar_produto(dados)
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            for e in entries.values():
                if key != "observacoes":
                    e.delete(0, "end")
                else:
                    e.delete("1.0", "end")
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar produto.")

    # === Botões ===
    btn_frame = ctk.CTkFrame(frame, fg_color=cfg.get("bg_color"))
    btn_frame.grid(row=len(labels)//2 + 2, column=0, columnspan=6, pady=25)

    btn_salvar = ctk.CTkButton(
        btn_frame,
        text="💾 Salvar Produto",
        width=180,
        height=40,
        command=salvar_produto,
        fg_color=cfg.get("button_color"),
        font=("Inter", 14, "bold"),
        corner_radius=10
    )
    btn_salvar.grid(row=0, column=0, padx=12)

    btn_cancel = ctk.CTkButton(
        btn_frame,
        text="❌ Fechar",
        width=160,
        height=40,
        command=janela.destroy,
        fg_color="#EF4444",
        hover_color="#DC2626",
        font=("Inter", 14, "bold"),
        corner_radius=10
    )
    btn_cancel.grid(row=0, column=1, padx=12)

    janela.mainloop()
