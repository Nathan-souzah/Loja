# ui/config.py
import customtkinter as ctk
from tkinter import colorchooser, messagebox
import json
import os

CONFIG_FILE = "config.json"


class Config:
    """
    Classe de configuração com suporte a salvar/carregar JSON.
    """
    def __init__(self):
        self.dados = {
            "bg_color": "#0f1720",
            "font_color": "#ffffff",
            "button_color": "#1f6feb",
            "font": "Inter 12"
        }
        self.carregar()

    def carregar(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.dados.update(json.load(f))
            except Exception as e:
                print("Erro ao carregar config.json:", e)

    def salvar(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Erro ao salvar config.json:", e)

    def get(self, key, default=None):
        return self.dados.get(key, default)

    def set(self, key, value):
        self.dados[key] = value
        self.salvar()


def criar_janela(title="App", size="900x600"):
    cfg = Config()
    janela = ctk.CTk()
    janela.title(title)
    janela.geometry(size)
    janela.configure(fg_color=cfg.get("bg_color"))

    class CfgProxy(dict):
        def get(self, k, default=None):
            return cfg.get(k, default)

    return janela, CfgProxy()


# === Função que o main.py espera ===
def tela():
    cfg = Config()
    janela = ctk.CTk()
    janela.title("Configurações")
    janela.geometry("600x400")
    janela.configure(fg_color=cfg.get("bg_color"))

    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    ctk.CTkLabel(frame, text="Configurações do Sistema",
                 font=("Inter", 16, "bold"),
                 text_color=cfg.get("font_color")).pack(pady=15)

    # Escolher cor de fundo
    def escolher_cor_bg():
        cor = colorchooser.askcolor(title="Escolher cor de fundo")[1]
        if cor:
            cfg.set("bg_color", cor)
            janela.configure(fg_color=cor)
            messagebox.showinfo("Sucesso", f"Cor de fundo alterada para {cor}")

    ctk.CTkButton(frame, text="Alterar Cor de Fundo",
                  command=escolher_cor_bg,
                  fg_color=cfg.get("button_color")).pack(pady=10)

    # Escolher cor da fonte
    def escolher_cor_fonte():
        cor = colorchooser.askcolor(title="Escolher cor da fonte")[1]
        if cor:
            cfg.set("font_color", cor)
            messagebox.showinfo("Sucesso", f"Cor da fonte alterada para {cor}")

    ctk.CTkButton(frame, text="Alterar Cor da Fonte",
                  command=escolher_cor_fonte,
                  fg_color=cfg.get("button_color")).pack(pady=10)

    # Escolher cor dos botões
    def escolher_cor_btn():
        cor = colorchooser.askcolor(title="Escolher cor dos botões")[1]
        if cor:
            cfg.set("button_color", cor)
            messagebox.showinfo("Sucesso", f"Cor dos botões alterada para {cor}")

    ctk.CTkButton(frame, text="Alterar Cor dos Botões",
                  command=escolher_cor_btn,
                  fg_color=cfg.get("button_color")).pack(pady=10)

    # Fechar
    ctk.CTkButton(frame, text="Fechar",
                  command=janela.destroy,
                  fg_color=cfg.get("button_color")).pack(pady=20)

    janela.mainloop()
