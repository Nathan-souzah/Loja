import customtkinter as ctk
from ui.config import criar_janela
from produtos import listar_produtos

def tela():
    janela, cfg = criar_janela("Estoque", "800x600")
    
    lista = ctk.CTkTextbox(janela, width=700, height=400, fg_color="#FFFFFF", text_color=cfg.get("font_color"))
    lista.pack(pady=10)

    for p in listar_produtos():
        lista.insert("end", f"{p[0]} - {p[2]} | {p[3]} | R$ {p[4]:.2f} | Estoque: {p[5]}\n")

    ctk.CTkButton(janela, text="Fechar", fg_color=cfg.get("button_color"), command=janela.destroy).pack(pady=10)
