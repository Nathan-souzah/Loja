# ui/dashboard.py
import customtkinter as ctk
from ui.config import criar_janela
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import conectar
from tkcalendar import DateEntry

def tela():
    # === Janela ===
    janela, cfg = criar_janela("Dashboard", "900x600")

    # === Frame Principal ===
    frame = ctk.CTkFrame(janela, fg_color=cfg.get("bg_color"), corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.95)

    # === Conexão com o banco ===
    conn = conectar()
    try:
        df = pd.read_sql("SELECT * FROM vendas", conn)
    except Exception:
        df = pd.DataFrame(columns=["id","produto_id","quantidade","valor_unitario","valor_total","forma_pagamento","data"])
    conn.close()

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])

    # === Função para atualizar dashboard ===
    def atualizar_dashboard():
        start_date = entry_data_inicio.get_date()
        end_date = entry_data_fim.get_date()

        df_filtrado = df.copy()
        if start_date:
            df_filtrado = df_filtrado[df_filtrado["data"] >= pd.Timestamp(start_date)]
        if end_date:
            df_filtrado = df_filtrado[df_filtrado["data"] <= pd.Timestamp(end_date)]

        faturamento = df_filtrado["valor_total"].sum() if not df_filtrado.empty else 0.0
        ticket_medio = df_filtrado["valor_total"].mean() if not df_filtrado.empty else 0.0
        qtd_vendas = len(df_filtrado)

        lbl_fat.configure(text=f"💰 Faturamento: R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        lbl_ticket.configure(text=f"🎯 Ticket Médio: R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        lbl_qtd.configure(text=f"🛒 Número de Vendas: {qtd_vendas}")

        # Gráfico
        ax.clear()
        if not df_filtrado.empty:
            df_day = df_filtrado.groupby(df_filtrado["data"].dt.date)["valor_total"].sum()
            df_day.plot(kind="line", marker="o", ax=ax, color="#10B981")
            ax.set_title("Faturamento Diário", fontsize=14, fontweight="bold")
            ax.set_ylabel("R$", fontsize=12)
            ax.set_xlabel("Data", fontsize=12)
            ax.grid(True, linestyle="--", alpha=0.5)
        else:
            ax.text(0.5, 0.5, "Sem dados para gráfico", ha="center", va="center", fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])

        fig.tight_layout()
        canvas.draw()

    # === Labels de resumo ===
    lbl_fat = ctk.CTkLabel(frame, text="", font=("Inter",16,"bold"), text_color=cfg.get("font_color"))
    lbl_fat.place(relx=0.02, rely=0.02)
    lbl_ticket = ctk.CTkLabel(frame, text="", font=("Inter",16,"bold"), text_color=cfg.get("font_color"))
    lbl_ticket.place(relx=0.02, rely=0.08)
    lbl_qtd = ctk.CTkLabel(frame, text="", font=("Inter",16,"bold"), text_color=cfg.get("font_color"))
    lbl_qtd.place(relx=0.02, rely=0.14)

    # === Filtros de data com DateEntry ===
    ctk.CTkLabel(frame, text="Data Início:", font=("Inter",12), text_color=cfg.get("font_color")).place(relx=0.02, rely=0.22)
    entry_data_inicio = DateEntry(frame, width=12, background="#3B82F6", foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy")
    entry_data_inicio.place(relx=0.12, rely=0.22)

    ctk.CTkLabel(frame, text="Data Fim:", font=("Inter",12), text_color=cfg.get("font_color")).place(relx=0.30, rely=0.22)
    entry_data_fim = DateEntry(frame, width=12, background="#3B82F6", foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy")
    entry_data_fim.place(relx=0.38, rely=0.22)

    btn_filtrar = ctk.CTkButton(frame, text="📅 Filtrar", command=atualizar_dashboard, width=120, height=32, fg_color="#3B82F6")
    btn_filtrar.place(relx=0.55, rely=0.22)

    # === Gráfico de linha ===
    fig, ax = plt.subplots(figsize=(8,3))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.5, rely=0.6, anchor="center")

    # === Botão Fechar ===
    btn_fechar = ctk.CTkButton(frame, text="Fechar", width=120, height=36, command=janela.destroy, fg_color=cfg.get("button_color"))
    btn_fechar.place(relx=0.9, rely=0.95, anchor="s")

    # Inicializa dashboard com todos os dados
    atualizar_dashboard()

    janela.mainloop()
