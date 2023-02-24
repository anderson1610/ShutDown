import os
from pathlib import Path
from datetime import date, datetime
import subprocess

print("--------------- DESLIGAR MAQUINAS ---------------")

date_today = date.today()
name = input("Digite o numero da sala: ")
LOG_FILE = Path(__file__).parent  / (f"Relatorio_Maquinas_S{name}_{date_today}.txt")
numbermax = int(input("Digite o numero de maquinas da sala: ")) #até qual maquina desligar
contador = 1 #aparti de qual maquina irá começar


def ping(sala, maquina):
    date_e_clock_today = datetime.now()
    date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
    txt = subprocess.run(f"shutdown /m \\\\10.10.{sala}.{maquina} /s /f /t 6", stdout=subprocess.PIPE) 
    stdout = txt.stdout
    return f"maquina 10.10.{sala}.{maquina} desligada com sucesso {date_e_clock} " if txt.returncode == 0 else f'maquina 10.10.{sala}.{maquina} não encontrada | Maquina ja desligada {date_e_clock}'

while contador <= numbermax:
    pings = [ping(name, contador)]
    print("salvando arquivo..")

    with open (LOG_FILE, "a", encoding='utf8') as arquivo:
                for p in pings: 
                    arquivo.write(f'{p}\n')

    contador += 1

# os.system(f"shutdown /m \\\\10.10.{name}.200 /s /f")
# with open (LOG_FILE, "a", encoding='utf8') as arquivo:
#       arquivo.write(f'Maquina 10.10.{name}.200, instrutor desligada')


#Desenvol. Anderson Camargo