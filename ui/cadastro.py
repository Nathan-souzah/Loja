# ui/cadastro.py
import customtkinter as ctk
from tkinter import messagebox
from produtos import adicionar_produto  # Sua função existente que adiciona produtos

def tela(root, conn):
    # Criar janela interna
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

    # Campos do formulário
    labels = ["Nome", "Status", "Marca", "Preço", "Quantidade", "Categoria", "Validade", "Código Interno", "Observações"]
    entradas = {}

    y_start = 20
    row_height = 40
    x_label = 20
    x_entry = 150

    for i, texto in enumerate(labels):
        label = ctk.CTkLabel(frame, text=texto, width=130, height=25)
        label.place(x=x_label, y=y_start + i*row_height)

        entry = ctk.CTkEntry(frame, width=200, height=25)
        entry.place(x=x_entry, y=y_start + i*row_height)
        entradas[texto.lower().replace(" ", "_")] = entry

    def salvar():
        dados = {}
        for key, entry in entradas.items():
            dados[key] = entry.get().strip()

        # Checar se campos obrigatórios estão preenchidos
        if not dados["nome"]:
            messagebox.showerror("Erro", "O campo Nome é obrigatório!")
            return

        try:
            sucesso = adicionar_produto(
                conn,
                dados["nome"],
                dados["status"],
                dados["marca"],
                dados["preco"],
                dados["quantidade"],
                dados["categoria"],
                dados["validade"],
                dados["codigo_interno"],
                dados["observacoes"]
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                # Limpar campos
                for entry in entradas.values():
                    entry.delete(0, "end")
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar o produto.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    # Botão de salvar
    btn_salvar = ctk.CTkButton(frame, text="Salvar", width=100, height=30, command=salvar)
    btn_salvar.place(relx=0.5, rely=1.0, anchor="s", y=-20)

