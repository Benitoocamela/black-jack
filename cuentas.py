from encriptacion import *
import urllib.request
import json
import os

def existeArchivo(destinacion):
    if os.path.exists(destinacion):
        return True
    return False

def crearArchivo(destinacion):
    with open(destinacion, "x"):
        pass
    return open(destinacion, "a")

def quitarLineasFantasma():
    with open("Usuarios.txt", "r") as archivo:
        lineas = [linea.strip() for linea in archivo.readlines() if linea.strip()]

    with open("Usuarios.txt", "w") as archivo:
        archivo.write("\n".join(lineas))

def registrarCuenta():
    desencriptarArchivo()
    nombre = input("Nombre de la cuenta: ")
    contra = input("Contra de la cuenta: ")

    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            nombreE = line.split("/")[0]
            if nombre == nombreE:
                print("YA EXISTE UNA CUENTA CON ESE NOMBRE")
                encriptarUsuarios()
                return False

    with open("Usuarios.txt", "a") as usuarios:
        usuarios.write(f"\n{nombre}/{contra}/0/user/0")
    print("CUENTA CREADA!")
    encriptarUsuarios()
    return True

def iniciarSesion():
    desencriptarArchivo()
    nombre = input("Nombre de la cuenta: ")
    contra = input("Contra de la cuenta: ")

    quitarLineasFantasma()

    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            nombreE, contraA = line.split("/")[:2]
            if nombreE == nombre and contra == contraA:
                print("SESION INICIADA!")
                encriptarUsuarios()
                return nombreE
    encriptarUsuarios()
    print("NO EXISTE NINGUNA CUENTA CON ESE NOMBRE O LA CONTRASE;A ES INCORRECTA!")
    return False

def obtenerDatosCuenta(cuenta):
    desencriptarArchivo()

    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            datos = line.strip().split("/")
            nombre = datos[0]
            if cuenta == nombre:
                encriptarUsuarios()
                return datos

    encriptarUsuarios()

def actualizarDatoCuenta(cuenta, indice, nuevo_valor):
    desencriptarArchivo()

    with open("Usuarios.txt", "r") as usuarios:
        lineas = usuarios.readlines()

    for i in range(len(lineas)):
        datos = lineas[i].strip().split("/")
        nombre = datos[0]
        if cuenta == nombre:
            datos[indice] = str(nuevo_valor)
            lineas[i] = "/".join(datos) + "\n"

    with open("Usuarios.txt", "w") as archivo:
        archivo.writelines(lineas)
    
    encriptarUsuarios()

def cambiarPrecioFichas(precio):
    with open("precio.txt", "w") as archivo:
        archivo.write(precio)

def precioFichas():
    with open("precio.txt", "r") as archivo:
        precio = int(archivo.readline())
    return precio

def actualizarFichas(cuenta, cantidad):
    nuevasFichas = cantidad + int(fichasCuenta(cuenta))

    cambiarFichas(cuenta, nuevasFichas)

    return True

def actualizarPartidas(cuenta):
    actualizarDatoCuenta(cuenta, 4, int(partidasCuenta(cuenta)) + 1)

    return True

def fichasCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[2]

def rolCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[3]

def partidasCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[4]

def cambiarFichas(cuenta, cantidad):
    actualizarDatoCuenta(cuenta, 2, cantidad)

def confirmarPago(cuenta, cantidad, tarjeta, cad):
    api_url = f"https://castelletsmxa.cat/app/tpv/?card={tarjeta}&data={cad}&amount={cantidad}"

    req = urllib.request.Request(api_url)
    with urllib.request.urlopen(req) as response:
        jsontopy = response.read().decode('utf-8')
        api_response = json.loads(jsontopy)

        resultado = api_response.get("result", "ko")  

        if resultado == "ko":
            print("El pago ha fallado")
            return False
        else:
            print("Pago exitoso")

            actualizarFichas(cuenta, cantidad)
            return True

while not existeArchivo("Usuarios.txt"):
    crearArchivo("Usuarios.txt")

while not existeArchivo("precio.txt"):
    crearArchivo("precio.txt")

while not existeArchivo("clave.key"):
    crearArchivo("clave.key")