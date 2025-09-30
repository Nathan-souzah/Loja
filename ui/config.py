import os
import json
import customtkinter as ctk
from tkinter import messagebox, colorchooser

CONFIG_FILE = "config.json"

# Classe Config para gerenciar configurações
class Config:
    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            self.dados = {
                "bg_color": "#222222",
                "font_color": "#FFFFFF",
                "button_color": "#1f6aa5",
                "font": "Arial"
            }
            self.salvar()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.dados = json.load(f)

        # Configurações do CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def get(self, key):
        return self.dados.get(key)

    def salvar(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.dados, f, indent=4)

# Função para criar uma janela padrão
def criar_janela(titulo, tamanho):
    janela = ctk.CTk()
    janela.title(titulo)
    janela.geometry(tamanho)
    cfg = Config()
    return janela, cfg

# Função para tela de configurações (usada no menu do main.py)
def tela():
    janela, cfg = criar_janela("Configurações", "400x300")

    def escolher_bg():
        cor = colorchooser.askcolor()[1]
        if cor:
            cfg.dados["bg_color"] = cor
            cfg.salvar()
            messagebox.showinfo("Sucesso", f"Cor de fundo alterada para {cor}")

    def escolher_font_color():
        cor = colorchooser.askcolor()[1]
        if cor:
            cfg.dados["font_color"] = cor
            cfg.salvar()
            messagebox.showinfo("Sucesso", f"Cor da fonte alterada para {cor}")

    ctk.CTkLabel(janela, text="Configurações", font=(cfg.get("font"), 16), text_color=cfg.get("font_color")).pack(pady=10)
    ctk.CTkButton(janela, text="Alterar cor de fundo", fg_color=cfg.get("button_color"), command=escolher_bg).pack(pady=5)
    ctk.CTkButton(janela, text="Alterar cor da fonte", fg_color=cfg.get("button_color"), command=escolher_font_color).pack(pady=5)
    ctk.CTkButton(janela, text="Fechar", fg_color=cfg.get("button_color"), command=janela.destroy).pack(pady=20)

    janela.mainloop()
