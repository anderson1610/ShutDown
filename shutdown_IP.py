import os

print("--------------- DESLIGAR MAQUINAS ---------------")


name = input("Digite o numero da sala: ")
numbermax = int(input("Digite o numero de maquinas da sala: ")) #até qual maquina desligar
contador = 1 #aparti de qual maquina irá começar

while contador <= numbermax:
    txt = os.system (f"shutdown /m \\\\10.10.{name}.{contador} /s /f") 
    # os.system(f"shutdown /m \\\\10.10.{name}.{contador} /s /f")
    if txt == "shutdown /m \\\\10.10.{name}.{contador} /s /f":
        print(f'maquina 10.10.{name}.{contador} com sucesso')
    else:
        #os.system('cls')
        print(f'maquina 10.10.{name}.{contador} não encontrada na rede')

    contador += 1






#Desenvol. Anderson Camargo