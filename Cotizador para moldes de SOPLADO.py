def is_valid_float(element: str) -> bool: #para que no reviente todo si no ingresan números en el input
    try:
        float(element)
        return True
    except ValueError:
        return False

def verificar_int(element):
    while element.isdigit() == False:
        element = input("Debe ingresar un número entero positivo. Ingrese de nuevo: ")
    element = int(element)
    return element

def verificar_num (element: str):
    element = element.replace(",",".") 
    
    while is_valid_float(element) == False: 
        element = input("No ha ingresado un número. Intente de nuevo: ")
    element = float(element)
    
    if element<0: 
        print("El número ingresado se cambió a positivo")
        element *= -1
    return element

def verificar_claves (letra: str, condicion):
    if condicion == "todo":
        claves_mat = "abcdefghm"

    elif condicion == "abcde":
        claves_mat = "abcde"

    elif condicion == "sinM":
        claves_mat = "abcdefg"

    elif condicion == "conH":
        claves_mat = "abcdefgh"
  
    while True: 
        if letra in claves_mat:
            return letra
        else:
            letra = input("Solo puede colocar una de letras indicadas. Ingrese otra vez: ")

def verificar_sino(element: str):
    element = element.lower()
    while element != "si" and element != "no" and element !="s" and element != "n":
        element = input("Solo puede colocar si o no. Intente de nuevo: ")
    return element

def designar_densidad(element):  
    if element == "e" or element == "f" or element == "g":
        densidad_mat = 2.8
    elif element == "a" or element == "b" or element == "c" or element == "d":
        densidad_mat = 8
    else:
        densidad_mat = 9

    return densidad_mat

print("PROGRAMA DE COTIZACIÓN PARA MOLDES DE SOPLADO\n____________________\n")
print("""a)Valor del acero Amutit: 7,50 US$
b)Valor del acero Especial K: 11 US$
c)Valor del acero Inoxidable: 16 US$
d)Valor del acero SAE 4140: 6 US$

e)Valor del aluminio 5083: 19 US$
f)Valor del aluminio 6061: 21,50 US$
g)Valor del aluminio 7075: 23,50 US$

h)Valor del cobre Berilio: 110 US$

m)Valor de hora para molde soplado: 35 US$

""")
precios_materiales = {"a":7.50, "b":11, "c":16, "d":6, "e":19, "f":21.50, "g":23.50, "h":110, "m":35} 

cambioSiNo = input("-¿Desea actualizar los precios? (si/no):\n")
cambioSiNo = verificar_sino(cambioSiNo)

while cambioSiNo == "si" or cambioSiNo == "s":
    cambioMaterial = input("¿Qué precio desea actualizar?(a/b/c/d/e/f/g/h/m):\n") 
    cambioMaterial = verificar_claves(cambioMaterial, "todo") #condicion: todo

    precioCambiado = input("que precio desea colocar: ")
    precioCambiado = verificar_num(precioCambiado)
    precios_materiales[cambioMaterial] = precioCambiado

    cambioSiNo = input("¿Desea cambiar otro precio?: ")
    cambioSiNo = verificar_sino(cambioSiNo)

n_moldes = input("\n-Cantidad de moldes a cotizar:\n") 
while n_moldes != "1" and n_moldes != "2":
    n_moldes = input("Solo puede ingresar 1 o 2. Ingrese de nuevo: ")
n_moldes = int(n_moldes)

n_cavidades = input("\n-Cantidad de cavidades del molde:\n")
n_cavidades = verificar_int(n_cavidades)

while n_cavidades<1 or n_cavidades>10:
    n_cavidades = input("Debe ingresar un número entero del 1 al 10. Ingrese de nuevo: ")
    n_cavidades = verificar_int(n_cavidades)

#Mascaras y troqueles
mascaras_troqueles = input("\n-¿Incluye máscaras de transporte y troqueles? (si/no):\n") 
mascaras_troqueles = verificar_sino(mascaras_troqueles)

cav_al = {1:(20,3),2:(36,5.5),3:(50,8),4:(64,10),5:(75,12),6:(84,14),7:(90,16),8:(96,18),9:(99,20),10:(110,22)}

horas_mas_troq = 0
costo_al_5083 = 0

if mascaras_troqueles == "si" or mascaras_troqueles == "s":
    lista_selec = cav_al[n_cavidades]
    horas_mas_troq = lista_selec[0]
    costo_al_5083 = lista_selec[1] * precios_materiales["a"]
    
#características del molde
altura = input("\n-Altura del envase (mm):\n")
altura = verificar_num (altura)

volumen = input("\n-Volumen del envase (mm):\n")
volumen = verificar_num(volumen)

dist_entre_centros = input("\n-Distancia entre centros que hay entre cavidades: (mm)\n")
dist_entre_centros = verificar_num (dist_entre_centros)
    
ancho_mitad = input("\n-Ancho por mitad del molde (mm):\n")
ancho_mitad = verificar_num (ancho_mitad)


dificultad = input ("\n-Nivel de dificultad del envase:\na)Bajo\t\t(cilíndricos - con rosca o snap)\nb)Medio\t\t(elípticos, rectangulares - con rosca o snap)\nc)Alto\t\t(asimétricos - rosca, rosca con trinquete o snap)\nd)Muy alto\t(asimétricos,L/C no plana, grabados en cavidad, encastre para tapa contorneado)\ne)Especiales\t(asimétricos, con asa, con postizos de pinch off)\n")
dificultad = verificar_claves(dificultad, "abcde") #condicion:abcde

#horas de trabajo

#tabla de horas

horas_cavidades = {1:70,2:120,3:165,4:205,5:243,6:281,7:318,8:355,9:392,10:429}
horas = horas_cavidades[n_cavidades]

if n_moldes == 2: 
    horas *= 1.92

#dificultad
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
horas_alt = ((altura - 100) / 450) +1 #FALTAN POSIBLES CAMBIOS

#cubicaje
if volumen >= 100:
    cubicaje = (volumen/500 * 0.1) + 1
else:
  cubicaje = 1

#total horas
horas = round((horas + horas_mas_troq) * coeficiente * horas_alt * cubicaje) #POR CONSIGUIENTE, CAMBIAR ACÁ

#postizos, materiales y esas cosas
print("""\n\nIngrese el material a utilizar:
a)acero Amutit
b)acero Especial K
c)acero inoxidable
d)acero SAE 4140

e)aluminio 5083
f)aluminio 6061
g)aluminio 7075

h)cobre berilio
""")
mat_post_cuerpo = input("\n-Postizos de cuerpo (a/b/c/d/e/f/g):\n")
mat_post_cuerpo = verificar_claves(mat_post_cuerpo, "sinM") 

precio_post_cuerpo = ((dist_entre_centros * n_cavidades) + 60) * (altura - 25) * 58 * 0.000001 * 2 * designar_densidad(mat_post_cuerpo) * precios_materiales[mat_post_cuerpo] * 1.1 

mat_post_cuello = input("\n-Postizos de cuello (a/b/c/d/e/f/g/h):\n") #cobre berilio solo
mat_post_cuello = verificar_claves(mat_post_cuello, "conH") 

precio_post_cuello = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * designar_densidad(mat_post_cuello) * precios_materiales[mat_post_cuello] 

mat_post_fondo = input("\n-Postizos de fondo (a/b/c/d/e/f/g):\n")
mat_post_fondo = verificar_claves(mat_post_fondo, "sinM")

precio_post_fondo = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * designar_densidad(mat_post_fondo) * precios_materiales[mat_post_fondo] 


mat_placas_respaldo = input("\n-Placas de respaldo (a/b/c/d/e/f/g):\n")
mat_placas_respaldo = verificar_claves(mat_placas_respaldo, "sinM") 

precio_placas_respaldo = ((dist_entre_centros * n_cavidades) + 60) * (altura + 65) * (ancho_mitad - 58) * 0.000001 * 2 * designar_densidad(mat_placas_respaldo) * precios_materiales[mat_placas_respaldo] * 1.1


mat_post_prensa = input("\n-Postizo prensamangas (a/b/c/d/e/f/g):\n")
mat_post_prensa = verificar_claves(mat_post_prensa, "sinM") 

precio_post_prensa = ((dist_entre_centros * n_cavidades) + 60) * 58 * 35 * 0.000001 * 2 * designar_densidad(mat_post_prensa) * precios_materiales[mat_post_prensa] * 1.1

costo_mat = precio_post_cuerpo + precio_post_cuello + precio_post_fondo + precio_placas_respaldo + precio_post_prensa

#costo de cada material
mat_precio = [mat_post_cuerpo,precio_post_cuerpo,mat_post_cuello,precio_post_cuello,mat_post_fondo,precio_post_fondo,mat_placas_respaldo,precio_placas_respaldo,mat_post_prensa,precio_post_prensa]

costo_ac_amutit = 0
costo_ac_especialk = 0
costo_ac_inox = 0
costo_ac_SAE = 0
#costo_al_5083 ya está arriba
costo_al_7075 = 0
costo_al_6061 = 0
costo_cob_berilio = 0


for index,item in enumerate(mat_precio):
    if item == "a":
        costo_ac_amutit += mat_precio[index+1] 
    elif item == "b":
        costo_ac_especialk += mat_precio[index+1]
    elif item == "c":
        costo_ac_inox += mat_precio[index+1]
    elif item == "d":
        costo_ac_SAE += mat_precio[index+1]
    elif item == "e":
        costo_al_5083 += mat_precio[index+1] 
    elif item == "f":
        costo_al_6061 += mat_precio[index+1] 
    elif item == "g":
        costo_al_7075 += mat_precio[index+1] 
    elif item == "h":
        costo_cob_berilio += mat_precio[index+1] 

#gastos varios 
if n_cavidades == 1:
    gastos_var = 200
else: 
    gastos_var = 300 + 50 * (n_cavidades - 2)

if n_moldes == 2:
    gastos_var *= 2

costo_total = costo_mat + gastos_var

#precio estimado
mano_obra = horas * precios_materiales["m"]
precio = round(mano_obra + costo_total) 
    
print(f"\n\n\nCOSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n") 
print(f"Costos de cada material (total: {costo_mat:.2f} US$): \n")

if costo_ac_amutit != 0:
    print(f"acero Amutit: {costo_ac_amutit} US$")

if costo_ac_especialk != 0:
    print(f"acero Especial K: {costo_ac_especialk} US$")

if costo_ac_inox != 0:
    print(f"acero inoxidable: {costo_ac_inox:.2f} US$")

if costo_ac_SAE != 0:
    print(f"acero SAE 4140: {costo_ac_SAE:.2f}")

if costo_al_5083 != 0:
    print(f"aluminio 5083: {costo_al_5083:.2f} US$")

if costo_al_6061 != 0:
    print(f"aluminio 6061: {costo_al_6061:.2f} US$")

if costo_al_7075 != 0:
    print(f"aluminio 7075: {costo_al_7075:.2f} US$")

if costo_cob_berilio != 0:
    print(f"cobre Berilio: {costo_cob_berilio} US$")

print(f"\nElementos STD, tornillería, o'rings, etc: {gastos_var} US$")

print(f"\nHORAS DE TRABAJO: {horas}hs\n")
print(f"PRECIO TOTAL: {precio} US$\n")
respuesta = input("Presione enter para finalizar\n")
