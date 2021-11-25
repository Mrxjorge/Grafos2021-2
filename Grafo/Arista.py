class Arista():
    
    def __init__(self, peso, origen, destino, obstruido = False):
        self.peso = peso
        self.origen = origen # dato del nodo
        self.destino = destino # dato del nodo
        self.obstruido = obstruido