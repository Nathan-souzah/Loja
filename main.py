import customtkinter as ctk
from ui import cadastro, vendas, estoque, dashboard, config as cfg_module

def main():
    # Tema global
    ctk.set_appearance_mode("dark")  # ou "light"
    ctk.set_default_color_theme("blue")  # outros: "green", "dark-blue"

    # Criar janela principal
    root = ctk.CTk()
    root.title("Sistema de Gestão de Loja")
    root.geometry("1200x800")

    # Carregar configuração
    cfg = cfg_module.Config()
    root.configure(fg_color=cfg.get("bg_color"))

    # Container para os botões
    frame = ctk.CTkFrame(root, fg_color=cfg.get("bg_color"))
    frame.pack(expand=True, pady=50)

    # Lista de botões: (texto, função)
    botoes = [
        ("Cadastrar Produto", cadastro.tela),
        ("Registrar Venda", vendas.tela),
        ("Ver Estoque", estoque.tela),
        ("Dashboard de Indicadores", dashboard.tela),
        ("Configurações", cfg_module.tela),
        ("Sair", root.quit)
    ]

    # Inserir botões em grid: 3 por linha
    for index, (texto, comando) in enumerate(botoes):
        linha = index // 3
        coluna = index % 3
        ctk.CTkButton(
            frame,
            text=texto,
            fg_color=cfg.get("button_color"),
            font=(cfg.get("font"), 14),
            width=300,
            height=70,
            command=comando
        ).grid(row=linha, column=coluna, padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
