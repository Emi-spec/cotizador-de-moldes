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

ManoDeObra_aceptada:ManoDeObra = ManoDeObra("35")

lista_materiales_aceptados:list[Material] = [Material("Aluminio 5083","2.8","19"),Material("Acero Amutit","8","7.5"), 
                                       Material("Acero Inoxidable","8","16")]



lista_registros_aceptados:list[RegistroDeCosto] = lista_materiales_aceptados.copy()
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


def ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana:Ventana, archivo:str, accionesYVerificaciones:Callable[[], None] ):
    ventana.guardarCambios()

    accionesYVerificaciones()

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_aceptados))


def test_03_VentanaGuardarCambiosSinCambiosRealizadosNoModificaElArchivo(qtbot, tmpdir, monkeypatch):

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda: None))



def verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana:Ventana, archivo:str):
    
    acero:Material = lista_registros_aceptados[1]
    ventana.input_precios[acero].setText("0")

    ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda: 
        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                            cotizador.Material.PrecioInvalidoDescripcionDeError(acero.nombre, "0")))


def test_04_VentanaNoSePuedeColocarUnPrecioInvalidoAUnMaterial(qtbot, tmpdir, monkeypatch):

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana, archivo))
    

def verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana:Ventana, archivo:str):

    ventana.input_precios[ManoDeObra_aceptada].setText("a")

    ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda:
        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                                cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("a")) )


def test_05_VentanaNoSePuedeColocarUnPrecioInvalidoAManoDeObra(qtbot, tmpdir, monkeypatch):
    
    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana, archivo))


def verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana:Ventana, archivo:str, registro_de_costo:RegistroDeCosto, registro_de_costo_con_precio_cambiado:RegistroDeCosto):

    lista_registros_modificada = lista_registros_aceptados.copy()

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                registro_de_costo, registro_de_costo_con_precio_cambiado)

    ventana.guardarCambios()

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_modificada))

def test_06_VentanaModificarElPrecioDeUnMaterialModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    aluminio:Material = lista_registros_aceptados[0]

    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana, archivo, 
                                        aluminio, Material(aluminio.nombre,aluminio.densidad_str(),"93")))

def test_07_VentanaModificarElPrecioDeManoDeObraModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana, archivo, 
                                                                                   ManoDeObra_aceptada, ManoDeObra("93")))

def ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana:Ventana, lista_registros:list[RegistroDeCosto],registro:RegistroDeCosto, 
        registro_con_precio_modificado:RegistroDeCosto):
    ventana.input_precios[registro].setText(registro_con_precio_modificado.precio_str())
    indice_registro = lista_registros.index(registro)
    lista_registros[indice_registro] = registro_con_precio_modificado

def verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana:Ventana, archivo:str):

    lista_registros_modificada = lista_registros_aceptados.copy()

    acero:Material = lista_registros_aceptados[1]

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, acero, Material(acero.nombre, acero.densidad_str(), "34"))
    
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, ManoDeObra_aceptada, ManoDeObra("42"))
    
    acero_2:Material = lista_registros_aceptados[2]
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                acero_2, Material(acero_2.nombre, acero_2.densidad_str(), "33"))

    ventana.guardarCambios()

    ui.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_modificada))

def test_08_VentanaModificarElPrecioDeVariosRegistrosModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana, archivo))
    

def test_09():
    