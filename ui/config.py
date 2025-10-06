# ui/config.py
import customtkinter as ctk
from tkinter import colorchooser, messagebox, filedialog, simpledialog
import json
import os
import pandas as pd
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Caminho seguro para salvar configuração
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".ribeiro_tecnologia_loja")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)


class Config:
    """Classe de configuração com suporte a salvar/carregar JSON."""
    def __init__(self):
        self.dados = {
            "bg_color": "#0f1720",
            "font_color": "#ffffff",
            "button_color": "#1f6feb",
            "font": "Segoe UI 12"
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


# === Função usada por cadastro.py ===
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


# === Funções de exportação ===
def exportar_excel(df):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
    )
    if file_path:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sucesso", f"Dados exportados para {file_path}")


def exportar_db(df, table_name="dados"):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".db", filetypes=[("SQLite DB", "*.db")]
    )
    if file_path:
        conn = sqlite3.connect(file_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        messagebox.showinfo("Sucesso", f"Dados exportados para {file_path}")


def exportar_dashboard_pdf(df):
    data_inicio = simpledialog.askstring("Período", "Data inicial (AAAA-MM-DD):")
    data_fim = simpledialog.askstring("Período", "Data final (AAAA-MM-DD):")

    if not data_inicio or not data_fim:
        return

    # Filtrar dataframe pelo período
    df['data'] = pd.to_datetime(df['data'])
    df_filtrado = df[(df['data'] >= data_inicio) & (df['data'] <= data_fim)]

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height-50, f"Relatório Dashboard: {data_inicio} a {data_fim}")

        y = height - 100
        for i, row in df_filtrado.iterrows():
            linha = ", ".join([f"{col}: {row[col]}" for col in df_filtrado.columns])
            c.drawString(50, y, linha)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()
        messagebox.showinfo("Sucesso", f"PDF salvo em {file_path}")


# === Tela de Configurações com exportações ===
def tela(df=None):
    cfg = Config()
    janela = ctk.CTk()
    janela.title("Configurações")
    janela.geometry("650x550")
    janela.configure(fg_color=cfg.get("bg_color"))

    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

    ctk.CTkLabel(frame, text="Configurações do Sistema",
                 font=("Segoe UI", 16, "bold"),
                 text_color=cfg.get("font_color")).pack(pady=15)

    # Funções de configuração de cores
    def escolher_cor_bg():
        cor = colorchooser.askcolor(title="Escolher cor de fundo")[1]
        if cor:
            cfg.set("bg_color", cor)
            janela.configure(fg_color=cor)
            messagebox.showinfo("Sucesso", f"Cor de fundo alterada para {cor}")

    def escolher_cor_fonte():
        cor = colorchooser.askcolor(title="Escolher cor da fonte")[1]
        if cor:
            cfg.set("font_color", cor)
            messagebox.showinfo("Sucesso", f"Cor da fonte alterada para {cor}")

    def escolher_cor_btn():
        cor = colorchooser.askcolor(title="Escolher cor dos botões")[1]
        if cor:
            cfg.set("button_color", cor)
            messagebox.showinfo("Sucesso", f"Cor dos botões alterada para {cor}")

    # Botões de configuração de cores
    ctk.CTkButton(frame, text="Alterar Cor de Fundo",
                  command=escolher_cor_bg,
                  fg_color=cfg.get("button_color")).pack(pady=10)
    ctk.CTkButton(frame, text="Alterar Cor da Fonte",
                  command=escolher_cor_fonte,
                  fg_color=cfg.get("button_color")).pack(pady=10)
    ctk.CTkButton(frame, text="Alterar Cor dos Botões",
                  command=escolher_cor_btn,
                  fg_color=cfg.get("button_color")).pack(pady=10)

    # Botões de exportação sempre visíveis, habilitados apenas se df existe
    export_enabled = df is not None
    ctk.CTkButton(frame, text="Exportar para Excel",
                  command=lambda: exportar_excel(df) if export_enabled else None,
                  fg_color=cfg.get("button_color"),
                  state="normal" if export_enabled else "disabled").pack(pady=10)

    ctk.CTkButton(frame, text="Exportar para DB",
                  command=lambda: exportar_db(df) if export_enabled else None,
                  fg_color=cfg.get("button_color"),
                  state="normal" if export_enabled else "disabled").pack(pady=10)

    ctk.CTkButton(frame, text="Exportar Dashboard PDF",
                  command=lambda: exportar_dashboard_pdf(df) if export_enabled else None,
                  fg_color=cfg.get("button_color"),
                  state="normal" if export_enabled else "disabled").pack(pady=10)

    # Botão fechar
    ctk.CTkButton(frame, text="Fechar",
                  command=janela.destroy,
                  fg_color=cfg.get("button_color")).pack(pady=20)

    janela.mainloop()
