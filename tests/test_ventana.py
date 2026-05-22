import tests.funciones_comunes_UI as ui
import tests.funciones_comunes_cotizador as com_cot

from . import (QDialog, QLabel, QLineEdit, Callable, Ventana, RegistroDeCosto,
DialogCrearRegistros, cotizador, Material, ManoDeObra, ventana_cotizador)



#test data
registros_aceptados:str= """Aluminio 5083,2.8,19
Aluminio 6061,2.8,21.50
Aluminio 7075,2.8,23.50
Acero Amutit,8,7.5
Acero Especial K,8,11
Acero Inoxidable,8,16
Acero Amutit,8,7.5
Cobre Berilio,9,110
mano de obra, 35"""

lista_materiales_aceptados:list[str] = [Material("Aluminio 5083","2.8","19"),Material("Acero Amutit","8","7.5"), 
                                       Material("Acero Inoxidable","8","16")]

ManoDeObra_aceptada:ManoDeObra = ManoDeObra("35")

lista_registros_aceptados = lista_materiales_aceptados.copy()
lista_registros_aceptados.append(ManoDeObra_aceptada)

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana:Ventana, descripcion_de_error_esperada:str):
    ui.verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana.dialogDescripcionDeError, 
                                                             descripcion_de_error_esperada)


def verificarQueSeMuestranLosMaterialesAgregados(ventana, materiales_agregados_esperados:list[Material], 
                                                 mano_de_obra:ManoDeObra):
    labels = ventana.tabla_materiales_registrados.findChildren(QLabel)
    inputs = ventana.tabla_materiales_registrados.findChildren(QLineEdit)

    cantidad_secciones = 3
    cantidad_de_registros_agregados_esperados = len(materiales_agregados_esperados)+1

                                                    #saco mano de obra, y agrego sus dos labels al final
    assert len(labels) == cantidad_secciones + 2 * (cantidad_de_registros_agregados_esperados-1) + 1 #por los de sección y materiales y manoDeobra
    assert len(inputs) == 1 * cantidad_de_registros_agregados_esperados

    labels_datos = [l.text() for l in labels]
    inputs_datos = [i.placeholderText() for i in inputs]

    assert "Material" in labels_datos
    assert "Densidad (Kg/dm3)" in labels_datos
    assert "Precio (US$)" in labels_datos

    for material in materiales_agregados_esperados:
        assert material.nombre in labels_datos
        assert material.densidad_str() in labels_datos
        assert material.precio_str() in inputs_datos

    assert mano_de_obra.nombre in labels_datos
    assert mano_de_obra.precio_str() in inputs_datos


def abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch, 
                                                               accionesYVerificaciones:Callable[[Ventana, str], None]):
    archivo = ui.crearArchivoConContenido(tmpdir, "archivo_registros.txt", 
                                          com_cot.pasarListaRegistrosATexto(lista_registros_aceptados))

    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    accionesYVerificaciones(ventana, archivo)
    

#nunca debería pasar porque se abre el dialog
#def test_01_DialogCrearRegistrosNoMuestraMaterialesSiArchivoInexistente(qtbot, tmpdir, monkeypatch):

def test_01_VentanaMuestraLosRegistrosCorrectamente(qtbot, tmpdir, monkeypatch):

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch, lambda ventana, archivo: 
        verificarQueSeMuestranLosMaterialesAgregados(ventana, lista_materiales_aceptados, ManoDeObra_aceptada))

    

def abrirVentanaYVerificarQueDialogDeErrorTengaComoDescripcion(qtbot,monkeypatch, archivo:str, descripcion_de_error_esperada:str):
    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)
  
    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, descripcion_de_error_esperada)

#MEJORAR LA PARTE DE MODIFICAR UN ARCHIVO CORRUPTO
def test_02_VentanaMandaARehacerTodoElArchivoAlHaberUnErrorEnElArchivo(qtbot, tmpdir, monkeypatch):
    lista_registros_incorrectos = [Material("Aluminio 5083","2.8","19"),Material("Acero Amutit","8","7.5"),]

    archivo = ui.crearArchivoConContenido(tmpdir, "archivo_registros.txt", 
                                          com_cot.pasarListaRegistrosATexto(lista_registros_incorrectos))

    ui.verificarQueDialogCrearRegistrosSeEjecuteHaciendo(monkeypatch, 
                        lambda: abrirVentanaYVerificarQueDialogDeErrorTengaComoDescripcion(qtbot, monkeypatch, 
                                    archivo,cotizador.debeHaberAlMenosUnRegistroManoDeObraDescripcionDeError(archivo)))

def ejecutarGuardarCambiosYVerificarQueElContenidoDeArchivoEstaIgual(ventana:Ventana, archivo:str):
    ventana.guardarCambios()

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_aceptados))

def test_03_VentanaGuardarCambiosSinCambiosRealizadosNoModificaElArchivo(qtbot, tmpdir, monkeypatch):

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: ejecutarGuardarCambiosYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo))



def verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana:Ventana, archivo:str):
    
    acero:Material = lista_registros_aceptados[1]
    ventana.input_precios[acero.nombre].setText("0")

    ventana.guardarCambios()

    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                cotizador.Material.PrecioInvalidoDescripcionDeError(acero.nombre, "0"))

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_aceptados))

def test_04_VentanaNoSePuedeColocarUnPrecioInvalidoAUnMaterial(qtbot, tmpdir, monkeypatch):

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana, archivo))
    

def verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana:Ventana, archivo:str):

    ventana.input_precios[ManoDeObra_aceptada].setText("a")

    ventana.guardarCambios()

    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("a"))

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_aceptados))


# def test_05_VentanaNoSePuedeColocarUnPrecioInvalidoAManoDeObra(qtbot, tmpdir, monkeypatch):
    
#     abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
#             lambda ventana, archivo: 
#             verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana, archivo))


# def verificarQueAlCambiarPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana:Ventana, archivo:str):
    
#     aluminio:Material = lista_registros_aceptados[0]
#     ventana.input_precios[aluminio.nombre].setText("93")

#     lista_registros_modificada = lista_registros_aceptados.copy()
#     lista_registros_modificada[0] = Material(aluminio.nombre,aluminio.densidad_str(),"93")

#     ventana.guardarCambios()

#     ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
#                                             com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_modificada))

# def test_05_VentanaModificarElPrecioDeUnMaterialModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):

#     abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
#             lambda ventana, archivo: verificarQueAlCambiarPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana, archivo))

    # lista_registros_aceptados = lista_materiales_aceptados.copy()
    # lista_registros_aceptados.append(ManoDeObra_aceptada)

    # archivo = ui.crearArchivoConContenido(tmpdir, "archivo_registros.txt", 
    #                                       com_cot.pasarListaRegistrosATexto(lista_registros_aceptados))

    # ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    