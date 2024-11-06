#65-95
"""
fichero_texto_plano  = "Los tres cerditos"
f = open(fichero_texto_plano + ".txt", 'w', newline=None)
print("Intoduzca su texto. Para terminar pulse dos veces intro.")
while True:
    linea = input()
    print(linea)
    if (linea):
        f.write(linea + "\n")
    else:
        f.close()
        break


hola = open("hola.txt", 'r', newline=None)
letra = hola.read(1)
print(letra)
while letra:
    letra = hola.read(1)
    print(letra)
"""
import random

fichero_texto_plano = "hola.txt"
fichero_cifrado_cesar = "holaCifrado.txt"

archivoLectura = open(fichero_texto_plano, "r", newline=None, encoding="latin-1")
archivoEscritura = open(fichero_cifrado_cesar, "w", newline=None)
clave = 10 #random.randint(1, 26)

pivoteParaEspacios = 1
textoCifrado = ""
letra = "algo"
while(letra):
    if pivoteParaEspacios > 5: 
        archivoEscritura.write(" ") #Cada cinco caracteresescribo un espacio
        pivoteParaEspacios = 0
    letra = archivoLectura.read(1).upper() #Lee uno a uno los caracteres
    if letra in [" ", ",", ".", ":", ";", ""]: continue #Ignora los espacios y signos de puntuacion
    if ord(letra) > 64 and ord(letra) < 91: # Comprueba que los caracteres sean letras
        if letra == "Á": letra = "A"
        elif letra == "É": letra = "E"
        elif letra == "Í": letra = "I"
        elif letra == "Ó": letra = "O"
        elif letra == "Ú": letra = "U"
        elif letra == "Ü": letra= "U"

        letraASCIIcifrada = ord(letra) + clave

        #Nuestras letras se encuentran entre 65 y en ascii 90 si se pasa de ese rango 
        # debe volver a empezar así que se le resta 26 
        if letraASCIIcifrada < 91:
            archivoEscritura.write(chr(letraASCIIcifrada))
            textoCifrado += chr(letraASCIIcifrada)
        else:
            archivoEscritura.write(chr(letraASCIIcifrada - 26))
            textoCifrado += chr(letraASCIIcifrada - 26)
    elif letra == "Ñ":
        letraASCIIcifrada = ord("N") + clave
        if letraASCIIcifrada < 91:
            archivoEscritura.write(chr(letraASCIIcifrada) + chr(letraASCIIcifrada))
            textoCifrado += chr(letraASCIIcifrada)
        else:
            archivoEscritura.write(chr(letraASCIIcifrada - 26) + chr(letraASCIIcifrada - 26))
            textoCifrado += chr(letraASCIIcifrada - 26)

    else: # En caso contrario los escribe tal cual
        archivoEscritura.write(letra)
    pivoteParaEspacios += 1