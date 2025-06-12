import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def criar_banco():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        matricula INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplinas (
        codigo TEXT PRIMARY KEY,
        nome TEXT NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula INTEGER,
        codigo TEXT,
        nota REAL,
        FOREIGN KEY (matricula) REFERENCES alunos(matricula),
        FOREIGN KEY (codigo) REFERENCES disciplinas(codigo)
    )""")
    conn.commit()
    conn.close()

def executar_query(query, params=()):
    conn = sqlite3.connect("estacio.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def listar_query(query):
    conn = sqlite3.connect("estacio.db")
    cursor = conn.cursor()
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

def incluir_dados(tabela, campos, valores):
    query = f"INSERT INTO {tabela} ({','.join(campos)}) VALUES ({','.join(['?' for _ in valores])})"
    try:
        executar_query(query, valores)
        messagebox.showinfo("Sucesso", f"Dados inseridos na tabela {tabela}.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", f"Chave já cadastrada na tabela {tabela}.")

def excluir_dado(tabela, chave, valor):
    query = f"DELETE FROM {tabela} WHERE {chave} = ?"
    executar_query(query, (valor,))
    messagebox.showinfo("Remoção", f"Registro removido da tabela {tabela}.")

def alterar_dado(tabela, campos, valores, chave, chave_valor):
    sets = ', '.join([f"{campo} = ?" for campo in campos])
    query = f"UPDATE {tabela} SET {sets} WHERE {chave} = ?"
    executar_query(query, (*valores, chave_valor))
    messagebox.showinfo("Atualização", f"Registro da tabela {tabela} atualizado.")

def listar_dados(tabela):
    dados = listar_query(f"SELECT * FROM {tabela}")
    return "\n".join(str(d) for d in dados)

def criar_interface():
    root = tk.Tk()
    root.title("Cadastro de Alunos, Disciplinas e Notas")
    root.geometry("600x500")
    root.configure(bg="#e6f2ff")  

    frame = tk.Frame(root, padx=20, pady=20, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    campos = {
        "alunos": ["matricula", "nome"],
        "disciplinas": ["codigo", "nome"],
        "notas": ["matricula", "codigo", "nota"]
    }

    def janela_acao(acao):
        janela = tk.Toplevel(bg="#f2f2f2")
        janela.title(f"{acao.title()} Dados")
        janela.geometry("500x500")
        aba = ttk.Notebook(janela)
        aba.pack(expand=True, fill='both')

        for tabela, colunas in campos.items():
            tab = tk.Frame(aba, bg="#f2f2f2")
            aba.add(tab, text=tabela.title())
            entradas = []
            for i, campo in enumerate(colunas):
                tk.Label(tab, text=campo, bg="#f2f2f2").grid(row=i, column=0, pady=5, padx=5)
                e = tk.Entry(tab)
                e.grid(row=i, column=1, pady=5, padx=5)
                entradas.append(e)

            if acao == "alterar":
                novos = []
                for i, campo in enumerate(colunas):
                    tk.Label(tab, text=f"Novo {campo}", bg="#f2f2f2").grid(row=i + len(colunas), column=0, pady=5, padx=5)
                    en = tk.Entry(tab)
                    en.grid(row=i + len(colunas), column=1, pady=5, padx=5)
                    novos.append(en)

            def acao_local(t=tabela, es=entradas, ns=novos if acao == "alterar" else []):
                if acao == "incluir":
                    incluir_dados(t, campos[t], [e.get() for e in es])
                elif acao == "excluir":
                    excluir_dado(t, campos[t][0], es[0].get())
                elif acao == "alterar":
                    alterar_dado(t, campos[t], [n.get() for n in ns], campos[t][0], es[0].get())
                elif acao == "listar":
                    dados = listar_dados(t)
                    messagebox.showinfo("Listagem", dados if dados else "Nada encontrado.")

            tk.Button(tab, text=acao.title(), command=acao_local, bg="#007acc", fg="white", width=20).grid(row=30, column=0, columnspan=2, pady=20)

    titulo = tk.Label(frame, text="Sistema Acadêmico", font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366")
    titulo.pack(pady=10)

    botoes = [
        ("Incluir", lambda: janela_acao("incluir")),
        ("Alterar", lambda: janela_acao("alterar")),
        ("Excluir", lambda: janela_acao("excluir")),
        ("Listar", lambda: janela_acao("listar")),
    ]

    for texto, comando in botoes:
        tk.Button(frame, text=texto, command=comando, width=20, bg="#007acc", fg="white").pack(pady=8)

    root.mainloop()

if __name__ == "__main__":
    criar_banco()
    criar_interface()
