#cuatroEnLinea_juego
def imprimirMatriz(matriz,f=0,c=0):  # imprimimos la matriz con recursividad 
    if f == len(matriz):
        print()
    else:    
        if c<=len(matriz[f])-1:
            print("%5s"% matriz[f][c], end="")
            imprimirMatriz(matriz, f, c+1)
        else:
            print()
            print()
            imprimirMatriz(matriz, f+1, 0)
         
def seleccionarFicha():   #función para que el jugador elija la ficha
    while True:
        try:
            v=input("Jugador 1 - Seleccione su ficha ( X - 0 ): ").upper() #en caso de que no juegue la máquina, seria jugador 1
            assert v=="X" or v=="0"
            break
        except AssertionError:
            print("Ingreso incorrecto. Intente nuevamente.")
    return v
        
def verificarColumna(matriz, columna, ficha):  #funcion para verificar si la columna se encuentre libre y no completa
    for i in range(len(matriz)):
        while "." not in matriz[0][columna]:
            columna=int(input("la Columna ya se encuentra ocupada. Ingrese otra posición: ")) #cuando la columna se encuentra completa

        if "." in matriz[-1-i][columna]: #la columna se encuentra disponible
            matriz[-1-i][columna]=ficha
            break
    return matriz

def verificar4enLinea(matriz):
    fila=5 #son 5 filas contando desde 0
    controlador=False
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if j<=3: #verifica 4 columnas del 0-3

                #verifica de manera horizontal                                                     
                if matriz[fila][j]==matriz[fila][j+1] and matriz[fila][j+1]==matriz[fila][j+2] and matriz[fila][j+2]==matriz[fila][j+3] and matriz[fila][j+3]!=".":
                    controlador=True #se obtuvo 4 en linea
                    break

                #diagonal creciente 
                if (matriz[fila][j]==matriz[fila-1][j+1] and matriz[fila-1][j+1]==matriz[fila-2][j+2] and matriz[fila-2][j+2]==matriz[fila-3][j+3] and matriz[fila][j]!="."):
                    controlador=True
                    break

                 #diagonal decreciente -> se lee de der a izq -> a diferencia de la diagonal creciente
                if (matriz[fila][-j-1]==matriz[fila-1][-j-2] and matriz[fila-1][-j-2]==matriz[fila-2][-j-3] and matriz[fila-2][-j-3]==matriz[fila-3][-j-4] and matriz[fila-3][-j-4]!=".") and fila>=3:
                    controlador=True
                    break

            if i<=2: #fila ->i
                # verificade manera Vertical (lo contrario a lo de la manera horizontal)
                if matriz[fila][j]==matriz[fila-1][j] and matriz[fila-1][j]==matriz[fila-2][j] and matriz[fila-2][j]==matriz[fila-3][j] and matriz[fila-3][j]!=".":
                    controlador=True
                    break
        fila-=1                
        if controlador==True:
            break
    return controlador

def verificarEmpate(matriz): #funcion que verifica si la matriz está completa o no, para detectar el empate de los jugadores
    empate=True 
    for fila in range(len(matriz)): #si ninguno logra el 4 en linea ->empate
        if "." in matriz[fila]:
            empate=False #empate -> false, porque todavía se encuentran espacios disponible para completar 
            break
    return empate


def seguirJugando():
    while True:
        try:
            repetirJuego=int(input("¿Quieren volver a jugar? Ingrese (1) para seguir, (0) para finalizar: "))
            assert repetirJuego==1 or repetirJuego==0
            break
        except AssertionError:
            print("¡ERROR! Ingrese (1 o 0)")
    return repetirJuego


# Programa Principal
m=[["."]*7 for i in range(6)]  #crea la matriz mxn de 7 columnas y 6 filas
imprimirMatriz(m) #llama a la funcion para imprimir matriz
ficha=seleccionarFicha() #le pedimos al jugador que elija su ficha -> si elije x, se le asigna automaticamente 0 al otro jugador
jugador=1
ganadores = {}
nombresGanadores=[]
    
while True:
    try:
        turno=int(input(f"\n Jugador {jugador} ingrese el N° de columna (0-6) para colocar la ficha: "))
        verificarColumna(m, turno, ficha)
        print("\n")
        imprimirMatriz(m)

        ganador=verificar4enLinea(m)
        if ganador: #hay ganador
            print("*"*50)
            print(f"\nGANADOR JUGADOR {jugador}")
            ganador = input("Nombre del ganador: ").capitalize()
            nombresGanadores.append(ganador)
            continuar=seguirJugando() #le pregunta si desea seguir jugando
            if continuar!=1:
                break
            else:
                m.clear()
                m=[["."]*7 for i in range(6)]
        else: #para el empate, no hubo ganadores
            if verificarEmpate(m):
                print("¡FIN DEL JUEGO! Se ha completado el tablero y se produjo un empate")
                continuar=seguirJugando() #le pregunta si desea seguir jugando
                if continuar!="1":
                    break
                else:
                    m.clear()
                    m=[["."]*7 for i in range(6)]
         
        if ficha=="X":
            ficha="O"
        else:
            ficha="X"
        if jugador==1:
            jugador=2
        else:
            jugador=1
        
    except IndexError:
        print("ERROR: IndexError, intente nuevamente")

    except ValueError:
        print("ERROR: ValueError, intente nuevamente")

print("*"*50)
print("¡FIN DEL JUEGO!")
print()
try: 
    archivo=open("ganadores.txt", "wt")  #dentro de un bloque protejido, abrimos el archivo donde escriberemos el ganador y la cantidad de partidas q realizó

    for x in nombresGanadores:
        ganadores[x]=nombresGanadores.count(x)
        if ganadores=={}:
            archivo.write("NO HUBIERON GANADORES")
        else:
            for g in ganadores:
                linea=(f"{g} : {str(ganadores[g])} partida/s")
                titulo="GANADORES"
                archivo.write(titulo.center(50," ")+"\n")
                archivo.write(linea+"\n")
                archivo.write(("*"*100)+"\n") 
                archivo.write("¡FELICIDADES POR GANAR! \n")

        
except FileNotFoundError:
    print("No se puede abrir el archivo correspondiente a los ganadores del juego")
except OSError:
    print("Error de SO")

finally:  #cerramos el archivo correspondiente 
    try:
        archivo.close()
    except NameError:
        pass