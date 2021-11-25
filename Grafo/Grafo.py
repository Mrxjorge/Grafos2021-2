from Grafo.Arista import *
from Grafo.Nodo import *
from copy import copy
from collections import deque
import json

class Grafo():
    
    def __init__(self):
        self.listaNodos = []
        self.listaAristas = []
        self.listaVisitados = []
        
    #Nodos###################################################################
    def obtenerNodo(self, dato):
        for nodo in self.listaNodos:
            if nodo.dato == dato:
                return nodo
        return None
            
    def ingresarN(self,dato):
        if not self.verificarN(dato):
            self.listaNodos.append(Nodo(dato))
        
    def verificarN(self,dato):
        for i in range (len(self.listaNodos)):
            if dato==self.listaNodos[i].dato:
                return True
        return False
    
    def imprimirN(self):
        for i in range(len(self.listaNodos)):
            print("vertice: {0}".format(self.listaNodos[i].dato))
            
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
        if nodo:
            nodo.listaAdyacentes.remove(adyacente)
            
    #Aristas##########################################################
    def eliminarArista(self, origen, destino):
        arista = self.obtenerArista(origen, destino)
        if arista:
            self.listaAristas.remove(arista)
            self.eliminarAdyacente(origen, destino)
            
    def obtenerArista(self, origen, destino):
        for arista in self.listaAristas:
            if arista.origen == origen and arista.destino == destino:
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
            self.eliminarArista(origen, destino)
            self.ingresarA(destino, origen, peso)
    
    def cambiarOrigen(self, arista, nuevoOrigen):
        aristas = self.obtenerAristasDestino(arista.destino)
        for a in aristas:
            if a.origen == nuevoOrigen:
                return False
        self.eliminarArista(arista.origen, arista.destino)
        self.ingresarA(nuevoOrigen, arista.destino, arista.peso)
        return True
    
    def cambiarDestino(self, arista, nuevoDestino):
        aristas = self.obtenerAristasOrigen(arista.origen)
        for a in aristas:
            if a.destino == nuevoDestino:
                return False
        self.eliminarArista(arista.origen, arista.destino)
        self.ingresarA(arista.origen, nuevoDestino, arista.peso)
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
        
    def verificarA(self, origen, destino):
        for i in range(len(self.listaAristas)):
            if self.obtenerArista(origen, destino):
                return True
        return False
    
    def imprimirA(self):
        for i in range(len(self.listaAristas)):
            arista = self.listaAristas[i]
            print(f"Arista: origen->{arista.origen} -- destino->{arista.destino} -- peso->{arista.peso} -- obstruido->{arista.obstruido}")
            
    #Grafo##########################################################################
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
        with open(ruta) as JSON:
            file = json.load(JSON)
            print(file)
            for planeta in file["Planetas"]:
                self.ingresarN(planeta)
            self.imprimirN()
            for ruta in file["Rutas"]:
                self.ingresarA(ruta["Origen"], ruta["Destino"], ruta["Peso"], ruta["Obstruido"])
            self.imprimirA()
            
    def boruvka(self):
        copiaNodos = copy(self.listaNodos)  # copia de los nodos
        copiaAristas = copy(self.listaAristas)  # copia de las aristas
        aristasBoruvka = []
        listaConjuntos = []
        bandera = True
        cantidad = 0
        while (cantidad > 1 or bandera):
            for nodo in copiaNodos:
                self.operacionesConjuntosB(nodo, listaConjuntos, aristasBoruvka, copiaAristas)
            bandera = False
            cantidad = self.cantidadConjuntos(listaConjuntos)
        for dato in aristasBoruvka:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.getOrigen(), dato.getDestino(), dato.getPeso()))

    def cantidadConjuntos(self, ListaConjuntos):
        cantidad = 0
        for conjunto in ListaConjuntos:
            if len(conjunto) > 0:
                cantidad = cantidad + 1
        return cantidad

    def operacionesConjuntosB(self, nodo, listaConjuntos, aristasBoruvka, copiaAristas):
        encontrado1 = -1
        encontrado2 = -1
        menor = self.buscarMenor(nodo, copiaAristas)

        if menor:  # si no esta vacio
            if not listaConjuntos:  # si esta vacia
                listaConjuntos.append({menor.origen, menor.destino})
                aristasBoruvka.append(menor)
            else:
                for i in range(len(listaConjuntos)):
                    if (menor.origen in listaConjuntos[i]) and (menor.destino in listaConjuntos[i]):
                        return False;  ##Camino cicliclo

                for i in range(len(listaConjuntos)):
                    if menor.origen in listaConjuntos[i]:
                        encontrado1 = i
                    if menor.destino in listaConjuntos[i]:
                        encontrado2 = i

                if encontrado1 != -1 and encontrado2 != -1:
                    if encontrado1 != encontrado2:  # si pertenecen a dos conjuntos diferentes
                        # debo unir los dos conjuntos
                        listaConjuntos[encontrado1].update(listaConjuntos[encontrado2])
                        listaConjuntos[encontrado2].clear();  # elimino el conjunto
                        aristasBoruvka.append(menor)

                if encontrado1 != -1 and encontrado2 == -1:  # si va unido por un conjunto
                    listaConjuntos[encontrado1].update(menor.origen)
                    listaConjuntos[encontrado1].update(menor.destino)
                    aristasBoruvka.append(menor)

                if encontrado1 == -1 and encontrado2 != -1:  # si va unido por un conjunto
                    listaConjuntos[encontrado2].update(menor.origen)
                    listaConjuntos[encontrado2].update(menor.destino)
                    aristasBoruvka.append(menor)

                if encontrado1 == -1 and encontrado2 == -1:  # si no existe en los conjuntos
                    listaConjuntos.append({menor.origen, menor.destino})
                    aristasBoruvka.append(menor)

    def buscarMenor(self, nodo, copiaAristas):
        temp = []
        for adyacencia in nodo.listaAdyacentes:
            for arista in copiaAristas:
                # busco las aristas de esa lista de adyacencia
                if arista.origen == nodo.dato and arista.destino == adyacencia:
                    temp.append(arista)
        if temp:  # si no esta vacia
            # una vez obtenga todas las aristas, saco la menor
            self.ordenar(temp)  # ordeno las aristas
            # elimin ese destino porque ya lo voy a visitar
            # print("{0}-{1}:{2}".format(temp[0].getOrigen(), temp[0].getDestino(), temp[0].getPeso()))
            nodo.listaAdyacentes.remove(temp[0].destino)
            return temp[0]  # es la menor
        return None  # es la menor

    def ordenar(self, aristas):
        for i in range(len(aristas)):
            for j in range(len(aristas)):
                if aristas[i].peso < aristas[j].peso:  # menor a mayor
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