import tkinter as tk
from produtos import listar_produtos

def tela():
    janela = tk.Toplevel()
    janela.title("Estoque")
    janela.geometry("500x400")
    
    lista = tk.Listbox(janela, width=80)
    lista.pack()
    
    for p in listar_produtos():
        lista.insert(tk.END, f"{p[0]} - {p[2]} | {p[3]} | R$ {p[4]} | Estoque: {p[5]}")
    
    tk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=5)