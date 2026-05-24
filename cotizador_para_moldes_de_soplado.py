import math
from collections.abc import Callable
from dataclasses import dataclass, field
#from ventana_cotizador import Ventana


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

def lanzarErrorLasSubclasesDebenImplementar(nombre_funcion:str): 
    raise NotImplementedError(
            f"Las subclases deben implementar {nombre_funcion}"
        )

def elMaterialTieneMasDeTresCamposDescripcionDeError(nombre_material:str, archivo:str):
    return f"El material {nombre_material} tiene más de tres campos en el archivo {archivo}"

def laManoDeObraTieneMasDeDosCamposDescripcionDeError(archivo:str):
    return f"La mano de obra tiene más de dos campos en el archivo {archivo}"

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
        lanzarErrorLasSubclasesDebenImplementar("assertPrecioValido")
    
    # def verificarPrecioValidoEnVentana(self, ventana:'Ventana', precio_en_str:str):
        
    #     self.verificarAtributoNumericoValidoLanzando(precio_en_str, 
    #                                         lambda: self.lanzarErrorPrecioInvalidoEnVentana(ventana, precio_en_str),
    #                                         lambda: self.lanzarErrorPrecioInvalidoEnVentana(ventana, precio_en_str))

    @staticmethod    
    def verificarAtributoNumericoValidoLanzando(atributo_en_str:str, lanzarErrorParaNoNumerico:Callable[[],None], lanzarErrorParaNoPositivo:Callable[[],None] ):
        if not(es_float_estricto(atributo_en_str)):
            lanzarErrorParaNoNumerico()
        else:

            atributo_en_str = float(atributo_en_str)

            if atributo_en_str <=0:
                lanzarErrorParaNoPositivo()

    @staticmethod
    def assertarAtributoNumericoValido(atributo_en_str:str, descripcion_error_para_no_numerico:str, 
                                       descripcion_error_para_no_positivo:str):
        
        RegistroDeCosto.verificarAtributoNumericoValidoLanzando(atributo_en_str, 
                                                    lambda: lanzarTypeError(descripcion_error_para_no_numerico), 
                                                    lambda: lanzarValueError(descripcion_error_para_no_positivo))

    #romper encapsulamiento
    def precio_str(self) -> str:
        return str(self.precio)
    
    #presentarse como string
    def espresarseEnFormatoRegistro(self) -> str:
        lanzarErrorLasSubclasesDebenImplementar("espresarseEnFormaRegistro")
    
    def esPrecioValido(self, precio_en_str:str):
        if(es_float_estricto(precio_en_str)):
            return (float(precio_en_str) >0)
        else: 
            return False
        
        
    def tieneComoNombre(self, nombre_esperado:str):
        return self.nombre == nombre_esperado
    
    def tieneIgualNombreQue(self, otroMaterialOManoDeObra:'RegistroDeCosto'):
        lanzarErrorLasSubclasesDebenImplementar("tieneIgualNombreQue")

    def tieneIgualNombreQueMaterial(self, otroMaterial:'Material'):
        lanzarErrorLasSubclasesDebenImplementar("tieneIgualNombreQueMaterial")

    def tieneIgualNombreQueManoDeObra(self, manoDeObra:'ManoDeObra'):
        lanzarErrorLasSubclasesDebenImplementar("tieneIgualNombreQueManoDeObra")
    
    def lanzarErrorConArchivoSiComparteNombreCon(self, otroMaterialOManoDeObra:'RegistroDeCosto', descripcion_de_err):
        lanzarErrorLasSubclasesDebenImplementar("verificarQueNoCompartaNombreCon")
    
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
        lanzarErrorLasSubclasesDebenImplementar("lanzarErrorYaEstaRegistradoRegistroDelMismoNombre")

    def lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre(self):
        lanzarErrorLasSubclasesDebenImplementar("lanzarErrorNoSePuedeRegistrarRegistrosDeMismoNombre")
    
    #lanzar error en ventana
    def lanzarErrorPrecioInvalidoEnVentana(self, ventana:'Ventana', precio_a_modificar:str):
        lanzarErrorLasSubclasesDebenImplementar("lanzarErrorPrecioInvalidoEnVentana")

    @staticmethod
    def lanzarErrorDeRegistrosDeIgualNombreEnArchivo():
        lanzarErrorLasSubclasesDebenImplementar("lanzarErrorDeRegistrosDeIgualNombre")
        
    @staticmethod
    def PrecioInvalidoDescripcionDeError(precio:str):
        lanzarErrorLasSubclasesDebenImplementar("PrecioInvalidoDescripcionDeError")
    
@dataclass(frozen=True)
class ManoDeObra(RegistroDeCosto):
    precio: str
    # Definimos nombre como fijo y le decimos que no se pida en el constructor
    nombre: str = field(default="Mano de obra", init=False)

    def __post_init__(self):
        # Aquí puedes validar. Si levanta una excepción, el objeto no se creará
        self.assertPrecioValido(self.precio)

        object.__setattr__(self, 'precio', float(self.precio))


    # def __init__(self, precio):

    #     self.assertPrecioValido(precio)

    #     self.nombre:str = "Mano de obra"
    #     self.precio:float          # precio por unidad (ej: por kg)


    def __str__(self):
        return f"{self.nombre} (precio={self.precio})"
    
    # def __eq__(self, otroObjeto):
    #     if not isinstance(otroObjeto, ManoDeObra):
    #         return NotImplemented

    #     return self.nombre == otroObjeto.nombre and self.precio == otroObjeto.precio
        # if(self.nombre == otroObjeto.nombre):
        #     # if(self.precio == otroObjeto.precio):
        #     #     raise ValueError(f"Comparando igualdad entre materiales de mismo nombre {self.nombre} y distinto precio")

        #     return True
        # else: 
        #     return False
    
    # def __hash__(self):
    #     return hash((self.nombre, self.precio))
    
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

    #mensajes de error en ventana
    def lanzarErrorPrecioInvalidoEnVentana(self, ventana:'Ventana', precio_a_modificar:str):
        ventana.ejecutarDialogDeErrorConDescripcion(
        ManoDeObra.PrecioInvalidoDescripcionDeError(precio_a_modificar))

    #Ventana
    def agregarseALaListaConElPrecioModificado(self, ventana:'Ventana', indice:int, precio_a_modificar:str):
        ventana.lista_registros[indice] = ManoDeObra(precio_a_modificar)

@dataclass(frozen=True)
class Material(RegistroDeCosto):
    nombre: str
    densidad:str
    precio: str    

    def __post_init__(self): #se ejecuta justo antes de crear al objeto
        Material.assertarCaracteristicasValidas(self.nombre,self.densidad,self.precio)

        #se modifica a float a ultimo momento porque si no queda en str 
        object.__setattr__(self, 'densidad', float(self.densidad))
        object.__setattr__(self, 'precio', float(self.precio))

    # def __init__(self, nombre, densidad, precio):

    #     Material.assertarCaracteristicasValidas(nombre,densidad,precio)

    #     self.nombre = nombre
    #     self.densidad = float(densidad)      # kg/m³, por ejemplo
    #     self.precio = float(precio)          # precio por unidad (ej: por kg)

    def __str__(self):
        return f"{self.nombre} (densidad={self.densidad}, precio={self.precio})"
    
    # def __eq__(self, otroObjeto):
    #     if not isinstance(otroObjeto, Material):
    #         return NotImplemented

    #     return (self.nombre == otroObjeto.nombre and self.densidad == otroObjeto.densidad and self.)

        # if(self.nombre == otroObjeto.nombre):
        #     # if(self.densidad != otroObjeto.densidad):
        #     #     raise ValueError(f"Comparando igualdad entre materiales de mismo nombre {self.nombre} y distinta densidad")
        #     # if(self.precio == otroObjeto.precio):
        #     #     raise ValueError(f"Comparando igualdad entre materiales de mismo nombre {self.nombre} y distinto precio")

        #     return True
        # else: 
        #     return False
    
    # def __hash__(self):
    #     return hash((self.nombre, self.densidad, self.precio))

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

    #Ventana
    def agregarseALaListaConElPrecioModificado(self, ventana:'Ventana', indice:int, precio_a_modificar:str):
        ventana.lista_registros[indice] = Material(self.nombre, self.densidad_str(), precio_a_modificar)

    #mensajes de error en ventana
    def lanzarErrorPrecioInvalidoEnVentana(self, ventana:'Ventana', precio_a_modificar:str):
        ventana.ejecutarDialogDeErrorConDescripcion(
            Material.PrecioInvalidoDescripcionDeError(self.nombre, precio_a_modificar))

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
            
            elif cant_comas == 3:
                lanzarValueError(elMaterialTieneMasDeTresCamposDescripcionDeError(nombre, archivo))

        #print(f"material: {material}, densidad:{densidad}, precio: {precio}")
        if (nombre == "Mano de obra" or nombre == "mano de obra"):
            if(precio != ""):
                lanzarValueError(laManoDeObraTieneMasDeDosCamposDescripcionDeError(archivo))

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


def limpiarArchivoYRegistrarListaRegistros(lista_registros:list[RegistroDeCosto], archivo:str):
    archivo_para_escribir = open(archivo, "w")
    archivo_para_escribir.write("")

    registrarListaRegistros(lista_registros, archivo)

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




