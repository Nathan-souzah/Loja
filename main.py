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
    frame.pack(expand=True)

    # Botões principais
    ctk.CTkButton(frame, text="Cadastrar Produto", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=cadastro.tela).pack(pady=20)

    ctk.CTkButton(frame, text="Registrar Venda", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=vendas.tela).pack(pady=20)

    ctk.CTkButton(frame, text="Ver Estoque", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=estoque.tela).pack(pady=20)

    ctk.CTkButton(frame, text="Dashboard de Indicadores", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=dashboard.tela).pack(pady=20)

    ctk.CTkButton(frame, text="Configurações", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=cfg_module.tela).pack(pady=20)

    ctk.CTkButton(frame, text="Sair", fg_color=cfg.get("button_color"),
                  font=(cfg.get("font"), 14), width=200, height=50, command=root.quit).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
