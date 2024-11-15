#Compia las palabras de un diccionario a un nuevo archivo "DiccionarioLimpio.txt"
#Cambia las letras que dan problemas como las vocales con acento y dieresis y las eñes
dicNormal = open("Diccionario.txt", 'r', encoding='latin-1')
dicNormal.readline()
dicNormal.readline()
dicLimpio = open("DiccionarioLimpio.txt", 'w')

while (palabra := dicNormal.readline()) != "":
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
        dicLimpio.write(palabraNueva)
dicLimpio.close()
dicNormal.close()