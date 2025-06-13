import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


class BancoDeDados:
    def __init__(self, nome_banco="escola.db"):
        self.nome_banco = nome_banco
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.nome_banco)

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                matricula INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                codigo TEXT PRIMARY KEY,
                nome TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula INTEGER,
                codigo TEXT,
                nota REAL,
                FOREIGN KEY (matricula) REFERENCES alunos(matricula),
                FOREIGN KEY (codigo) REFERENCES disciplinas(codigo)
            )
        """)
        conn.commit()
        conn.close()

    def executar(self, query, params=()):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def consultar(self, query):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        conn.close()
        return dados


class CadastroAlunosDiscNota:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Alunos, Disciplinas e Nota")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c2c2c")
        self.db = BancoDeDados()
        self.campos = {
            "Alunos": ["Matricula", "Nome"],
            "Disciplinas": ["Codigo", "Nome"],
            "Notas": ["Matricula", "Codigo", "Nota"]
        }

        self.criar_interface_principal()

    def criar_interface_principal(self):
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#2c2c2c")
        frame.pack(fill="both", expand=True)

        titulo = tk.Label(frame, text="Sistema Acadêmico", font=("Helvetica", 16, "bold"),
                          bg="#2c2c2c", fg="#f5f5f5")
        titulo.pack(pady=10)

        botoes = [
            ("Incluir", lambda: self.janela_acao("incluir")),
            ("Alterar", lambda: self.janela_acao("alterar")),
            ("Excluir", lambda: self.janela_acao("excluir")),
            ("Listar", lambda: self.janela_acao("listar")),
        ]

        for texto, comando in botoes:
            tk.Button(frame, text=texto, command=comando, width=20,
                      bg="#444", fg="white", activebackground="#555").pack(pady=8)

    def janela_acao(self, acao):
        janela = tk.Toplevel(bg="#1e1e1e")
        janela.title(f"{acao.title()} Dados")
        janela.geometry("500x500")

        aba = ttk.Notebook(janela)
        aba.pack(expand=True, fill='both')

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#333", foreground="white")
        style.map("TNotebook.Tab", background=[("selected", "#555")])

        for tabela, colunas in self.campos.items():
            tab = tk.Frame(aba, bg="#1e1e1e")
            aba.add(tab, text=tabela.title())
            entradas = []

            conteudo = tk.Frame(tab, bg="#1e1e1e")
            conteudo.pack(expand=True)
            conteudo.grid_columnconfigure(0, weight=1)
            conteudo.grid_columnconfigure(1, weight=1)

            for i, campo in enumerate(colunas):
                tk.Label(conteudo, text=campo, bg="#1e1e1e", fg="white").grid(row=i, column=0, pady=5, padx=10, sticky="e")
                e = tk.Entry(conteudo, bg="#2b2b2b", fg="white", insertbackground="white")
                e.grid(row=i, column=1, pady=5, padx=10, sticky="w")
                entradas.append(e)

            novos = []
            if acao == "alterar":
                for i, campo in enumerate(colunas):
                    tk.Label(conteudo, text=f"Novo {campo}", bg="#1e1e1e", fg="white").grid(
                        row=i + len(colunas), column=0, pady=5, padx=10, sticky="e")
                    en = tk.Entry(conteudo, bg="#2b2b2b", fg="white", insertbackground="white")
                    en.grid(row=i + len(colunas), column=1, pady=5, padx=10, sticky="w")
                    novos.append(en)

            def acao_local(t=tabela, es=entradas, ns=novos if acao == "alterar" else []):
                try:
                    if acao == "incluir":
                        self.incluir_dados(t, self.campos[t], [e.get() for e in es])
                    elif acao == "excluir":
                        self.excluir_dado(t, self.campos[t][0], es[0].get())
                    elif acao == "alterar":
                        self.alterar_dado(t, self.campos[t], [n.get() for n in ns], self.campos[t][0], es[0].get())
                    elif acao == "listar":
                        dados = self.listar_dados(t)
                        messagebox.showinfo("Listagem", dados if dados else "Nada encontrado.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro: {e}")

            tk.Button(conteudo, text=acao.title(), command=acao_local,
                      bg="#444", fg="white", width=20).grid(row=30, column=0, columnspan=2, pady=20)

    def incluir_dados(self, tabela, campos, valores):
        query = f"INSERT INTO {tabela.lower()} ({','.join(campos).lower()}) VALUES ({','.join(['?' for _ in valores])})"
        try:
            self.db.executar(query, valores)
            messagebox.showinfo("Sucesso", f"Dados inseridos na tabela {tabela}.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"Chave já cadastrada na tabela {tabela}.")

    def excluir_dado(self, tabela, chave, valor):
        query = f"DELETE FROM {tabela.lower()} WHERE {chave.lower()} = ?"
        self.db.executar(query, (valor,))
        messagebox.showinfo("Remoção", f"Registro removido da tabela {tabela}.")

    def alterar_dado(self, tabela, campos, valores, chave, chave_valor):
        sets = ', '.join([f"{campo.lower()} = ?" for campo in campos])
        query = f"UPDATE {tabela.lower()} SET {sets} WHERE {chave.lower()} = ?"
        self.db.executar(query, (*valores, chave_valor))
        messagebox.showinfo("Atualização", f"Registro da tabela {tabela} atualizado.")

    def listar_dados(self, tabela):
        dados = self.db.consultar(f"SELECT * FROM {tabela.lower()}")
        return "\n".join(str(d) for d in dados)


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroAlunosDiscNota(root)
    root.mainloop()
