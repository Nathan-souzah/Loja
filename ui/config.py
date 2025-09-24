import customtkinter as ctk
import json
import os

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            self.dados = {
                "bg_color": "#FFFFFF",
                "font_color": "#000000",
                "font": "Arial",
                "logo_path": ""
            }
            self.salvar()
        else:
            with open(CONFIG_FILE, "r") as f:
                self.dados = json.load(f)

    def get(self, chave):
        return self.dados.get(chave)

    def set(self, chave, valor):
        self.dados[chave] = valor
        self.salvar()

    def salvar(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.dados, f, indent=4)

# Função independente para chamar no main.py
def tela():
    cfg = Config()
    
    janela = ctk.CTkToplevel()
    janela.title("Configurações")
    janela.geometry("400x300")
    janela.resizable(False, False)

    # Frame principal
    frame = ctk.CTkFrame(janela)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Cor de fundo
    ctk.CTkLabel(frame, text="Cor de fundo:").pack(anchor="w", pady=(0,5))
    cor_bg = ctk.CTkEntry(frame)
    cor_bg.insert(0, cfg.get("bg_color"))
    cor_bg.pack(fill="x", pady=(0,10))

    # Cor da fonte
    ctk.CTkLabel(frame, text="Cor da fonte:").pack(anchor="w", pady=(0,5))
    cor_font = ctk.CTkEntry(frame)
    cor_font.insert(0, cfg.get("font_color"))
    cor_font.pack(fill="x", pady=(0,10))

    # Fonte
    ctk.CTkLabel(frame, text="Fonte:").pack(anchor="w", pady=(0,5))
    fonte = ctk.CTkEntry(frame)
    fonte.insert(0, cfg.get("font"))
    fonte.pack(fill="x", pady=(0,10))

    # Botão Salvar
    def salvar_config():
        cfg.set("bg_color", cor_bg.get())
        cfg.set("font_color", cor_font.get())
        cfg.set("font", fonte.get())
        janela.destroy()

    ctk.CTkButton(frame, text="Salvar", command=salvar_config).pack(pady=10)
