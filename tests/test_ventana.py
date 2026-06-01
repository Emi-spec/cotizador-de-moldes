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

# lista_materiales_aceptados:list[Material] = [Material("Aluminio 5083","2.8","19"),Material("Acero Amutit","8","7.5"), 
#                                        Material("Acero Inoxidable","8","16")]



# lista_registros_aceptados:list[RegistroDeCosto] = lista_materiales_aceptados.copy()
# lista_registros_aceptados.append(ManoDeObra_aceptada)

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


# def abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch, 
#                                                                accionesYVerificaciones:Callable[[Ventana, str], None]):
#     archivo = ui.crearArchivoConContenido(tmpdir, "archivo_registros.txt", 
#                                           com_cot.pasarListaRegistrosATexto(ui.lista_registros_aceptados))

#     ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

#     accionesYVerificaciones(ventana, archivo)
    


def ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana:Ventana, 
                                                        lista_registros:list[RegistroDeCosto],registro:RegistroDeCosto, 
        registro_con_precio_modificado:RegistroDeCosto):
    ventana.input_precios[registro].setText(registro_con_precio_modificado.precio_str())
    indice_registro = lista_registros.index(registro)
    lista_registros[indice_registro] = registro_con_precio_modificado

#nunca debería pasar porque se abre el dialog
#def test_01_DialogCrearRegistrosNoMuestraMaterialesSiArchivoInexistente(qtbot, tmpdir, monkeypatch):

def test_01_VentanaMuestraLosRegistrosCorrectamente(qtbot, tmpdir, monkeypatch):

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch, lambda ventana, archivo: 
        verificarQueSeMuestranLosMaterialesAgregados(ventana, ui.lista_materiales_aceptados, ManoDeObra_aceptada))


# def ttt(qtbot, ventana:Ventana, archivo:str):
#     #ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)
    
    

#     verificarQueSeMuestranLosMaterialesAgregados(ventana, ui.lista_materiales_aceptados, ManoDeObra_aceptada)

# def test_01_1_ventanaProyectaLosRegistrosRecienRegistradosPorDialogCrearRegistros(qtbot, tmpdir, monkeypatch):
#     archivo = tmpdir / "archivo_inexistente.txt"

#     ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

#     ui.verificarQueSeReseteaLaTablaDeMaterialesAlGuardar(qtbot, ventana.dialogParaCrearRegistro, archivo)

#     verificarQueSeMuestranLosMaterialesAgregados(ventana, com_cot.lista_materiales_aceptada, ManoDeObra_aceptada)
  


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

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(ui.lista_registros_aceptados))


def test_03_VentanaGuardarCambiosSinCambiosRealizadosNoModificaElArchivo(qtbot, tmpdir, monkeypatch):

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda: None))



def verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana:Ventana, archivo:str):
    
    acero:Material = ui.lista_registros_aceptados[1]
    ventana.input_precios[acero].setText("0")

    ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda: 
        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                            cotizador.Material.PrecioInvalidoDescripcionDeError(acero.nombre, "0")))


def test_04_VentanaNoSePuedeColocarUnPrecioInvalidoAUnMaterial(qtbot, tmpdir, monkeypatch):

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana, archivo))
    

def verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana:Ventana, archivo:str):

    ventana.input_precios[ManoDeObra_aceptada].setText("a")

    ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda:
        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, 
                                                cotizador.ManoDeObra.PrecioInvalidoDescripcionDeError("a")) )


def test_05_VentanaNoSePuedeColocarUnPrecioInvalidoAManoDeObra(qtbot, tmpdir, monkeypatch):
    
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarLanzamientoDeErrorAlPonerPrecioInvalidoALaManoDeObra(ventana, archivo))


def verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana:Ventana, archivo:str, 
                                                                    lista_registros_modificada:list[RegistroDeCosto]):
    ventana.guardarCambios()

    assert ventana.lista_registros == lista_registros_modificada

    for registro in ventana.input_precios.keys():
        assert registro in lista_registros_modificada
    
    assert len(ventana.input_precios.keys()) == len(lista_registros_modificada)

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                            com_cot.pasarListaRegistrosALineasParaArchivo(lista_registros_modificada))

def verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana:Ventana, archivo:str, registro_de_costo:RegistroDeCosto, registro_de_costo_con_precio_cambiado:RegistroDeCosto):

    lista_registros_modificada = ui.lista_registros_aceptados.copy()

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                registro_de_costo, registro_de_costo_con_precio_cambiado)

    verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana, archivo, 
                                                                                lista_registros_modificada)

def test_06_VentanaModificarElPrecioDeUnMaterialModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    aluminio:Material = ui.lista_registros_aceptados[0]

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana, archivo, 
                                        aluminio, Material(aluminio.nombre,aluminio.densidad_str(),"93")))

def test_07_VentanaModificarElPrecioDeManoDeObraModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeUnRegistroSeModificaSuPrecioEnElArchivo(ventana, archivo, 
                                                                                   ManoDeObra_aceptada, ManoDeObra("93")))



def verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana:Ventana, archivo:str):

    lista_registros_modificada = ui.lista_registros_aceptados.copy()

    acero:Material = ui.lista_registros_aceptados[1]

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                                                acero, Material(acero.nombre, acero.densidad_str(), "34"))
    
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                                                                 ManoDeObra_aceptada, ManoDeObra("42"))
    
    acero_2:Material = ui.lista_registros_aceptados[2]
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                acero_2, Material(acero_2.nombre, acero_2.densidad_str(), "33"))

    verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana, archivo, lista_registros_modificada)

def test_08_VentanaModificarElPrecioDeVariosRegistrosModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana, archivo))
    


def verificarQueSeReseteenLosInputsAlGuardarCambios(ventana:Ventana, archivo:str):
    
    verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana,archivo)

    for registro,input in ventana.input_precios.items():

        assert input.text() == ""
        assert input.placeholderText() == registro.precio_str()

def test_09_VentanaGuardarCambiosReseteaTodosLosPrecios(qtbot, tmpdir, monkeypatch):

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            verificarQueSeReseteenLosInputsAlGuardarCambios(ventana, archivo))

# def yyy(qtbot, ventana:Ventana):
#     breakpoint()
#     ventana.empezarCotizacion()
#     qtbot.wait(10)
    
#     assert ventana.layout_general.count() == 0

# No se puede porque empezar a cotizar agrega sus propios widgets y layouts

# def test_10_VentanaEmpezarCotizacionBorraTodo(qtbot, tmpdir, monkeypatch): #????? #fijarse si están borrados los layouts
#     abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
#             lambda ventana, archivo: 
#             yyy(qtbot, ventana))

def verificarLanzamientoDeErrorAlIngresar(ventana:Ventana, input_altura:str, input_volumen:str, input_distancia_centros:str,
                                          input_ancho_mitad:str, otros_inputs:Callable[[],None], 
                                          descripcion_de_error_esperada:str):
    ventana.empezarCotizacion()

    ventana.input_altura_envase.setText(input_altura)
    ventana.input_volumen_envase.setText(input_volumen)
    ventana.input_distancia_centros.setText(input_distancia_centros)
    ventana.input_ancho_mitad.setText(input_ancho_mitad)
    otros_inputs()

    ventana.cotizar()
    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, descripcion_de_error_esperada)


def verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana:Ventana, input_altura:str, input_volumen:str, input_distancia_centros:str, 
                                          input_ancho_mitad:str, descripcion_de_error_esperada:str):
    
    verificarLanzamientoDeErrorAlIngresar(ventana, input_altura, input_volumen, input_distancia_centros, input_ancho_mitad, 
        lambda: ventana.opcion_nivel_bajo.setChecked(True), descripcion_de_error_esperada)


def verificarLanzamientoDeErrorAlIngresarAlturaInvalida(ventana:Ventana):
   
    verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "", "10", "10", "10", 
                                          cotizador.alturaDeEnvaseInvalidaDescripcionDeError(""))
                                                


def test_11_NoSePuedeCotizarConAlturaDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarAlturaInvalida(ventana))
    
def verificarLanzamientoDeErrorAlIngresarVolumenInvalido(ventana:Ventana):
    verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "-10", "10", "10", 
                                          cotizador.volumenDeEnvaseInvalidoDescripcionDeError("-10"))

def test_12_NoSePuedeCotizarConAlturaDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarVolumenInvalido(ventana))
    
def test_13_NoSePuedeCotizarConDistanciaEntreCentrosDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "10", "1,", "10", 
                                                 cotizador.distanciaEntreCentrosInvalidaDescripcionDeError("1,")))
    
def test_14_NoSePuedeCotizarConAnchoPorMitadDelMoldeInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "10", "10", "0", 
                                                 cotizador.anchoPorMitadDelMoldeInvalidoDescripcionDeError("0")))
    
def verificarLanzamientoDeErrorAlNoElegirNivelDeDificultad(ventana:Ventana):
    verificarLanzamientoDeErrorAlIngresar(ventana, "10", "10", "10", "10", 
                                    lambda: None, cotizador.NoSeEligioUnNivelDeDificultadDelEnvaseDescripcionDeError())
    

def test_15_NoSePuedeCotizarSinNivelDeDificultadDelEnvaseElegido(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlNoElegirNivelDeDificultad(ventana))

def yyy(ventana:Ventana):
    ventana.empezarCotizacion()

    ventana.input_altura_envase.setText("10")
    ventana.input_volumen_envase.setText("10")
    ventana.input_distancia_centros.setText("10")
    ventana.input_ancho_mitad.setText("10")
    ventana.input_mascaras_troqueles.setCurrentIndex(0)
    ventana.opcion_nivel_bajo.setChecked(True)

    ventana.cotizar()
    

    # verificarLanzamientoDeErrorAlIngresar(ventana, "10", "10", "10", "10", 
    #                                       lambda: ventana.input_mascaras_troqueles.setCurrentIndex(0),
    #                                       )

def test_16_Verific(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           yyy(ventana))