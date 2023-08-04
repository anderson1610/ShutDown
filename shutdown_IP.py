from datetime import date, datetime
import subprocess
import locale
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import os
import shutil

def verify_psexec():

    specific_folder = 'C:/Windows/System32'  # Substitua pelo caminho da pasta específica que deseja verificar
    file_name = 'PsExec.exe'      # Substitua pelo nome do arquivo que deseja verificar
    file_path = os.path.join(specific_folder, file_name)
    path_destination = 'C:/Windows/System32/PsExec.exe'
    path_psexec = 'C:/Users/Administrator/Downloads/PsExec.exe'


    if os.path.exists(file_path):
        subprocess.run(path_destination)
        print(f"O arquivo {file_name} existe na pasta {specific_folder}.")
        os.system("cls")
        os.system("color 0A")
        return True
    else:
        if os.path.exists(path_psexec):
            print("Arquivo PsExec encontrado")
            # Caminho do arquivo .exe original
            original_path = 'C:/Users/Administrator/Downloads/PsExec.exe'

            # Copiar o arquivo .exe para o destino desejado
            shutil.copy(original_path, path_destination)

            # Executar o arquivo .exe
            subprocess.run(path_destination)  

            return True         
        
        else:
            messagebox.showinfo("ERRO!", "Coloque o arquivo PsExec.exe na pasta Downloads para realizarmos a instalação")
            return False



def month():
    locale.setlocale(locale.LC_ALL, '')
    today = datetime.today()
    return today.strftime("%b")

def check_status_ping(sala, maquina, failed):
    comando_ping = ['ping', '-n', '2', f"10.10.{sala}.{maquina}"]  # Comando 'ping' para Windows
    resultado = subprocess.run(comando_ping, stdout=subprocess.PIPE)
    if resultado.returncode == 0:
        print(f'O IP 10.10.{sala}.{maquina} está acessível.')
    else:
        machine = int(maquina)
        failed.append(machine)
        print(f'O IP 10.10.{sala}.{maquina} não está acessível.')

def error_password(sala, maquinas_com_senha_diferente, log_file):
    for l in maquinas_com_senha_diferente:
        print(f'maquina 10.10.{sala}.{l} com senha ADM diferente\n')
        with open (log_file, "a", encoding='utf8') as arquivo:
            arquivo.write(f'maquina 10.10.{sala}.{l} com senha ADM diferente\n')
    

def verify_machine(sala, failed, log_file):
    for maquina in failed:
        print(f"Maquina 10.10.{sala}.{maquina} já estava desligada")
        with open(log_file, "a", encoding='utf8') as arquivo:
            arquivo.write(f"Maquina 10.10.{sala}.{maquina} já estava desligada\n")

def ping(sala, maquina, password):
    date_e_clock_today = datetime.now()
    date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
    txt = subprocess.run(f"shutdown /m \\\\10.10.{sala}.{maquina} /s /f /t 6", stdout=subprocess.PIPE)
    stdout = txt.stdout
    return f"maquina 10.10.{sala}.{maquina} desligada com sucesso {date_e_clock}" if txt.returncode == 0 else password.append(maquina)

def desligar_maquinas(name, start, numbermax, log_file):
    failed = []
    password = []
    lista = [n for n in range(start, numbermax + 1)]
    
    while start <= numbermax:
        pings = [check_status_ping(name, start, failed)]    
        start +=1

    combination = list(set(lista + failed))
    list_difference = []
    lista.sort()
    list_difference.sort()
    failed.sort()



    for n in combination:
        if n not in failed:
            list_difference.append(n)

    for i in list_difference:
        pings = [ping(name, i, password)]
        print(f"Maquina: {i} Sala: {name} | salvando arquivo..")
        

        with open (log_file, "a", encoding='utf8') as arquivo:
                    for p in pings: 
                        arquivo.write(f'{p}\n')

    with open (log_file, "a", encoding='utf8') as arquivo:
        
        arquivo.write("--------------- MAQUINAS NÃO DESLIGADAS ---------------\n")

    verify_machine(name, failed, log_file)

    with open (log_file, "a", encoding='utf8') as arquivo:
        
        arquivo.write("--------------- MAQUINAS COM SENHAS DIFERENTES --------\n")

    error_password(name, password, log_file)

def create_log_file(name):
    current_time = datetime.now()
    month_current = month()
    month_current_number = current_time.month
    month_day_current = current_time.day
    date_today = date.today()
    log_file = f"C:\\Users\\Administrator\\Desktop\\Log_Desligar_Maquinas\\{month_current_number:02d}_Relatorios_{month_current}\\{month_day_current:02d}_Sala{name}_{date_today}.txt"
    path = Path(f"C:\\Users\\Administrator\\Desktop\\Log_Desligar_Maquinas\\{month_current_number:02d}_Relatorios_{month_current}")
    path.mkdir(parents=True, exist_ok=True)
    return log_file

def start_process():
    rooms = [21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63] #Lista de salas da empresa

    if int(sala_entry.get()) in rooms:
        name = sala_entry.get()
        start = int(start_entry.get())
        numbermax = int(numbermax_entry.get())
        log_file = create_log_file(name)
        desligar_maquinas(name, start, numbermax, log_file)
        messagebox.showinfo("Processo concluído", "As máquinas foram desligadas e os resultados foram salvos no arquivo de log.")

    else:
        messagebox.showinfo("Erro", "Sala não encontrada")
        

if verify_psexec() == True:

    root = tk.Tk()
    root.title("Desligar Máquinas")
    root.geometry("300x200")

    sala_label = tk.Label(root, text="Digite o número da sala:")
    sala_label.pack()
    sala_entry = tk.Entry(root)
    sala_entry.pack()

    start_label = tk.Label(root, text="Digite qual máquina deseja iniciar:")
    start_label.pack()
    start_entry = tk.Entry(root)
    start_entry.pack()

    numbermax_label = tk.Label(root, text="Digite até qual máquina deseja desligar:")
    numbermax_label.pack()
    numbermax_entry = tk.Entry(root)
    numbermax_entry.pack()

    start_button = tk.Button(root, text="Iniciar", command=start_process)
    start_button.pack()
    assinatura_label = tk.Label(root, text="Desenvolvido por: Anderson Camargo", fg="gray")
    assinatura_label.pack(side=tk.BOTTOM, padx=5, pady=5)
    root.mainloop()

else:
    print("Verifique se possui o instalador do PsExec esta na pasta Downloads")

#Desenvol. Anderson Camargo
