import math
from collections.abc import Callable

def es_float_estricto(cadena) -> bool:
    try:
        valor = float(cadena)
        # Comprobamos que no sea infinito ni NaN
        return math.isfinite(valor)
    except (ValueError, TypeError):
        return False
    
def lanzarValueError(descripcion_de_error:str):
    raise ValueError(descripcion_de_error)

def lanzarTypeError(descripcion_de_error:str):
    raise TypeError(descripcion_de_error)

def debeHaberAlMenosUnRegistroManoDeObraDescripcionDeError(archivo:str) -> str:
    return f"debe haber al menos un registro de mano de obra en el archivo {archivo}"

def debeHaberAlMenosUnMaterialEnElArchivoDescripcionDeError(archivo:str) -> str:
    return f"debe haber al menos un material en el archivo {archivo}"

def noSePuedeRegistrarSinCostoManoDeObraDescripcionDeError() -> str:
    return f"No se puede registrar en el archivo sin el costo de la mano de obra"

def noSePuedeRegistrarSinMaterialesDescripcionDeError() -> str:
    return f"No se puede registrar en el archivo sin al menos un material"

def noSePuedeRegistrarConDosCostosDeManoDeObraDescripcionDeError() ->str:
    return f"No se puede registrar en el archivo con dos costos de mano de obra"

def noSePuedeRegistrarConMaterialesDeMismoNombreDescripcionDeError() -> str:
    return f"No se puede registrar en el archivo con materiales de mismo nombre"

def noSePuedeRegistrarMaterialSiYaHayUnoDelMismoNombreRegistradoEn(nombre_material:str, archivo:str) -> str:
    return f"No se puede registrar el material {nombre_material} porque ya hay uno del mismo nombre registrado en el archivo {archivo}"

def noSePuedeRegistrarManoDeObraSiYaHayUnaRegistradaEn(archivo:str) -> str:
    return f"No se puede registrar mano de obra si ya hay una registrada en el archivo {archivo}"

class RegistroDeCosto:

    #asserciones
    def assertPrecioValido(self, precio:str):
        raise NotImplementedError(
            "Las subclases deben implementar assertPrecioValido"
        )
    
    #romper encapsulamiento
    def precio_str(self) -> str:
        return str(self.precio)
    
    #presentarse como string
    def espresarseEnFormatoRegistro(self) -> str:
        raise NotImplementedError(
            "Las subclases deben implementar espresarseEnFormatoRegistro"
        )
    
    @staticmethod
    def assertarAtributoNumericoValido(atributo_en_str:str, descripcion_error_para_no_numerico:str, descripcion_error_para_no_positivo:str):
        if not(es_float_estricto(atributo_en_str)):
            lanzarTypeError(descripcion_error_para_no_numerico)
            

        atributo_en_str = float(atributo_en_str)

        if atributo_en_str <=0:
            lanzarValueError(descripcion_error_para_no_positivo)
    
        
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
    
    def lanzarErrorConArchivoSiComparteNombreCon(self, otroMaterialOManoDeObra:'RegistroDeCosto', descripcion_de_err):
        raise NotImplementedError(
            "Las subclases deben implementar verificarQueNoCompartaNombreCon"
        )
    
    def realizarAccionSiComparteNombreCon(self, otroRegistroDeCosto:'RegistroDeCosto', 
                                          accionDelRegistro:Callable[['RegistroDeCosto'], None]):
        if(self.tieneIgualNombreQue(otroRegistroDeCosto)):
            accionDelRegistro(self)

    def lanzarErrorConArchivoSiComparteNombreCon(self, otroRegistroDeCosto:'RegistroDeCosto', archivo:str):
        self.realizarAccionSiComparteNombreCon(otroRegistroDeCosto, 
                 lambda registro: registro.lanzarErrorDeRegistrosDeIgualNombreEnArchivo(archivo))

    def lanzarErrorSiComparteNombreEnLaListaParaRegistrarCon(self, otroRegistroDeCosto:'RegistroDeCosto'):
        self.realizarAccionSiComparteNombreCon(otroRegistroDeCosto, 
                 lambda registro: registro.lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre())

    def lanzarErrorAlRegistrarseSiNombreEs(self, nombre_a_comparar:str, archivo:str):
        if(self.tieneComoNombre(nombre_a_comparar)):
            self.lanzarErrorYaEstaRegistradoRegistroDelMismoNombreEn(archivo)

    def esMaterial(self) -> bool:
        return False

    def esManoDeObra(self) -> bool:
        return False
    
    #errores 
    def lanzarErrorYaEstaRegistradoRegistroDelMismoNombreEn(archivo):
        raise NotImplementedError(
            "Las subclases deben implementar lanzarErrorYaEstaRegistradoRegistroDelMismoNombre"
        )

    def lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre(self):
        raise NotImplementedError(
            "Las subclases deben implementar lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre"
        )

    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombreEnArchivo():
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
    
    #presentarse como string
    def espresarseEnFormatoRegistro(self) -> str:
        return f"{self.nombre},{self.precio_str()}"
    
    #cosas
    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombreEnArchivo(nombre_archivo:str):
        lanzarValueError(f"No puede haber dos registros de mano de obra en el archivo {nombre_archivo}")
    
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

    #mensajes de error    
    def lanzarErrorYaEstaRegistradoRegistroDelMismoNombreEn(archivo):
        lanzarValueError(noSePuedeRegistrarManoDeObraSiYaHayUnaRegistradaEn(archivo))

    def lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre(self):
        lanzarValueError(noSePuedeRegistrarConDosCostosDeManoDeObraDescripcionDeError())

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
    
    #romper encapsulamiento
    def densidad_str(self) -> str:
        return str(self.densidad)
    
    
    #espresarse en string
    def espresarseEnFormatoRegistro(self) -> str:
        return f"{self.nombre},{self.densidad_str()},{self.precio_str()}"
   
    # aserciones
    @staticmethod
    def assertarCaracteristicasValidas(nombre:str, densidad:str, precio:str):
        Material.assertNombreValido(nombre, densidad, precio)
        Material.assertDensidadValida(nombre, densidad)
        Material.assertPrecioValido(nombre, precio)

    @staticmethod
    def assertNombreValido(nombre:str, densidad:str, precio:str):
        if not nombre: 
            lanzarValueError(Material.NombreNuloDescripcionDeError(densidad, precio))

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
        
    def verificarQueNombreNoSea(self, nombre:str, archivo:str):
        if(self.tieneComoNombre(nombre)):
                self.lanzarErrorDeRegistrosDeIgualNombreEnArchivo(archivo)
    
    
       
    def caracteristicasSon(self, nombre_esperado:str, densidad_esperada:str, precio_esperado:str):
        return self.tieneComoNombre(nombre_esperado) and self.densidad == densidad_esperada and self.precio == precio_esperado

    def tieneIgualNombreQue(self, otroMaterialOManoDeObra:'Material|ManoDeObra'):
        return otroMaterialOManoDeObra.tieneIgualNombreQueMaterial(self)

    def tieneIgualNombreQueMaterial(self, otroMaterial:'Material'):
        return otroMaterial.tieneComoNombre(self.nombre)

    def tieneIgualNombreQueManoDeObra(self, manoDeObra:ManoDeObra):
        return False

    def esMaterial(self):
        return True


    #mensajes de error
    def lanzarErrorYaEstaRegistradoRegistroDelMismoNombreEn(self, archivo):
        lanzarValueError(noSePuedeRegistrarMaterialSiYaHayUnoDelMismoNombreRegistradoEn(self.nombre,archivo))

    def lanzarErrorDeRegistrosDeIgualNombreEnArchivo(self, nombre_archivo:str):
        lanzarValueError(self.registrosDeIgualNombreDescripcionDeError(nombre_archivo))
    
    def registrosDeIgualNombreDescripcionDeError(self, nombre_archivo:str):
        return f"Hay más de un material con el nombre {self.nombre} en el archivo {nombre_archivo}."
    
    def lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre(self):
        lanzarValueError(noSePuedeRegistrarConMaterialesDeMismoNombreDescripcionDeError())

    @staticmethod
    def NombreNuloDescripcionDeError(densidad:str, precio:str):
        return f"El nombre del material con densidad: {densidad} (Kg/dm3) y precio: ${precio} no puede estar vacío"
    
    @staticmethod
    def DensidadInvalidaDescripcionDeError(nombre:str, densidad_invalida:str):
        return f"El material {nombre} tiene una densidad inválida de: {densidad_invalida} Kg/dm3"
    
    @staticmethod
    def PrecioInvalidoDescripcionDeError(nombre:str, precio_invalido:str):
        return f"El material {nombre} tiene un precio inválido de: ${precio_invalido}"


def verificarValidezDeListaDeRegistros(lista_registros:list[RegistroDeCosto], 
        comparacionEntreRegistrosYLanzamientoDeError:Callable[[RegistroDeCosto, RegistroDeCosto], None], 
        descripcion_de_error_para_falta_ManoDeObra:str, descripcion_de_error_para_falta_material:str ):
    
    cantidad_mano_de_obra = False
    hay_materiales = False

    for indice, registroDeCosto in enumerate(lista_registros):
        if(registroDeCosto.esManoDeObra()):
            cantidad_mano_de_obra = True

        if(registroDeCosto.esMaterial()):
            hay_materiales = True

        for otroRegistroDeCosto in lista_registros[indice+1:]:
            comparacionEntreRegistrosYLanzamientoDeError(registroDeCosto, otroRegistroDeCosto)

    if(cantidad_mano_de_obra == False):
        lanzarValueError(descripcion_de_error_para_falta_ManoDeObra)
    
    if(hay_materiales == False):
        lanzarValueError(descripcion_de_error_para_falta_material)


def verificarValidezDeLaListaDeRegistrosLeidaDeArchivo(lista_registros:list[Material], archivo:str):

    verificarValidezDeListaDeRegistros(lista_registros, lambda registroDeCosto, otroRegistroDeCosto: 
        registroDeCosto.lanzarErrorConArchivoSiComparteNombreCon(otroRegistroDeCosto, archivo),
          debeHaberAlMenosUnRegistroManoDeObraDescripcionDeError(archivo),
          debeHaberAlMenosUnMaterialEnElArchivoDescripcionDeError(archivo))


def crear_lista_registros_a_partir_de(archivo:str) -> list[RegistroDeCosto]:
    archivo_precios = open(archivo,"r")
    lineas_archivo:list[str] = archivo_precios.readlines()
    archivo_precios.close() #CERRE EL ARCHIVO

    lista_materiales:list[RegistroDeCosto] = []

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


    verificarValidezDeLaListaDeRegistrosLeidaDeArchivo(lista_materiales, archivo)

    return lista_materiales


def registrarRegistroDeCosto(registro:RegistroDeCosto, archivo:str):
    archivo_modificable = open(archivo,"a")

    archivo_lectura = open(archivo, "r")
    lineas_archivo:list[str] = archivo_lectura.readlines()

    for linea in lineas_archivo:
        caracteristicas_registro:str = linea.split(',')
        registro.lanzarErrorAlRegistrarseSiNombreEs(caracteristicas_registro[0], archivo) 

    if(lineas_archivo == []):
        archivo_modificable.write(registro.espresarseEnFormatoRegistro())
    else:
        archivo_modificable.write("\n"+registro.espresarseEnFormatoRegistro())
    
    archivo_modificable.close()

def registrarListaRegistros(lista_registros:list[RegistroDeCosto], archivo:str):
    
    verificarValidezDeListaDeRegistros(lista_registros, lambda registroDeCosto, otroRegistroDeCosto: 
        registroDeCosto.lanzarErrorSiComparteNombreEnLaListaParaRegistrarCon(otroRegistroDeCosto),
          noSePuedeRegistrarSinCostoManoDeObraDescripcionDeError(),
          noSePuedeRegistrarSinMaterialesDescripcionDeError())
    
    for registro in lista_registros:
        registrarRegistroDeCosto(registro, archivo)
    



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




