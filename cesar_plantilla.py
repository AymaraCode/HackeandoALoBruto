import os
import re
import sys
import random

# Constantes
rueda_cifrado = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def procesar(dicc):
    '''Lee el fichero del diccionario y lo procesa: sin tildes ni diéresis, mayúsculas 
    y Ñ -> NN. Retorna una lista sin \n o \r\n al final de cada elemento.

    :param dicc: str Nombre del fichero que contiene palabras en castellano
    :returns: list Lista de palabras procesada. Lista vacia en caso de error
    '''
    try:
        # La librería en Linux falla si no se hace así ...
        if os.name == 'posix':  # Linux, MacOS
            d = open(dicc, 'r', encoding='latin-1')
        else:                   # Windows
            d = open(dicc,'r')

        todo = d.read()
        lista = todo.splitlines() # genero lista y elimino basurilla del final de cada palabra

        # proceso de la lista        
        lista_procesada = []
        for palabra in lista:
            if len(list(palabra))> 3:
                palabraNueva = ""
                for letra in palabra.upper():
                    if letra == "Á":
                        palabraNueva += "A"
                    elif letra == "É":
                        palabraNueva += "E"
                    elif letra == "Í":
                        palabraNueva += "I"
                    elif letra == "Ó":
                        palabraNueva += "O"
                    elif letra == "Ú":
                        palabraNueva += "U"
                    elif letra =="Ñ":
                        palabraNueva += "NN"
                    elif letra == "Ü":
                        palabraNueva += "U"
                    else:
                        palabraNueva += letra
                lista_procesada.append(palabraNueva)        
        return lista_procesada

    except FileNotFoundError:
        print('Fichero "{0}" no encontrado.\nPor favor, escriba correctamente el nombre del fichero y/o la ruta'.format(dicc))
        return []
    except:
        print("Error inesperado: {0}".format(sys.exc_info()[0]))
        return []



def max_palabra(lista_palabras):
    '''
    Retorna el tamaño máximo de palabra en la lista de palabras en castellano

    :param lista_palabras: list(str) lista de palabras en castellano
    :returns:
    int Tamaño máximo encontrado
    '''

    '''###########################'''
    '''RELLENA EL CÓDIGO QUE FALTA'''
    '''###########################'''

    pass


def num_coincidencias(lista_palabras, texto_candidato, min_sub, max_sub):
    '''
    Compara el todas las posibles subcadenas de texto_candidato entre los tamaños
    min_sub y max_sub contra la lista de palabras

    :param lista_palabras: list todas las palabras del castellano
    :param texto_candidato: str Texto en el que se buscan coincidencias dentro de la lista
    :param min_sub: int Tamaño mínimo de subcadena a buscar
    :param max_sub: int Tamaño máximo de subcadena a buscar

    :returns:
    int Número de coincidencias en el diccionario
    '''

    '''###########################'''
    '''RELLENA EL CÓDIGO QUE FALTA'''
    '''###########################'''
    
    pass

#Metodo ya hecho
def texto_plano(fichero_texto_plano:str):
    '''Pide al ususario que escriba un texto y se guarda en un fichero. Se pide línea a línea
    y ,para acabar, pulsamos INTRO dos veces
    
    :param fichero_texto_plano: str nombre del fichero donde se guarda el texto plano
    '''
    #abro el fichero en modo lectura, falta comprobar que no exista ya
    #no estoy segura de si hacerlo dentro del metodo o al llamarlo, lo dejo así por el momento
    f = open(fichero_texto_plano, 'w', newline=None) #ojo al .txt 
    print("Intoduzca su texto. Para terminar pulse dos veces intro.")

    #Lee lineas y la escribe en el fichero, si se introduce una linea vacía cierro fichero y salgo.
    while True:
        linea = input()
        print(linea)
        if (linea):
            f.write(linea + "\n")
        else:
            f.close()
            break
    pass


def cifrar(fichero_texto_plano, fichero_cifrado_cesar):
    '''
    Dado un fichero de texto en plano y una clave aplica el cifrado César según los
    requerimientos: eliminar espacios y signos de puntuación, 
    vocal con tildes -> sin tildes, min -> MAY, Ñ -> NN, texto cifrado 5 en 5 
    comenzando por la izquierda.
    ASUMO que los números se quedan igual y caracteres tipo: ¡!¿? también
    La clave utilizada será aleatoria de 1 a 25.

    :param fichero_texto_plano: str nombre de fichero con el Texto a cifrar. 
    Se procesa para cumplir requisitos
    :param fichero_cifrado_cesar: str nombre de fichero donde se guardan el texto cifrado
    
    :returns:
    str | None Texto cifrado para la clave aleatoria o None si hubo algún error

    '''
    try:
        archivoLectura = open(fichero_texto_plano, "r", newline=None, encoding="utf-8")
        archivoEscritura = open(fichero_cifrado_cesar, "w", newline=None)
        clave = 10 #random.randint(1, 26)

        textoCifrado = ""
        textoSinEspacios = ""
        textoConEspacios = ""
        letra = "algo"

        #Lee el archivo caracter a caracter y para cuando ya no quedan 
        while(letra):
            letra = archivoLectura.read(1).upper() #Lee uno a uno los caracteres

            #Cuando se encuentra un salto de linea crea los espacios y escribe el texto en el archivo y lo suma a la variable textoCifrado que se devolverá
            if letra == "\n":
                for i in range(len(textoSinEspacios)):
                    textoConEspacios += textoSinEspacios[i]
                    if (i+1) % 5 == 0:
                        textoConEspacios += " "
                textoConEspacios += "\n"
                archivoEscritura.write(textoConEspacios)
                textoCifrado += textoConEspacios
                textoConEspacios = ""
                textoSinEspacios = ""
                continue
            if letra in [" ", ",", ".", ":", ";", ""]: continue #Ignora los espacios y signos de puntuacion
            
            if letra == "Á": letra = "A"
            if letra == "É": letra = "E"
            if letra == "Í": letra = "I"
            if letra == "Ó": letra = "O"
            if letra == "Ú": letra = "U"
            if letra == "Ü": letra= "U"

            if ord(letra) > 64 and ord(letra) < 91: # Comprueba que los caracteres sean letras

                letraASCIIcifrada = ord(letra) + clave

                #Nuestras letras se encuentran entre 65 y en ascii 90 si se pasa de ese rango 
                # debe volver a empezar así que se le resta 26 
                if letraASCIIcifrada < 91:
                    textoSinEspacios += chr(letraASCIIcifrada)
                else:
                    textoSinEspacios += chr(letraASCIIcifrada - 26)
            elif letra == "Ñ": #Excepcion para la letra ñ que debe escribirse como nn
                letraASCIIcifrada = ord("N") + clave                                            #Calcula su valor como si fuera una n 
                if letraASCIIcifrada < 91:
                    textoSinEspacios += chr(letraASCIIcifrada) + chr(letraASCIIcifrada)     # y lo escribe dos veces
                else:
                    textoSinEspacios += chr(letraASCIIcifrada - 26) + chr(letraASCIIcifrada - 26)
            else: # En caso contrario los escribe tal cual
                textoSinEspacios += letra
        archivoEscritura.close()
        archivoLectura.close()
        return textoCifrado
    except Exception:
        return None

def descifra(fichero_cifrado_cesar, fichero_texto_plano_candidato, clave):
    '''
    Dado un texto cifrado (del fichero_cifrado_cesar) y una clave realiza un 
    desplazamiento en sentido contrario a dicha clave. El resultado se guarda en 
    fichero_texto_plano_candidato y se pone como sufijo la clave empleada

    :param fichero_cifrado_cesar: str nombre del fichero con el texto a descifrar
    :param fichero_texto_plano_candidato: str nombre del fichero con el texto tras 
    aplicar la clave en sentido contrario para descifrar
    :param clave: int clave a aplicar. De 1 a 25

    :returns: str | None texto descifrado o None si hubo algún error
    '''
    
    '''###########################'''
    '''RELLENA EL CÓDIGO QUE FALTA'''
    '''###########################'''
    
    pass

def descifras(texto_cifrado, clave):
    '''
    Dado un texto cifrado realiza un desplazamiento en sentido contrario de la rueda según la clave
    
    :param texto_cifrado: str Cadena con el texto cifrado
    :param clave: int Valor de la clave (1 a 25)

    :returns:
    str Texto descifrado
    '''
    
    # SIN AÑADIR LA Ñ A LA RUEDA CUANDO SE HACE LA ROTACIÓN Y ES UNA N
    # SE DESCIFRA EN UNA 'M' (POSIBLE FALLO SIN ARREGLAR?)
    rueda_descifrado = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    texto_descifrado = ""
    
    # Recorrer cada caracter del texto a descifrar
    for letra in texto_cifrado:
        # Convertir los caracteres a mayusculas para posterior busqueda
        # en rueda_descifrado
        letra = letra.upper()

        # Los espacios en blanco y cualquier caracter que no sea letra 
        # se dejan igual 
        if letra in ["", " "] or ord(letra) > 90 or ord(letra) < 65: 
            texto_descifrado += letra
            continue
        
        # Buscar la posicion de la letra en la rueda
        pos_letra_rueda = rueda_descifrado.find(letra)
        # Buscar la letra correspondiente en el string de la rueda de descifrado 
        # utilizando la posicion de la letra en sentido contrario
        letra_descifrada = rueda_descifrado[(pos_letra_rueda - clave) % 26] 
    
        print(f"posicion de la letra {letra}: {pos_letra_rueda} con pivoteo: {(pos_letra_rueda - clave) % 26} es {letra_descifrada}")
        # Concatenar el caracter encontrado al string que se devolverá
        texto_descifrado += letra_descifrada

        
    return texto_descifrado



#Ya está hecha, pero falta comentarla!! Perdón :(
def descifrar_fuerza_bruta(fichero_cifrado_cesar, fichero_resultados):
    '''
    Abre el fichero con el texto cifrado y saca los textos correspondientes 
    a intentos de descifrar con las claves de 0 a 26 (en realidad solo hace falta 
    de 1 a 25).
    
    :param fichero_cifrado_cesar: str Fichero con el texto cifrado
    :param fichero_resultados: str se generan 25 ficheros como resultado de aplicar todas las claves. 
    La clave aplicada aparece como sufijo en el nombre del fichero

    :returns:
    stdout Todos los textos precedidos de la clave aplicada en cada caso.
    '''
    
    for clave in range(1, 27):
        letra = "algo"
        archivoLectura = open(fichero_cifrado_cesar, "r", newline=None)
        archivoEscritura = open(fichero_resultados + str(clave) + ".txt", "w", newline=None) 
        while(letra):
            letra = archivoLectura.read(1)
            if letra in ["", " "]: continue
            if ord(letra)>64 and ord(letra)<91:
                letraASCII = ord(letra) + clave
                if letraASCII > 90: letraASCII = letraASCII - 26
                archivoEscritura.write(chr(letraASCII))
            else:
                archivoEscritura.write(letra)
    pass


def descifrar_fuerza_bruta_dic(fichero_cifrado_cesar, fichero_resultado, diccionario:list , porcentaje=0.25, rapido=False, minPalabra=None, maxPalabra=None):
    '''
    Abre el fichero con el texto cifrado y saca los textos correspondientes 
    a intentos de descifrar con las claves de 0 a 26 (en realidad solo hace falta 
    de 1 a 25). Por cada texto, indica el número de subcadenas que coinciden con 
    entradas del diccionario

    :param fichero_cifrado_cesar: str Fichero con el texto cifrado
    :param fichero_resultado: str Fichero con los resultados (texto y coincidencias) de aplicar todas las claves
    :param diccionario: list lista de palabras en castellano
    :param porcentaje: int Aquellas claves que generen un porcentaje (en tanto por 1) de coincidencias cercano a 
    la mejor (porcentaje 1) tal que 1 - porcentaje <= coincidencias <= 1 serán consideradas como solución
    alternativa
    :param rapido: boolean Si es False mira todas las posibles subcadenas. Si es True pide la longitud mínima y 
    máxima de las cadenas a considerar. De esta forma, si se hace con criterio, se acelera bastante la búsqueda 
    en el diccionario
    :param minPalabra: int Tamaño mínimo de palabra a considerar
    :param maxPalabra: int Tamaño máximo de palabra a considerar

    :returns:
    stdout Todos los textos precedidos de la clave aplicada en cada caso. Como 
    side-effect crea un fichero con los resultados. Si hay algún tipo de error 
    informa de ello
    '''
    
    '''###########################'''
    '''RELLENA EL CÓDIGO QUE FALTA'''
    '''###########################'''
    
    pass

def menu():
    '''Muestra un menú por pantalla

    :returns:
    int opción escojida
    '''
    print('\n*** Hackeando, a lo bruto, a Julio César ***')
    print('1) Crear fichero en texto plano')
    print('2) Cifrar fichero')
    print('3) Fuerza bruta y resolución a "ojo"')
    print('4) Fuerza bruta y resolución por diccionario')
    print('5) Salir')
    opcion = input('Escoge opción: ')

    # validación
    modelo = re.compile(r'[12345]')
    while modelo.fullmatch(opcion) == None:
        opcion = input('Escoge opción (entre 1 y 5): ')

    return int(opcion)


def esFlotanteAdecuado(porcentaje):
    '''
    Comprueba si es un float adecuado: 0.0 <= porcentaje <= 1.0

    :returns:
    bool
    '''
    try:
        porcentaje = float(porcentaje)
        if 0.0 <= porcentaje <= 1.0:
            return True
        else:
            return False 
    except:
        return False
    

def esIntAdecuado(numero, minimo, maximo):
    '''
    Comprueba si es un int adecuado: minimo <= numero <= maximo

    :returns:
    bool
    ''' 
    try:
        numero = int(numero)
        if minimo <= numero <= maximo:
            return True
        else:
            return False
    except:
        return False
    



                          
                          
""""""""""""""""""""""""""
""" PROGRAMA PRINCIPAL """   #Según Aymara
""""""""""""""""""""""""""     
while True:
    opcion = menu()

    if opcion == 1:
        print("\nCREAR FICHERO EN TEXTO PLANO")
        print("============================")
        nombreArchivo = input("Introduzca un nombre para el archivo: ")
        texto_plano(nombreArchivo + ".txt")
    elif opcion == 2:
        print("\nCIFRAR FICHERO")
        print("================")
        archivoPlano = input("¿Que archivo desea cifrar?(sin extensión)")
        archivoCifrado = input("Introduzca un nombre para el archivo cifrado: ")
        if cifrar(archivoPlano + ".txt", archivoCifrado + ".txt") is None:
            print("Ha ocurrido un error. Probablemente el archivo " + archivoPlano + ".txt no se encontro en el directorio actual.")
    elif opcion == 3: #Aquí falta después mostrar todos los mensajes con cada clave
        print("\nFUERZA BRUTA Y RESOLUCIÓN \"A OJO\"")
        print("===================================")
        archivoCifrado = input("¿Que archivo desea descifrar?(sin extensión) ")
        descifrar_fuerza_bruta(archivoCifrado + ".txt", archivoCifrado + "_clave")
        pass
    elif opcion == 4:
        pass
    elif opcion == 5:
        break






#Esto de aquí abajo es el programa principal según el profe
if __name__ == "__main__":

   


    lista_palabras_castellano = procesar("Diccionario.txt")
    # print(lista_palabras)

    print(max_palabra(lista_palabras_castellano))

    

    texto_plano('test.txt')

    texto_cifrado = cifrar('test.txt', 'test_cifrado.txt')

    #texto_descifrado = descifra('test_cifrado.txt', 'test_candidato.txt', 10)

    descifrar_fuerza_bruta('test_cifrado.txt', 'test_resultado_.txt')