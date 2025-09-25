import customtkinter as ctk
from ui.config import criar_janela
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import conectar

def tela():
    janela, cfg = criar_janela("Dashboard", "900x600")

    conn = conectar()
    df = pd.read_sql("SELECT * FROM vendas", conn)
    conn.close()

    # Indicadores
    faturamento = df["total"].sum()
    ticket_medio = df["total"].mean()
    qtd_vendas = len(df)

    ctk.CTkLabel(janela, text=f"Faturamento: R$ {faturamento:.2f}", font=(cfg.get("font"),14), text_color=cfg.get("font_color")).pack(pady=5)
    ctk.CTkLabel(janela, text=f"Ticket Médio: R$ {ticket_medio:.2f}", font=(cfg.get("font"),14), text_color=cfg.get("font_color")).pack(pady=5)
    ctk.CTkLabel(janela, text=f"Número de Vendas: {qtd_vendas}", font=(cfg.get("font"),14), text_color=cfg.get("font_color")).pack(pady=5)

    # Agrupar por dia
    df["data"] = pd.to_datetime(df["data"])
    df_dia = df.groupby(df["data"].dt.date)["total"].sum()

    fig, ax = plt.subplots(figsize=(6,4))
    df_dia.plot(kind="bar", ax=ax)
    ax.set_title("Faturamento Diário")
    ax.set_ylabel("R$")

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    ctk.CTkButton(janela, text="Fechar", fg_color=cfg.get("button_color"), command=janela.destroy).pack(pady=10)
