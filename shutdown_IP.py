import os
from pathlib import Path
from datetime import date, datetime

print("--------------- DESLIGAR MAQUINAS ---------------")

date_today = date.today()
# date_e_clock_today = datetime.now()
# date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
LOG_FILE = Path(__file__).parent  / (f"log_{date_today}.txt")
name = input("Digite o numero da sala: ")
numbermax = int(input("Digite o numero de maquinas da sala: ")) #até qual maquina desligar
contador = 1 #aparti de qual maquina irá começar

while contador <= numbermax:
    txt = os.system (f"shutdown /m \\\\10.10.{name}.{contador} /s /f") 
    # os.system(f"shutdown /m \\\\10.10.{name}.{contador} /s /f")
    if txt == "shutdown /m \\\\10.10.{name}.{contador} /s /f":
        print(f'maquina 10.10.{name}.{contador} desligada com sucesso')
        date_e_clock_today = datetime.now()
        date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
        txt2 = (f'maquina 10.10.{name}.{contador} desligada com sucesso {date_e_clock_today}')
    else:
        #os.system('cls')
        print(f'maquina 10.10.{name}.{contador} não encontrada na rede')
        date_e_clock_today = datetime.now()
        date_e_clock = date_e_clock_today.strftime('%d/%m/%Y %H:%M')
        txt2 = (f'maquina 10.10.{name}.{contador} não encontrada na rede | Maquina ja desligada {date_e_clock_today}')
    
    with open (LOG_FILE, "a", encoding='utf8') as arquivo:
            arquivo.write(txt2)
            arquivo.write("\n")

    contador += 1






#Desenvol. Anderson Camargo