from suds.client import Client


def main():
    client = Client("http://localhost:9999/ws/hello?wsdl")
    
    persona = client.factory.create('jugador')
    persona.nombre = "Cebolla"
    persona.club = "Independiente"
    persona.costo = "10000000"
    persona.posicion = "Volante"
    persona.comentarios = "Uruguayo"

    client.service.agregarJugador(persona)

    print(client.service.listarJugadores())
    #print( client.service.listarJugadores()[0] )
    
main()