import customtkinter as ctk
from ui import cadastro, vendas, estoque, dashboard

def main():
    # Tema global
    ctk.set_appearance_mode("dark")  # ou "light"
    ctk.set_default_color_theme("blue")  # outros: "green", "dark-blue"

    root = ctk.CTk()
    root.title("Sistema de Gestão de Loja")
    root.geometry("1200x800")

    # Botões principais
    ctk.CTkButton(root, text="Cadastrar Produto", command=cadastro.tela, width=200, height=50).pack(pady=20)
    ctk.CTkButton(root, text="Registrar Venda", command=vendas.tela, width=200, height=50).pack(pady=20)
    ctk.CTkButton(root, text="Ver Estoque", command=estoque.tela, width=200, height=50).pack(pady=20)
    ctk.CTkButton(root, text="Dashboard de Indicadores", command=dashboard.tela, width=200, height=50).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
