import tkinter as tk
from tkinter import messagebox
from produtos import listar_produtos
from vendas import registrar_venda

def tela():
    janela = tk.Toplevel()
    janela.title("Registrar Venda")
    janela.geometry("800x600")
    
    tk.Label(janela, text="Selecione o produto:").pack()
    lista = tk.Listbox(janela, width=50)
    lista.pack()
    
    for p in listar_produtos():
        lista.insert(tk.END, f"{p[0]} - {p[2]} | Estoque: {p[5]} | Preço: {p[4]}")
    
    tk.Label(janela, text="Quantidade:").pack()
    entry_qtd = tk.Entry(janela)
    entry_qtd.pack()
    
    def vender():
        try:
            item = lista.get(lista.curselection())
            produto_id = int(item.split(" - ")[0])
            qtd = int(entry_qtd.get())
            preco = float(item.split("R$ ")[1])
            ok = registrar_venda(produto_id, qtd, preco)
            if ok:
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
                janela.destroy()
            else:
                messagebox.showwarning("Erro", "Quantidade insuficiente em estoque.")
        except:
            messagebox.showwarning("Erro", "Selecione um produto e insira uma quantidade válida.")
        
    tk.Button(janela, text="Registrar Venda", command=vender).pack(pady=5)
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=5)