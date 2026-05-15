import pytest
from collections.abc import Callable
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import Material

#faltan tests más simples porque alta paja hacerlos

#refactors y coso

def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = tmpdir / nombre_archivo

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def assertarLevantamientoDeErrorAlEjecutarFuncion(tmpdir, tipo_de_error, funcion:Callable[[], any], descripcion_de_error_esperada:str):
    
    with pytest.raises(tipo_de_error) as excinfo:
        funcion()

    assert str(excinfo.value) == descripcion_de_error_esperada


def assertarLevantamientoErrorAlLeerArchivoInvalidoConDescripcion(tmpdir, nombre_archivo:str, 
                                                        contenido:str, tipo_de_error, 
                                                        descripcion_de_error_esperada:str ):
    
    # Creamos una ruta para el archivo dentro del directorio temporal
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)
    
    assertarLevantamientoDeErrorAlEjecutarFuncion(tmpdir, 
        tipo_de_error, 
        lambda: cotizador.crear_lista_materiales_a_partir_de(archivo),
        descripcion_de_error_esperada)
    

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):

    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    assert lineas_archivo == contenido_esperado

def assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
                                            nombre_material:str, densidad_material:str, precio_material:str,
                                            tipo_de_error, descripcion_de_error_esperada:str):
    
    assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, "archivo_vacio.txt", "", nombre_material, densidad_material,
                                                     precio_material, tipo_de_error, lambda archivo: descripcion_de_error_esperada, [])


def assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, 
                                            nombre_archivo:str, contenido:str,
                                            nombre_material:str, densidad_material:str, precio_material:str,
                                            tipo_de_error, descripcion_de_error_esperada:Callable[[str],str],
                                            contenido_final_esperado:list[str]):
    
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    assertarLevantamientoDeErrorAlEjecutarFuncion(tmpdir, tipo_de_error, 
        lambda: cotizador.registrar_material(nombre_material, densidad_material, precio_material, archivo),
        descripcion_de_error_esperada(archivo))

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_final_esperado)


def verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, nombre_archivo:str, contenido:str, 
                                                      nombre_material:str, densidad_material:str, precio_material:str,
                                                      contenido_final_esperado:str):
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    cotizador.registrar_material(nombre_material, densidad_material, precio_material, archivo)

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_final_esperado) 


def verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, nombre_archivo:str, contenido:str, materiales_esperados:list[tuple[str,float,float]]) -> list[Material]:
    
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    lista_materiales:list[Material] = cotizador.crear_lista_materiales_a_partir_de(archivo)

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
        cotizador.crear_lista_materiales_a_partir_de(archivo)



#tests como tal

def test_01_crearMaterialesArchivoInexistente():
    with pytest.raises(FileNotFoundError):
        cotizador.crear_lista_materiales_a_partir_de("archivoInexistente.txt")

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


def test_11_noSePuedeRegistrarUnMaterialSiSuNombreEsNulo(tmpdir):

    assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
                                            "", "9", "3.4", 
                                            ValueError,
                                            cotizador.Material.NombreNuloDescripcionDeError("9","3.4"))


def test_12_noSePuedeRegistrarUnMaterialConDensidadInvalida(tmpdir):

    assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
                                            "Aluminio", "-1", "3.4",
                                            ValueError, 
                                            cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio", "-1"))


def test_13_noSePuedeRegistrarUnMaterialConPrecioInvalido(tmpdir):
    assertarQueNoSeRegistroMaterialInvalidoEnArchivoVacio(tmpdir, 
                                            "Aluminio", "1", "a",
                                            TypeError, 
                                            cotizador.Material.PrecioInvalidoDescripcionDeError("Aluminio", "a"))

  


def test_14_SeRegistraUnMaterialCorrectamente(tmpdir):

    verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, "archivo_vacio.txt", "", "Aluminio", "2", "2.9", ["Aluminio,2,2.9"])  


def test_15_RegistrarUnMaterialNoBorraRegistrosAnteriores(tmpdir):
    registros_anteriores = """Aluminio,2,4.5
cobre Berilio,5,4.3"""

    verificarQueMaterialSeHayaRegistradoCorrectamente(tmpdir, "archivo_vacio.txt", registros_anteriores, 
        "Aluminio 34", "2", "2.9", ["Aluminio,2,4.5\n","cobre Berilio,5,4.3\n","Aluminio 34,2,2.9"])   


def test_16_NoSePuedeRegistrarUnMaterialConNombreRegistradoHabiendoUno(tmpdir):
    registros_anteriores = "Aluminio,2,4.5"

    assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, "archivo_con_un_material.txt", registros_anteriores,
                                                    "Aluminio", "3", "4.5", ValueError, 
                                                    lambda archivo:cotizador.Material.registrosDeIgualNombreDescripcionDeError("Aluminio", archivo),
                                                    [registros_anteriores])

def test_17_NoSePuedeRegistrarUnMaterialConNombreRegistradoHabiendoVarios(tmpdir):
    registros_anteriores = """hojalata,5,6.5
cobre berilio,4,3.5
Aluminio,2,4.5
barulla,4.3,5,6"""

    lista_registros_anteriores:list[str] = ["hojalata,5,6.5\n", "cobre berilio,4,3.5\n", 
                                                "Aluminio,2,4.5\n", "barulla,4.3,5,6"] 

    assertarQueNoSeRegistroMaterialInvalidoEnArchivo(tmpdir, "archivo_con_un_material.txt", registros_anteriores,
                                                    "Aluminio", "3", "5.5", ValueError, 
                                                    lambda archivo:cotizador.Material.registrosDeIgualNombreDescripcionDeError("Aluminio", archivo),
                                                    lista_registros_anteriores)

#el chequeo del Aluminio 5083 lo hago cuando el user de que sí a las máscaras y troqueles y no lo tenga en el registro