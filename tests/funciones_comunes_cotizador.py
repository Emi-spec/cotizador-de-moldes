from . import (pytest, Callable, RegistroDeCosto, cotizador, Material, ManoDeObra)

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def crearDireccionDeArchivoInexistente(tmpdir, nombre_archivo:str) -> str:
    archivo = tmpdir / nombre_archivo

    return archivo

def crearArchivoConRegistrosAnteriores(tmpdir, nombre_archivo:str, registros_anteriores:list[RegistroDeCosto]):
    contenido_archivo = pasarListaRegistrosATexto(registros_anteriores)

    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido_archivo)

    return archivo

def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = crearDireccionDeArchivoInexistente(tmpdir, nombre_archivo)

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def extraerSoloRegistros(lineas_archivo:list[str]):

    linea_registros:list[str] = []

    for linea in lineas_archivo[:-1]: 
        linea_registros.append(linea[:-1])

    linea_registros.append(lineas_archivo[-1])

    return linea_registros

def verificarSaltosDeLineaCorrectos(lineas_archivo:list[str]):
    for linea in lineas_archivo[:-1]:
        assert linea[-1:] == "\n"

    assert lineas_archivo[-1][-1:] != "\n"

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):

    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    # registros_esperados:list[str] = []

    # for linea in contenido_esperado[:-1]: 
    #     registros_esperados.append(linea[:-2])

    # registros_esperados.append(contenido_esperado[-1])
    #breakpoint()
    #chequeo de correctamente identado(?)
    verificarSaltosDeLineaCorrectos(lineas_archivo)

    registros_archivo = extraerSoloRegistros(lineas_archivo)
    registros_esperados = extraerSoloRegistros(contenido_esperado)

    for registro in registros_archivo:
        assert registro in registros_esperados

    assert len(registros_archivo) == len(registros_esperados)

    # assert lineas_archivo == contenido_esperado

def pasarListaRegistrosATexto(lista_registros:list[RegistroDeCosto]) -> str:
    contenido_archivo_esperado:str = ""
    
    if(lista_registros != []):
        primer_registro:RegistroDeCosto = lista_registros[0]

        if(primer_registro.esMaterial()):
            contenido_archivo_esperado += f"{primer_registro.nombre},{primer_registro.densidad_str()},{primer_registro.precio_str()}"
        if(primer_registro.esManoDeObra()):
            contenido_archivo_esperado += f"{primer_registro.nombre},{primer_registro.precio}"


        for registro in lista_registros[1:]:
            if(registro.esMaterial()):
                contenido_archivo_esperado +=(f"\n{registro.nombre},{registro.densidad},{registro.precio}")
            if(registro.esManoDeObra()):
                contenido_archivo_esperado += (f"\n{registro.nombre},{registro.precio}")

    return contenido_archivo_esperado

def pasarListaRegistrosALineasParaArchivo(lista_registros:list[RegistroDeCosto]) -> list[str]:
    lineas_archivo_esperadas:list[str] = []
    #breakpoint()
    if(lista_registros != []):
        ultimo_registro:RegistroDeCosto = lista_registros[-1]

        for registro in lista_registros[:-1]:
            if(registro.esMaterial()):
                lineas_archivo_esperadas.append(f"{registro.nombre},{registro.densidad},{registro.precio}\n")
            if(registro.esManoDeObra()):
                lineas_archivo_esperadas.append(f"{registro.nombre},{registro.precio}\n")

        if(ultimo_registro.esMaterial()):
            lineas_archivo_esperadas.append(f"{ultimo_registro.nombre},{ultimo_registro.densidad_str()},{ultimo_registro.precio_str()}")
        if(ultimo_registro.esManoDeObra()):
            lineas_archivo_esperadas.append(f"{ultimo_registro.nombre},{ultimo_registro.precio}")
    
    return lineas_archivo_esperadas

#test data
mano_de_obra_aceptada:ManoDeObra = ManoDeObra("35")

lista_registros_aceptada:list[RegistroDeCosto] = [Material("Aluminio 7075", "2.8", "23.50"),
                                                  Material("Aluminio 5083", "3", "4.5"), 
                                                  Material("Acero Amutit", "8", "7.5"),
                                                  mano_de_obra_aceptada,
                                                  Material("Acero Especial K", 8, 11)]

lista_materiales_aceptada:list[Material] = [reg for reg in lista_registros_aceptada if reg.esMaterial()]


#COTIZADOR ORIGINAL

#probablemente sea mejor reformularlo y chequearlo con cotizaciones ya hechas de una vez 

# def verificar_clave(elemento:str, claves:list[str]) -> str: #sensible a mayúsculas y minúsculas
#     while not(elemento in claves):
#         elemento = input("Solo puede colocar una de las siguientes letras "+crear_str_opciones(claves)+". Intente de nuevo: ") #arreglar 
#     return elemento

# def is_valid_float(element: str) -> bool: #para que no reviente todo si no ingresan números en el input
#     try:
#         float(element)
#         return True
#     except ValueError:
#         return False

# def verificar_int(element):
#     while element.isdigit() == False:
#         element = input("Debe ingresar un número entero positivo. Ingrese de nuevo: ")
#     element = int(element)
#     return element

# def verificar_sino(element: str) -> str:
#     element = element.lower()
#     while element != "si" and element != "no" and element !="s" and element != "n":  
#         element = input("Solo puede colocar si o no. Intente de nuevo: ")
#         element = element.lower()
#     return element

# def verificar_num (element: float) -> float:
#     element = element.replace(",",".") 
    
#     while is_valid_float(element) == False: 
#         element = input("No ha ingresado un número. Intente de nuevo: ")
#         element = element.replace(",",".") 

#     element = float(element)
    
#     if element<0: 
#         print("El número ingresado se cambió a positivo")
#         element *= -1
#     return element

# def crear_lista_claves(Aluminio_5083:bool, M:bool) -> list[str]: #requisito: el diccionario debe tener siempre clave a(Aluminio 5083) y M. 

#     lista_claves:list[str]= []

#     for clave in dic_materiales.keys():
#         lista_claves.append(clave)
    
#     if Aluminio_5083 == False:  
#         lista_claves.remove("a")
    
#     if M == False:
#         lista_claves.remove("M")
#     return lista_claves

# def crear_str_opciones(lista_opciones:list[str]) -> str:
#     str_opciones:str = "("
#     for i in range(len(lista_opciones)):
#         if i == len(lista_opciones)-1:
#             str_opciones = str_opciones+lista_opciones[i]
#         else:
#             str_opciones = str_opciones+lista_opciones[i]+"/"
#     str_opciones = str_opciones+")"
#     return str_opciones



# def cotizador_original(n_moldes:str, n_cavidades:str, dic_materiales:dict[str, float], mascaras_troqueles:str, 
#                        altura:float, volumen:float, dist_entre_centros:float, ancho_mitad:float, dificultad:str,
#                        mat_post_cuerpo:str, mat_post_cuello:str, mat_post_fondo:str, mat_placas_respaldo:str, mat_post_prensa:str):
#         #COMIENZO DE INTERROGATORIO

#     #n_moldes:int = input("\n-Cantidad de moldes a cotizar:\n") 
#     if (n_moldes != "1" and n_moldes != "2"):
#         raise ValueError("n_moldes debe ser 1 o 2 (en str)")
#     #     n_moldes = input("Solo puede ingresar 1 o 2. Ingrese de nuevo: ")
#     n_moldes = int(n_moldes)

#     #n_cavidades:int = input("\n-Cantidad de cavidades del molde:\n")
#     n_cavidades = verificar_int(n_cavidades)

#     if (n_cavidades<1 or n_cavidades>10):
#         raise ValueError("n_cavidades debe ser un numero entre 1 y 10 en str")
#     #     n_cavidades = input("Debe ingresar un número entero del 1 al 10. Ingrese de nuevo: ")
#     #     n_cavidades = verificar_int(n_cavidades)

#     #Mascaras y troqueles
#     #mascaras_troqueles:str = input("\n-¿Incluye máscaras de transporte y troqueles? (si/no):\n") 
#     mascaras_troqueles = verificar_sino(mascaras_troqueles)

#     cav_al:dict[int,tuple[int,float]] = {1:(20,3),2:(36,5.5),3:(50,8),4:(64,10),5:(75,12),6:(84,14),7:(90,16),8:(96,18),
#                                         9:(99,20),10:(110,22)}

#     horas_mas_troq:float = 0
#     costo_al_5083:float = 0

#     if mascaras_troqueles == "si" or mascaras_troqueles == "s":
#         tupla_selec:tuple[int,float] = cav_al[n_cavidades]
#         horas_mas_troq = tupla_selec[0]
#         costo_al_5083 = tupla_selec[1] * dic_materiales["a"][2]

#     #características del molde
#     #altura:float = input("\n-Altura del envase (mm):\n")
#     altura = verificar_num (altura)

#     #volumen:float = input("\n-Volumen del envase (mm):\n")
#     volumen = verificar_num(volumen)

#     #dist_entre_centros:float = input("\n-Distancia entre centros que hay entre cavidades: (mm)\n")
#     dist_entre_centros = verificar_num (dist_entre_centros)
        
#     #ancho_mitad:float = input("\n-Ancho por mitad del molde (mm):\n")
#     ancho_mitad = verificar_num (ancho_mitad)


#     # dificultad:str = input ('''\n-Nivel de dificultad del envase:
#     # a)Bajo\t\t(cilíndricos - con rosca o snap)
#     # b)Medio\t\t(elípticos, rectangulares - con rosca o snap)
#     # c)Alto\t\t(asimétricos - rosca, rosca con trinquete o snap)
#     # d)Muy alto\t(asimétricos,L/C no plana, grabados en cavidad, encastre para tapa contorneado)
#     # e)Especiales\t(asimétricos, con asa, con postizos de pinch off)\n''')
#     dificultad = verificar_clave(dificultad, ["a","b","c","d","e"])

#     #horas de trabajo

#     #tabla de horas

#     horas_cavidades:dict[int,int] = {1:70,2:120,3:165,4:205,5:243,6:281,7:318,8:355,9:392,10:429}
#     horas:int = horas_cavidades[n_cavidades]

#     if n_moldes == 2: 
#         horas *= 1.92

#     #dificultad
#     coeficiente:int = 0

#     if dificultad == "a":
#         coeficiente = 1
#     elif dificultad == "b":
#         coeficiente = 1.12
#     elif dificultad == "c":                         
#         coeficiente = 1.25
#     elif dificultad == "d": 
#         coeficiente = 1.35
#     else: 
#         coeficiente = 1.48

#     #horas extra por altura
#     horas_alt:float = ((altura - 100) / 450) +1 #FALTAN POSIBLES CAMBIOS

#     #cubicaje
#     cubicaje:float = 0

#     if volumen >= 100:
#         cubicaje = (volumen/500 * 0.1) + 1
#     else:
#         cubicaje = 1

#     #total horas
#     horas = round((horas + horas_mas_troq) * coeficiente * horas_alt * cubicaje) #POR CONSIGUIENTE, CAMBIAR ACÁ

#     #postizos, materiales y esas cosas
#     lista_claves_sinM:list[str] = crear_lista_claves(True,False)
#     str_opciones_sinM:str =crear_str_opciones(lista_claves_sinM)

#     lista_mat_costos:list[tuple[str,float]] = []

#     #print("\n\nIngrese el material a utilizar:")
#     #imprimir_letras_mat()

#     #mat_post_cuerpo:str = input("-Postizos de cuerpo"+str_opciones_sinM+":\n")
#     mat_post_cuerpo = verificar_clave(mat_post_cuerpo, lista_claves_sinM) 

#     precio_post_cuerpo:float = ((dist_entre_centros * n_cavidades) + 60) * (altura - 25) * 58 * 0.000001 * 2 * dic_materiales[mat_post_cuerpo][1] * dic_materiales[mat_post_cuerpo][2] * 1.1 

#     lista_mat_costos.append((mat_post_cuerpo,precio_post_cuerpo))


#     #mat_post_cuello:str = input("\n-Postizos de cuello"+str_opciones_sinM+":\n") 
#     mat_post_cuello = verificar_clave(mat_post_cuello, lista_claves_sinM) 

#     precio_post_cuello:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * dic_materiales[mat_post_cuello][1] * dic_materiales[mat_post_cuello][2]

#     lista_mat_costos.append((mat_post_cuello,precio_post_cuello))


#     #mat_post_fondo:str = input("\n-Postizos de fondo"+str_opciones_sinM+":\n")
#     mat_post_fondo = verificar_clave(mat_post_fondo, lista_claves_sinM)

#     precio_post_fondo:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * dic_materiales[mat_post_fondo][1] * dic_materiales[mat_post_fondo][2] 

#     lista_mat_costos.append((mat_post_fondo,precio_post_fondo))


#     #mat_placas_respaldo:str = input("\n-Placas de respaldo"+str_opciones_sinM+"\n")
#     mat_placas_respaldo = verificar_clave(mat_placas_respaldo, lista_claves_sinM) 

#     precio_placas_respaldo:float = ((dist_entre_centros * n_cavidades) + 60) * (altura + 65) * (ancho_mitad - 58) * 0.000001 * 2 * dic_materiales[mat_placas_respaldo][1] * dic_materiales[mat_placas_respaldo][2] * 1.1

#     lista_mat_costos.append((mat_placas_respaldo,precio_placas_respaldo))


#     #mat_post_prensa:str = input("\n-Postizo prensamangas"+str_opciones_sinM+"\n")
#     mat_post_prensa = verificar_clave(mat_post_prensa, lista_claves_sinM) 

#     precio_post_prensa:float = ((dist_entre_centros * n_cavidades) + 60) * 58 * 35 * 0.000001 * 2 * dic_materiales[mat_post_prensa][1] * dic_materiales[mat_post_prensa][2] * 1.1

#     lista_mat_costos.append((mat_post_prensa,precio_post_prensa))


#     costo_mat:float = precio_post_cuerpo + precio_post_cuello + precio_post_fondo + precio_placas_respaldo + precio_post_prensa

#     #costo de cada material

#     dic_costos_mat:dict[str,float] = {} #diccionario que solo contiene los precios de materiales utilizados

#     for tupla in lista_mat_costos:
#         if tupla[0] in dic_costos_mat.keys():
#             dic_costos_mat[tupla[0]] += tupla[1]
#         else:
#             dic_costos_mat[tupla[0]] = tupla[1]

#     #gastos varios 
#     if n_cavidades == 1:
#         gastos_var = 200
#     else: 
#         gastos_var = 300 + 50 * (n_cavidades - 2)

#     if n_moldes == 2:
#         gastos_var *= 2

#     costo_total = costo_mat + gastos_var

#     #precio estimado
#     mano_obra:float = horas * dic_materiales["M"][2]
#     precio:float = round(mano_obra + costo_total) 

#     #IMPRESIÓN FINAL
        
#     info_a_imprimir:str = f'''COSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n
#     Costos de cada material (total: {costo_mat:.2f} US$): \n'''

#     #print(f"\n\n\nCOSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n") 
#     #print(f"Costos de cada material (total: {costo_mat:.2f} US$): \n")

#     #costos de cada material

#     for clave,costo in dic_costos_mat.items():
#         #print(dic_materiales[clave][0]+f": {costo:.2f} US$")
#         info_a_imprimir = info_a_imprimir+dic_materiales[clave][0]+f": {costo:.2f} US$\n"

#     #print(f"\nElementos STD, tornillería, o'rings, etc: {gastos_var} US$")

#     #print(f"\nHORAS DE TRABAJO: {horas}hs\n")
#     #print(f"PRECIO TOTAL: {precio} US$\n")

#     info_a_imprimir = info_a_imprimir+f'''\nElementos STD, tornilleria, o'rings, etc: {gastos_var} US$\n
#     HORAS DE TRABAJO: {horas}hs\n
#     PRECIO TOTAL: {precio} US$\n'''

#     return infor_a_imprimir