import os
from pathlib import Path

print("--------------- DESLIGAR MAQUINAS ---------------")

LOG_FILE = Path(__file__).parent  / "log.txt"
name = input("Digite o numero da sala: ")
numbermax = int(input("Digite o numero de maquinas da sala: ")) #até qual maquina desligar
contador = 1 #aparti de qual maquina irá começar

while contador <= numbermax:
    txt = os.system (f"shutdown /m \\\\10.10.{name}.{contador} /s /f") 
    # os.system(f"shutdown /m \\\\10.10.{name}.{contador} /s /f")
    if txt == "shutdown /m \\\\10.10.{name}.{contador} /s /f":
        print(f'maquina 10.10.{name}.{contador} desligada com sucesso')
        txt2 = (f'maquina 10.10.{name}.{contador} desligada com sucesso')
    else:
        #os.system('cls')
        print(f'maquina 10.10.{name}.{contador} não encontrada na rede')
        txt2 = (f'maquina 10.10.{name}.{contador} não encontrada na rede | Maquina ja desligada')
    
    with open (LOG_FILE, "a", encoding='utf8') as arquivo:
            arquivo.write(txt2)
            arquivo.write("\n")

    contador += 1






#Desenvol. Anderson Camargo