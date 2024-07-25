def is_valid_float(element: str) -> bool: #para que no reviente todo si no ingresan números en el input
    try:
        float(element)
        return True
    except ValueError:
        return False

def verificar_num (element: float|str) -> float:
    element = element.replace(",",".") 
    
    while is_valid_float(element) == False: 
        element = input("No ha ingresado un número. Intente de nuevo: ")
        element = element.replace(",",".") 

    element = float(element)
    
    if element<0: 
        print("El número ingresado se cambió a positivo")
        element *= -1
    return element

def verificar_int(element):
    while element.isdigit() == False:
        element = input("Debe ingresar un número entero positivo. Ingrese de nuevo: ")
    element = int(element)
    return element

def verificar_sino(element: str) -> str:
    element = element.lower()
    while element != "si" and element != "no" and element !="s" and element != "n":  
        element = input("Solo puede colocar si o no. Intente de nuevo: ")
        element = element.lower()
    return element

def crear_lista_claves(Aluminio_5083:bool, M:bool) -> list[str]: #requisito: el diccionario debe tener siempre clave a(Aluminio 5083) y M. 

    lista_claves:list[str]= []

    for clave in dic_materiales.keys():
        lista_claves.append(clave)
    
    if Aluminio_5083 == False:  
        lista_claves.remove("a")
    
    if M == False:
        lista_claves.remove("M")
    return lista_claves

def crear_str_opciones(lista_opciones:list[str]) -> str:
    str_opciones:str = "("
    for i in range(len(lista_opciones)):
        if i == len(lista_opciones)-1:
            str_opciones = str_opciones+lista_opciones[i]
        else:
            str_opciones = str_opciones+lista_opciones[i]+"/"
    str_opciones = str_opciones+")"
    return str_opciones

def verificar_clave(elemento:str, claves:list[str]) -> str: #sensible a mayúsculas y minúsculas
    while not(elemento in claves):
        elemento = input("Solo puede colocar una de las siguientes letras "+crear_str_opciones(claves)+". Intente de nuevo: ") #arreglar 
    return elemento

def imprimir_letras_mat():
    for letra,tupla in dic_materiales.items():
        if letra != "M":
            print(letra+") "+tupla[0])
    print("")



#COMIENZO PROGRAMA

print("____________________\n\nPROGRAMA DE COTIZACIÓN PARA MOLDES DE SOPLADO\n____________________\n")
try:
    archivo_precios = open("precios.txt","r")
    archivo_precios.close()
except OSError:
    archivo_precios_w = open("precios.txt","w")
    print("No existe un registro de materiales y precios para iniciar la cotización. Usted está por crear uno.")
    
    agregar:str = "si"
    precios_para_archivo:str = ""
    precios_para_mostrar:list[tuple[str,str,str]]= []
    char:int = 98

    #Aluminio 5083 elemento obligatorio (para mascaras y troqueles)
    precio_aluminio_5083:float|str = input("Ingrese el precio del Aluminio 5083 (elemento obligatorio para máscaras y troqueles): ") 
    precio_aluminio_5083 = verificar_num(precio_aluminio_5083)
    precios_para_archivo ="a,Aluminio 5083,2.8,"+str(precio_aluminio_5083)+"\n"
    precios_para_mostrar.append(("Aluminio 5083","2.8",str(precio_aluminio_5083)))

    while ((agregar == "si" or agregar =="s") and char<122): #Si se ingresa mas materiales que letras(-1) del abecedario se rompe
        material:str = input("Ingrese el nombre de un material: ")
        densidad:str = input("Ingrese su densidad (Kg/dm3): ")
        densidad = str(verificar_num(densidad))
        precio:str = input("Ingrese su precio (US$): ")
        precio = str(verificar_num (precio)) 

        precios_para_archivo = precios_para_archivo+chr(char)+","+material+","+densidad+","+precio+"\n"
        precios_para_mostrar.append((material,densidad,precio))
        print("--------")
        for e in precios_para_mostrar:
            print(e[0]+":",e[1],"g/cm3 y",e[2],"US$")
        print("\nPuede ingresar hasta 26 materiales") #porque si no se me terminan las letras del abecedario gringo 
        print("--------")    
        char += 1
        agregar = input("Desea agregar otro material? ")
        agregar = verificar_sino(agregar)
    
    mano_obra:str = input("Ingrese el valor de hora para molde soplado (US$):  ")
    mano_obra = str(verificar_num(mano_obra)) 
    precios_para_archivo = precios_para_archivo+"M"+",mano de obra,0,"+mano_obra+"\n"

    archivo_precios_w.write(precios_para_archivo)
    archivo_precios_w.close()
    print("\n")

archivo_precios = open("precios.txt","r")
lineas_archivo:list[str] = archivo_precios.readlines()
archivo_precios.close() #CERRE EL ARCHIVO

dic_materiales:dict[str,tuple[str,float|str,float|str]] = {}

for linea in lineas_archivo: #requisito que el archivo tenga todo escrito de la forma "a,material,densidad,precio\n" para que funcione
    letra:str = ""
    cant_comas:int = 0
    material:str = ""
    precio:str = ""
    densidad:str = ""

    for i in range(len(linea)):
        if linea[i] ==",":
            cant_comas += 1

        elif cant_comas == 0:
            letra = letra+linea[i]

        elif cant_comas == 1: 
            material = material+linea[i]

        elif cant_comas == 2:
            densidad = densidad+linea[i]   
        
        elif cant_comas == 3 and linea[i]!="\n":
            precio = precio+linea[i]

    dic_materiales[letra]=(material,float(densidad),float(precio))

print("REGISTRO DE MATERIALES")
for letra,tupla in dic_materiales.items(): #presenta la en la posicion donde estaba en el diccionario 
    if letra == "M":
        print("\nM) Valor de hora para molde soplado:   ",tupla[2],"US$")
    else:    
        print(letra+") Valor del",tupla[0]+":   "+str(tupla[2]),"US$")
print("____________________\n")

#PARA CAMBIAR ALGUN PRECIO/MATERIAL MAL ESCRITO/AGREGAR NUEVOS/ELIMINAR
# verificar claves debe cambiar de acuerdo a cuantos materiales haya (u opciones).  
cambioSiNo:str= input("¿Desea modificar el registro de materiales? (si/no): ")
cambioSiNo = verificar_sino(cambioSiNo)

while cambioSiNo == "si" or cambioSiNo == "s":
    #imprime los materiales, sus densidades y sus precios
    print("")
    for letra,tupla in dic_materiales.items():
        if letra != "M":
            print(letra+")",tupla[0]+":   "+str(tupla[1]),"kg/dm3   "+str(tupla[2]),"US$") 
        
    print("\nM) Valor de hora para molde soplado:   "+str(dic_materiales["M"][2])+"US$")
    
    tipoCambio:str =input('''\n¿Qué desea modificar?
a) Nombre del material
b) Precio
c) Densidad
d) Agregar un material nuevo
e) Eliminar un material\n''')
    
    tipoCambio = verificar_clave(tipoCambio,["a","b","c","d","e"])
    
    if tipoCambio == "a" or tipoCambio =="b" or tipoCambio =="c": #no se puede cambiar el nombre y densidad de M
        letra_a_cambiar:str = ""
        cambio_nombre:str = ""
        cambio_densidad:float|str = 0
        cambio_precio:float|str = 0

        if tipoCambio == "a" or tipoCambio == "c":
            letra_a_cambiar = input("¿Que material desea modificar? "+crear_str_opciones(crear_lista_claves(False,False))+": ")
            letra_a_cambiar = verificar_clave(letra_a_cambiar,crear_lista_claves(False,False))
            cambio_nombre = dic_materiales[letra_a_cambiar][0]
            cambio_densidad = dic_materiales[letra_a_cambiar][1]
            cambio_precio = dic_materiales[letra_a_cambiar][2]

            if tipoCambio =="a":
                cambio_nombre = input("¿Qué nombre desearía colocar?: ")

            elif tipoCambio == "c":
                cambio_densidad = input("¿Qué densidad desearía colocar? (kg/dm3): ")
                cambio_densidad = verificar_num(cambio_densidad)

        
        else: #se puede cambiar el precio de M 
            letra_a_cambiar = input("¿Que precio desea modificar? "+crear_str_opciones(crear_lista_claves(True,True))+": ")
            letra_a_cambiar = verificar_clave(letra_a_cambiar,crear_lista_claves(True,True))
            cambio_nombre  = dic_materiales[letra_a_cambiar][0]
            cambio_densidad = dic_materiales[letra_a_cambiar][1]
            cambio_precio  = dic_materiales[letra_a_cambiar][2]

            cambio_precio = input("¿Qué precio desearía colocar? (US$): ")
            cambio_precio = verificar_num(cambio_precio)

        dic_materiales[letra_a_cambiar] = (cambio_nombre,cambio_densidad,cambio_precio)
    
    elif tipoCambio == "d":
        #se busca la clave de mayor ord
        letra_max_ord:str = "a"
        for clave in dic_materiales.keys():
            if  ord(letra_max_ord) < ord(clave):
                letra_max_ord = clave 

        letra_a_agregar:str = chr(ord(letra_max_ord)+1)        
        
        nombre_a_agregar:str = input("Ingrese el nombre del nuevo material: ")
        densidad_a_agregar:float|str = input("Ingrese su densidad: ")
        densidad_a_agregar = verificar_num(densidad_a_agregar)

        precio_a_agregar:float|str = input("Ingrese su precio: ")
        precio_a_agregar = verificar_num(precio_a_agregar)

        dic_materiales[letra_a_agregar] = (nombre_a_agregar,densidad_a_agregar,precio_a_agregar)
    
    else: 
        #IMPRIMIR LETRAS Y MATERIALES
        print("")
        imprimir_letras_mat()
        letra_a_eliminar:str = input("¿Qué material desearía eliminar?"+crear_str_opciones(crear_lista_claves(False,False))+ ": ")
        letra_a_eliminar = verificar_clave(letra_a_eliminar,crear_lista_claves(False,False))
        
        ultimo_orden:int = 97
        for letra in crear_lista_claves(False,False):
            if ord(letra) > ultimo_orden:
                ultimo_orden = ord(letra)

        if letra_a_eliminar != chr(ultimo_orden):   
            dic_materiales[letra_a_eliminar] = dic_materiales[chr(ultimo_orden)]

        del(dic_materiales[chr(ultimo_orden)])

    cambioSiNo = input("\n¿Desea modificar algo más?: ")
    cambioSiNo = (verificar_sino(cambioSiNo)).lower()

    if cambioSiNo == "no" or cambioSiNo =="n":
        lista_archivo:str = ""
        for clave,tupla in dic_materiales.items():
            if clave != "M":
                lista_archivo = lista_archivo+clave+","+tupla[0]+","+str(tupla[1])+","+str(tupla[2])+"\n"
        lista_archivo = lista_archivo+"M,"+dic_materiales["M"][0]+",0,"+str(dic_materiales["M"][2])+"\n"
        #Mano de obra no cambia la densidad ni aunque le paguen

        archivo_modificado = open("precios.txt","w")
        archivo_modificado.write(lista_archivo)
        archivo_modificado.close()

#COMIENZO DE INTERROGATORIO

n_moldes:int|str = input("\n-Cantidad de moldes a cotizar:\n") 
while n_moldes != "1" and n_moldes != "2":
    n_moldes = input("Solo puede ingresar 1 o 2. Ingrese de nuevo: ")
n_moldes = int(n_moldes)

n_cavidades:int|str = input("\n-Cantidad de cavidades del molde:\n")
n_cavidades = verificar_int(n_cavidades)

while n_cavidades<1 or n_cavidades>10:
    n_cavidades = input("Debe ingresar un número entero del 1 al 10. Ingrese de nuevo: ")
    n_cavidades = verificar_int(n_cavidades)

#Mascaras y troqueles
mascaras_troqueles:str = input("\n-¿Incluye máscaras de transporte y troqueles? (si/no):\n") 
mascaras_troqueles = verificar_sino(mascaras_troqueles)

cav_al:dict[int,tuple[int,float]] = {1:(20,3),2:(36,5.5),3:(50,8),4:(64,10),5:(75,12),6:(84,14),7:(90,16),8:(96,18),9:(99,20),10:(110,22)}

horas_mas_troq:float = 0
costo_al_5083:float = 0

if mascaras_troqueles == "si" or mascaras_troqueles == "s":
    tupla_selec:tuple[int,float] = cav_al[n_cavidades]
    horas_mas_troq = tupla_selec[0]
    costo_al_5083 = tupla_selec[1] * dic_materiales["a"][2]

#características del molde
altura:float|str = input("\n-Altura del envase (mm):\n")
altura = verificar_num (altura)

volumen:float|str = input("\n-Volumen del envase (mm):\n")
volumen = verificar_num(volumen)

dist_entre_centros:float|str = input("\n-Distancia entre centros que hay entre cavidades: (mm)\n")
dist_entre_centros = verificar_num (dist_entre_centros)
    
ancho_mitad:float|str = input("\n-Ancho por mitad del molde (mm):\n")
ancho_mitad = verificar_num (ancho_mitad)


dificultad:str = input ('''\n-Nivel de dificultad del envase:
a)Bajo\t\t(cilíndricos - con rosca o snap)
b)Medio\t\t(elípticos, rectangulares - con rosca o snap)
c)Alto\t\t(asimétricos - rosca, rosca con trinquete o snap)
d)Muy alto\t(asimétricos,L/C no plana, grabados en cavidad, encastre para tapa contorneado)
e)Especiales\t(asimétricos, con asa, con postizos de pinch off)\n''')
dificultad = verificar_clave(dificultad, ["a","b","c","d","e"])

#horas de trabajo

#tabla de horas

horas_cavidades:dict[int,int] = {1:70,2:120,3:165,4:205,5:243,6:281,7:318,8:355,9:392,10:429}
horas:int = horas_cavidades[n_cavidades]

if n_moldes == 2: 
    horas *= 1.92

#dificultad
coeficiente:int = 0

if dificultad == "a":
    coeficiente = 1
elif dificultad == "b":
    coeficiente = 1.12
elif dificultad == "c":                         
    coeficiente = 1.25
elif dificultad == "d": 
    coeficiente = 1.35
else: 
    coeficiente = 1.48

#horas extra por altura
horas_alt:float = ((altura - 100) / 450) +1 #FALTAN POSIBLES CAMBIOS

#cubicaje
cubicaje:float = 0

if volumen >= 100:
    cubicaje = (volumen/500 * 0.1) + 1
else:
  cubicaje = 1

#total horas
horas = round((horas + horas_mas_troq) * coeficiente * horas_alt * cubicaje) #POR CONSIGUIENTE, CAMBIAR ACÁ

#postizos, materiales y esas cosas
lista_claves_sinM:list[str] = crear_lista_claves(True,False)
str_opciones_sinM:str =crear_str_opciones(lista_claves_sinM)

lista_mat_costos:list[tuple[str,float]] = []

print("\n\nIngrese el material a utilizar:")
imprimir_letras_mat()

mat_post_cuerpo:str = input("-Postizos de cuerpo"+str_opciones_sinM+":\n")
mat_post_cuerpo = verificar_clave(mat_post_cuerpo, lista_claves_sinM) 

precio_post_cuerpo:float = ((dist_entre_centros * n_cavidades) + 60) * (altura - 25) * 58 * 0.000001 * 2 * dic_materiales[mat_post_cuerpo][1] * dic_materiales[mat_post_cuerpo][2] * 1.1 

lista_mat_costos.append((mat_post_cuerpo,precio_post_cuerpo))


mat_post_cuello:str = input("\n-Postizos de cuello"+str_opciones_sinM+":\n") 
mat_post_cuello = verificar_clave(mat_post_cuello, lista_claves_sinM) 

precio_post_cuello:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * dic_materiales[mat_post_cuello][1] * dic_materiales[mat_post_cuello][2]

lista_mat_costos.append((mat_post_cuello,precio_post_cuello))


mat_post_fondo:str = input("\n-Postizos de fondo"+str_opciones_sinM+":\n")
mat_post_fondo = verificar_clave(mat_post_fondo, lista_claves_sinM)

precio_post_fondo:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * dic_materiales[mat_post_fondo][1] * dic_materiales[mat_post_fondo][2] 

lista_mat_costos.append((mat_post_fondo,precio_post_fondo))


mat_placas_respaldo:str = input("\n-Placas de respaldo"+str_opciones_sinM+"\n")
mat_placas_respaldo = verificar_clave(mat_placas_respaldo, lista_claves_sinM) 

precio_placas_respaldo:float = ((dist_entre_centros * n_cavidades) + 60) * (altura + 65) * (ancho_mitad - 58) * 0.000001 * 2 * dic_materiales[mat_placas_respaldo][1] * dic_materiales[mat_placas_respaldo][2] * 1.1

lista_mat_costos.append((mat_post_cuerpo,precio_post_cuerpo))


mat_post_prensa:str = input("\n-Postizo prensamangas"+str_opciones_sinM+"\n")
mat_post_prensa = verificar_clave(mat_post_prensa, lista_claves_sinM) 

precio_post_prensa:float = ((dist_entre_centros * n_cavidades) + 60) * 58 * 35 * 0.000001 * 2 * dic_materiales[mat_post_prensa][1] * dic_materiales[mat_post_prensa][2] * 1.1

lista_mat_costos.append((mat_post_prensa,precio_post_prensa))


costo_mat:float = precio_post_cuerpo + precio_post_cuello + precio_post_fondo + precio_placas_respaldo + precio_post_prensa

#costo de cada material

#ALGUIEN QUE ME EXPLIQUE QUE ESTÁ PASANDO ACA
dic_costos_mat:dict[str,float] = {} #diccionario que solo contiene los precios de materiales utilizados

for tupla in lista_mat_costos:
    if tupla[0] in dic_costos_mat.keys():
        dic_costos_mat[tupla[0]] += tupla[1]
    else:
        dic_costos_mat[tupla[0]] = tupla[1]

#gastos varios 
if n_cavidades == 1:
    gastos_var = 200
else: 
    gastos_var = 300 + 50 * (n_cavidades - 2)

if n_moldes == 2:
    gastos_var *= 2

costo_total = costo_mat + gastos_var

#precio estimado
mano_obra:float = horas * dic_materiales["M"][2]
precio:float = round(mano_obra + costo_total) 
    
print(f"\n\n\nCOSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n") 
print(f"Costos de cada material (total: {costo_mat:.2f} US$): \n")

#IMPRESIÓN FINAL
#costos de cada material

for clave,costo in dic_costos_mat.items():
    print(dic_materiales[clave][0]+f": {costo:.2f} US$")

print(f"\nElementos STD, tornillería, o'rings, etc: {gastos_var} US$")

print(f"\nHORAS DE TRABAJO: {horas}hs\n")
print(f"PRECIO TOTAL: {precio} US$\n")
respuesta = input("Presione enter para finalizar\n")

#FALTA TEST DE QUE LAS CUENTAS ESTÁN BIEN
#los costos de los materiales a veces me dan en negativo
#FALTA HABLAR CON EL SEÑOR SOBRE COMO QUIERE QUE SE IMPRIMAN EN .TXT LOS RESULTADOS 