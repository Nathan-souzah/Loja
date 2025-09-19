import tkinter as tk
from tkinter import cadastro, vendas, estoque

def main():
    root = tk.Tk()
    root.title("Sistema de Gestão de Loja")
    root.geometry("400x300")

    btn_cadastro = tk.Button(root, text="Cadastra Produto", command=cadastro.tela).pack(pady=10)

    btn_vendas = tk.Button(root, text="Registrar Venda", command=vendas.tela).pack(pady=10)

    btn_estoque = tk.Button(root, text="Ver Estoque", command=estoque.tela).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()