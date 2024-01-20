from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


#CORES
cor_bg = '#D3D3D3'
cor_fg = 'black'

root = Tk()
root.title('CRUD - INTRODUÇÃO')
root.title()
root.geometry('1000x500')


#CRIAR UM BANCO OU CONECTAR A UM JÁ EXISTENTE
conn = sqlite3.connect('crm_banco.db')

c = conn.cursor()

#CRIANDO TABELA
c.execute("""CREATE TABLE if not exists alunos (
    nome text,
    disciplina text,
    id integer,
    nota_1 real,
    nota_2 real,
    nota_3 real,
    media real)
    """)

conn.commit()

conn.close()

def query_banco():
    conn = sqlite3.connect('crm_banco.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM alunos")
    dados = c.fetchall()

    global count
    count = 0

    for dado in dados:
        if count % 2 == 0:
            meu_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (dado[1], dado[2], dado[0], dado[4], dado[5], dado[6], dado[7]), tags = ('evenrow',))
        else:
            meu_tree.insert(parent = '', index = 'end', iid = count, text = '', values = (dado[1], dado[2], dado[0], dado[4], dado[5], dado[6], dado[7]), tags = ('oddrow',))

        count += 1

    conn.commit()
    conn.close()

#Estilo
estilo = ttk.Style()
estilo.theme_use('default')

#CORES TREEVIEW
estilo.configure('Treeview',
    background = cor_bg,
    foreground = cor_fg,
    rowheight = 25,
    fieldbackground = cor_bg)

#CORES SELECIONADOS
estilo.map('Treeview',
    backgound = [('selected', '#347083')])

#TREEVIEW FRAME
tree_frame = Frame(root)
tree_frame.pack(pady = 10)

#TREEVIEW SCROLLBAR
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side = RIGHT, fill = Y)

#TREEVIEW
meu_tree = ttk.Treeview(tree_frame, yscrollcommand = tree_scroll.set, selectmode = 'extended')
meu_tree.pack()

#CONFIGURAR A SCROLLBAR
tree_scroll.config(command = meu_tree.yview)


#DEFININDO AS COLUNAS
meu_tree['columns'] = ('Nome', 'Disciplina', 'ID', 'Nota 1', 'Nota 2', 'Nota 3', 'Média')

#FORMATANDO AS COLUNAS
meu_tree.column('#0', width = 0, stretch = NO)
meu_tree.column('Nome', anchor = W, width = 140)
meu_tree.column('Disciplina', anchor = W, width = 100)
meu_tree.column('ID', anchor = CENTER, width = 140)
meu_tree.column('Nota 1', anchor = CENTER, width = 140)
meu_tree.column('Nota 2', anchor = CENTER, width = 140)
meu_tree.column('Nota 3', anchor = CENTER, width = 140)
meu_tree.column('Média', anchor = CENTER, width = 140)


#CRIANDO HEADINGS
meu_tree.heading('#0', text = '', anchor = W)
meu_tree.heading('Nome', text = 'Nome', anchor = W)
meu_tree.heading('Disciplina', text = 'Disciplina', anchor = W)
meu_tree.heading('ID', text = 'ID', anchor = CENTER)
meu_tree.heading('Nota 1', text = 'Nota 1', anchor = CENTER)
meu_tree.heading('Nota 2', text = 'Nota 2', anchor = CENTER)
meu_tree.heading('Nota 3', text = 'Nota 3', anchor = CENTER)
meu_tree.heading('Média', text = 'Média', anchor = CENTER)

#CRIANDO TAGS
meu_tree.tag_configure('oddrow', background = "white")
meu_tree.tag_configure('evenrow', background = "lightblue")

#ADICIONAR DADOS
data_frame = LabelFrame(root, text = "Inserir")
data_frame.pack(fill = 'x', expand = 'yes', padx = 20)

nome_label = Label(data_frame, text = 'Nome')
nome_label.grid(row = 0, column = 0, padx =10, pady = 10)
nome_entry = Entry(data_frame)
nome_entry.grid(row = 0, column = 1, padx =10, pady = 10)

disciplina_label = Label(data_frame, text = 'Disciplina')
disciplina_label.grid(row = 0, column = 2, padx =10, pady = 10)
disciplina_entry = Entry(data_frame)
disciplina_entry.grid(row = 0, column = 3, padx =10, pady = 10)

id_label = Label(data_frame, text = 'ID')
id_label.grid(row = 0, column = 4, padx =10, pady = 10)
id_entry = Entry(data_frame)
id_entry.grid(row = 0, column = 5, padx =10, pady = 10)

nota_um_label = Label(data_frame, text = 'Nota 1')
nota_um_label.grid(row = 1, column = 0, padx =10, pady = 10)
nota_um_entry = Entry(data_frame)
nota_um_entry.grid(row = 1, column = 1, padx =10, pady = 10)

nota_dois_label = Label(data_frame, text = 'Nota 2')
nota_dois_label.grid(row = 1, column = 2, padx =10, pady = 10)
nota_dois_entry = Entry(data_frame)
nota_dois_entry.grid(row = 1, column = 3, padx =10, pady = 10)

nota_tres_label = Label(data_frame, text = 'Nota 3')
nota_tres_label.grid(row = 1, column = 4, padx =10, pady = 10)
nota_tres_entry = Entry(data_frame)
nota_tres_entry.grid(row = 1, column = 5, padx =10, pady = 10)

media_label = Label(data_frame, text = 'Média')
media_label.grid(row = 1, column = 6, padx =10, pady = 10)
media_entry = Entry(data_frame)
media_entry.grid(row = 1, column = 7, padx =10, pady = 10)

#MOVER PARA CIMA
def mover_para_cima():
    linhas = meu_tree.selection()
    for linha in linhas:
        meu_tree.move(linha, meu_tree.parent(linha), meu_tree.index(linha) - 1)

#MOVER PARA BAIXO
def mover_para_baixo():
    linhas = meu_tree.selection()
    for linha in reversed(linhas):
        meu_tree.move(linha, meu_tree.parent(linha), meu_tree.index(linha) + 1)

#REMOVE UM
def remover_um():
    x = meu_tree.selection()[0]
    meu_tree.delete(x)

    conn = sqlite3.connect('crm_banco.db')
    c = conn.cursor()
    
    c.execute("DELETE from alunos WHERE oid=" + id_entry.get())

    conn.commit()
    conn.close()

    limpar_registros()

    messagebox.showinfo("Deletado!", "O dado foi apagado com sucesso!")



#REMOVE TODOS
def remover_todos():
    
    resposta = messagebox.askyesno("Cuidado!", "Isto irá apagar TODOS os dados da tabela\nVocê tem certeza?")

    if resposta == 1:

        for dado in meu_tree.get_children(): #limpar o TREEVIEW
            meu_tree.delete(dado)

        conn = sqlite3.connect('crm_banco.db')
        c = conn.cursor()
        
        c.execute("DROP TABLE alunos")
        
        conn.commit()
        conn.close()

        limpar_registros()

        criar_tabela_novamente()


#INSERIR DADO
def inserir_dado():
    media = (float(nota_um_entry.get()) + float(nota_dois_entry.get()) + float(nota_tres_entry.get())) / 3
    conn = sqlite3.connect('crm_banco.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO alunos VALUES (:nome, :disciplina, :id, :nota_1, :nota_2, :nota_3, :media)",
        {
            'nome': nome_entry.get(),
            'disciplina': disciplina_entry.get(),
            'id': id_entry.get(),
            'nota_1': nota_um_entry.get(),
            'nota_2': nota_dois_entry.get(),
            'nota_3': nota_tres_entry.get(),
            'media': media
        })
        
    conn.commit()
    conn.close()

    nome_entry.delete(0, END)
    disciplina_entry.delete(0, END)
    id_entry.delete(0, END)
    nota_um_entry.delete(0, END)
    nota_dois_entry.delete(0, END)
    nota_tres_entry.delete(0, END)
    media_entry.delete(0, END)

    #LIMPAR A TABELA TREEVIEW
    meu_tree.delete(*meu_tree.get_children())

    query_banco()





#ATUALIZAR REGISTROS
def atualizar_registro():
    media = (float(nota_um_entry.get()) + float(nota_dois_entry.get()) + float(nota_tres_entry.get())) / 3
    selecionado = meu_tree.focus()
    meu_tree.item(selecionado, text = '', values = (nome_entry.get(), disciplina_entry.get(), id_entry.get(), nota_um_entry.get(), nota_dois_entry.get(), nota_tres_entry.get(), media_entry.get(),))

    #ATUALIZAR BANDO DE CADOS
    conn = sqlite3.connect('crm_banco.db')
    c = conn.cursor()
    
    c.execute("""UPDATE alunos SET
        nome = :nome,
        disciplina = :disciplina,
        nota_1 = :nota_1,
        nota_2 = :nota_2,
        nota_3 = :nota_3,
        media = :media
        
        WHERE oid = :oid""",
        {
            'nome': nome_entry.get(),
            'disciplina': disciplina_entry.get(),
            'nota_1': nota_um_entry.get(),
            'nota_2': nota_dois_entry.get(),
            'nota_3': nota_tres_entry.get(),
            'media': media,
            'oid': id_entry.get(),
        })

    conn.commit()
    conn.close()

    nome_entry.delete(0, END)
    disciplina_entry.delete(0, END)
    id_entry.delete(0, END)
    nota_um_entry.delete(0, END)
    nota_dois_entry.delete(0, END)
    nota_tres_entry.delete(0, END)
    media_entry.delete(0, END)

    #LIMPAR O TREEVIEW
    meu_tree.delete(*meu_tree.get_children())

    query_banco()



#LIMPAR REGISTROS
def limpar_registros():
    nome_entry.delete(0, END)
    disciplina_entry.delete(0, END)
    id_entry.delete(0, END)
    nota_um_entry.delete(0, END)
    nota_dois_entry.delete(0, END)
    nota_tres_entry.delete(0, END)
    media_entry.delete(0, END)


#SELECIONAR REGISTRO
def selecionar_registro(evento): #quando soltar o botão
    
    #LIMPAR TODAS AS CAIXAS
    nome_entry.delete(0, END)
    disciplina_entry.delete(0, END)
    id_entry.delete(0, END)
    nota_um_entry.delete(0, END)
    nota_dois_entry.delete(0, END)
    nota_tres_entry.delete(0, END)
    media_entry.delete(0, END)

    #PEGAR NÚMERO DO REGISTRO
    selecionado = meu_tree.focus()

    #PEGAR VALORES
    valores = meu_tree.item(selecionado, 'values')

    #SAÍDA PARA CAIXAS DE ENTRADA
    if valores:
        nome_entry.insert(0, valores[0])
        disciplina_entry.insert(0, valores[1])
        id_entry.insert(0, valores[2])
        nota_um_entry.insert(0, valores[3])
        nota_dois_entry.insert(0, valores[4])
        nota_tres_entry.insert(0, valores[5])
        media_entry.insert(0, valores[6])


def criar_tabela_novamente():
    conn = sqlite3.connect('crm_banco.db')

    c = conn.cursor()

    #CRIANDO TABELA
    c.execute("""CREATE TABLE if not exists alunos (
        nome text,
        disciplina text,
        id integer,
        nota_1 real,
        nota_2 real,
        nota_3 real,
        media real)
        """)

    conn.commit()

    conn.close()


#ADICIONANDO BOTÕES
botao_frame = LabelFrame(root, text = 'Ações')
botao_frame.pack(fill = 'x', expand = 'yes', padx = 20)

atualizar_botao = Button(botao_frame, text = 'Atualizar dado', command = atualizar_registro)
atualizar_botao.grid(row = 0, column = 0, padx = 10, pady = 10)

inserir_botao = Button(botao_frame, text = 'Inserir', command = inserir_dado)
inserir_botao.grid(row = 0, column = 1, padx = 10, pady = 10)

remover_todos_botao = Button(botao_frame, text = 'Remover todos', command = remover_todos)
remover_todos_botao.grid(row = 0, column = 2, padx = 10, pady = 10)

remover_um_botao = Button(botao_frame, text = 'Remover item selecionado', command = remover_um)
remover_um_botao.grid(row = 0, column = 3, padx = 10, pady = 10)

mover_para_cima_botao = Button(botao_frame, text = 'Para cima', command = mover_para_cima)
mover_para_cima_botao.grid(row = 0, column = 4, padx = 10, pady = 10)

mover_para_baixo_botao = Button(botao_frame, text = 'Para baixo', command = mover_para_baixo)
mover_para_baixo_botao.grid(row = 0, column = 5, padx = 10, pady = 10)

seleciona_registro_botao = Button(botao_frame, text = 'Limpar registros', command = limpar_registros)
seleciona_registro_botao.grid(row = 0, column = 6, padx = 10, pady = 10)

#CONECTANDO COM O TREEVIEW
meu_tree.bind("<ButtonRelease-1>", selecionar_registro)


query_banco()

root.mainloop()