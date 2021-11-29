from Grafo.Grafo import *
    
grafo = Grafo(True)
grafo.loadDefault()
print("Sistema planetario")
option = -1
while option != "99":
    print("Escoja una opcion")
    print("1. Ver planetas")
    print("2. Ver rutas")
    print("3. Agregar planeta")
    print("4. Agregar ruta")
    print("5. Eliminar planeta")
    print("6. Eliminar ruta")
    print("7. Modificar ruta")
    print("8. Conocer si la Galaxia está fuertemente Conectada")
    print("9. Conocer si hay planetas sin rutas salientes (pozos)")
    print("10. Conocer las rutas que entran y salen de cada planeta")
    print("11. Cambiar tipo de grafo")
    option = input("Opcion a elegir: ")
    if option == "1":
        grafo.imprimirN()
    if option == "2":
        grafo.imprimirA()
    if option == "3":
        nombre = input("Diga el nombre del planeta a agregar:\n")
        if grafo.ingresarN(nombre):
            print(f"Planeta {nombre} agregado")
        else:
            print(f"Planeta {nombre} ya presente en el sistema")
    if option == "4":
        origen = input("Diga el origen de la ruta: ")
        destino = input("Diga el destino de la ruta: ")
        peso = input("Diga el peso de la ruta: ")
        obstruido = input("La ruta está obstruida? 1: Sí -- 2: No")
        if grafo.ingresarA(origen, destino, peso, obstruido == "1"):
            print("Ruta creada")
        else:
            print("La ruta no pudo ser creada")
    if option=="5":
        print("Dijite el nombre del planeta a elimiar del sistema: ")
        eliminar=input()
        if grafo.eliminarNodo(eliminar):
            print("Planeta eliminado")
        else:
            print("No se pudo eliminar el planeta")
    if option=="6":
        print("Para eliminar la ruta, digite el planeta origen y el planeta destino")
        origen = input("Origen: ")
        destino = input("Destino: ")
        if grafo.eliminarArista(origen,destino):
            print("Ruta eliminada")
        else:
            print("La ruta no pudo ser eliminada")
    if option == "7":
        print("De el origen y el destino de la ruta a modificar")
        origen = input("Origen: ")
        destino = input("Destino: ")
        arista = grafo.obtenerArista(origen, destino)
        if arista:
            print(f"Arista a modificar: Origen->{arista.origen} -- Destino->{arista.destino} -- Peso->{arista.peso} -- Está obstruida->{arista.obstruido}")
            print("Escoja la modificación a realizar")
            mod = input("1. Origen -- 2. Destino -- 3. Peso -- 4. Obstrucción")
            if mod == "1":
                origen = input("Escoja un nuevo origen: ")
                if grafo.cambiarOrigen(arista, origen):
                    print("Origen actualizado")
                else:
                    print("No se pudo actualizar el origen")
            if mod == "2":
                destino = input("Escoja un nuevo destino: ")
                if grafo.cambiarDestino(arista, destino):
                    print("Destino actualizado")
                else:
                    print("No se pudo actualizar el destino")
            if mod == "3":
                arista.peso = input("Escoja un nuevo peso: ")
                print("Peso actualizado")
            if mod == "4":
                obstruccion = input("Desea que la ruta se obstruya? 1. Sí -- 2. No")
                arista.obstruido = obstruccion == 1
    if option == "8":
        print("")
    if option == "9":
        pozos = grafo.buscarPozos()
        print(f"Los pozos presentes en el sistema son {pozos}")
    if option == "10":
        nombre = input("Diga el nombre del planeta a analizar: ")
        planeta = grafo.obtenerNodo(nombre)
        if planeta:
            print(f"Las rutas de salida del planeta son: {planeta.listaAdyacentes}")
            print(f"Las rutas de entrada al planeta son: {grafo.obtenerEntradas(nombre)}")
        else:
            print("Planeta no encontrado en el sistema")
    if option == "11":
        reinicio = input("Esta acción reinicia el grafo a sus valores por defecto, continuar? 1. Sí -- 2. No")
        if reinicio == "1":
            tipo = input("Escoja el tipo de grafo nuevo: 1. Dirigido -- 2. No Dirigido")
            nuevoTipo = tipo == "1"
            if grafo.dirigido != nuevoTipo:
                grafo.cambiarTipoGrafo(nuevoTipo)
                print("Tipo de grafo actualizado")
            else:
                print("El grafo ya es del tipo seleccionado")
        
    print("------------------------------------------------------------------")


# visitados = grafo.amplitud("Saturno")
# nodos = grafo.obtenerNodos()
# setV = set(visitados)
# setN = set(nodos)
# print(f"Visitados: {setV}")
# print(f"Nodos: {setN}")
# print(f"Diferencia: {setN.difference(setV)}")

# desconectados = []
# for nodo in grafo.listaNodos:
#     if not grafo.estaConectado(nodo.dato):
#         desconectados.append(nodo.dato)
# print(desconectados)