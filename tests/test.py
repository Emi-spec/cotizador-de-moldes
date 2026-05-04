import pytest
import cotizador_para_moldes_de_soplado as cotizador

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
        cotizador.crear_dic_materiales_a_partir_de(archivo)

    assert str(excinfo.value) == descripcion_de_error_esperada


#tests como tal

def test_01_crearMaterialesArchivoInexistente():
    with pytest.raises(FileNotFoundError):
        cotizador.crear_dic_materiales_a_partir_de("archivoInexistente.txt")

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

    archivo = crearArchivoConContenido(tmpdir, "materiales_correctos", registro_correcto)

    lista_materiales:list[Material] = cotizador.crear_dic_materiales_a_partir_de(archivo)

    assert lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.8, 23.50)

    #chequear funcion caracteristicasSon
    assert not(lista_materiales[0].caracteristicasSon("Alumino 7075", 2.8, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.9, 23.50))
    assert not (lista_materiales[0].caracteristicasSon("Aluminio 7075", 2.8, 22.50))

    assert lista_materiales[1].caracteristicasSon("Acero Amutit", 8, 7.5)
    assert lista_materiales[2].caracteristicasSon("Acero Especial K", 8, 11)