import tkinter as tk
from tkinter import messagebox
from produtos import adicionar_produto
from api import buscar_internet

def tela():
    janela = tk.Toplevel()
    janela.title("Cadastro de Produto")
    janela.geometry("800x600")
    
    tk.Label(janela, text="Código de Barras:").pack()
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()
    tk.Label(janela, text="Nome:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()
    
    tk.Label(janela, text="Marca:").pack()
    entry_marca = tk.Entry(janela)
    entry_marca.pack()
    
    tk.Label(janela, text="Preço:").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()
    
    tk.Label(janela, text="Quantidade:").pack()
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()
    
    def buscar():
        dados = buscar_internet(entry_codigo.get())
        if dados:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, dados["nome"])
            entry_marca.delete(0, tk.END)
            entry_marca.insert(0, dados["marca"])
        else:
            messagebox.showinfo("Info", "Produto não encontrado na internet.")
    
    def salvar(): 
        adicionar_produto(entry_codigo.get(), entry_nome.get(), entry_marca.get(),
                          float(entry_preco.get()), int(entry_qtd.get()))
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        janela.destroy()
        
    tk.Button(janela, text="Buscar na Internet", command=buscar).pack(pady=5)
    tk.Button(janela, text="Salvar", command=salvar).pack(pady=5)