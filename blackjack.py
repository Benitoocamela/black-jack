from bj import Partida
from cuentas import *

existe = True
login = False
cuenta = ""

while existe:
    while not login:
        print("""
    
        L PARA INICIAR SESION EN UNA CUENTA
        R PARA CREAR UNA CUENTA
        E PARA SALIR

        """)
        eleccion = input("QUE QUIERES HACER?").lower()

        if eleccion == "e":
            existe = False

        if eleccion == "r":
            registrarCuenta()

        if eleccion == "l":
            cuenta = iniciarSesion()

            if cuenta != "":
                break

            if cuenta == False:
                existe = False
                break

            
    if not existe:
        break
    login = True

    # AQUI COMIENZA EL MENU
    rolUsuario = rolCuenta(cuenta)

    if rolUsuario == "admin":
        print("""
            
            J PARA EMPEZAR UNA PARTIDA
            P PARA VER CUANTAS PARTIDAS HAS JUGADO
            F PARA MIRAR LAS FICHAS QUE TIENES
            C PARA COMPRAR FICHAS
            P PARA CAMBIAR EL PRECIO DE LAS FICHAS
            E PARA SALIR

        """)
    elif rolUsuario == "user":
        print("""
            
            J PARA EMPEZAR UNA PARTIDA
            P PARA VER CUANTAS PARTIDAS HAS JUGADO
            F PARA MIRAR LAS FICHAS QUE TIENES
            C PARA COMPRAR FICHAS
            E PARA SALIR

        """)

    eleccion = input("QUE QUIERES HACER?").lower()

    if eleccion == "e":
        print(cuenta)
        existe = False

    if eleccion == "f":
        print(f"Tienes: {fichasCuenta(cuenta)} fichas!")
    if eleccion == "p" and rolUsuario == "admin":
        nuevoPrecio = input("Elige un nuevo precio para las fichas: ")
        cambiarPrecioFichas(nuevoPrecio)
    if eleccion == "c":
        cantidad = int(input("Cuantas fichas quieres comprar?"))
        tarjeta = int(input("Numero de tarjeta de credito:"))
        cad = int(input("Fecha de caducidad:"))

        if (confirmarPago(cuenta, cantidad, tarjeta, cad)):
            print("Gracias por comprar :)\n")

    if eleccion == "p":
        print(f"Has jugado {partidasCuenta(cuenta)} partidas!\n")

    if eleccion == "j":
        actualizarPartidas(cuenta)
        Fichas = input("Cuantas fichas quieres jugar?\n")

        if (int(Fichas) > int(fichasCuenta(cuenta))):
            print("No tienes suficientes fichas para jugar\n")
            break

        PartidaBucle = Partida(int(Fichas))

        while not PartidaBucle.PartidaAcabada:
            print("""

                H Para una carta
                S Para parar

            """)

            eleccion = input("Que eliges?\n").lower()

            if eleccion == "h":
                PartidaBucle.DarCarta(True)
                PartidaBucle.ActualizarEstado()
                PartidaBucle.DarEstado()
                if PartidaBucle.PartidaAcabada:
                    actualizarFichas(cuenta, PartidaBucle.Jugador.FichasGanadas)
                    PartidaBucle.Vocal()
                    _ = input("Presiona cualquier tecla para continuar\n")

                    
            elif eleccion == "s":
                while not PartidaBucle.PartidaAcabada:
                    PartidaBucle.DarCarta(False)

                    PartidaBucle.ActualizarEstado()
                    if PartidaBucle.PartidaAcabada: 
                        actualizarFichas(cuenta, PartidaBucle.Jugador.FichasGanadas)
                        PartidaBucle.Vocal()

                        _ = input("Presiona cualquier tecla para continuar\n")

                        break

                    PartidaBucle.DarEstado()