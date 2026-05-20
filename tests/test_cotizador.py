import pytest
from collections.abc import Callable
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import (Material, ManoDeObra, RegistroDeCosto)

#faltan tests más simples porque alta paja hacerlos

#refactors y coso

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

def assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error, funcion:Callable[[], None], descripcion_de_error_esperada:str):
    
    with pytest.raises(tipo_de_error) as excinfo:
        funcion()

    assert str(excinfo.value) == descripcion_de_error_esperada


def assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, nombre_archivo:str, 
                                                        contenido:str, tipo_de_error, 
                                                        descripcion_de_error_esperada:str ):
    
    # Creamos una ruta para el archivo dentro del directorio temporal
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)
    
    assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error, 
        lambda: cotizador.crear_lista_registros_a_partir_de(archivo),
        descripcion_de_error_esperada)
    

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):

    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    assert lineas_archivo == contenido_esperado

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

def assertarMaterialesRegistradosCorrectamente(archivo:str, registros_esperados:list[Material]):

    contenido_esperado = pasarListaRegistrosALineasParaArchivo(registros_esperados)

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)


# def assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
#                                             nombre_material:str, densidad_material:str, precio_material:str,
#                                             tipo_de_error, descripcion_de_error_esperada:str):
    
#     assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, "archivo_vacio.txt", "", nombre_material, densidad_material,
#                                                      precio_material, tipo_de_error, lambda archivo: descripcion_de_error_esperada, [])


def assertarQueNoSeRegistroMaterialEnArchivo(tmpdir, 
                                            nombre_archivo:str, contenido:str, material:Material,
                                            tipo_de_error, descripcion_de_error_esperada:Callable[[str],str],
                                            contenido_final_esperado:list[str]):
    
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error, 
        lambda: cotizador.registrarRegistroDeCosto(material, archivo),
        descripcion_de_error_esperada(archivo))

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_final_esperado)


def verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, nombre_archivo:str, registros_anteriores:list[Material], 
                                                      material:Material, registros_esperados:list[Material]):
    
    archivo = crearArchivoConRegistrosAnteriores(tmpdir, nombre_archivo, registros_anteriores)

    cotizador.registrarRegistroDeCosto(material, archivo)

    assertarMaterialesRegistradosCorrectamente(archivo, registros_esperados)


def verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, nombre_archivo:str, contenido:str, 
                                                      materiales_esperados:list[tuple[str,float,float]]) -> list[RegistroDeCosto]:
    
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    lista_materiales:list[RegistroDeCosto] = cotizador.crear_lista_registros_a_partir_de(archivo)

    for indice, carac_material in enumerate(materiales_esperados):
        if(carac_material[0] == "Mano de obra"):
            assert lista_materiales[indice].caracteristicasSon(carac_material[0], carac_material[1])
        else:
            assert lista_materiales[indice].caracteristicasSon(carac_material[0], carac_material[1], carac_material[2])

    return lista_materiales

def assertarLevantamientoErrorMatcheandoDescripcion(tmpdir, nombre_archivo:str, contenido:str, tipo_de_error, descripcion_de_error_esperada:str):
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    with pytest.raises(tipo_de_error, match= f".*{descripcion_de_error_esperada}.* {tmpdir}/{nombre_archivo}") as excinfo:
        #para que el patrón regex matchee debe aparece exactamente el string descripcion_de_error esperada dentro del mensaje
        cotizador.crear_lista_registros_a_partir_de(archivo)

def verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, lista_registros:list[RegistroDeCosto], descripcion_de_error_esperada:str):
    archivo = crearDireccionDeArchivoInexistente(tmpdir, "archivo_inexistente.txt")

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, 
                                    lambda: cotizador.registrarListaRegistros(lista_registros, archivo),
                        descripcion_de_error_esperada)
    
    assertarArchivoInexistente(archivo)

#tests como tal

def test_01_crearMaterialesArchivoInexistente():
    with pytest.raises(FileNotFoundError):
        cotizador.crear_lista_registros_a_partir_de("archivoInexistente.txt")

def test_02_noCreaMaterialSiNombreVacio(tmpdir):

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, 
                                            "material_nombre_vacio.txt", 
                                            ",2.8,19", 
                                            ValueError, 
                                            cotizador.Material.NombreNuloDescripcionDeError("2.8","19")  )


    
def test_03_noCreaMaterialSiDensidadNoEsNumero(tmpdir):

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, 
                                            "material_densidad_no_float.txt", 
                                            "Aluminio 5083,rata,19", 
                                            TypeError, 
                                            cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio 5083","rata"))



def test_04_noCreaMaterialSiDensidadNegativa(tmpdir):

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, 
                                            "material_densidad_negativa.txt", 
                                            "Aluminio 5083,-1,19", 
                                            ValueError, 
                                            cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio 5083","-1"))


def test_05_noCreaMaterialSiPrecioInvalido(tmpdir):

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, 
                                            "material_precio_invalido.txt", 
                                            "Aluminio 5083,1,e3", 
                                            TypeError, 
                                            cotizador.Material.PrecioInvalidoDescripcionDeError("Aluminio 5083","e3"))
    

def test_05_1_noCreListaSinRegistroDeManoDeObra(tmpdir):

    registro_sin_mano_de_obra = """Aluminio 7075,2.8,23.50
Acero Amutit,8,7.5
Acero Especial K,8,11"""

    assertarLevantamientoErrorMatcheandoDescripcion(tmpdir, 
                                            "sin_mano_de_obra.txt",
                                            registro_sin_mano_de_obra, 
                                            ValueError, 
                                            "debe haber al menos un registro de mano de obra")


#falta noCreaListaSinAlMenosUnMaterial pero alta paja hacerlo, ya está cubierto

def test_06_creaListaDeVariosMateriales(tmpdir):

    registro_correcto = """Aluminio 7075,2.8,23.50
Acero Amutit,8,7.5
Mano de obra,4
Acero Especial K,8,11
"""

    materiales_esperados:list[tuple[str,float,float]|tuple[str,float]] = [("Aluminio 7075", 2.8, 23.50),
                                                         ("Acero Amutit", 8, 7.5),
                                                         ("Mano de obra",4),
                                                         ("Acero Especial K", 8, 11)] 

    lista_materiales = verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, 
                                                                         "materiales_correctos.txt", 
                                                                         registro_correcto, materiales_esperados)

    #chequear funcion caracteristicasSon
    assert not(lista_materiales[0].caracteristicasSon("Alumino 7075", 2.8, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.9, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.8, 22.50))




#Se puede calcular costos de soplado sin mano de obra? (Si no es así, hay que modificar todos los tests anteriores)

def test_07_manoDeObraSeRegistraCorrectamente(tmpdir):

    registro_con_mano_de_obra = """Aluminio 7075,2.8,23.50
Cobre Berilio,9,110
Mano de obra,35"""

    materiales_esperados:list[tuple[str,float,float]] = [("Aluminio 7075", 2.8, 23.50),
                                                         ("Cobre Berilio", 9, 110)] 

    lista_materiales = verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, 
                                                                         "materiales_y_mano_de_obra.txt", 
                                                                         registro_con_mano_de_obra, materiales_esperados)

    assert lista_materiales[2].caracteristicasSon("Mano de obra", 35)

def test_08_manoDeObraNoPuedeTenerPrecioInvalido(tmpdir):

    registro_con_mano_de_obra = """Aluminio 7075,2.8,23.50
Cobre Berilio,9,110
Mano de obra,-35"""

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, 
                                            "mano_de_obra_precio_invalido.txt", 
                                            registro_con_mano_de_obra, 
                                            ValueError, 
                                            cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("-35"))


def test_09_noPuedeHaberDosMaterialesDeMismoNombreEnUnMismoArchivo(tmpdir):
    registro_con_nombres_repetidos = """Aluminio 7075,2.8,23.50
Cobre Berilio,9,110
Cobre Berilio,11,45
Mano de obra,35"""

    assertarLevantamientoErrorMatcheandoDescripcion(tmpdir, 
                                                      "nombres_repetidos.txt",
                                                      registro_con_nombres_repetidos, 
                                                      ValueError,
                                                      "más de un material con el nombre")



def test_10_noPuedeHaberDosRegistrosDeManoDeObra(tmpdir):
    registro_dos_mano_de_obra = """Aluminio 7075,2.8,23.50
Mano de obra,32
Cobre Berilio,11,45
mano de obra,35"""

    assertarLevantamientoErrorMatcheandoDescripcion(tmpdir, 
                                                      "doble_mano_de_obra.txt",
                                                      registro_dos_mano_de_obra,
                                                      ValueError, 
                                                      "dos registros de mano de obra")

#estos tests ya dejaron de tener sentido porque registrar_material recibe un objeto Material
# def test_11_noSePuedeRegistrarUnMaterialSiSuNombreEsNulo(tmpdir):

#     assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
#                                             "", "9", "3.4", 
#                                             ValueError,
#                                             cotizador.Material.NombreNuloDescripcionDeError("9","3.4"))


# def test_12_noSePuedeRegistrarUnMaterialConDensidadInvalida(tmpdir):

#     assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
#                                             "Aluminio", "-1", "3.4",
#                                             ValueError, 
#                                             cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio", "-1"))


# def test_13_noSePuedeRegistrarUnMaterialConPrecioInvalido(tmpdir):
#     assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
#                                             "Aluminio", "1", "a",
#                                             TypeError, 
#                                             cotizador.Material.PrecioInvalidoDescripcionDeError("Aluminio", "a"))

  
def test_14_SeRegistraUnMaterialCorrectamente(tmpdir):

    material = Material("Aluminio", "2", "2.9")

    verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, "archivo_vacio.txt", [],
                                                       material, [material])  


def test_15_RegistrarUnMaterialNoBorraRegistrosAnteriores(tmpdir):
#     registros_anteriores = """Aluminio,2,4.5
# cobre Berilio,5,4.3"""

    registro_anterior_1 = Material("Aluminio","2","4.5")
    registro_anterior_2 = Material("cobre Berilio","5","4.3")
    
    material_a_agregar = Material("Acero", "2", "2.9")
    

    verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, "archivo_vacio.txt", 
                                                      [registro_anterior_1, registro_anterior_2], 
        material_a_agregar, [registro_anterior_1, registro_anterior_2, material_a_agregar])   


def test_16_NoSePuedeRegistrarUnMaterialConNombreRegistradoHabiendoUno(tmpdir):
    registros_anteriores = "Aluminio,2,4.5"

    material = Material("Aluminio", "3", "4.5")

    assertarQueNoSeRegistroMaterialEnArchivo(tmpdir, "archivo_con_un_material.txt", registros_anteriores,
                                                    material, 
                                                    ValueError, 
        lambda archivo: cotizador.noSePuedeRegistrarMaterialSiYaHayUnoDelMismoNombreRegistradoEn(material.nombre, archivo),
                                                    [registros_anteriores])

def test_17_NoSePuedeRegistrarUnMaterialConNombreRegistradoHabiendoVarios(tmpdir):
    registros_anteriores = """hojalata,5,6.5
cobre berilio,4,3.5
Aluminio,2,4.5
barulla,4.3,5,6"""

    material = Material("Aluminio", "3", "5.5")

    lista_registros_anteriores:list[str] = ["hojalata,5,6.5\n", "cobre berilio,4,3.5\n", 
                                                "Aluminio,2,4.5\n", "barulla,4.3,5,6"] 

    assertarQueNoSeRegistroMaterialEnArchivo(tmpdir, "archivo_con_un_material.txt", registros_anteriores,
                                                    material, 
                                                    ValueError, 
    lambda archivo: cotizador.noSePuedeRegistrarMaterialSiYaHayUnoDelMismoNombreRegistradoEn(material.nombre, archivo),
                                                    lista_registros_anteriores)



def test_18_NoSePuedeRegistrarEnArchivoListaDeMaterialesSiNoEstaCostoManoDeObra(tmpdir):
    lista_materiales = [Material("Aluminio","3","3.4"), Material("Cobre","4","5.4"), Material("Plomo","4","5.4")]

    verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, lista_materiales, cotizador.noSePuedeRegistrarSinCostoManoDeObraDescripcionDeError())
  

def test_19_NoSePuedeRegistrarEnArchivoListaDeRegistrosSinMateriales(tmpdir):
    lista_doble_mano_de_obra = [ManoDeObra("3")]

    verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, 
                                                                              lista_doble_mano_de_obra, 
                                                        cotizador.noSePuedeRegistrarSinMaterialesDescripcionDeError())


def test_20_NoSePuedeRegistrarEnArchivoVacioListaDeRegistrosSiHayDosCostosDeManoDeObra(tmpdir):
    lista_registros = [Material("Aluminio","3","3.4"), ManoDeObra("3"), ManoDeObra("4")]
    
    verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, 
                                                                              lista_registros, 
                                                  cotizador.noSePuedeRegistrarConDosCostosDeManoDeObraDescripcionDeError())
    
def test_21_NoSePuedeRegistrarEnArchivoInexistenteListaDeRegistrosSiHayDosMaterialesDeMismoNombre(tmpdir):
    lista_registros = [Material("Aluminio","3","3.4"), Material("Aluminio","3.4","5.4") , ManoDeObra("4")]
    
    verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, 
                                                                              lista_registros, 
                                            cotizador.noSePuedeRegistrarConMaterialesDeMismoNombreDescripcionDeError())
    
def test_22_listaDeRegistrosAceptadaSeRegistraCorrectamenteEnArchivoInexistente(tmpdir):
    lista_registros_aceptada = [Material("Aluminio","3","3.4"), Material("Cobre","3.4","5.4") , ManoDeObra("4")]

    archivo = crearDireccionDeArchivoInexistente(tmpdir, "archivo_inexistente.txt")

    cotizador.registrarListaRegistros(lista_registros_aceptada, archivo)

    assertarMaterialesRegistradosCorrectamente(archivo, lista_registros_aceptada)

# el chequeo del Aluminio 5083 lo hago cuando el user de que sí a las máscaras y troqueles y no lo tenga en el registro