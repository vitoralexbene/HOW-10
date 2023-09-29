import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

def abrir_calendario():
    def selecionar_data():
        data_selecionada = cal.get_date()
        entry_data.delete(0, tk.END)
        entry_data.insert(0, data_selecionada)
        popup.destroy()
    
    popup = tk.Toplevel(root)
    popup.title("Escolha uma Data")
    
    cal = Calendar(popup, selectmode="day", date_pattern="dd/mm/yyyy")
    cal.pack(padx=10, pady=10)
    
    btn_selecionar = ttk.Button(popup, text="Selecionar Data", command=selecionar_data)
    btn_selecionar.pack(padx=10, pady=10)

def adicionar_tarefa():
    nome = entry_nome.get()
    data = entry_data.get()
    prioridade = entry_prioridade.get()
    
    if nome and data and prioridade:
        if validar_data(data):
            with open("Base.txt", "a") as file:
                file.write(f"{nome}, {data}, {prioridade}, Não\n")
            entry_nome.delete(0, tk.END)
            entry_data.delete(0, tk.END)
            entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
            entry_prioridade.delete(0, tk.END)
            listar_tarefas()
        else:
            mensagem_erro("Data inválida. Use o formato dd/mm/aaaa.")
    else:
        mensagem_erro("Preencha todos os campos.")

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def mensagem_erro(mensagem):
    erro_label.config(text=mensagem, fg="red")

def limpar_erro():
    erro_label.config(text="")

def listar_tarefas():
    for row in tree.get_children():
        tree.delete(row)
    
    try:
        with open("Base.txt", "r") as file:
            for index, line in enumerate(file, start=1):
                tarefa_info = line.strip().split(", ")
                tarefa_index = index
                tarefa_nome, tarefa_data, tarefa_prioridade, tarefa_executada = tarefa_info
                tree.insert('', 'end', values=(tarefa_index, tarefa_nome, tarefa_data, tarefa_prioridade, tarefa_executada))
    except FileNotFoundError:
        pass

def marcar_desmarcar_executada():
    selected_item = tree.selection()[0]
    tarefa_index = int(tree.item(selected_item, 'values')[0])
    
    with open("Base.txt", "r") as file:
        tarefas = file.readlines()
    
    tarefa_info = tarefas[tarefa_index - 1].strip().split(", ")
    tarefa_status = tarefa_info[-1]
    
    if tarefa_status == "Sim":
        tarefa_info[-1] = "Não"
    else:
        tarefa_info[-1] = "Sim"
    
    tarefas[tarefa_index - 1] = ", ".join(tarefa_info) + "\n"
    with open("Base.txt", "w") as file:
        file.writelines(tarefas)
    
    listar_tarefas()

def excluir_tarefa():
    selected_item = tree.selection()[0]
    tarefa_index = int(tree.item(selected_item, 'values')[0])
    
    with open("Base.txt", "r") as file:
        tarefas = file.readlines()
    
    tarefas.pop(tarefa_index - 1)
    
    with open("Base.txt", "w") as file:
        file.writelines(tarefas)
    
    listar_tarefas()

root = tk.Tk()
root.title("Gerenciador de Tarefas")

frame_adicionar = ttk.Frame(root)
frame_adicionar.grid(row=0, column=0, padx=10, pady=10)

label_nome = ttk.Label(frame_adicionar, text="Nome da Tarefa:")
label_nome.grid(row=0, column=0, sticky="e")
entry_nome = ttk.Entry(frame_adicionar)
entry_nome.grid(row=0, column=1)

label_data = ttk.Label(frame_adicionar, text="Data (dd/mm/aaaa):")
label_data.grid(row=1, column=0, sticky="e")
entry_data = ttk.Entry(frame_adicionar)
entry_data.grid(row=1, column=1)
entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

btn_escolher_data = ttk.Button(frame_adicionar, text="Escolher Data", command=abrir_calendario)
btn_escolher_data.grid(row=1, column=2)

label_prioridade = ttk.Label(frame_adicionar, text="Prioridade:")
label_prioridade.grid(row=2, column=0, sticky="e")
entry_prioridade = ttk.Entry(frame_adicionar)
entry_prioridade.grid(row=2, column=1)

btn_adicionar = ttk.Button(frame_adicionar, text="Adicionar Tarefa", command=adicionar_tarefa)
btn_adicionar.grid(row=3, column=0, padx=10, pady=10)

btn_listar = ttk.Button(frame_adicionar, text="Listar Tarefas", command=listar_tarefas)
btn_listar.grid(row=3, column=1, padx=10, pady=10)

frame_lista = ttk.Frame(root)
frame_lista.grid(row=1, column=0, padx=10, pady=5)

tree = ttk.Treeview(frame_lista, columns=("Índice", "Nome", "Data", "Prioridade", "Executada"), show="headings")
tree.heading("Índice", text="Índice")
tree.heading("Nome", text="Nome")
tree.heading("Data", text="Data")
tree.heading("Prioridade", text="Prioridade")
tree.heading("Executada", text="Executada")
tree.column("Índice", width=0, stretch=tk.NO)
tree.pack()

erro_label = ttk.Label(root, text="", foreground="red")
erro_label.grid(row=2, column=0, padx=10, pady=5)

btn_marcar_desmarcar_executada = ttk.Button(root, text="Marcar/Desmarcar como Executada", command=marcar_desmarcar_executada)
btn_marcar_desmarcar_executada.grid(row=3, column=0, padx=10, pady=10)

btn_excluir = ttk.Button(root, text="Excluir Tarefa", command=excluir_tarefa)
btn_excluir.grid(row=4, column=0, padx=10, pady=10)

listar_tarefas()

root.mainloop()