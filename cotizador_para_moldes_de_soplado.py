import math

def es_float_estricto(cadena) -> bool:
    try:
        valor = float(cadena)
        # Comprobamos que no sea infinito ni NaN
        return math.isfinite(valor)
    except (ValueError, TypeError):
        return False
    


class RegistroDeCosto:

    #asserciones
    def assertPrecioValido(self, precio:str):
        raise NotImplementedError(
            "Las subclases deben implementar assertPrecioValido"
        )
    
    @staticmethod
    def assertarAtributoNumericoValido(atributo_en_str:str, descripcion_error_para_no_numerico:str, descripcion_error_para_no_positivo:str):
        if not(es_float_estricto(atributo_en_str)):
            raise TypeError(descripcion_error_para_no_numerico)

        atributo_en_str = float(atributo_en_str)

        if atributo_en_str <=0:
            raise ValueError(descripcion_error_para_no_positivo)
    
        
    def tieneComoNombre(self, nombre_esperado:str):
        return self.nombre == nombre_esperado
    
    def tieneIgualNombreQue(self, otroMaterialOManoDeObra:'RegistroDeCosto'):
        raise NotImplementedError(
            "Las subclases deben implementar tieneIgualNombreQue"
        )

    def tieneIgualNombreQueMaterial(self, otroMaterial:'Material'):
        raise NotImplementedError(
            "Las subclases deben implementar tieneIgualNombreQueMaterial"
        )

    def tieneIgualNombreQueManoDeObra(self, manoDeObra:'ManoDeObra'):
        raise NotImplementedError(
            "Las subclases deben implementar tieneIgualNombreQueManoDeObra"
        )
    
    def verificarQueNoCompartaNombreCon(self, otroMaterialOManoDeObra:'RegistroDeCosto'):
        raise NotImplementedError(
            "Las subclases deben implementar verificarQueNoCompartaNombreCon"
        )
    
    #errores 
    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombre():
        raise NotImplementedError(
            "Las subclases deben implementar lanzarErrorDeRegistrosDeIgualNombre"
        )
        
    @staticmethod
    def PrecioInvalidoDescripcionDeError(precio:str):
        raise NotImplementedError(
            "Las subclases deben implementar PrecioInvalidoDescripcionDeError"
        )
    

class ManoDeObra(RegistroDeCosto):
    def __init__(self, precio):

        self.assertPrecioValido(precio)

        self.nombre = "Mano de obra"
        self.precio = float(precio)          # precio por unidad (ej: por kg)

    def __str__(self):
        return f"{self.nombre} (precio={self.precio})"
    
    #cosas
    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombre(nombre_archivo:str):
        raise ValueError(f"No puede haber dos registros de mano de obra en el archivo {nombre_archivo}")
    
    #asserciones
    def assertPrecioValido(self, precio:str):

        self.assertarAtributoNumericoValido(precio, 
                                            ManoDeObra.PrecioInvalidoDescripcionDeError(precio), 
                                            ManoDeObra.PrecioInvalidoDescripcionDeError(precio) )
    

    def caracteristicasSon(self, nombre_esperado:str, precio_esperado:str):
        return self.tieneComoNombre(nombre_esperado)  and self.precio == precio_esperado
    

    def tieneIgualNombreQue(self, otroMaterialOManoDeObra:'RegistroDeCosto'):
        return otroMaterialOManoDeObra.tieneIgualNombreQueManoDeObra(self)

    def tieneIgualNombreQueMaterial(self, otroMaterial:'Material'):
        return False

    def tieneIgualNombreQueManoDeObra(self, manoDeObra:'ManoDeObra'):
        return True

    def esManoDeObra(self):
        return True
    
    def verificarQueNoCompartaNombreCon(self, otroRegistroDeCosto:'RegistroDeCosto', archivo:str):
        if(self.tieneIgualNombreQue(otroRegistroDeCosto)):
                self.lanzarErrorDeRegistrosDeIgualNombre(archivo)

    #mensajes de error    
    @staticmethod
    def PrecioInvalidoDescripcionDeError(precio_invalido:str):
        return f"La mano de obra tiene un precio inválido de: ${precio_invalido}"


class Material(RegistroDeCosto):
    def __init__(self, nombre, densidad, precio):

        Material.assertarCaracteristicasValidas(nombre,densidad,precio)

        self.nombre = nombre
        self.densidad = float(densidad)      # kg/m³, por ejemplo
        self.precio = float(precio)          # precio por unidad (ej: por kg)

    def __str__(self):
        return f"{self.nombre} (densidad={self.densidad}, precio={self.precio})"
    
   
    # aserciones
    @staticmethod
    def assertarCaracteristicasValidas(nombre:str, densidad:str, precio:str):
        Material.assertNombreValido(nombre, densidad, precio)
        Material.assertDensidadValida(nombre, densidad)
        Material.assertPrecioValido(nombre, precio)

    @staticmethod
    def assertNombreValido(nombre:str, densidad:str, precio:str):
        if not nombre: 
            raise ValueError(Material.NombreNuloDescripcionDeError(densidad, precio))

    @staticmethod
    def assertDensidadValida(nombre:str, densidad:str):

        Material.assertarAtributoNumericoValido(densidad, 
                                        Material.DensidadInvalidaDescripcionDeError(nombre, densidad), 
                                        Material.DensidadInvalidaDescripcionDeError(nombre, densidad)) 
        
    @staticmethod
    def assertPrecioValido(nombre:str, precio:str):

        Material.assertarAtributoNumericoValido(precio, 
                                        Material.PrecioInvalidoDescripcionDeError(nombre, precio), 
                                        Material.PrecioInvalidoDescripcionDeError(nombre, precio) )
        
    def verificarQueNoCompartaNombreCon(self, otroRegistroDeCosto:'RegistroDeCosto', archivo:str):
        if(self.tieneIgualNombreQue(otroRegistroDeCosto)):
                self.lanzarErrorDeRegistrosDeIgualNombre(self.nombre, archivo)
       
    def caracteristicasSon(self, nombre_esperado:str, densidad_esperada:str, precio_esperado:str):
        return self.tieneComoNombre(nombre_esperado) and self.densidad == densidad_esperada and self.precio == precio_esperado

    def tieneIgualNombreQue(self, otroMaterialOManoDeObra:'Material|ManoDeObra'):
        return otroMaterialOManoDeObra.tieneIgualNombreQueMaterial(self)

    def tieneIgualNombreQueMaterial(self, otroMaterial:'Material'):
        return otroMaterial.tieneComoNombre(self.nombre)

    def tieneIgualNombreQueManoDeObra(self, manoDeObra:ManoDeObra):
        return False

    def esManoDeObra(self):
        return False


    #mensajes de error
    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombre(nombre_duplicado:str, nombre_archivo:str):
        raise ValueError(Material.registrosDeIgualNombreDescripcionDeError(nombre_duplicado, nombre_archivo))
    
    @staticmethod
    def registrosDeIgualNombreDescripcionDeError(nombre_duplicado:str, nombre_archivo:str):
        return f"Hay más de un material con el nombre {nombre_duplicado} en el archivo {nombre_archivo}."

    @staticmethod
    def NombreNuloDescripcionDeError(densidad:str, precio:str):
        return f"El nombre del material con densidad: {densidad} (Kg/dm3) y precio: ${precio} no puede estar vacío"
    
    @staticmethod
    def DensidadInvalidaDescripcionDeError(nombre:str, densidad_invalida:str):
        return f"El material {nombre} tiene una densidad inválida de: {densidad_invalida} Kg/dm3"
    
    @staticmethod
    def PrecioInvalidoDescripcionDeError(nombre:str, precio_invalido:str):
        return f"El material {nombre} tiene un precio inválido de: ${precio_invalido}"
    


def verificarValidezDeLaLista(lista_materiales:list[Material], archivo:str):
    hay_registro_mano_de_obra:bool = False

    for indice, materialOManoDeObra in enumerate(lista_materiales):
        if(materialOManoDeObra.esManoDeObra()):
            hay_registro_mano_de_obra = True

        for otroMaterialOManoDeObra in lista_materiales[indice+1:]:
            materialOManoDeObra.verificarQueNoCompartaNombreCon(otroMaterialOManoDeObra, archivo)
           

    if(hay_registro_mano_de_obra == False):
        raise ValueError(f"debe haber al menos un registro de mano de obra en el archivo {archivo}")

def crear_lista_materiales_a_partir_de(archivo:str) -> list[Material]:
    archivo_precios = open(archivo,"r")
    lineas_archivo:list[str] = archivo_precios.readlines()
    archivo_precios.close() #CERRE EL ARCHIVO

    lista_materiales:list[Material] = []

    for linea in lineas_archivo: #requisito que el archivo tenga todo escrito de la forma "a,material,densidad,precio\n" para que funcione
        cant_comas:int = 0
        nombre:str = ""
        precio:str = ""
        densidadOPrecio:str = ""

        for i in range(len(linea)):
            if linea[i] ==",":
                cant_comas += 1

            elif cant_comas == 0: 
                nombre = nombre+linea[i]

            elif cant_comas == 1:
                densidadOPrecio = densidadOPrecio+linea[i]   
            
            elif cant_comas == 2 and linea[i]!="\n":
                precio = precio+linea[i]

        #print(f"material: {material}, densidad:{densidad}, precio: {precio}")
        if (nombre == "Mano de obra" or nombre == "mano de obra"):
            lista_materiales.append(ManoDeObra(densidadOPrecio))
        else:
            lista_materiales.append(Material(nombre, densidadOPrecio, precio))


    verificarValidezDeLaLista(lista_materiales, archivo)

    return lista_materiales

def registrar_material(nombre:str, densidad:str, precio:str, archivo:str):
    archivo_modificable = open(archivo,"a")

    Material.assertarCaracteristicasValidas(nombre, densidad, precio)

    archivo_lectura = open(archivo, "r")
    lineas_archivo:list[str] = archivo_lectura.readlines()

    for linea in lineas_archivo:
        caracteristicas_material:str = linea.split(',') 
        if (caracteristicas_material[0] == nombre):
            Material.lanzarErrorDeRegistrosDeIgualNombre(nombre, archivo)


    if(lineas_archivo == []):
        archivo_modificable.write(f"{nombre},{densidad},{precio}")
    else:
        archivo_modificable.write(f"\n{nombre},{densidad},{precio}")
    
    archivo_modificable.close()



# def crear_texto_registro_materiales(dic_materiales:dict[str,tuple[str,float,float]]) -> str:
#     texto:str = "" 
#     texto = texto+"REGISTRO DE MATERIALES\n"

#     for letra,tupla in dic_materiales.items(): #presenta la en la posicion donde estaba en el diccionario 
#         if letra == "M":
#             texto = texto+"\nM) Valor de hora para molde soplado:   "+str(tupla[2])+" US$\n"
#         else:    
#             texto = texto+letra+") Valor del "+tupla[0]+" :   "+str(tupla[2])+" US$\n"
    
#     texto+"____________________\n"

#     return texto




