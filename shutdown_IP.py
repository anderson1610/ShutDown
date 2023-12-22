from datetime import date, datetime
import subprocess
import locale
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import os
import shutil
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

# Credenciais do login
email_username = ''
email_password = ''
email_client = '' #e-mail que receberá o arquivo

def get_username():
    return getpass.getuser()

def verify_psexec():
    name_user = get_username()
    specific_folder = 'C:/Windows/System32'  # Substitua pelo caminho da pasta específica que deseja verificar
    file_name = 'PsExec.exe'      # Substitua pelo nome do arquivo que deseja verificar
    file_path = os.path.join(specific_folder, file_name)
    path_destination = 'C:/Windows/System32/PsExec.exe'
    path_psexec = f'C:/Users/{name_user}/Downloads/PsExec.exe'


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
            original_path = f'C:/Users/{name_user}/Downloads/PsExec.exe'

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
        print(f'-maquina 10.10.{sala}.{l} com senha ADM diferente\n')
        with open (log_file, "a", encoding='utf8') as arquivo:
            arquivo.write(f'-maquina 10.10.{sala}.{l} com senha ADM diferente\n')
    

def verify_machine(sala, failed, log_file):
    for maquina in failed:
        print(f"Maquina 10.10.{sala}.{maquina} estava desligada")
        with open(log_file, "a", encoding='utf8') as arquivo:
            arquivo.write(f"-Maquina 10.10.{sala}.{maquina} estava desligada\n")

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
                        arquivo.write(f'-{p}\n')

    with open (log_file, "a", encoding='utf8') as arquivo:
        
        arquivo.write("-=============== MAQUINAS NAO DESLIGADAS ===============\n")

    verify_machine(name, failed, log_file)

    with open (log_file, "a", encoding='utf8') as arquivo:
        
        arquivo.write("-=============== MAQUINAS COM SENHAS DIFERENTES ========\n")

    error_password(name, password, log_file)

def create_log_file(name):
    name_user = get_username()
    current_time = datetime.now()
    month_current = month()
    month_current_number = current_time.month
    month_day_current = current_time.day
    date_today = date.today()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\LOG Desligar Maquinas\\{month_current_number:02d}.Relatorios.{month_current}\\{date_today}_SALA{name}.txt"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\LOG Desligar Maquinas\\{month_current_number:02d}.Relatorios.{month_current}")
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
        estado_botao = atualizar_estado_checkbox()
        if estado_botao == True:
            send_email()
        messagebox.showinfo("Concluído", "Troca de senha concluída com sucesso.")

    else:
        messagebox.showinfo("Erro", "Sala não encontrada")

def send_email():
    # Configurações do servidor SMTP do office
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    number_room = sala_entry.get()
    log_file = create_log_file(number_room)

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = email_client 
    msg['Subject'] = f'SETUP SERVER - Arquivo maquinas desligadas | SALA: {number_room}'

    nome_arquivo = log_file

    # Inicializar a variável para armazenar o conteúdo do arquivo
    conteudo_arquivo = None

    # Tentar abrir e ler o arquivo
    try:
        with open(nome_arquivo, "r") as arquivo:
            conteudo_arquivo = arquivo.read()
            print("Conteúdo do arquivo lido com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")

    # Verificar se o conteúdo foi lido com sucesso
    if conteudo_arquivo is not None:
        # Faça o que quiser com a variável 'conteudo_arquivo'
        print("Sucesso")
        print(conteudo_arquivo)

    minha_string_com_quebra = conteudo_arquivo.replace("-", "\n")

    body = f"Segue arquivo TXT. \n\nRELATORIO: \n{minha_string_com_quebra}"
    
    msg.attach(MIMEText(body, 'plain'))

    with open(log_file, "r") as f:
        attachment = MIMEText(f.read())
        attachment.add_header("Content-Disposition", "attachment", filename=log_file)
        msg.attach(attachment)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(email_username, email_client, msg.as_string())
    server.quit()
    print('Email enviado!')

def validar_entrada(event):
    # Obter o caractere inserido
    char = event.char

    # Verificar se o caractere é um dígito
    if not char.isdigit() and char != '\x08':
        return 'break'  # Impede a inserção do caractere no campo de entrada
    
def avancar_para_proximo_widget(event):
    # Mova o foco para o próximo widget
    event.widget.tk_focusNext().focus()
    return 'break'

def atualizar_estado_checkbox():
    estado = checkbox_var.get()
    if estado == 1:
        return True
    else:
        return False

if verify_psexec() == True:

    root = tk.Tk()
    root.title("Desligar Máquinas - Ka Solution")
    root.geometry("300x200")

    sala_label = tk.Label(root, text="Digite o número da sala:")
    sala_label.pack()
    sala_entry = tk.Entry(root)
    sala_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    sala_entry.bind("<Key>", validar_entrada)
    sala_entry.bind("<Tab>", avancar_para_proximo_widget)

    start_label = tk.Label(root, text="Digite qual máquina deseja iniciar:")
    start_label.pack()
    start_entry = tk.Entry(root)
    start_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    start_entry.bind("<Key>", validar_entrada)
    start_entry.bind("<Tab>", avancar_para_proximo_widget)

    numbermax_label = tk.Label(root, text="Digite até qual máquina deseja desligar:")
    numbermax_label.pack()
    numbermax_entry = tk.Entry(root)
    numbermax_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    numbermax_entry.bind("<Key>", validar_entrada)
    numbermax_entry.bind("<Tab>", avancar_para_proximo_widget)

    # Criar a variável de controle para a caixa de seleção
    checkbox_var = tk.IntVar()

    # Criar a caixa de seleção
    checkbox = tk.Checkbutton(root, text="Enviar e-mail de LOG ", variable=checkbox_var, command=atualizar_estado_checkbox)
    checkbox.pack()

    start_button = tk.Button(root, text="Iniciar", command=start_process)
    start_button.pack()
    assinatura_label = tk.Label(root, text="Desenvolvido por: Anderson Camargo", fg="gray")
    assinatura_label.pack(side=tk.BOTTOM, padx=5, pady=5)
    root.mainloop()

else:
    print("Verifique se possui o instalador do PsExec esta na pasta Downloads")

#Desenvol. Anderson Camargo
