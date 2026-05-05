import pytest
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import Material

#faltan tests más simples porque alta paja hacerlos

#refactors y coso

def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = tmpdir / nombre_archivo

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, nombre_archivo:str, 
                                                        contenido:str, tipo_de_error, 
                                                        descripcion_de_error_esperada:str ):
    # Creamos una ruta para el archivo dentro del directorio temporal
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    with pytest.raises(tipo_de_error) as excinfo:
        cotizador.crear_lista_materiales_a_partir_de(archivo)

    assert str(excinfo.value) == descripcion_de_error_esperada

def verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, nombre_archivo:str, contenido:str, materiales_esperados:list[tuple[str,float,float]]) -> list[Material]:
    
    archivo = crearArchivoConContenido(tmpdir, nombre_archivo, contenido)

    lista_materiales:list[Material] = cotizador.crear_lista_materiales_a_partir_de(archivo)

    for indice, carac_material in enumerate(materiales_esperados):
        assert lista_materiales[indice].caracteristicasSon(carac_material[0], carac_material[1], carac_material[2])

    return lista_materiales


#tests como tal

def test_01_crearMaterialesArchivoInexistente():
    with pytest.raises(FileNotFoundError):
        cotizador.crear_lista_materiales_a_partir_de("archivoInexistente.txt")

def test_02_noCreaMaterialSiNombreVacio(tmpdir):

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "material_nombre_vacio.txt", 
                                                        ",2.8,19", 
                                                        ValueError, 
                                                        cotizador.Material.NombreNuloDescripcionDeError("2.8","19")  )


    
def test_03_noCreaMaterialSiDensidadNoEsNumero(tmpdir):

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "material_densidad_no_float.txt", 
                                                        "Aluminio 5083,rata,19", 
                                                        TypeError, 
                                                        cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio 5083","rata"))



def test_04_noCreaMaterialSiDensidadNegativa(tmpdir):

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "material_densidad_negativa.txt", 
                                                        "Aluminio 5083,-1,19", 
                                                        ValueError, 
                                                        cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio 5083","-1"))


def test_05_noCreaMaterialSiPrecioInvalido(tmpdir):

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "material_precio_invalido.txt", 
                                                        "Aluminio 5083,1,e3", 
                                                        TypeError, 
                                                        cotizador.Material.PrecioInvalidoDescripcionDeError("Aluminio 5083","e3"))

def test_06_creaListaDeVariosMateriales(tmpdir):

    registro_correcto = """Aluminio 7075,2.8,23.50
Acero Amutit,8,7.5
Acero Especial K,8,11"""

    materiales_esperados:list[tuple[str,float,float]] = [("Aluminio 7075", 2.8, 23.50),
                                                         ("Acero Amutit", 8, 7.5),
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
mano de obra,35"""

    materiales_esperados:list[tuple[str,float,float]] = [("Aluminio 7075", 2.8, 23.50),
                                                         ("Cobre Berilio", 9, 110)] 

    lista_materiales = verificarQueSeRegistrenLosMaterialesCorrectamente(tmpdir, 
                                                                         "materiales_y_mano_de_obra.txt", 
                                                                         registro_con_mano_de_obra, materiales_esperados)

    assert lista_materiales[2].caracteristicasSon("mano de obra", 35)

def test_08_manoDeObraNoPuedeTenerPrecioInvalido(tmpdir):

    registro_con_mano_de_obra = """Aluminio 7075,2.8,23.50
Cobre Berilio,9,110
mano de obra,-35"""

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "mano_de_obra_precio_invalido.txt", 
                                                        registro_con_mano_de_obra, 
                                                        ValueError, 
                                                        cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("-35"))


def test_09_noPuedeHaberDosMaterialesDeMismoNombreEnUnMismoArchivo(tmpdir):
    registro_con_nombres_repetidos = """Aluminio 7075,2.8,23.50
Cobre Berilio,9,110
Cobre Berilio,11,45
mano de obra,35"""

    assertarLevantamientoErrorMedianteArchivoIncorrecto(tmpdir, 
                                                        "nombres_repetidos.txt", 
                                                        registro_con_nombres_repetidos, 
                                                        ValueError, 
                                                        cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("-35"))