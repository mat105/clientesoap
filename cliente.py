from suds.client import Client

class Cliente:

    def crear_jugador(self, nomb, posi):
        perso = self.client.factory.create('jugador')
        perso.nombre = nomb
        perso.posicion = posi
        
        self.client.service.agregarJugador(perso)
        
        return perso

    def agregar_ojeos(self, jugador, ojeos):
        if jugador and ojeos:
            for _ojeo in ojeos:
                ojeo = self.client.factory.create('ojeo')
                ojeo.clubActual = _ojeo.get("club", "libre")
                ojeo.comentarios = _ojeo.get("comentarios", "Sin comentarios")
                ojeo.costoPase = _ojeo.get("costo", 0)
                ojeo.fecha = _ojeo.get("fecha", "2016/01/01")
                
                self.client.service.agregarOjeo(jugador, ojeo)
        

    def listar_ojeados_club(self, club):
        jugadores = []
        for jug in self.client.service.listarJugadores()[0]:
            ojeos = self.client.service.listarOjeos(jug)
            
            if ojeos:
                ojeos = ojeos[0]
                clubActual = ojeos[len(ojeos)-1].clubActual
                if clubActual == club:
                    jugadores.append(jug)
                    
        return jugadores
        
        
    def listar_jugadores_precio(self, precio):
        jugadores = []
        for jug in self.client.service.listarJugadores()[0]:
            ojeos = self.client.service.listarOjeos(jug)
            
            if ojeos:
                ojeos = ojeos[0]
                costo = ojeos[len(ojeos)-1].costoPase
                if costo > precio:
                    jugadores.append(jug)
                    
        return jugadores
            
            
    def eliminar_jugador(self, juga):
        if juga:
            self.client.service.eliminarJugador(juga)
        

    def __init__(self):
        self.client = Client("http://localhost:9999/ws/ojeador?wsdl")
        
        #print(client)
        #print(self.client.service)
        
        #persona = client.factory.create('jugador')
        #print(persona)
        
        lista = (
            ("German Denis", "Delantero", [{"club":"Independiente", "costo":1000005, "comentarios":"goleador", "fecha":"2016/03/08"}] ),
            ("Ivan Pillud", "Lateral", [] ),
            ("Victor Cuesta", "Defensor", [] ),
            ("Sebastian Ereros", "Delantero", [ {"club":"Quilmes", "costo":2, "fecha":"2016/1/12"} ] )
            )
        
        for a, b, c in lista:
            jug = self.crear_jugador(a,b)
            self.agregar_ojeos( jug, c )
            
        print("Jugadores actuales: \n:", self.client.service.listarJugadores()[0])


        jugaclub = self.listar_ojeados_club("Quilmes")
        print("Jugadores ojeados de quilmes: \n:", jugaclub)
        
        jugapre = self.listar_jugadores_precio(1000000)
        print("Jugadores con pase mayor al millon: \n:", jugapre)
        
        print("Eliminando...")
        
        for a in jugaclub:
            self.eliminar_jugador(a)
        for b in jugapre:
            self.eliminar_jugador(b)
        
        
        
        print("Jugadores final:")
        print(self.client.service.listarJugadores()[0])
    
    
def main():
    Cliente()
    
main()
