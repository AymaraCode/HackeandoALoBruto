import os
import re
import sys
import random

# Constantes
rueda_cifrado = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# FUNCION PROVISIONAL (NO SÉ SI SE PUEDE) PARA ABRIR ARCHIVOS Y MANEJAR ERRORES
def abrir_fichero_multiplataforma(ruta_fichero:str, accion:str):
    '''
    Abre el fichero comprobando si ocurre alguna excepcion

    :param fichero: str Fichero que se va a abrir
    
    :returns: 
    fichero, si no ocurre ningun error
    '''
    try:
        # Abrir el fichero
        # La librería en Linux falla si no se hace así ...
        if os.name == 'posix':  # Linux, MacOS
            fichero = open(ruta_fichero, accion, encoding='latin-1')
        else:                   # Windows
            fichero = open(ruta_fichero, accion)
            
    except FileNotFoundError:
        print('Fichero "{0}" no encontrado.\nPor favor, escriba correctamente el nombre del fichero y/o la ruta'.format(ruta_fichero))
        return None
    except:
        print("Error inesperado: {0}".format(sys.exc_info()[0]))
        return None
    
    return fichero

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

    # Mapear la lista de palabras al tamaño de cada palabra, y 
    # devolver el máximo de dicha lista
    return max(list(map(lambda palabra: len(palabra), lista_palabras)))

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
    #Convierte la lista de palabras a set para agilizar la búsqueda
    set_palabras = set(lista_palabras)
    # Contar las coincidencias que encuentra en cada subcadena del texto candidato
    coincidencias = 0
    # por cada caracter en el string texto_candidato(i)
    for i in range(len(texto_candidato)):
        # genera las cadenas hasta el tamaño maximo indicado en max_sub
        for j in range(i+min_sub, min((i+max_sub+1), len(texto_candidato)+1)):
            # comprobar que no se pase del tamaño del texto_candidato
            subcadena = texto_candidato[i:j]
            coincidencias += (subcadena in set_palabras)
            
    
    return coincidencias
            


def texto_plano(fichero_texto_plano:str):
    '''Pide al ususario que escriba un texto y se guarda en un fichero. Se pide línea a línea
    y ,para acabar, pulsamos INTRO dos veces
    
    :param fichero_texto_plano: str nombre del fichero donde se guarda el texto plano
    '''
    #abro el fichero en modo lectura, falta comprobar que no exista ya
    #no estoy segura de si hacerlo dentro del metodo o al llamarlo, lo dejo así por el momento
    try:
        f = open(fichero_texto_plano, 'w', newline=None, encoding="utf-8") #ojo al .txt 
        print("Intoduzca su texto. Para terminar pulse dos veces intro.")

        #Lee lineas y la escribe en el fichero, si se introduce una linea vacía cierro fichero y salgo.
        while True:
            linea = input()
            if (linea):
                f.write(linea + "\n")
            else:
                f.close()
                break
    except Exception as er:
        print("Hubo un error al intentar abrir o escribir: " + fichero_texto_plano + "\n" + str(er))
        return None


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
        textoPlano = open(fichero_texto_plano, "r", newline=None, encoding="utf-8").read() #Lee el archivo de texto plano y guarda el texto en la variable textoPlano
    except Exception as er:
        print("Hubo un error al intentar abrir o leer: " + fichero_texto_plano + "\n" + str(er))
        return None
    textoCifrado = "" #Variable donde se añadiran las letras cifradas una a una
    clave = random.randint(1, 25) #La clave sera aleatoria del 1 al 25
    for letra in textoPlano:
        if letra in [" ", ",", ".", ":", ";", "", "\n"]: continue #Ignora los espacios, saltos de linea y signos de puntuación
        letra = letra.upper()#Pasa todas las letras a mayúscula
        #Quita los acentos y dieresis
        if letra == "Á": letra = "A"
        if letra == "É": letra = "E"
        if letra == "Í": letra = "I"
        if letra == "Ó": letra = "O"
        if letra == "Ú": letra = "U"
        if letra == "Ü": letra= "U"

        if ord(letra) > 64 and ord(letra) < 91: # Comprueba que los caracteres sean letras

            letraASCIIcifrada = ord(letra) + clave # Pasa las letras a código ascii

            #Nuestras letras se encuentran entre 65 y en ascii 90 si se pasa de ese rango 
            # debe volver a empezar así que se le resta 26 
            if letraASCIIcifrada < 91:
                textoCifrado += chr(letraASCIIcifrada)
            else:
                textoCifrado += chr(letraASCIIcifrada - 26)
        elif letra == "Ñ": #Excepcion para la letra ñ que debe escribirse como nn
            letraASCIIcifrada = ord("N") + clave  # Calcula su valor como si fuera una n 
            if letraASCIIcifrada < 91:
                textoCifrado += chr(letraASCIIcifrada) + chr(letraASCIIcifrada)     # y lo escribe dos veces
            else:
                textoCifrado += chr(letraASCIIcifrada - 26) + chr(letraASCIIcifrada - 26)
        else: # Si no es una letra la escribe tal cual
            textoCifrado += letra

    textoConEspacios = "" # Variable donde meteremos el texto cifrado con espacios cada 5 caracteres
    #Bucle para añadir espacios cada 5 caracteres
    for i in range(len(textoCifrado)):
        textoConEspacios += textoCifrado[i]
        if (i + 1) % 5 == 0: textoConEspacios += " "
    #Crea el archivo y escribe el texto cifrado en el
    try:
        open(fichero_cifrado_cesar, "w", newline=None).write(textoConEspacios)
    except Exception as ew:
        print("Hubo un error al intentar abrir o escribir el fichero: " + fichero_cifrado_cesar + "\n" + str(ew))
        return None
    return textoConEspacios #Devuelve el texto cifrado con espacios 


## ESTO PARECE SER INÚTIL, REVISAR!!!!!!!!!
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
    texto_descifrado = ""
    
    # Recorrer cada caracter del texto a descifrar
    for letra in texto_cifrado:
        # Convertir los caracteres a mayusculas para posterior busqueda
        # en rueda_descifrado
        letra = letra.upper()

        # Los espacios en blanco se ignoran
        if letra in ["", " "]: continue
        
        # los signos se dejan igual
        if ord(letra) > 90 or ord(letra) < 65: 
            texto_descifrado += letra
            continue
        
        # Buscar la posicion de la letra en la rueda
        pos_letra_rueda = rueda_cifrado.find(letra)
        # Buscar la letra correspondiente en el string de la rueda de descifrado 
        # utilizando la posicion de la letra en sentido contrario
        letra_descifrada = rueda_cifrado[(pos_letra_rueda - clave) % 26] 
    
        # Concatenar el caracter encontrado al string que se devolverá
        texto_descifrado += letra_descifrada

        
    return texto_descifrado




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
    #Este try-except lee le fichero cifrado y guarda el texto en la variable textoCifrado
    try:
        with open(fichero_cifrado_cesar, "r", newline=None) as ficheroCif:
            textoCifrado = ficheroCif.read()
    except Exception as er:
         print("Hubo un error al intentar leer: " + fichero_cifrado_cesar + "\n" + str(er))

    claves = "" #Aquí se irán guardando los textos descifrados con cada clave

    try:
        #Por cada clave crea un archivo con el numero de la clave y escribe el texto descifrado con esa clave
        #Va guardando cada intento en la variable claves
        for clave in range(1, 26):
            with open(fichero_resultados + str(clave) + ".txt", "w", newline=None) as ficheroEscritura:
                intentoDescifrar = descifras(textoCifrado, clave) 
                claves += "Clave " + str(clave) + ": " + intentoDescifrar + "\n" 
                ficheroEscritura.write(intentoDescifrar)
    except Exception as ew:
        print("Hubo un error al intentar abrir o escribir ficheros\n" + str(ew))
    return claves #Devuelve todas las opciones de descifrado



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
    
    # Comprobar si se requiere un descifrado rápido, en cuyo caso harán falta
    # los parametros minPalabra y maxPalabra
    if(rapido and (minPalabra == None or maxPalabra == None)):
        print('No se especificaron tamaño minimo y maximo de subcadenas para'
              +' un descifrado rápido')
        return
    
    
    
    # Guardar el contenido del fichero en variable texto_cifrado
    try:
        texto_cifrado = fichero_cifrado_cesar.read()
    except Exception as er:
        print("Hubo un error al intentar leer: " + fichero_cifrado_cesar + "\n" + str(er))
        return None
            
    # Diccionario con las coincidencias de cada clave en la lista de palabras
    clave_coincidencias = {} # -> Lista ordenada por valores de claves
    
    # Diccionario con las claves y el resultado de aplicarla en el descifrado
    clave_descifrado = {}
    for clave in range(1,26):
        # descifrar el texto cifrado con la funcion descifras y cada clave
        txt_descifrado_clave = descifras(texto_cifrado, clave)
        # Si no es rápido se especifica tamaño minimo de palabra igual al máximo
        # para no crear ninguna subcadena
        if(not rapido):
            minPalabra = 1
            maxPalabra = len(txt_descifrado_clave)
            
        # comprobar cuantas coincidencias hay de las subcadenas del texto en el diccionario
        coincidencias = num_coincidencias(diccionario, txt_descifrado_clave, minPalabra, maxPalabra)
        # Guardar la clave y las coincidencias encontradas en la lista de palabras
        # en el diccionario
        clave_coincidencias[clave] = coincidencias    
        # Guardar las claves y el resultado de aplicarlas en el texto
        clave_descifrado[clave] = txt_descifrado_clave
            
    # Buscar la clave con más coincidencias en el diccionario de {clave, coincidencias} 
    # se obtiene buscando el mayor valor en las tuplas del diccionario, y obteniendo de esta su clave correspondiente: elemento[0]   
    clave_max_coincidencias = max(clave_coincidencias.items(), key= lambda x: x[1])[0]
    
    
    # Buscar la mayor cantidad de coincidencias, de la clave anterior
    max_coincidencias = clave_coincidencias[clave_max_coincidencias]
    
    
    
    print('\n')
    # Imprimir soluciones y guardarlas en fichero_resultado
    for clave, texto_descifrado in clave_descifrado.items():
        # String de informacion sobre la clave, que se va a imprimir, y a escribir en archivo
        str_info_clave_coincidencia = f'Clave {clave} descifrada como {texto_descifrado},con {clave_coincidencias[clave]} coincidencias'        
        
        #Comprobar si es solucion definitiva o alternativa
        if(clave == clave_max_coincidencias):
            # Concatenar la informacion al string que se va a mostrar
            str_info_clave_coincidencia += "--- SOLUCION DEFINITIVA! ---"
        else:
            if(max_coincidencias > 0):
                # Calcular porcentaje de coincidencia de cada clave sobre 1
                porcentaje_coincidencia = clave_coincidencias[clave] / max_coincidencias
                # Comprobar Si el porcentaje de coincidencia de la clave es mayor al porcentaje 
                # pasado como parametro para determinar solucion alternativa
                if(porcentaje_coincidencia >= porcentaje):
                    # Concatenar la informacion al string que se va a mostrar
                    str_info_clave_coincidencia += "SOLUCION ALTERNATIVA!"
                
        # Imprimir información de cada descifrado
        print(str_info_clave_coincidencia + '\n')
        # Escribir información de cada descifrado al fichero_resultado
        try:
            fichero_resultado.write(str_info_clave_coincidencia + '\n') 
        except Exception as er:
            print("Hubo un error al intentar escribir en: " + fichero_resultado + "\n" + str(er))
            return
        
    
    fichero_cifrado_cesar.close()
    fichero_resultado.close()   
                
            

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
""" PROGRAMA PRINCIPAL """  
""""""""""""""""""""""""""     
while True:
    opcion = menu()

    if opcion == 1:
        print("\nCREAR FICHERO EN TEXTO PLANO")
        print("============================")
        nombreArchivo = input("Introduzca un nombre para el archivo(sin extensión): ")
        texto_plano(nombreArchivo + ".txt")
    elif opcion == 2:
        print("\nCIFRAR FICHERO")
        print("================")
        archivoPlano = input("¿Que archivo desea cifrar?(sin extensión)")
        archivoCifrado = input("Introduzca un nombre para el archivo cifrado(sin extensión): ")
        textCif = cifrar(archivoPlano + ".txt", archivoCifrado + ".txt")
        if textCif:
            print("Texto cifrado con exito (guardado en " + archivoCifrado + ".txt ): \n" + textCif)

    elif opcion == 3: 
        print("\nFUERZA BRUTA Y RESOLUCIÓN \"A OJO\"")
        print("===================================")
        archivoCifrado = input("¿Que archivo desea descifrar?(sin extensión) ")
        print(descifrar_fuerza_bruta(archivoCifrado + ".txt", archivoCifrado + "_clave"))
    elif opcion == 4:
        print("\nFUERZA BRUTA Y RESOLUCIÓN POR DICCIONARIO")
        print("===================================")
        
        # Pedir el archivo que se quiere descifrar
        # Mientras el archivo sea None, la funcion abrir_fichero_multiplataforma
        # no pudo encontrarlo
        archivoCifrado = None
        while(not archivoCifrado):
            rutaArchivoCifrado = input("¿Que archivo desea descifrar?(sin extensión) ")
            archivoCifrado = abrir_fichero_multiplataforma(f'{rutaArchivoCifrado}.txt', 'r')
        
        # Pedir el archivo donde se guardará el resultado de descifrado
        # Mientras el archivo sea None, la funcion abrir_fichero_multiplataforma
        # no pudo encontrarlo
        archivoResultado = None
        while(not archivoResultado):
            rutaArchivoResultado = input("¿En qué archivo quieres guardar el texto descifrado?(sin extensión) ")
            archivoResultado = abrir_fichero_multiplataforma(f'{rutaArchivoResultado}.txt', 'w')
        
        # Pedir el archivo que contiene el diccionario
        listaDiccionario = []
        # Mientras la lista esté vacía, es que no se ha podido encontrar el 
        # archivo que escribió el usuario
        while(not listaDiccionario):
            archivoDiccionario = input("¿Cuál es el archivo con el diccionario?(sin extensión) ")
            # Extraer del archivo diccionario, la lista de palabras
            listaDiccionario = procesar(f'{archivoDiccionario}.txt')
            
        # Pedir el porcentaje para buscar claves alternativas, comprobando que
        # sea un flotante entre 0 y 1
        porcentaje = 1
        while(True):
            if(esFlotanteAdecuado(porcentaje = input('¿Qué porcentaje de coincidencias quieres utilizar para las soluciones alternativas? (ENTRE 0 Y 1) '))):
                break
        
        # Preguntar si desea la opción rápida de descifrado
        opcionRapido = input('¿Quieres hacer un descifrado con la opcion rapido?(S/N)').lower()
        # validación de input con regex para opcion rápido solo valido S o N como respuesta
        modelo_regex_valid = re.compile(r'[s|n]')
        while modelo_regex_valid.fullmatch(opcionRapido) == None:
            print('ERROR: Debes responder S(sí) o N(no)')
        
        # si se elige la opcion rápido pedir minimo y máximo para subccadneas
        minPalabra = 0
        maxPalabra = 0
        
        if(opcionRapido == 's'):
            while True:
                try:
                    # el tamaño minimo para las palabras debe ser 1
                    while(minPalabra <= 0):
                        minPalabra = int(input('¿Qué tamaño minimo quieres para comprobar palabras? (MAYOR A 0)'))
                    
                    # el tamamño máximo para las palabras debe ser mayor que el mínimo
                    while(maxPalabra <= minPalabra):
                        maxPalabra = int(input('¿Qué tamaño máximo quieres para comprobar palabras? (MAYOR AL MINIMO)'))
                    
                    break
                
                except ValueError:
                    # si se inserta algo que no sea número da error
                    print("ERROR: Debes insertar un número. ")
            
        
        descifrar_fuerza_bruta_dic(archivoCifrado, archivoResultado, listaDiccionario, porcentaje,False, minPalabra, maxPalabra)
    elif opcion == 5:
        break







#Esto de aquí es para probar según el profe
if __name__ == "__main__":
    lista_palabras_castellano = procesar("Diccionario.txt")
    # print(lista_palabras)

    print(max_palabra(lista_palabras_castellano))

    

    texto_plano('test.txt')

    texto_cifrado = cifrar('test.txt', 'test_cifrado.txt')

    #texto_descifrado = descifra('test_cifrado.txt', 'test_candidato.txt', 10)

    descifrar_fuerza_bruta('test_cifrado.txt', 'test_resultado_.txt')