from Grafo.Arista import *
from Grafo.Nodo import *
from copy import copy
from collections import deque
import json

class Grafo():
    
    def __init__(self, dirigido):
        self.listaNodos = []
        self.listaAristas = []
        self.listaVisitados = []
        self.dirigido = dirigido
        
    def clear(self):
        self.listaNodos = []
        self.listaAristas = []
        self.listaVisitados = []
        
    def loadDefault(self):
        self.cargarGrafoJSON("./Data/planets.json")
        
    #Nodos###################################################################
    def obtenerNodo(self, dato):
        for nodo in self.listaNodos:
            if nodo.dato == dato:
                return nodo
        return None
    
    def obtenerNodos(self):
        nodos = []
        for nodo in self.listaNodos:
            nodos.append(nodo.dato)
        return nodos
    
    def eliminarNodo(self, dato):
        nodo = self.obtenerNodo(dato)
        if nodo:
            for arista in self.listaAristas:
                if dato == arista.origen or dato == arista.destino:
                    self.listaAristas.remove(arista)
            for n in self.listaNodos:
                if dato in n.listaAdyacentes:
                    n.listaAdyacentes.remove(dato)
            self.listaNodos.remove(nodo)
            return True
        return False
            
    def ingresarN(self,dato):
        if not self.verificarN(dato):
            self.listaNodos.append(Nodo(dato))
            return True
        return False
        
    def verificarN(self,dato):
        for i in range (len(self.listaNodos)):
            if dato==self.listaNodos[i].dato:
                return True
        return False
    
    def imprimirN(self):
        print("Nodos en el sistema---------------------------")
        print(f"Número de nodos: {len(self.listaNodos)}")
        for i in range(len(self.listaNodos)):
            print("Nodo: {0}".format(self.listaNodos[i].dato))
            
    def imrpimirAdyacencia(self, dato):
        nodo = self.obtenerNodo(dato)
        print(f"Adyacencias de {dato} son {len(nodo.listaAdyacentes)}:")
        for adyacente in nodo.listaAdyacentes:
            print(f"Adyacente a {dato} es {adyacente}")
            
    def buscarPozos(self):
        pozos = []
        for nodo in self.listaNodos:
            if len(nodo.listaAdyacentes) == 0:
                if self.estaConectado(nodo.dato):
                    pozos.append(nodo.dato)
        return pozos
    
    def buscarFuentes(self):
        fuentes = []
        for nodo in self.listaNodos:
            isFuente = True
            for arista in self.listaAristas:
                if nodo.dato == arista.destino:
                    isFuente = False
                    break
            if isFuente and self.estaConectado(nodo.dato):
                fuentes.append(nodo.dato)
        return fuentes
    
    def esConexo(self):
        fuentes = self.buscarFuentes()
        pozos = self.buscarPozos()
        if len(fuentes) == 0 and len(pozos) == 0:
            return True
        return False
    
    def estaConectado(self, dato):
        nodo = self.obtenerNodo(dato)
        if nodo:
            for arista in self.listaAristas:
                if not arista.obstruido:
                    if arista.origen == dato or arista.destino == dato:
                        return True
        return False
    
    def gradoNodo(self, dato):
        nodo = self.obtenerNodo(dato)
        grado = -1
        if nodo:
            grado = 0
            for arista in self.listaAristas:
                if arista.origen == dato or arista.destino == dato:
                    grado += 1
        return grado
    
    def cambiarAdyacente(self, nodo, viejo, nuevo):
        adyacentes = nodo.listaAdyacentes
        pos = -1
        pos = adyacentes.index(viejo)
        if pos != -1:
            adyacentes[pos] = nuevo
            nodo.listaAdyacentes = adyacentes
            
    def eliminarAdyacente(self, dato, adyacente):
        nodo = self.obtenerNodo(dato)
        nodo2 = self.obtenerNodo(adyacente)
        if nodo and adyacente in nodo.listaAdyacentes:
            nodo.listaAdyacentes.remove(adyacente)
        if nodo2 and dato in nodo2.listaAdyacentes:
            nodo2.listaAdyacentes.remove(dato)
            
    def obtenerEntradas(self, dato):
        entradas = []
        for arista in self.listaAristas:
            if arista.destino == dato:
                entradas.append(arista.origen)
        return entradas
            
    #Aristas##########################################################
    def eliminarArista(self, origen, destino):
        arista = self.obtenerArista(origen, destino)
        if arista:
            self.listaAristas.remove(arista)
            self.eliminarAdyacente(origen, destino)
            return True
        return False
            
    def obtenerArista(self, origen, destino):
        for arista in self.listaAristas:
            if arista.origen == origen and arista.destino == destino:
                return arista
            if not self.dirigido:
                if arista.origen == destino and arista.destino == origen:
                    return arista
        return None
    
    def obtenerAristasOrigen(self, origen):
        aristas = []
        for arista in self.listaAristas:
            if arista.origen == origen:
                aristas.append(arista)
        return aristas
    
    def obtenerAristasDestino(self, destino):
        aristas = []
        for arista in self.listaAristas:
            if arista.destino == destino:
                aristas.append(arista)
        return aristas
    
    def invertirArista(self, origen, destino):
        arista = self.obtenerArista(origen, destino)
        if arista:
            peso = arista.peso
            obstruido = arista.obstruido
            self.eliminarArista(origen, destino)
            self.ingresarA(destino, origen, peso, obstruido)
            return True
        return False
    
    def cambiarOrigen(self, arista, nuevoOrigen):
        aristas = self.obtenerAristasDestino(arista.destino)
        for a in aristas:
            if a.origen == nuevoOrigen:
                return False
        self.eliminarArista(arista.origen, arista.destino)
        self.ingresarA(nuevoOrigen, arista.destino, arista.peso, arista.obstruido)
        return True
    
    def cambiarDestino(self, arista, nuevoDestino):
        aristas = self.obtenerAristasOrigen(arista.origen)
        for a in aristas:
            if a.destino == nuevoDestino:
                return False
        self.eliminarArista(arista.origen, arista.destino)
        self.ingresarA(arista.origen, nuevoDestino, arista.peso, arista.obstruido)
        return True
    
    def controlarObstruccionArista(self, origen, destino, control):
        arista = self.obtenerArista(origen, destino)
        if arista:
            arista.obstruido = control
            
    def estaObstruido(self, origen, destino):
        arista = self.obtenerArista(origen, destino)
        if arista:
            return arista.obstruido
        return True
            
    def ingresarA(self, origen, destino, peso, obstruido = False):
        nodoOrigen = self.obtenerNodo(origen)
        nodoDestino = self.obtenerNodo(destino)
        if nodoOrigen and nodoDestino:
            if not self.verificarA(origen, destino):
                self.listaAristas.append(Arista(peso, origen, destino, obstruido))
                nodoOrigen.listaAdyacentes.append(nodoDestino.dato)
                if not self.dirigido:
                    nodoDestino.listaAdyacentes.append(nodoOrigen.dato)
                return True
        return False
        
    def verificarA(self, origen, destino):
        for i in range(len(self.listaAristas)):
            if self.obtenerArista(origen, destino):
                return True
        return False
    
    def imprimirA(self):
        print("Aristas en el sistema---------------------------")
        print(f"Número de aristas: {len(self.listaAristas)}")
        for i in range(len(self.listaAristas)):
            arista = self.listaAristas[i]
            print(f"Arista: origen->{arista.origen} -- destino->{arista.destino} -- peso->{arista.peso} -- obstruido->{arista.obstruido}")
            
    #Grafo##########################################################################
    def cambiarTipoGrafo(self, tipo):
        if tipo != self.dirigido:
            self.clear()
            self.dirigido = tipo
            self.loadDefault()
    
    def amplitud(self, origen):
        visitadosA = []
        cola = deque()
        nodo = self.obtenerNodo(origen)
        if nodo != None:
            visitadosA.append(origen)
            cola.append(nodo)
            while (cola):
                elemento = cola.popleft()
                for adyacencia in elemento.listaAdyacentes:
                    if not self.estaObstruido(elemento.dato, adyacencia):
                        if adyacencia not in visitadosA:
                            nodo = self.obtenerNodo(adyacencia)
                            visitadosA.append(adyacencia)
                            cola.append(nodo)
        return visitadosA
    
    def profundidad(self, origen):
        if origen in self.listaVisitados:
            return
        else:
            nodo = self.obtenerNodo(origen)
            if nodo != None:
                self.listaVisitados.append(nodo.dato)
                for n in nodo.listaAdyacentes:
                    if not self.estaObstruido(origen, n):
                        self.profundidad(n)
        return self.listaVisitados
    
    def cargarGrafoJSON(self, ruta):
        with open(ruta) as inInfo:
            file = json.load(inInfo)
            # print(file)
            for planeta in file["Planetas"]:
                # print(f"Ingresando planeta {planeta}")
                self.ingresarN(planeta)
            for ruta in file["Rutas"]:
                origen = ruta["Origen"]
                destino = ruta["Destino"]
                # print(f"Ingresando ruta {origen} -- {destino}")
                self.ingresarA(ruta["Origen"], ruta["Destino"], ruta["Peso"], ruta["Obstruido"])
        # self.imprimirN()
        # self.imprimirA()
            
    def boruvka(self):
        copiaNodos = copy(self.listaNodos)
        copiaAristas = copy(self.listaAristas)
        aristasBoruvka = []
        visitados = []#Arreglo de conjuntos
        bandera = True
        cantidad = 0
        while cantidad > 1 or bandera:
            for nodo in copiaNodos:
                self.boruvkaNodo(nodo, copiaAristas, aristasBoruvka, visitados)
            bandera = False
            cantidad = len(visitados)
        for i in range(len(aristasBoruvka)):
            print(f"Arista en posición {i}: Origen->{aristasBoruvka[i].origen} -- Destino->{aristasBoruvka[i].destino}")
                
    def boruvkaNodo(self, nodo, copiaAristas, aristasBoruvka, visitados):
        aristas = []
        for n in nodo.listaAdyacentes:
            for arista in copiaAristas:
                if arista.origen == nodo.dato and arista.destino == n:
                    aristas.append(arista)
                elif not self.dirigido and arista.origen == n and arista.destino == nodo.dato:
                    aristas.append(arista)
        for arista in aristas:
            if arista in aristasBoruvka:
                aristas.remove(arista)
                # print(f"Arista {arista.origen} -- {arista.destino} ya presente")
        menor = self.aristaMenor(aristas)
        if menor:
            nodo1 = menor.origen
            nodo2 = menor.destino
            pos1 = -1
            pos2 = -1
            for i in range(len(visitados)):
                if nodo1 in visitados[i]:
                    pos1 = i
                if nodo2 in visitados[i]:
                    pos2 = i
            if pos1 != -1 and pos2 != -1:
                if pos1 == pos2:
                    # print(f"Arista {nodo1} -- {nodo2} encontrada en {pos1}")
                    return
                indice = pos1 if pos1 < pos2 else pos2
                porBorrar = pos1 if pos1 >= pos2 else pos2
                visitados[indice] = visitados[indice] + visitados[porBorrar]
                del visitados[porBorrar]
                aristasBoruvka.append(menor)
                # for i in range(len(aristasBoruvka)):
                #     print(f"Arista repetida en posición {i}: Origen->{aristasBoruvka[i].origen} -- Destino->{aristasBoruvka[i].destino}")
                return
            if pos1 == -1 and pos2 == -1:
                aristasBoruvka.append(menor)
                visitados.append([nodo1, nodo2])
                # for i in range(len(aristasBoruvka)):
                #     print(f"Arista nueva en posición {i}: Origen->{aristasBoruvka[i].origen} -- Destino->{aristasBoruvka[i].destino}")
                return
            aristasBoruvka.append(menor)
            # for i in range(len(aristasBoruvka)):
            #     print(f"Arista con un dato repetido en posición {i}: Origen->{aristasBoruvka[i].origen} -- Destino->{aristasBoruvka[i].destino}")
            if pos1 != -1:
                visitados[pos1].append(nodo2)
            else:
                visitados[pos2].append(nodo1)
        return
                    
    def aristaMenor(self, listaAristas):
        menor = None
        if listaAristas:
            menor = listaAristas[0]
            for arista in listaAristas:
                if arista.peso < menor.peso:
                    menor = arista
        return menor
    
    def ordenar(self, aristas):
        for i in range(len(aristas)):
            for j in range(len(aristas)):
                if aristas[i].peso < aristas[j].peso:
                    temp = aristas[i]
                    aristas[i] = aristas[j]
                    aristas[j] = temp

    def kruskal(self):
        copiaAristas=copy(self.listaAristas)#copia de las aristas
        aristasKruskal=[]
        listaConjuntos=[]
        self.ordenar(copiaAristas)#ordeno las aristas
        for menor in copiaAristas:
            self.operacionesconjuntos(menor,listaConjuntos,aristasKruskal)
        #esta ordenada de mayor a menor
        #print("la lista de conjunto se redujo a : {0}".format(len(ListaConjuntos)))
        for dato in aristasKruskal:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.origen, dato.destino, dato.peso))

    def operacionesconjuntos(self, menor, listaConjuntos, AristasKruskal):
       encontrado1 =- 1
       encontrado2 =- 1
       if not listaConjuntos:#si esta vacia
            listaConjuntos.append({menor.origen, menor.destino})
            AristasKruskal.append(menor)
       else:
            for i in range(len(listaConjuntos)):
                if  (menor.origen  in listaConjuntos[i]) and (menor.destino in listaConjuntos[i]):
                    return False;##Camino cicliclo
            for i in range(len(listaConjuntos)):
                if menor.origen in listaConjuntos[i]:
                   encontrado1 = i
                if menor.destino in listaConjuntos[i]:
                   encontrado2 = i
            if encontrado1 != -1 and encontrado2 != -1:
                if encontrado1 != encontrado2:#si pertenecen a dos conjuntos diferentes
                    #debo unir los dos conjuntos
                    #print("{0} : {1}".format(encontrado1,encontrado2))
                    listaConjuntos[encontrado1].update(listaConjuntos[encontrado2])#uno los dos conjuntos
                    listaConjuntos[encontrado2].clear();#elimino el conjunto
                    AristasKruskal.append(menor)
            if encontrado1 != -1 and encontrado2 == -1:# si va unido por un conjunto
                #ListaConjuntos[encontrado1].add(menor.getOrigen())
                listaConjuntos[encontrado1].add(menor.destino)
                AristasKruskal.append(menor)
            if encontrado1 == -1 and encontrado2 != -1:# si va unido por un conjunto
                listaConjuntos[encontrado2].add(menor.origen)
                #ListaConjuntos[encontrado2].add(menor.getDestino())
                AristasKruskal.append(menor)
            if encontrado1 == -1 and encontrado2 == -1:# si no existe en los conjuntos
                listaConjuntos.append({menor.origen, menor.destino})
                AristasKruskal.append(menor)
                
    def caminoMasCorto(self, origen, destino):
        VerticesAux = []
        VerticesD = []
        self.dijkstra(origen, VerticesAux)
        if self.rutas(VerticesD, VerticesAux, destino, origen):
            print("El camino más corto de: " + origen + " a " + destino + " es: ")
            print(VerticesD)
        else:
            print("El sistema no pudo encontrar un camino")

    def rutas(self, VerticesD, VerticesAux, destino, origen):
        verticeDestino = self.obtenerNodo(destino)
        indice = self.listaNodos.index(verticeDestino)
        if VerticesAux[indice] is None:
            print("No hay camino entre: ", (origen, destino))
            return False
        aux = destino
        while aux != origen:
            verticeDestino = self.obtenerNodo(aux)
            indice = self.listaNodos.index(verticeDestino)
            VerticesD.insert(0, aux)
            aux = VerticesAux[indice]
        VerticesD.insert(0, aux)
        return True

    def dijkstra(self, origen, VerticesAux):
        marcados = []  # la lista de los que ya hemos visitado
        caminos = []  # la lista final
        # iniciar los valores en infinito
        for v in self.listaNodos:
            caminos.append(float("inf"))
            marcados.append(False)
            VerticesAux.append(None)
            if v.dato == origen:
                caminos[self.listaNodos.index(v)] = 0
                VerticesAux[self.listaNodos.index(v)] = v.dato
        while not self.todosMarcados(marcados):
            aux = self.menorNoMarcado(caminos, marcados)  # obtuve el menor no marcado
            if aux is None:
                break
            indice = self.listaNodos.index(aux)  # indice del menor no marcado
            marcados[indice] = True  # marco como visitado
            valorActual = caminos[indice]
            for vAdya in aux.listaAdyacentes:
                indiceNuevo = self.listaNodos.index(self.obtenerNodo(vAdya))
                arista = self.obtenerArista(aux.dato, vAdya)
                if caminos[indiceNuevo] > valorActual + arista.peso:
                    caminos[indiceNuevo] = valorActual + arista.peso
                    VerticesAux[indiceNuevo] = self.listaNodos[indice].dato
        return caminos

    def menorNoMarcado(self, caminos, marcados):
        verticeMenor = None
        caminosAux = sorted(caminos)
        copiacaminos = copy(caminos)
        bandera = True
        contador = 0
        while bandera:
            menor = caminosAux[contador]
            if marcados[copiacaminos.index(menor)] == False:
                verticeMenor = self.listaNodos[copiacaminos.index(menor)]
                bandera = False
            else:
                copiacaminos[copiacaminos.index(menor)] = "x"
                contador = contador + 1
        return verticeMenor

    def todosMarcados(self, marcados):
        for j in marcados:
            if not j:
                return False
        return True