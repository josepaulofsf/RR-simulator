import time
import keyboard

tempo_limite = 2  # Segundos da janela de tempo
tecla_pressionada = None


def registrar_tecla(evento):
    global tecla_pressionada
    if tecla_pressionada is None:
        tecla_pressionada = evento.name

def view_menu():
    print("\n1. add process")
    print("2. execute")
    print("3. view process")
    print("4. exit")
    print("\nEscolha uma ação: ")

def view_process(list_process):
    for i in list_process:
        print(f"Processo {i['id']}, tempo restante: {i['tempo']}s")

def addp(list_process):
    tmp = int(input("Tempo do processo: "))
    process = {"id":len(list_process), "tempo":tmp}
    list_process.append(process)
    print("Novo processo adicionado à fila!")

def execute(list_process, time_slice):
    i = 0
    while len(list_process) > 0:
        process = list_process[i]
        t_ini = int(time.monotonic())
        print(f"Executando processo {i}...")
        while True:
            if (process["tempo"] - (int(time.monotonic()) - t_ini)) <= 0:
                list_process.pop(i)
                print(f"Processo {i} finalizado!")
                break
            elif (int(time.monotonic()) - t_ini) >= time_slice:
                process["tempo"] = process['tempo'] - (int(time.monotonic()) - t_ini)
                break


        hook = keyboard.on_press(registrar_tecla)
        tempo_limite
        print(f"Deseja executar alguma ação? Voce tem {tempo_limite}s para precionar 'a' ou 'b'")
        tempo_inicial = time.monotonic()
        while time.monotonic() - tempo_inicial < tempo_limite:
            if tecla_pressionada:
                break
            time.sleep(0.05)  # Evita alto consumo de CPU

        keyboard.unhook(hook)

        if tecla_pressionada == "a":#keyboard.is_pressed('a'):
            print("Interrupção para adicionar mais um processo")
            addp(list_process)
        if tecla_pressionada == "b":#keyboard.is_pressed('b'):
            print("Execução interrompida!")
            return None

        if len(list_process) == 0:
            print("Todos os processos foram finalizados!")
            return None

        i = (i+1) % len(list_process)



time_slice = int(input("Defina um Time Slice: "))
list_process = []

while True:
    view_menu()
    option = input("")
    if option == "4": break
    elif option == "1":
        addp(list_process)
    elif option == "2":
        print("ATEÇÃO: Para adicionar mais um processo no meio da execução, precione a tecla 'a' do seu teclado")
        print("Caso queira parar a execução, aperte a tecla 'b'")
        execute(list_process, time_slice)
    elif option == "3":
        view_process(list_process)
    else:
        print("Opa! Essa não é uma opção correspondente às disponíveis.\nTente novamente.")
