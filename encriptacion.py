import cryptography
from cryptography.fernet import Fernet

def guardarClave(clave):
    with open("clave.key", "rb") as r:
        existe = r.read()

    if existe == "":
        with open("clave.key", "wb") as archivo:
            archivo.write(clave)
    else:
        return existe
    
def generarClaveEncriptacion():
    clave = Fernet.generate_key()
    guardarClave(clave)

def leerClave():
    with open("clave.key", "rb") as archivo:
        clave = archivo.read()
        return clave

def encriptarUsuarios():
    cipherSuite = Fernet(leerClave())
    with open("Usuarios.txt", "rb") as usuarios:
        usuariosDatos = usuarios.read()
    
    usuariosEncriptados = cipherSuite.encrypt(usuariosDatos)

    with open("Usuarios.txt", "wb") as archivo:
        archivo.write(usuariosEncriptados)

def desencriptarArchivo():
    cipherSuite = Fernet(leerClave())

    with open("Usuarios.txt", "rb") as usuarios:
        usuariosDatos = usuarios.read()
    
    try:
        usuariosDesencriptados = cipherSuite.decrypt(usuariosDatos)

        with open("Usuarios.txt", "wb") as archivo:
            archivo.write(usuariosDesencriptados)

    except cryptography.fernet.InvalidToken:
        pass

generarClaveEncriptacion()