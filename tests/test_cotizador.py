#faltan tests más simples porque alta paja hacerlos
import tests.funciones_comunes_cotizador as com_cot

from . import (pytest, Callable, RegistroDeCosto, cotizador, Material, ManoDeObra)

def assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error, funcion:Callable[[], None], descripcion_de_error_esperada:str):

    with pytest.raises(tipo_de_error) as excinfo:
        funcion()

    assert str(excinfo.value) == descripcion_de_error_esperada

def verificarLevantamientoDeErrorAlLeerArchivoInvalidoConDescripcionEnBaseAArchivo(tmpdir, nombre_archivo:str,
                                                lista_registros_anteriores:list[RegistroDeCosto], tipo_de_error,
                                                descripcion_de_error_esperada_en_base_a_archivo:Callable[[str],str]):

    contenido = com_cot.pasarListaRegistrosATexto(lista_registros_anteriores)
    archivo = com_cot.crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error,
        lambda: cotizador.crear_lista_registros_a_partir_de(archivo),
        descripcion_de_error_esperada_en_base_a_archivo(archivo))

    contenido_esperado = com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_anteriores)
    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)

def assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, nombre_archivo:str,
                                                        contenido:str, tipo_de_error,
                                                        descripcion_de_error_esperada:str ):

    # Creamos una ruta para el archivo dentro del directorio temporal
    archivo = com_cot.crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error,
        lambda: cotizador.crear_lista_registros_a_partir_de(archivo),
        descripcion_de_error_esperada)


def assertarMaterialesRegistradosCorrectamente(archivo:str, registros_esperados:list[Material]):

    contenido_esperado = com_cot.pasarListaRegistrosALineasParaArchivo(registros_esperados)

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)


# def assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir,
#                                             nombre_material:str, densidad_material:str, precio_material:str,
#                                             tipo_de_error, descripcion_de_error_esperada:str):

#     assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, "archivo_vacio.txt", "", nombre_material, densidad_material,
#                                                      precio_material, tipo_de_error, lambda archivo: descripcion_de_error_esperada, [])


def assertarQueNoSeRegistroMaterialEnArchivo(tmpdir,
                                            nombre_archivo:str, contenido:str, material:Material,
                                            tipo_de_error, descripcion_de_error_esperada:Callable[[str],str],
                                            contenido_final_esperado:list[str]):

    archivo = com_cot.crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    assertarLevantamientoDeErrorAlEjecutarFuncion(tipo_de_error,
        lambda: cotizador.registrarRegistroDeCosto(material, archivo),
        descripcion_de_error_esperada(archivo))

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, contenido_final_esperado)


def verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, nombre_archivo:str, registros_anteriores:list[Material],
                                                      material:Material, registros_esperados:list[Material]):

    archivo = com_cot.crearArchivoConRegistrosAnteriores(tmpdir, nombre_archivo, registros_anteriores)

    cotizador.registrarRegistroDeCosto(material, archivo)

    assertarMaterialesRegistradosCorrectamente(archivo, registros_esperados)


def verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, nombre_archivo:str, registros_esperados:list[RegistroDeCosto]) -> list[RegistroDeCosto]:

    contenido = com_cot.pasarListaRegistrosATexto(registros_esperados)

    archivo = com_cot.crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    lista_materiales:list[RegistroDeCosto] = cotizador.crear_lista_registros_a_partir_de(archivo)

    for registro in registros_esperados:
        assert registro in lista_materiales

    assert len(registros_esperados) == len(lista_materiales)

    return lista_materiales

def assertarLevantamientoErrorMatcheandoDescripcion(tmpdir, nombre_archivo:str, contenido:str, tipo_de_error, descripcion_de_error_esperada:str):
    archivo = com_cot.crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    with pytest.raises(tipo_de_error, match= f".*{descripcion_de_error_esperada}.* {tmpdir}/{nombre_archivo}") as excinfo:
        #para que el patrón regex matchee debe aparece exactamente el string descripcion_de_error esperada dentro del mensaje
        cotizador.crear_lista_registros_a_partir_de(archivo)

def verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, lista_registros:list[RegistroDeCosto], descripcion_de_error_esperada:str):
    archivo = com_cot.crearDireccionDeArchivoInexistente(tmpdir, "archivo_inexistente.txt")

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError,
                                    lambda: cotizador.registrarListaRegistros(lista_registros, archivo),
                        descripcion_de_error_esperada)

    com_cot.assertarArchivoInexistente(archivo)

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

def test_05_1_noCreaMaterialSiTieneMasDeTresCampos(tmpdir):
    registro_invalido = """Aluminio 5083,1,34,r
mano de obra,34"""

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir,
                                            "material_precio_invalido.txt",
                                            registro_invalido,
                                            ValueError,
        cotizador.elMaterialTieneMasDeTresCamposDescripcionDeError("Aluminio 5083", tmpdir/"material_precio_invalido.txt"))

def test_05_2_noCreaManoDeObraSiTieneMasDeDosCampos(tmpdir):
    registro_invalido = """Aluminio 5083,1,34
mano de obra,34,3"""

    assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir,
                                            "material_precio_invalido.txt",
                                            registro_invalido,
                                            ValueError,
            cotizador.laManoDeObraTieneMasDeDosCamposDescripcionDeError(tmpdir/"material_precio_invalido.txt"))

def test_05_3_noCreListaSinRegistroDeManoDeObra(tmpdir):

    lista_registros_sin_mano_de_obra = [Material("Aluminio 7075","2.8","23.50"), Material("Acero Amutit","8","7.5"),
                                        Material("Acero Especial K","8","11")]

    verificarLevantamientoDeErrorAlLeerArchivoInvalidoConDescripcionEnBaseAArchivo(tmpdir, "sin_mano_de_obra.txt",
                                                                                lista_registros_sin_mano_de_obra,
                                                                                ValueError,
                            lambda archivo: cotizador.debeHaberAlMenosUnRegistroManoDeObraDescripcionDeError(archivo))

     # assertarLevantamientoErrorMatcheandoDescripcion(tmpdir,
    #                                         "sin_mano_de_obra.txt",
    #                                         registro_sin_mano_de_obra,
    #                                         ValueError,
    #                                         "debe haber al menos un registro de mano de obra")

def test_05_4_noCreaListaSinAluminio5083(tmpdir):
    lista_registros_sin_aluminio_5083 = [Material("Aluminio 7075","2.8","23.50"), Material("Acero Amutit","8","7.5"),
                                        Material("Acero Especial K","8","11"), ManoDeObra("3")]

    verificarLevantamientoDeErrorAlLeerArchivoInvalidoConDescripcionEnBaseAArchivo(tmpdir, "sin_aluminio_5083.txt",
                                                                                lista_registros_sin_aluminio_5083,
                                                                                ValueError,
                            lambda archivo: cotizador.debeHaberUnRegistroDeAluminio5083DescripcionDeError(archivo))


#falta noCreaListaSinAlMenosUnMaterial pero alta paja hacerlo, ya está cubierto

# com_cot.lista_registros_aceptada:list[RegistroDeCosto] = [Material("Aluminio 7075", "2.8", "23.50"),
#                                                   Material("Aluminio 5083", "3", "4.5"), 
#                                                   Material("Acero Amutit", "8", "7.5"),
#                                                   ManoDeObra("35"),
#                                                   Material("Acero Especial K", 8, 11)]

def test_06_creaListaDeVariosMateriales(tmpdir):

    lista_materiales = verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir,
                                                                         "materiales_correctos.txt", 
                                                                         com_cot.lista_registros_aceptada)

    #chequear funcion caracteristicasSon
    assert not(lista_materiales[0].caracteristicasSon("Alumino 7075", 2.8, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.9, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.8, 22.50))


def test_07_manoDeObraSeRegistraCorrectamente(tmpdir):

    lista_materiales = verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir,
                                                                         "materiales_y_mano_de_obra.txt",
                                                                         com_cot.lista_registros_aceptada)

    assert lista_materiales[3].caracteristicasSon("Mano de obra", 35)

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

    archivo = com_cot.crearDireccionDeArchivoInexistente(tmpdir, "archivo_inexistente.txt")

    cotizador.registrarListaRegistros(com_cot.lista_registros_aceptada, archivo)

    assertarMaterialesRegistradosCorrectamente(archivo, com_cot.lista_registros_aceptada)

def cotizarConListaRegistroAceptada(input_numero_de_moldes:int|str, input_cantidad_cavidades:int|str,
                                    input_altura:int|str, input_volumen:int|str, input_distancia_entre_centros:int|str,
                                    input_ancho_mitad:int|str):

    aluminio_7075 = com_cot.lista_registros_aceptada[0]

    cotizador.cotizarEnBaseA(input_numero_de_moldes, input_cantidad_cavidades, False, input_altura, input_volumen,
                            input_distancia_entre_centros, input_ancho_mitad, "a", aluminio_7075, aluminio_7075, 
                            aluminio_7075, aluminio_7075, aluminio_7075, com_cot.lista_registros_aceptada, ManoDeObra("30"))

def cotizarConInputCantDeMoldesInvalido(input_numero_de_moldes:int|str):

    cotizarConListaRegistroAceptada(input_numero_de_moldes, 1, 100, 100, 100, 100)


def test_23_NoSePuedeCotizarSiLaCantidadDeMoldesNoEs1O2():

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputCantDeMoldesInvalido(0),
                                                  cotizador.cantidadDeMoldesACotizarInvalidaDescripcionDeError(0))

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputCantDeMoldesInvalido(3),
                                                  cotizador.cantidadDeMoldesACotizarInvalidaDescripcionDeError(3))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputCantDeMoldesInvalido("1"),
                                                  cotizador.cantidadDeMoldesACotizarInvalidaDescripcionDeError("1"))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputCantDeMoldesInvalido("a"),
                                                  cotizador.cantidadDeMoldesACotizarInvalidaDescripcionDeError("a"))

def cotizarConInputCantidadCavidadesInvalido(input_cantidad_cavidades:int):

    cotizarConListaRegistroAceptada(1, input_cantidad_cavidades, 100, 100, 100, 100)


def test_24_NoSePuedeCotizarSiLaCantidadDeCavidadesEsInvalida():

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputCantidadCavidadesInvalido(0),
                                                  cotizador.cantidadDeCavidadesACotizarInvalidaDescripcionDeError(0))

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputCantidadCavidadesInvalido(11),
                                                  cotizador.cantidadDeCavidadesACotizarInvalidaDescripcionDeError(11))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputCantidadCavidadesInvalido("9"),
                                                  cotizador.cantidadDeCavidadesACotizarInvalidaDescripcionDeError("9"))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputCantidadCavidadesInvalido("-"),
                                                  cotizador.cantidadDeCavidadesACotizarInvalidaDescripcionDeError("-"))

def cotizarConInputAlturaInvalida(input_altura_invalida:int|str):

    cotizarConListaRegistroAceptada(1, 1, input_altura_invalida, 100, 100, 100)

def test_25_NoSePuedeCotizarConAlturaInvalida():
    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputAlturaInvalida(0),
                                                  cotizador.alturaDeEnvaseInvalidaDescripcionDeError(0))

    assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputAlturaInvalida(-11),
                                                  cotizador.alturaDeEnvaseInvalidaDescripcionDeError(-11))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputAlturaInvalida("1"),
                                                  cotizador.alturaDeEnvaseInvalidaDescripcionDeError("1"))

    assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputAlturaInvalida("-"),
                                                  cotizador.alturaDeEnvaseInvalidaDescripcionDeError("-"))
    
# def cotizarConInputVolumenInvalido(input_volumen_invalido:int|str):

#     cotizarConListaRegistroAceptada(1, 1, 100, input_volumen_invalido, 100, 100)

# def test_26_NoSePuedeCotizarConVolumenInvalido():
#     assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputAlturaInvalida(0),
#                                                   cotizador.alturaDeEnvaseInvalidaDescripcionDeError(0))

#     assertarLevantamientoDeErrorAlEjecutarFuncion(ValueError, lambda: cotizarConInputAlturaInvalida(-11),
#                                                   cotizador.alturaDeEnvaseInvalidaDescripcionDeError(-11))

#     assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputAlturaInvalida("1"),
#                                                   cotizador.alturaDeEnvaseInvalidaDescripcionDeError("1"))

#     assertarLevantamientoDeErrorAlEjecutarFuncion(TypeError, lambda: cotizarConInputAlturaInvalida("-"),
#                                                   cotizador.alturaDeEnvaseInvalidaDescripcionDeError("-"))

#no hago estos tests y directamente pongo las verificaciones en el código


# el chequeo del Aluminio 5083 lo hago cuando el user de que sí a las máscaras y troqueles y no lo tenga en el registro

def test_26_DialogCrearRegistrosNoCreaRegistroYLevantaDialogDeErrorAlNoIngresarAluminio5083(qtbot, tmpdir, monkeypatch):

    lista_registros_sin_aluminio:list[RegistroDeCosto] = [Material("Aluminio","3","3.4"), 
                                                      Material("Cobre","3.4","5.4"),
                                                      ManoDeObra("4")]

    verificarArchivoInexistenteYLanzamientoDeErrorAlRegistrarListaDeRegistros(tmpdir, lista_registros_sin_aluminio, 
                                                            cotizador.noSePuedeRegistrarSiElAluminio5083NoEstaAgregado())