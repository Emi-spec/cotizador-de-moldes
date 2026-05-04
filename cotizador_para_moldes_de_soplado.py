import math

class Material:
    def __init__(self, nombre, densidad, precio):

        if not nombre: 
            raise ValueError(Material.NombreNuloDescripcionDeError(densidad, precio))
    

        self.assertDensidadValida(nombre, densidad)
        self.assertPrecioValido(nombre, precio)

        self.nombre = nombre
        self.densidad = float(densidad)      # kg/m³, por ejemplo
        self.precio = float(precio)          # precio por unidad (ej: por kg)

    def __str__(self):
        return f"{self.nombre} (densidad={self.densidad}, precio={self.precio})"
    
    # aserciones
    def assertDensidadValida(self, nombre:str, densidad:str):

        self.assertarAtributoNumericoValido(densidad, 
                                            Material.DensidadInvalidaDescripcionDeError(nombre, densidad), 
                                            Material.DensidadInvalidaDescripcionDeError(nombre, densidad)) 
        

    def assertPrecioValido(self, nombre:str, precio:str):

        self.assertarAtributoNumericoValido(precio, 
                                            Material.PrecioInvalidoDescripcionDeError(nombre, precio), 
                                            Material.PrecioInvalidoDescripcionDeError(nombre, precio) )
       
        
    def assertarAtributoNumericoValido(self, atributo_en_str:str, descripcion_error_para_no_numerico:str, descripcion_error_para_no_positivo:str):
        if not(es_float_estricto(atributo_en_str)):
            raise TypeError(descripcion_error_para_no_numerico)

        atributo_en_str = float(atributo_en_str)

        if atributo_en_str <=0:
            raise ValueError(descripcion_error_para_no_positivo)
        
    def caracteristicasSon(self, nombre_esperado:str, densidad_esperada:str, precio_esperado:str):
        return self.nombre == nombre_esperado and self.densidad == densidad_esperada and self.precio == precio_esperado

    #mensajes de error
    @staticmethod
    def NombreNuloDescripcionDeError(densidad:str, precio:str):
        return f"El nombre del material con densidad: {densidad} (Kg/dm3) y precio: ${precio} no puede estar vacío"
    
    @staticmethod
    def DensidadInvalidaDescripcionDeError(nombre:str, densidad:str):
        return f"El material {nombre} tiene una densidad inválida de: {densidad} Kg/dm3"
    
    @staticmethod
    def PrecioInvalidoDescripcionDeError(nombre:str, precio:str):
        return f"El material {nombre} tiene un precio inválido de: ${precio}"
    



def es_float_estricto(cadena):
    try:
        valor = float(cadena)
        # Comprobamos que no sea infinito ni NaN
        return math.isfinite(valor)
    except (ValueError, TypeError):
        return False


def crear_dic_materiales_a_partir_de(archivo:str) -> list[Material]:
    archivo_precios = open(archivo,"r")
    lineas_archivo:list[str] = archivo_precios.readlines()
    archivo_precios.close() #CERRE EL ARCHIVO

    lista_materiales:list[Material] = []

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
                material = material+linea[i]

            elif cant_comas == 1:
                densidad = densidad+linea[i]   
            
            elif cant_comas == 2 and linea[i]!="\n":
                precio = precio+linea[i]

        #print(f"material: {material}, densidad:{densidad}, precio: {precio}")
        lista_materiales.append(Material(material, densidad, precio))

    return lista_materiales


def crear_texto_registro_materiales(dic_materiales:dict[str,tuple[str,float,float]]) -> str:
    texto:str = "" 
    texto = texto+"REGISTRO DE MATERIALES\n"

    for letra,tupla in dic_materiales.items(): #presenta la en la posicion donde estaba en el diccionario 
        if letra == "M":
            texto = texto+"\nM) Valor de hora para molde soplado:   "+str(tupla[2])+" US$\n"
        else:    
            texto = texto+letra+") Valor del "+tupla[0]+" :   "+str(tupla[2])+" US$\n"
    
    texto+"____________________\n"

    return texto




