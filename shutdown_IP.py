from datetime import date, datetime
import subprocess
import locale
from pathlib import Path

print("--------------- DESLIGAR MAQUINAS ---------------")

def month():
    
  locale.setlocale(locale.LC_ALL, '')
  today = datetime.today()
  return today.strftime("%b")

current_time = datetime.now()
month_current = month()
month_current_number = current_time.month
month_day_current = current_time.day
failed = []

date_today = date.today()
name = input("Digite o numero da sala: ")
start = int(input("Digite qual maquina deseja iniciar: ")) #aparti de qual maquina irá começar

path = Path(f"C:\\Users\\Administrator\\Desktop\\Scripts\\{month_current_number:02d}_Relatorios_{month_current}")
path.mkdir(parents=True, exist_ok=True)

LOG_FILE = f"C:\\Users\\Administrator\\Desktop\\Scripts\\{month_current_number:02d}_Relatorios_{month_current}\\{month_day_current:02d}_Sala{name}_{date_today}.txt"
numbermax = int(input("Digite até que maquina deseja desligar: ")) #até qual maquina desligar
lista = [n for n in range(start, numbermax + 1)]

def verificar_status_ping(sala, maquina, list):
    # ip = f"10.10.{sala}.{maquina}"
    comando_ping = ['ping', '-n', '2', f"10.10.{sala}.{maquina}"]  # Comando 'ping' para Windows

    resultado = subprocess.run(comando_ping, stdout=subprocess.PIPE)

    if resultado.returncode == 0:
        print(f'O IP f"10.10.{sala}.{maquina} está acessível.')
    else:
        machine = int(maquina)
        list.append(machine)
        print(f'O IP f"10.10.{sala}.{maquina} não está acessível.')

    # return f'O IP {ip} está acessível.' if resultado.returncode == 0 else f'O IP {ip} não está acessível.'


def ping(sala, maquina):
    date_e_clock_today = datetime.now()
    date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
    txt = subprocess.run(f"shutdown /m \\\\10.10.{sala}.{maquina} /s /f /t 6", stdout=subprocess.PIPE) 
    stdout = txt.stdout
    return f"maquina 10.10.{sala}.{maquina} desligada com sucesso {date_e_clock} " if txt.returncode == 0 else f'maquina 10.10.{sala}.{maquina} não encontrada | Maquina ja desligada {date_e_clock}'
  

while start <= numbermax:
    pings = [verificar_status_ping(name, start, failed)]    
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
    pings = [ping(name, i)]
    print(f"Maquina: {i} Sala: {name} | salvando arquivo..")
    

    with open (LOG_FILE, "a", encoding='utf8') as arquivo:
                for p in pings: 
                    arquivo.write(f'{p}\n')

with open (LOG_FILE, "a", encoding='utf8') as arquivo:
     
     arquivo.write("--------------- MAQUINAS NÃO DESLIGADAS ---------------\n")


for j in failed:
     print(f"Maquina {j} desligada ")    
     with open (LOG_FILE, "a", encoding='utf8') as arquivo:
         arquivo.write(f"Maquina 10.10.{name}.{j} está desligada ou com uma senha diferente\n")




#Desenvol. Anderson Camargo
