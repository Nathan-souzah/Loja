import customtkinter as ctk
from ui.config import criar_janela
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import conectar

def tela():
    janela, cfg = criar_janela("Dashboard - PDV Profissional", "1000x700")

    conn = conectar()
    df = pd.read_sql("SELECT * FROM vendas", conn)
    conn.close()

    if df.empty:
        df = pd.DataFrame(columns=["data","total"])

    # ---------- FRAME DE INDICADORES ----------
    frame_indicadores = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"))
    frame_indicadores.pack(pady=10, padx=10, fill="x")

    faturamento = df["total"].sum()
    ticket_medio = df["total"].mean() if not df.empty else 0
    qtd_vendas = len(df)

    indicadores = [
        ("Faturamento Total", f"R$ {faturamento:.2f}"),
        ("Ticket Médio", f"R$ {ticket_medio:.2f}"),
        ("Número de Vendas", f"{qtd_vendas}")
    ]

    for i, (titulo, valor) in enumerate(indicadores):
        frame = ctk.CTkFrame(frame_indicadores, fg_color="#1f1f1f")
        frame.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
        frame_indicadores.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(frame, text=titulo, font=(cfg.get("font"),12), text_color="#FFFFFF").pack(pady=5)
        ctk.CTkLabel(frame, text=valor, font=(cfg.get("font"),16,"bold"), text_color="#00FF00").pack(pady=5)

    # ---------- GRÁFICO DE LINHA - FATURAMENTO DIÁRIO ----------
    df["data"] = pd.to_datetime(df["data"])
    df_dia = df.groupby(df["data"].dt.date)["total"].sum()

    fig, ax = plt.subplots(figsize=(8,4))
    df_dia.plot(kind="line", marker="o", ax=ax, color="#00AAFF")
    ax.set_title("Faturamento Diário", fontsize=14)
    ax.set_ylabel("R$")
    ax.set_xlabel("Data")
    ax.grid(True, linestyle="--", alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, pady=10, padx=10)

    # ---------- BOTÃO FECHAR ----------
    ctk.CTkButton(janela, text="Fechar", fg_color=cfg.get("button_color"), width=180, height=50, command=janela.destroy).pack(pady=10)

    janela.mainloop()


if __name__ == "__main__":
    tela()
