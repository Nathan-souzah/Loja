import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import conectar

def tela():
    janela = ctk.CTkToplevel()
    janela.title("Dashboard de Vendas")
    janela.geometry("900x600")

    # 🔹 Conectar ao banco e pegar dados
    conn = conectar()
    df = pd.read_sql_query("""
        SELECT v.id, p.nome AS produto, v.quantidade, v.total, v.forma_pagamento, v.data
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
    """, conn)
    conn.close()

    if df.empty:
        messagebox.showinfo("Info", "Não há vendas registradas.")
        return

    # Converter coluna de data (corrigido para microssegundos)
    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date

    # 🔹 Frame para filtros de data
    filtro_frame = ctk.CTkFrame(janela)
    filtro_frame.pack(pady=10, fill=tk.X, padx=10)

    tk.Label(filtro_frame, text="Data Inicial:").pack(side=tk.LEFT, padx=5)
    entry_inicio = tk.Entry(filtro_frame, width=12)
    entry_inicio.pack(side=tk.LEFT, padx=5)
    calendario_inicio = DateEntry(filtro_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    calendario_inicio.pack(side=tk.LEFT, padx=5)

    tk.Label(filtro_frame, text="Data Final:").pack(side=tk.LEFT, padx=5)
    entry_fim = tk.Entry(filtro_frame, width=12)
    entry_fim.pack(side=tk.LEFT, padx=5)
    calendario_fim = DateEntry(filtro_frame, width=12, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    calendario_fim.pack(side=tk.LEFT, padx=5)

    def atualizar_grafico():
        # Prioridade: usar datas do calendário, se preenchidas; senão usar entrada manual
        inicio = calendario_inicio.get_date() if calendario_inicio.get() else entry_inicio.get().strip()
        fim = calendario_fim.get_date() if calendario_fim.get() else entry_fim.get().strip()

        df_filtrado = df.copy()

        if inicio:
            try:
                if isinstance(inicio, str):
                    inicio_dt = pd.to_datetime(inicio).date()
                else:
                    inicio_dt = inicio
                df_filtrado = df_filtrado[df_filtrado["data"] >= inicio_dt]
            except:
                messagebox.showerror("Erro", "Data inicial inválida.")
                return

        if fim:
            try:
                if isinstance(fim, str):
                    fim_dt = pd.to_datetime(fim).date()
                else:
                    fim_dt = fim
                df_filtrado = df_filtrado[df_filtrado["data"] <= fim_dt]
            except:
                messagebox.showerror("Erro", "Data final inválida.")
                return

        if df_filtrado.empty:
            messagebox.showinfo("Info", "Não há vendas nesse período.")
            return

        # 🔹 Agregar vendas por data
        resumo = df_filtrado.groupby("data")["total"].sum()

        # Limpar figura anterior
        for widget in grafico_frame.winfo_children():
            widget.destroy()

        # Criar gráfico
        fig, ax = plt.subplots(figsize=(8,4))
        resumo.plot(kind="bar", ax=ax, color="#4CAF50")
        ax.set_title("Vendas por Dia")
        ax.set_xlabel("Data")
        ax.set_ylabel("Total (R$)")
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    tk.Button(filtro_frame, text="Atualizar Gráfico", command=atualizar_grafico).pack(side=tk.LEFT, padx=10)

    # 🔹 Frame para gráfico
    grafico_frame = ctk.CTkFrame(janela)
    grafico_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Carregar gráfico inicial
    atualizar_grafico()
