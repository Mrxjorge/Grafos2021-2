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
    print("12. Invertir la dirección de una ruta")
    print("13. Recorridos por anchura y profundidad")
    print("14. Árbol de expansión mínima Kruskal y Boruvka")
    print("15. Recorrido de menor distancia de un planeta a otro")
    option = input("Opcion a elegir: ")
    if option == "1":#Ver planetas
        grafo.imprimirN()
    if option == "2":#Ver rutas
        grafo.imprimirA()
    if option == "3":#Agregar planeta
        nombre = input("Diga el nombre del planeta a agregar:\n")
        if grafo.ingresarN(nombre):
            print(f"Planeta {nombre} agregado")
        else:
            print(f"Planeta {nombre} ya presente en el sistema")
    if option == "4":#Agregar ruta
        origen = input("Diga el origen de la ruta: ")
        destino = input("Diga el destino de la ruta: ")
        peso = input("Diga el peso de la ruta: ")
        obstruido = input("La ruta está obstruida? 1: Sí -- 2: No ")
        if grafo.ingresarA(origen, destino, peso, obstruido == "1"):
            print("Ruta creada")
        else:
            print("La ruta no pudo ser creada")
    if option=="5":#Eliminar planeta
        print("Dijite el nombre del planeta a elimiar del sistema: ")
        eliminar=input()
        if grafo.eliminarNodo(eliminar):
            print("Planeta eliminado")
        else:
            print("No se pudo eliminar el planeta")
    if option=="6":#Eliminar ruta
        print("Para eliminar la ruta, digite el planeta origen y el planeta destino")
        origen = input("Origen: ")
        destino = input("Destino: ")
        if grafo.eliminarArista(origen,destino):
            print("Ruta eliminada")
        else:
            print("La ruta no pudo ser eliminada")
    if option == "7":#Modificar ruta
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
    if option == "8":#Conocer si la Galaxia está fuertemente Conectada
        print("")
    if option == "9":#Conocer si hay planetas sin rutas salientes (pozos)
        pozos = grafo.buscarPozos()
        print(f"Los pozos presentes en el sistema son {pozos}")
    if option == "10":#Conocer las rutas que entran y salen de cada planeta
        nombre = input("Diga el nombre del planeta a analizar: ")
        planeta = grafo.obtenerNodo(nombre)
        if planeta:
            print(f"Las rutas de salida del planeta son: {planeta.listaAdyacentes}")
            print(f"Las rutas de entrada al planeta son: {grafo.obtenerEntradas(nombre)}")
        else:
            print("Planeta no encontrado en el sistema")
    if option == "11":#Cambiar tipo de grafo
        reinicio = input("Esta acción reinicia el grafo a sus valores por defecto, continuar? 1. Sí -- 2. No")
        if reinicio == "1":
            tipo = input("Escoja el tipo de grafo nuevo: 1. Dirigido -- 2. No Dirigido")
            nuevoTipo = tipo == "1"
            if grafo.dirigido != nuevoTipo:
                grafo.cambiarTipoGrafo(nuevoTipo)
                print("Tipo de grafo actualizado")
            else:
                print("El grafo ya es del tipo seleccionado")
    if option == "12":#Invertir la dirección de una ruta
        origen = input("Diga el origen de la ruta a invertir: ")
        destino = input("Diga el destino de la ruta a invertir: ")
        if grafo.invertirArista(origen, destino):
            print("La ruta se invirtió correctamente")
        else:
            print("Ruta inexistente")
    if option == "13":#Recorridos por anchura y profundidad
        opt = input("Escoja el tipo de recorrido: 1. Anchura -- 2. Profundidad ")
        nombre = input("Escoja el planeta para iniciar el recorrido: ")
        recorrido = []
        if opt == "1":
            recorrido = grafo.amplitud(nombre)
        else:
            recorrido = grafo.profundidad(nombre)
        if recorrido:
            print(f"El recorrido empezando por {nombre} es {recorrido}")
        else:
            print("El recorrido no se pudo completar")
    if option == "14":#Árbol de expansión mínima Kruskal y Boruvka
        print("El recorrido por Kruskal:")
        grafo.kruskal()
        print("El recorrido por Boruvka:")
        grafo.boruvka()
    if option == "15":#Recorrido de menor distancia de un planeta a otro
        origen = input("Escoja el planeta para iniciar el recorrido: ")
        destino = input("Escoja el planeta para finalizar el recorrido: ")
        grafo.caminoMasCorto(origen, destino)
            
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