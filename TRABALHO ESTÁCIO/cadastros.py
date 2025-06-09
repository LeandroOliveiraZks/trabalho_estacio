import tkinter as tk
from tkinter import messagebox
import sqlite3


def criar_bancodados():
    conexao = sqlite3.connect('escola.db')
    cursor = conexao.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS alunos (
                        matricula INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS disciplinas (
                        codigo INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS notas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matricula INTEGER,
                        codigo INTEGER,
                        nota REAL,
                        FOREIGN KEY (matricula) REFERENCES alunos (matricula),
                        FOREIGN KEY (codigo) REFERENCES disciplinas (codigo))''')

    conexao.commit()
    conexao.close()

   


def adicionar_aluno(matricula, nome):
    try:
        conexao = sqlite3.connect('escola.db')
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO alunos (matricula, nome) VALUES (?, ?)", (matricula, nome))
        conexao.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Matrícula já cadastrada.")
    finally:
        conexao.close()

def adicionar_disciplina(codigo, nome):
    try:
        conexao = sqlite3.connect('escola.db')
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO disciplinas (codigo, nome) VALUES (?, ?)", (codigo, nome))
        conexao.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Código de disciplina já cadastrado.")
    finally:
        conexao.close()

def adicionar_nota(matricula, codigo, nota):
    if nota < 0 or nota > 10:
        messagebox.showerror("Erro", "Nota deve estar entre 0 e 10.")
        return

    conexao = sqlite3.connect('escola.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM alunos WHERE matricula = ?", (matricula,))
    if not cursor.fetchone():
        messagebox.showerror("Erro", "Aluno não encontrado.")
        conexao.close()
        return

    cursor.execute("SELECT * FROM disciplinas WHERE codigo = ?", (codigo,))
    if not cursor.fetchone():
        messagebox.showerror("Erro", "Disciplina não encontrada.")
        conexao.close()
        return

    cursor.execute("INSERT INTO notas (matricula, codigo, nota) VALUES (?, ?, ?)", (matricula, codigo, nota))
    conexao.commit()
    conexao.close()

def buscar_notas(matricula):
    conexao = sqlite3.connect('escola.db')
    cursor = conexao.cursor()

    cursor.execute('''SELECT disciplinas.nome, notas.nota 
                      FROM notas 
                      JOIN disciplinas ON notas.codigo = disciplinas.codigo 
                      WHERE notas.matricula = ?''', (matricula,))
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

class Interface:
    def __init__(self, master):
        self.master = master
        master.title("Cadastro de Alunos, Disciplinas e Notas")
        master.configure(bg="#f0f0f0")

        
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        width = 600
        height = 600
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        master.geometry(f"{width}x{height}+{x}+{y}")
        section_font = ("Arial", 14, "bold")
        label_font = ("Arial", 12)
        button_font = ("Arial", 10, "bold")
        main_frame = tk.Frame(master, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        
        aluno_frame = tk.LabelFrame(main_frame, text="Cadastro do Aluno", font=section_font, bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        aluno_frame.pack(fill="x", pady=10)
        tk.Label(aluno_frame, text="Matrícula:", bg="#f0f0f0", fg="#333333", font=label_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.matricula_entry = tk.Entry(aluno_frame, bg="#ffffff", fg="#333333", font=label_font, width=30)
        self.matricula_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(aluno_frame, text="Nome:", bg="#f0f0f0", fg="#333333", font=label_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.nome_entry = tk.Entry(aluno_frame, bg="#ffffff", fg="#333333", font=label_font, width=30)
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(aluno_frame, text="Adicionar Aluno", command=self.add_aluno, bg="#4CAF50", fg="white", font=button_font).grid(row=2, column=0, columnspan=2, pady=10)

       
        disciplina_frame = tk.LabelFrame(main_frame, text="Cadastro da Disciplina", font=section_font, bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        disciplina_frame.pack(fill="x", pady=10)
        tk.Label(disciplina_frame, text="Código da Disciplina:", bg="#f0f0f0", fg="#333333", font=label_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.codigo_entry = tk.Entry(disciplina_frame, bg="#ffffff", fg="#333333", font=label_font, width=30)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(disciplina_frame, text="Nome da Disciplina:", bg="#f0f0f0", fg="#333333", font=label_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.disciplina_entry = tk.Entry(disciplina_frame, bg="#ffffff", fg="#333333", font=label_font, width=30)
        self.disciplina_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(disciplina_frame, text="Adicionar Disciplina", command=self.add_disciplina, bg="#4CAF50", fg="white", font=button_font).grid(row=2, column=0, columnspan=2, pady=10)

       
        nota_frame = tk.LabelFrame(main_frame, text="Adicionar Nota", font=section_font, bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        nota_frame.pack(fill="x", pady=10)
        tk.Label(nota_frame, text="Nota:", bg="#f0f0f0", fg="#333333", font=label_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nota_entry = tk.Entry(nota_frame, bg="#ffffff", fg="#333333", font=label_font, width=30)
        self.nota_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(nota_frame, text="Adicionar Nota", command=self.add_nota, bg="#4CAF50", fg="white", font=button_font).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(nota_frame, text="Buscar Notas", command=self.mostrar_notas, bg="#2196F3", fg="white", font=button_font).grid(row=2, column=0, columnspan=2, pady=10)

    def add_aluno(self):
        matricula = self.matricula_entry.get()
        nome = self.nome_entry.get()
        if not matricula or not nome:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        adicionar_aluno(int(matricula), nome)
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso.")

    def add_disciplina(self):
        codigo = self.codigo_entry.get()
        nome = self.disciplina_entry.get()
        if not codigo or not nome:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        adicionar_disciplina(int(codigo), nome)
        messagebox.showinfo("Sucesso", "Disciplina adicionada com sucesso.")

    def add_nota(self):
        matricula = self.matricula_entry.get()
        codigo = self.codigo_entry.get()
        nota = self.nota_entry.get()
        if not matricula or not codigo or not nota:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        adicionar_nota(int(matricula), int(codigo), float(nota))
        messagebox.showinfo("Sucesso", "Nota adicionada com sucesso.")

    def mostrar_notas(self):
        matricula = self.matricula_entry.get()
        if not matricula:
            messagebox.showerror("Erro", "Informe a matrícula do aluno.")
            return
        resultados = buscar_notas(int(matricula))
        if not resultados:
            messagebox.showinfo("Notas", "Nenhuma nota encontrada.")
        else:
            notas = "\n".join([f"{disciplina}: {nota}" for disciplina, nota in resultados])
            messagebox.showinfo("Notas", notas)


if __name__ == "__main__":
    criar_bancodados()
    root = tk.Tk()
    root.iconbitmap('img.jpg')  
    interface = Interface(root)
    root.mainloop()
