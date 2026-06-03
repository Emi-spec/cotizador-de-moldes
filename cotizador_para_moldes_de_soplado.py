import math
from collections.abc import Callable
from dataclasses import dataclass, field
#from ventana_r import Ventana


def es_float_estricto(cadena) -> bool:
    try:
        valor = float(cadena)
        # Comprobamos que no sea infinito ni NaN
        return math.isfinite(valor)
    except (ValueError, TypeError):
        return False
    
def verificarAtributoNumericoValidoLanzando(atributo_en_str:str, lanzarErrorParaNoNumerico:Callable[[],None], 
                                            lanzarErrorParaNoPositivo:Callable[[],None] ):
    if not(es_float_estricto(atributo_en_str)):
        lanzarErrorParaNoNumerico()
    else:

        atributo_en_str = float(atributo_en_str)

        if atributo_en_str <=0:
            lanzarErrorParaNoPositivo()
    

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

def debeHaberUnRegistroDeAluminio5083DescripcionDeError(archivo:str) -> str:
    return f"debe haber al menos un registro de aluminio 5083 en el archivo {archivo}"

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

def noSePuedeRegistrarSiElAluminio5083NoEstaAgregado():
    return f"No se puede registrar si el material Aluminio 5083 no está añadido (porque se necesita para máscaras y troqueles)"

def descripcionDeErrorIndicandoTipo(descripcion_de_error_antes_de_poner_input:str, input_invalido:int|str):
    return f"{descripcion_de_error_antes_de_poner_input} {str(input_invalido)} (de tipo {type(input_invalido).__name__})"

def cantidadDeMoldesACotizarInvalidaDescripcionDeError(cantidad_moldes_invalida:int|str) -> str:
    return descripcionDeErrorIndicandoTipo("La cantidad de moldes a cotizar debe ser 1 o 2, no", cantidad_moldes_invalida)

def cantidadDeCavidadesACotizarInvalidaDescripcionDeError(cantidad_de_cavidades_invalida:int|str):
    return descripcionDeErrorIndicandoTipo("La cantidad de cavidades a cotizar debe ser un número entre 1 y 10, no", 
                                           cantidad_de_cavidades_invalida)
    
def alturaDeEnvaseInvalidaDescripcionDeError(altura_invalida:int|str) -> str:
    return descripcionDeErrorIndicandoTipo("El envase tiene una altura inválida de:", altura_invalida)

def volumenDeEnvaseInvalidoDescripcionDeError(volumen_invalido:int|str) -> str:
    return descripcionDeErrorIndicandoTipo("El envase tiene un volumen inválido de:", volumen_invalido)

def distanciaEntreCentrosInvalidaDescripcionDeError(distancia_entre_centros_invalida:str) -> str:
    return descripcionDeErrorIndicandoTipo("El envase tiene una distancia entre centros inválida de",
                                            distancia_entre_centros_invalida)

def anchoPorMitadDelMoldeInvalidoDescripcionDeError(ancho_por_mitad_invalido:str) -> str:
    return descripcionDeErrorIndicandoTipo("El molde tiene un ancho por mitad invalido de", ancho_por_mitad_invalido)

def NoSeEligioUnNivelDeDificultadDelEnvaseDescripcionDeError() -> str: 
    return "No se eligió un nivel de dificultad para el envase"

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
        return self.nombre.lower() == nombre_esperado.lower()
    
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
    
    #Ventana
    def agregarseALaListaConElPrecioModificado(self, ventana:'Ventana', indice:int, precio_a_modificar:str):
        lanzarErrorLasSubclasesDebenImplementar("agregarseALaListaConElPrecioModificado")
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
    def agregarseALaListaConElPrecioModificado(self, ventana:'Ventana', indice:RegistroDeCosto, precio_a_modificar:str):
        #input = ventana.input_precios.pop(registro)
        #ventana.input_precios[ManoDeObra(precio_a_modificar)] = input
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
        #input = ventana.input_precios.pop(registro)
        #ventana.input_precios[Material(self.nombre, self.densidad_str(), precio_a_modificar)] = input
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

@dataclass(frozen=True)
class NivelDeDificultad():
    presentacion_en_str:str
    coeficiente:int

    # def crearRadioButton(self) -> QRadioButton:
    #     return QRadioButton(self.presentacion_en_str)

nivelDeDificultadBajo = NivelDeDificultad("Bajo\t\t(cilíndricos - con rosca o snap)", 1)
nivelDeDificultadMedio = NivelDeDificultad("Medio\t\t(elípticos, rectangulares - con rosca o snap)", 1.12)
nivelDeDificultadAlto = NivelDeDificultad("Alto\t\t(asimétricos - rosca, rosca con trinquete o snap)", 1.25)
nivelDeDificultadMuyAlto = NivelDeDificultad(
    "Muy alto\t(asimétricos,L/C no plana, grabados en cavidad, encastre para tapa contorneado)", 1.35)
nivelDeDificultadEspeciales = NivelDeDificultad("Especiales\t(asimétricos, con asa, con postizos de pinch off)", 1.48)

    # if dificultad == "a":
    #     coeficiente = 1
    # elif dificultad == "b":
    #     coeficiente = 1.12
    # elif dificultad == "c":                         
    #     coeficiente = 1.25
    # elif dificultad == "d": 
    #     coeficiente = 1.35
    # else: 
    #     coeficiente = 1.48


@dataclass(frozen=True)
class ResultadoCotizacion():
    diccionario_costos_material:dict[Material, float]
    costo_total:float
    costo_mat:float
    gastos_varios:float
    horas_trabajo:float
    precio_total:float

    def imprimirResultado(self) -> str:
        info_a_imprimir:str = f'''COSTO TOTAL MATERIA PRIMA: ${self.costo_total:.2f} US$\n
Costos de cada material (total: {self.costo_mat:.2f} US$): \n'''

        #costos de cada material
        for material, costo in self.diccionario_costos_material.items():
            #print(self.diccionario_costos_material[material].nombre +f": {costo:.2f} US$")
            info_a_imprimir = info_a_imprimir+ material.nombre +f": {costo:.2f} US$\n"

        info_a_imprimir = info_a_imprimir+f'''\nElementos STD, tornilleria, o'rings, etc: {self.gastos_varios} US$\n
HORAS DE TRABAJO: {self.horas_trabajo}hs\n
PRECIO TOTAL: {self.precio_total} US$\n'''
        
        return info_a_imprimir

 #probablemente esta parte no entre en la función
    #IMPRESIÓN FINAL
        
    # info_a_imprimir:str = f'''COSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n
    # Costos de cada material (total: {costo_mat:.2f} US$): \n'''

    # print(f"\n\n\nCOSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n") 
    # print(f"Costos de cada material (total: {costo_mat:.2f} US$): \n")

   
    #costos de cada material

    # for clave,costo in dic_costos_mat.items():
    #     print(dic_materiales[clave][0]+f": {costo:.2f} US$")
    #     info_a_imprimir = info_a_imprimir+dic_materiales[clave][0]+f": {costo:.2f} US$\n"

    # print(f"\nElementos STD, tornillería, o'rings, etc: {gastos_var} US$")

    # print(f"\nHORAS DE TRABAJO: {horas}hs\n")
    # print(f"PRECIO TOTAL: {precio} US$\n")

    # info_a_imprimir = info_a_imprimir+f'''\nElementos STD, tornilleria, o'rings, etc: {gastos_var} US$\n
    # HORAS DE TRABAJO: {horas}hs\n
    # PRECIO TOTAL: {precio} US$\n'''

    # imprimirSiNo:str = input("¿Desea guardar esta información en un archivo de texto?: ")
    # imprimirSiNo = verificar_sino(imprimirSiNo)

    # if imprimirSiNo == "s" or imprimirSiNo == "si":
    #     nombre_archivo:str = input("¿Que nombre desearía colocarle al archivo? (sin extensiones): ")
    #     existe_nombre:bool = True
    #     #verificamos si el pelotudo que usa esto no le puso el mismo nombre que un archivo existente

    #     while existe_nombre:
    #         try:    
    #             ver_archivo = open(nombre_archivo+".txt","r")
    #             ver_archivo.close()
    #             nombre_archivo = input("Ese archivo ya existe, por favor pruebe con otro nombre: ")
            
    #         except OSError:
    #             existe_nombre = False

    #     archivo_info_molde = open(nombre_archivo+".txt","w")
    #     archivo_info_molde.write(info_a_imprimir)
    #     archivo_info_molde.close()

    # respuesta = input("Presione enter para finalizar\n")


def verificarValidezDeListaDeRegistros(lista_registros:list[RegistroDeCosto], 
        comparacionEntreRegistrosYLanzamientoDeError:Callable[[RegistroDeCosto, RegistroDeCosto], None], 
        descripcion_de_error_para_falta_ManoDeObra:str, descripcion_de_error_para_falta_material:str,
        descripcion_de_error_para_falta_de_Aluminio5083:str):
    
    cantidad_mano_de_obra = False
    hay_materiales = False
    hay_aluminio_5083 = False

    for indice, registroDeCosto in enumerate(lista_registros):
        if(registroDeCosto.esManoDeObra()):
            cantidad_mano_de_obra = True

        if(registroDeCosto.esMaterial()):
            hay_materiales = True

        if(registroDeCosto.tieneComoNombre("Aluminio 5083")):
            hay_aluminio_5083 = True

        for otroRegistroDeCosto in lista_registros[indice+1:]:
            comparacionEntreRegistrosYLanzamientoDeError(registroDeCosto, otroRegistroDeCosto)

    if(cantidad_mano_de_obra == False):
        lanzarValueError(descripcion_de_error_para_falta_ManoDeObra)
    
    if(hay_materiales == False):
        lanzarValueError(descripcion_de_error_para_falta_material)

    if(hay_aluminio_5083 == False):
        lanzarValueError(descripcion_de_error_para_falta_de_Aluminio5083)


def verificarValidezDeLaListaDeRegistrosLeidaDeArchivo(lista_registros:list[Material], archivo:str):

    verificarValidezDeListaDeRegistros(lista_registros, lambda registroDeCosto, otroRegistroDeCosto: 
        registroDeCosto.lanzarErrorConArchivoSiComparteNombreCon(otroRegistroDeCosto, archivo),
          debeHaberAlMenosUnRegistroManoDeObraDescripcionDeError(archivo),
          debeHaberAlMenosUnMaterialEnElArchivoDescripcionDeError(archivo),
          debeHaberUnRegistroDeAluminio5083DescripcionDeError(archivo))


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
          noSePuedeRegistrarSinMaterialesDescripcionDeError(),
          noSePuedeRegistrarSiElAluminio5083NoEstaAgregado())
    
    for registro in lista_registros:
        registrarRegistroDeCosto(registro, archivo)
    

def verificarQueInputSeaNumericoLanzandoErrorConDescripcion(input:int|str, descripcion_de_error:str):
    if not isinstance(input, (int, float)):
        lanzarTypeError(descripcion_de_error)

def verificarQueInputNumericoSeaPositivoLanzandoErrorConDescripcion(input:int, descripcion_de_error:str):
    if(input <=0):
        lanzarValueError(descripcion_de_error)

def verificarMedidaValida(input:int|str, descripcion_de_error:str):
    verificarQueInputSeaNumericoLanzandoErrorConDescripcion(input, descripcion_de_error)

    verificarQueInputNumericoSeaPositivoLanzandoErrorConDescripcion(input, descripcion_de_error)

def cotizarEnBaseA(n_moldes:int, n_cavidades:int, mascaras_troqueles:bool, altura:str, volumen:str, dist_entre_centros:str, 
        ancho_mitad:str, dificultad:NivelDeDificultad, mat_post_cuerpo:Material, mat_post_cuello:Material, 
        mat_post_fondo:Material, mat_placas_respaldo:Material, mat_post_prensa:Material, dic_materiales:list[Material], 
        mano_de_obra:ManoDeObra):


    verificarQueInputSeaNumericoLanzandoErrorConDescripcion(n_moldes, 
                                                        cantidadDeMoldesACotizarInvalidaDescripcionDeError(n_moldes))

    if (n_moldes != 1 and n_moldes != 2):
        lanzarValueError(cantidadDeMoldesACotizarInvalidaDescripcionDeError(n_moldes)) 

    # if not isinstance(n_moldes, (int, float)):
    #     lanzarTypeError(cantidadDeMoldesACotizarInvalidaDescripcionDeError(str(n_moldes)))

    # if (n_moldes != 1 and n_moldes != 2):
    #     lanzarValueError(cantidadDeMoldesACotizarInvalidaDescripcionDeError(str(n_moldes))) 

    # n_moldes:int = input("\n-Cantidad de moldes a cotizar:\n") 
    # while n_moldes != "1" and n_moldes != "2":
    #     n_moldes = input("Solo puede ingresar 1 o 2. Ingrese de nuevo: ")
    # n_moldes = int(n_moldes)

    verificarQueInputSeaNumericoLanzandoErrorConDescripcion(n_cavidades, 
                                                cantidadDeCavidadesACotizarInvalidaDescripcionDeError(n_cavidades))

    if (n_cavidades < 1 or n_cavidades > 10):
        lanzarValueError(cantidadDeCavidadesACotizarInvalidaDescripcionDeError(n_cavidades)) 

    # n_cavidades:int = input("\n-Cantidad de cavidades del molde:\n")
    # n_cavidades = verificar_int(n_cavidades)

    # while n_cavidades<1 or n_cavidades>10:
    #     n_cavidades = input("Debe ingresar un número entero del 1 al 10. Ingrese de nuevo: ")
    #     n_cavidades = verificar_int(n_cavidades)

    #Mascaras y troqueles
    # mascaras_troqueles:str = input("\n-¿Incluye máscaras de transporte y troqueles? (si/no):\n") 
    # mascaras_troqueles = verificar_sino(mascaras_troqueles)

    cav_al:dict[int,tuple[int,float]] = {1:(20,3),2:(36,5.5),3:(50,8),4:(64,10),5:(75,12),6:(84,14),7:(90,16),8:(96,18),
                                        9:(99,20),10:(110,22)}

    horas_mas_troq:float = 0
    costo_al_5083:float = 0

    #breakpoint() #Aluminio 5083
    for material in dic_materiales:
        if(material.tieneComoNombre("Aluminio 5083")):
            aluminio_5083 = material

    # if(aluminio_5083 == None):
    #     raise ValueError("El Material aluminio 5083 no esta en dic_materiales")

    if mascaras_troqueles:
        tupla_selec:tuple[int,float] = cav_al[n_cavidades]
        horas_mas_troq = tupla_selec[0]
        costo_al_5083 = tupla_selec[1] * aluminio_5083.precio

    #características del molde

    verificarMedidaValida(altura, alturaDeEnvaseInvalidaDescripcionDeError(altura))
    # altura:float = input("\n-Altura del envase (mm):\n")
    # altura = verificar_num (altura)
    
    verificarMedidaValida(volumen, volumenDeEnvaseInvalidoDescripcionDeError(volumen))
    # volumen:float = input("\n-Volumen del envase (mm):\n")
    # volumen = verificar_num(volumen)
    
    verificarMedidaValida(dist_entre_centros, distanciaEntreCentrosInvalidaDescripcionDeError(dist_entre_centros))
    # dist_entre_centros:float = input("\n-Distancia entre centros que hay entre cavidades: (mm)\n")
    # dist_entre_centros = verificar_num (dist_entre_centros)
        
    verificarMedidaValida(ancho_mitad, anchoPorMitadDelMoldeInvalidoDescripcionDeError(ancho_mitad))
    # ancho_mitad:float = input("\n-Ancho por mitad del molde (mm):\n")
    # ancho_mitad = verificar_num (ancho_mitad)



    # dificultad:str = input ('''\n-Nivel de dificultad del envase:
    # a)Bajo\t\t(cilíndricos - con rosca o snap)
    # b)Medio\t\t(elípticos, rectangulares - con rosca o snap)
    # c)Alto\t\t(asimétricos - rosca, rosca con trinquete o snap)
    # d)Muy alto\t(asimétricos,L/C no plana, grabados en cavidad, encastre para tapa contorneado)
    # e)Especiales\t(asimétricos, con asa, con postizos de pinch off)\n''')
    # dificultad = verificar_clave(dificultad, ["a","b","c","d","e"])

    #horas de trabajo
    #tabla de horas

    horas_por_cavidad:dict[int,int] = {1:70,2:120,3:165,4:205,5:243,6:281,7:318,8:355,9:392,10:429}
    horas_de_trabajo:int = horas_por_cavidad[n_cavidades]

    if n_moldes == 2: 
        horas_de_trabajo *= 1.92

    #dificultad
    # coeficiente:int = 0

    # if dificultad == "a":
    #     coeficiente = 1
    # elif dificultad == "b":
    #     coeficiente = 1.12
    # elif dificultad == "c":                         
    #     coeficiente = 1.25
    # elif dificultad == "d": 
    #     coeficiente = 1.35
    # else: 
    #     coeficiente = 1.48

    #horas extra por altura
    horas_alt:float = ((altura - 100) / 450) +1 #FALTAN POSIBLES CAMBIOS

    #cubicaje
    cubicaje:float = 0

    if volumen >= 100:
        cubicaje = (volumen/500 * 0.1) + 1
    else:
        cubicaje = 1

    #total horas
    horas_de_trabajo = round((horas_de_trabajo + horas_mas_troq) * dificultad.coeficiente * horas_alt * cubicaje) #POR CONSIGUIENTE, CAMBIAR ACÁ

    #postizos, materiales y esas cosas
    #lista_claves_sinM:list[str] = crear_lista_claves(True,False)
    #str_opciones_sinM:str =crear_str_opciones(lista_claves_sinM)

    lista_mat_costos:list[tuple[str,float]] = []

    #print("\n\nIngrese el material a utilizar:")
    #imprimir_letras_mat()

    # mat_post_cuerpo:str = input("-Postizos de cuerpo"+str_opciones_sinM+":\n")
    # mat_post_cuerpo = verificar_clave(mat_post_cuerpo, lista_claves_sinM) 

    precio_post_cuerpo:float = ((dist_entre_centros * n_cavidades) + 60)* (altura - 25) * 58 * 0.000001 * 2 * mat_post_cuerpo.densidad * mat_post_cuerpo.precio * 1.1 

    lista_mat_costos.append((mat_post_cuerpo,precio_post_cuerpo))

    # mat_post_cuello:str = input("\n-Postizos de cuello"+str_opciones_sinM+":\n") 
    # mat_post_cuello = verificar_clave(mat_post_cuello, lista_claves_sinM) 

    precio_post_cuello:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * mat_post_cuello.densidad * mat_post_cuello.precio

    lista_mat_costos.append((mat_post_cuello,precio_post_cuello))

    #mat_post_fondo:str = input("\n-Postizos de fondo"+str_opciones_sinM+":\n")
    #mat_post_fondo = verificar_clave(mat_post_fondo, lista_claves_sinM)

    precio_post_fondo:float = ((dist_entre_centros * n_cavidades) + 60) * 30 * 58 * 1.1 * 0.000001 * 2 * mat_post_fondo.densidad * mat_post_fondo.precio 

    lista_mat_costos.append((mat_post_fondo,precio_post_fondo))


    # mat_placas_respaldo:str = input("\n-Placas de respaldo"+str_opciones_sinM+"\n")
    # mat_placas_respaldo = verificar_clave(mat_placas_respaldo, lista_claves_sinM) 

    precio_placas_respaldo:float = ((dist_entre_centros * n_cavidades) + 60) * (altura + 65) * (ancho_mitad - 58) * 0.000001 * 2 * mat_placas_respaldo.densidad * mat_placas_respaldo.precio * 1.1

    lista_mat_costos.append((mat_placas_respaldo,precio_placas_respaldo))


    # mat_post_prensa:str = input("\n-Postizo prensamangas"+str_opciones_sinM+"\n")
    # mat_post_prensa = verificar_clave(mat_post_prensa, lista_claves_sinM) 

    precio_post_prensa:float = ((dist_entre_centros * n_cavidades) + 60) * 58 * 35 * 0.000001 * 2 * mat_post_prensa.densidad * mat_post_prensa.precio * 1.1

    lista_mat_costos.append((mat_post_prensa,precio_post_prensa))


    costo_de_materiales:float = precio_post_cuerpo + precio_post_cuello + precio_post_fondo + precio_placas_respaldo + precio_post_prensa

    #costo de cada material

    dic_costos_por_material:dict[Material,float] = {} #diccionario que solo contiene los precios de materiales utilizados

    for material,costo in lista_mat_costos:
        if material in dic_costos_por_material.keys():
            dic_costos_por_material[material] += costo
        else:
            dic_costos_por_material[material] = costo

    #gastos varios 
    if n_cavidades == 1:
        gastos_varios = 200
    else: 
        gastos_varios = 300 + 50 * (n_cavidades - 2)

    if n_moldes == 2:
        gastos_varios *= 2

    costo_total = costo_de_materiales + gastos_varios

    #precio estimado
    mano_obra:float = horas_de_trabajo * mano_de_obra.precio
    precio_total:float = round(mano_obra + costo_total) 

    return ResultadoCotizacion(dic_costos_por_material, costo_total, costo_de_materiales, gastos_varios, horas_de_trabajo, precio_total)
    #probablemente esta parte no entre en la función
    #IMPRESIÓN FINAL
        
    # info_a_imprimir:str = f'''COSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n
    # Costos de cada material (total: {costo_mat:.2f} US$): \n'''

    # print(f"\n\n\nCOSTO TOTAL MATERIA PRIMA: ${costo_total:.2f} US$\n") 
    # print(f"Costos de cada material (total: {costo_mat:.2f} US$): \n")

   
    #costos de cada material

    # for clave,costo in dic_costos_mat.items():
    #     print(dic_materiales[clave][0]+f": {costo:.2f} US$")
    #     info_a_imprimir = info_a_imprimir+dic_materiales[clave][0]+f": {costo:.2f} US$\n"

    # print(f"\nElementos STD, tornillería, o'rings, etc: {gastos_var} US$")

    # print(f"\nHORAS DE TRABAJO: {horas}hs\n")
    # print(f"PRECIO TOTAL: {precio} US$\n")

    # info_a_imprimir = info_a_imprimir+f'''\nElementos STD, tornilleria, o'rings, etc: {gastos_var} US$\n
    # HORAS DE TRABAJO: {horas}hs\n
    # PRECIO TOTAL: {precio} US$\n'''

    # imprimirSiNo:str = input("¿Desea guardar esta información en un archivo de texto?: ")
    # imprimirSiNo = verificar_sino(imprimirSiNo)

    # if imprimirSiNo == "s" or imprimirSiNo == "si":
    #     nombre_archivo:str = input("¿Que nombre desearía colocarle al archivo? (sin extensiones): ")
    #     existe_nombre:bool = True
    #     #verificamos si el pelotudo que usa esto no le puso el mismo nombre que un archivo existente

    #     while existe_nombre:
    #         try:    
    #             ver_archivo = open(nombre_archivo+".txt","r")
    #             ver_archivo.close()
    #             nombre_archivo = input("Ese archivo ya existe, por favor pruebe con otro nombre: ")
            
    #         except OSError:
    #             existe_nombre = False

    #     archivo_info_molde = open(nombre_archivo+".txt","w")
    #     archivo_info_molde.write(info_a_imprimir)
    #     archivo_info_molde.close()

    # respuesta = input("Presione enter para finalizar\n")


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




