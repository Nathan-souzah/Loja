import customtkinter as ctk
from tkinter import colorchooser
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


def tela():
    cfg = Config()
    
    janela = ctk.CTkToplevel()
    janela.title("Configurações")
    janela.geometry("400x350")
    janela.resizable(False, False)

    frame = ctk.CTkFrame(janela)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # ---------- Cor de fundo ----------
    ctk.CTkLabel(frame, text="Cor de fundo:").pack(anchor="w", pady=(0,5))
    cor_bg_var = ctk.StringVar(value=cfg.get("bg_color"))
    cor_bg_entry = ctk.CTkEntry(frame, textvariable=cor_bg_var)
    cor_bg_entry.pack(fill="x", pady=(0,5))

    def escolher_cor_bg():
        cor = colorchooser.askcolor(title="Escolher cor de fundo")[1]
        if cor:
            cor_bg_var.set(cor)

    ctk.CTkButton(frame, text="Selecionar cor", command=escolher_cor_bg).pack(pady=(0,10))

    # ---------- Cor da fonte ----------
    ctk.CTkLabel(frame, text="Cor da fonte:").pack(anchor="w", pady=(0,5))
    cor_font_var = ctk.StringVar(value=cfg.get("font_color"))
    cor_font_entry = ctk.CTkEntry(frame, textvariable=cor_font_var)
    cor_font_entry.pack(fill="x", pady=(0,5))

    def escolher_cor_font():
        cor = colorchooser.askcolor(title="Escolher cor da fonte")[1]
        if cor:
            cor_font_var.set(cor)

    ctk.CTkButton(frame, text="Selecionar cor", command=escolher_cor_font).pack(pady=(0,10))

    # ---------- Fonte ----------
    ctk.CTkLabel(frame, text="Fonte:").pack(anchor="w", pady=(0,5))
    fontes_disponiveis = ["Arial", "Helvetica", "Courier", "Times New Roman", "Verdana"]
    fonte_var = ctk.StringVar(value=cfg.get("font"))
    fonte_combo = ctk.CTkComboBox(frame, values=fontes_disponiveis, variable=fonte_var)
    fonte_combo.pack(fill="x", pady=(0,10))

    # ---------- Botão salvar ----------
    def salvar_config():
        cfg.set("bg_color", cor_bg_var.get())
        cfg.set("font_color", cor_font_var.get())
        cfg.set("font", fonte_var.get())
        janela.destroy()

    ctk.CTkButton(frame, text="Salvar", command=salvar_config).pack(pady=10)
