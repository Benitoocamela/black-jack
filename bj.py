import random

class Partida:
    def __init__(self, Fichas):
        self.Fichas = Fichas
        self.Baraja = Baraja()
        self.Jugador = Jugador(Fichas)
        self.Croupier = Croupier()
        self.PartidaAcabada = False
        self.Empate = False
        self.CasaGana = False
        self.Blackjack = False

        self.Baraja.Generar()
        self.Baraja.Mezclar()

        self.Jugador.FichasGanadas = self.Jugador.Fichas * -1 

        self.DarCarta(True)
        self.ActualizarEstado()
        self.DarEstado()

        self.DarCarta(False)
        self.ActualizarEstado()
        self.DarEstado()

    def DarCarta(self, AJugador: bool):
        Carta = self.Baraja.DarCarta()

        if AJugador:
            self.Jugador.Carta(Carta)
            print(f"Has sacado un {Carta}\n")
            return self.Jugador.Mano
        
        print(f"El croupier a sacado un {Carta}\n")
        self.Croupier.Carta(Carta)
        return self.Croupier.Mano
    
    def ActualizarEstado(self):
        self.Jugador.Actualizar()
        self.Croupier.Actualizar()
        self.Logica()

    def DarEstado(self):
        print(f"Jugador: {self.Jugador.Valor}\nCroupier: {self.Croupier.Valor}\n")

    def Logica(self):
        if self.Jugador.Valor == 21 and len(self.Jugador.Mano) == 2:
            self.CasaGana = False
            self.Blackjack = True
            self.PartidaAcabada = True
            self.Jugador.FichasGanadas += self.Jugador.Fichas * 3
            return True

        if self.Jugador.Valor > 21:
            self.CasaGana = True
            self.Blackjack = False
            self.PartidaAcabada = True
            
            return False
        
        if self.Croupier.Valor == 21 and len(self.Croupier.Mano) == 2:
            self.CasaGana = True
            self.Blackjack = True
            self.PartidaAcabada = True
            return True
        
        if self.Croupier.Valor > 21:
            self.CasaGana = False
            self.Blackjack = False
            self.PartidaAcabada = True
            self.Jugador.FichasGanadas += self.Jugador.Fichas * 2
            return True

        if self.Croupier.Valor >= 17 and self.Jugador.Valor > self.Croupier.Valor and self.Jugador.Valor <= 21:
            self.CasaGana = False
            self.Blackjack = False
            self.PartidaAcabada = True
            self.Jugador.FichasGanadas += self.Jugador.Fichas * 2

            return True
        
        if self.Croupier.Valor >= 17 and self.Jugador.Valor < self.Croupier.Valor and self.Croupier.Valor <= 21:
            self.CasaGana = True
            self.Blackjack = False
            self.PartidaAcabada = True
            return False

        if self.Croupier.Valor >= 17 and self.Jugador.Valor == self.Croupier.Valor and self.Croupier.Valor <= 21:
            self.Empate = True
            self.PartidaAcabada = True
            self.Jugador.FichasGanadas += self.Jugador.Fichas
            return False
        
        return False
    
    def Vocal(self):
        if self.Empate:
            print("Empate!")
            self.ReiniciarVars()
            return

        if not self.CasaGana and self.Blackjack:
            print("Has ganado con un blackjack!")
            print(f"Has ganado {self.Jugador.FichasGanadas} fichas!")
            self.ReiniciarVars()
            return
        
        if self.CasaGana and self.Blackjack:
            print("Has perdido la casa tiene un blackjack!")
            print(f"Has perdido {self.Jugador.FichasGanadas} fichas!")
            self.ReiniciarVars()
            return

        if self.CasaGana and not self.Blackjack:
            print(f"La casa gana con un {self.Croupier.Valor}!")
            print(f"Has perdido {self.Jugador.FichasGanadas} fichas!")
            self.ReiniciarVars()
            return

        if not self.CasaGana and not self.Blackjack:
            print("Has ganado!")
            print(f"Has ganado {self.Jugador.FichasGanadas} fichas!")
            self.ReiniciarVars()
            return
        
    def ReiniciarVars(self):
        self.Jugador = Jugador(self.Fichas)
        self.Croupier = Croupier()

class Jugador:
    def __init__(self, Fichas):
        self.Mano = []
        self.Valor = 0
        self.Fichas = Fichas
        self.FichasGanadas = 0

    def Carta(self, Carta):
        self.Mano.append(Carta)
    
    def Actualizar(self):
        self.Valor = 0

        for Valor in self.Mano:
            self.Valor += Valor

        return self.Valor
    
class Croupier:
    def __init__(self):
        self.Mano = []
        self.Valor = 0
    
    def Carta(self, Carta):
        self.Mano.append(Carta)

    def Actualizar(self):
        self.Valor = 0

        for Valor in self.Mano:
            self.Valor += Valor
            
        return self.Valor

class Baraja():
    def __init__(self):
        self.Cartas = []

    def Generar(self):
        NumeroDeBarajas = random.randint(1, 8)
        NumeroDeCartas = 13
        TipoDeCartas = 4
        
        for i in range(NumeroDeBarajas):
            for j in range(TipoDeCartas):
                for k in range(NumeroDeCartas):
                    if (k + 2) > 11:
                        Valor = 10
                        self.Cartas.append(Valor)
                    else:
                        self.Cartas.append(k + 2)

        return self.Cartas
    
    def Mezclar(self):
        random.shuffle(self.Cartas)
        return self.Cartas
    
    def DarCarta(self):
        Carta = self.Cartas.pop(0)
        return Carta