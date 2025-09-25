import customtkinter as ctk
from tkinter import colorchooser
import json
import os

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            self.dados = {
                "bg_color": "#0C0C0C",
                "font_color": "#F6F2F2",
                "button_color": "#0078D7",  # nova opção
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


def criar_janela(titulo, tamanho="800x800"):
    """
    Cria uma janela CustomTkinter com cores e fontes do Config
    Retorna a janela e o objeto Config
    """
    cfg = Config()
    janela = ctk.CTkToplevel()
    janela.title(titulo)
    janela.geometry(tamanho)
    janela.configure(fg_color=cfg.get("bg_color"))
    return janela, cfg


def tela():
    cfg = Config()
    
    janela = ctk.CTkToplevel()
    janela.title("Configurações")
    janela.geometry("400x600")
    janela.resizable(False, False)
    janela.configure(fg_color=cfg.get("bg_color"))

    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # ---------- Cor de fundo ----------
    ctk.CTkLabel(frame, text="Cor de fundo:", text_color=cfg.get("font_color")).pack(anchor="w", pady=(0,5))
    cor_bg_var = ctk.StringVar(value=cfg.get("bg_color"))
    cor_bg_entry = ctk.CTkEntry(
        frame,
        textvariable=cor_bg_var,
        fg_color="#FFFFFF",
        text_color=cfg.get("font_color")
    )
    cor_bg_entry.pack(fill="x", pady=(0,5))

    def escolher_cor_bg():
        cor = colorchooser.askcolor(title="Escolher cor de fundo")[1]
        if cor:
            cor_bg_var.set(cor)

    ctk.CTkButton(
        frame,
        text="Selecionar cor de fundo",
        fg_color=cfg.get("button_color"),
        command=escolher_cor_bg
    ).pack(pady=(0,10))

    # ---------- Cor da fonte ----------
    ctk.CTkLabel(frame, text="Cor da fonte:", text_color=cfg.get("font_color")).pack(anchor="w", pady=(0,5))
    cor_font_var = ctk.StringVar(value=cfg.get("font_color"))
    cor_font_entry = ctk.CTkEntry(
        frame,
        textvariable=cor_font_var,
        fg_color="#FFFFFF",
        text_color=cfg.get("font_color")
    )
    cor_font_entry.pack(fill="x", pady=(0,5))

    def escolher_cor_font():
        cor = colorchooser.askcolor(title="Escolher cor da fonte")[1]
        if cor:
            cor_font_var.set(cor)

    ctk.CTkButton(
        frame,
        text="Selecionar cor da fonte",
        fg_color=cfg.get("button_color"),
        command=escolher_cor_font
    ).pack(pady=(0,10))

    # ---------- Cor dos botões ----------
    ctk.CTkLabel(frame, text="Cor dos botões:", text_color=cfg.get("font_color")).pack(anchor="w", pady=(0,5))
    cor_button_var = ctk.StringVar(value=cfg.get("button_color"))
    cor_button_entry = ctk.CTkEntry(
        frame,
        textvariable=cor_button_var,
        fg_color="#FFFFFF",
        text_color=cfg.get("font_color")
    )
    cor_button_entry.pack(fill="x", pady=(0,5))

    def escolher_cor_button():
        cor = colorchooser.askcolor(title="Escolher cor dos botões")[1]
        if cor:
            cor_button_var.set(cor)

    ctk.CTkButton(
        frame,
        text="Selecionar cor dos botões",
        fg_color=cfg.get("button_color"),
        command=escolher_cor_button
    ).pack(pady=(0,10))

    # ---------- Fonte ----------
    ctk.CTkLabel(frame, text="Fonte:", text_color=cfg.get("font_color")).pack(anchor="w", pady=(0,5))
    fontes_disponiveis = ["Arial", "Helvetica", "Courier", "Times New Roman", "Verdana"]
    fonte_var = ctk.StringVar(value=cfg.get("font"))
    fonte_combo = ctk.CTkComboBox(
        frame,
        values=fontes_disponiveis,
        variable=fonte_var,
        fg_color="#FFFFFF",
        text_color=cfg.get("font_color")
    )
    fonte_combo.pack(fill="x", pady=(0,10))

    # ---------- Botão salvar ----------
    def salvar_config():
        cfg.set("bg_color", cor_bg_var.get())
        cfg.set("font_color", cor_font_var.get())
        cfg.set("button_color", cor_button_var.get())
        cfg.set("font", fonte_var.get())
        janela.destroy()

    ctk.CTkButton(
        frame,
        text="Salvar",
        fg_color=cfg.get("button_color"),
        command=salvar_config
    ).pack(pady=10)
