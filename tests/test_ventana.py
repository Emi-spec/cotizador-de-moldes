import tests.funciones_comunes_UI as ui
import tests.funciones_comunes_cotizador as com_cot

from . import (QDialog, QLabel, QLineEdit, Callable, Ventana, RegistroDeCosto, QComboBox, QWidget, QLayout, QFileDialog,
DialogCrearRegistros, cotizador, Material, ManoDeObra, ventana_cotizador, NivelDeDificultad, 
nivelDeDificultadBajo, nivelDeDificultadMedio, nivelDeDificultadAlto, nivelDeDificultadMuyAlto, nivelDeDificultadEspeciales)



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



# lista_registros_aceptada:list[RegistroDeCosto] = lista_materiales_aceptados.copy()
# lista_registros_aceptada.append(ManoDeObra_aceptada)

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
#                                           com_cot.pasarListaRegistrosATexto(com_cot.lista_registros_aceptada))

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
        verificarQueSeMuestranLosMaterialesAgregados(ventana, com_cot.lista_materiales_aceptada, ManoDeObra_aceptada))



def test_01_1_ventanaProyectaLosRegistrosRecienRegistradosPorDialogCrearRegistros(qtbot, tmpdir, monkeypatch):

    archivo = ui.crearArchivoInexistenteConDireccion(tmpdir)

    # # Aplicamos el parche al DialogCrearRegistros antes de crear la ventana
    ui.simularExecDeDialogCrearRegistrosCon(monkeypatch, lambda dialog_self: 
                        ui.registrarListaMaterialesEInputManoDeObra(dialog_self, com_cot.lista_materiales_aceptada, 
                                                                    com_cot.mano_de_obra_aceptada.precio_str()))

    # Ahora sí, creamos la ventana. Al intentar abrir el diálogo, correrá nuestro parche
    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)
    qtbot.addWidget(ventana)

    # 3. Verificamos que el archivo se creó correctamente en el disco
    com_cot.assertarContenidoDeArchivoEsElEsperado(
        archivo, 
        com_cot.pasarListaRegistrosALineasParaArchivo(com_cot.lista_registros_aceptada)
    )

    # 4. Verificamos que la ventana se enteró y dibujó los controles correspondientes
    verificarQueSeMuestranLosMaterialesAgregados(
        ventana, 
        com_cot.lista_materiales_aceptada, 
        com_cot.mano_de_obra_aceptada
    )  


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
                                            com_cot.pasarListaRegistrosALineasParaArchivo(com_cot.lista_registros_aceptada))


def test_03_VentanaGuardarCambiosSinCambiosRealizadosNoModificaElArchivo(qtbot, tmpdir, monkeypatch):

    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
            ejecutarGuardarCambiosYAccionesYVerificarQueElContenidoDeArchivoEstaIgual(ventana, archivo, lambda: None))



def verificarQueLanzamientoDeErrorAlPonerPrecioInvalidoAUnRegistro(ventana:Ventana, archivo:str):
    
    acero:Material = com_cot.lista_registros_aceptada[1]
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

    lista_registros_modificada = com_cot.lista_registros_aceptada.copy()

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                registro_de_costo, registro_de_costo_con_precio_cambiado)

    verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana, archivo, 
                                                                                lista_registros_modificada)

def test_06_VentanaModificarElPrecioDeUnMaterialModificaSuPrecioEnElArchivo(qtbot, tmpdir, monkeypatch):
    
    aluminio:Material = com_cot.lista_registros_aceptada[0]

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

    lista_registros_modificada = com_cot.lista_registros_aceptada.copy()

    acero:Material = com_cot.lista_registros_aceptada[1]

    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                                                acero, Material(acero.nombre, acero.densidad_str(), "34"))
    
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                                                                 ManoDeObra_aceptada, ManoDeObra("42"))
    
    acero_2:Material = com_cot.lista_registros_aceptada[2]
    ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
                                acero_2, Material(acero_2.nombre, acero_2.densidad_str(), "33"))

    verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana, archivo, 
                                                                                        lista_registros_modificada)

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


def ingresarInputsYCotizar(ventana:Ventana, input_altura:str, input_volumen:str, input_distancia_centros:str, 
                           input_ancho_mitad:str, indice_desicion_mascaras_troqueles:int, 
                           index_material_postizos_cuerpo:int, index_material_postizos_cuello:int, 
                           index_material_postizos_fondo:int, index_material_placas_respaldo:int, 
                           index_material_prensamangas:int, hay_opcion_elegida:bool):
    
    ventana.empezarCotizacion()

    ventana.input_altura_envase.setText(input_altura)
    ventana.input_volumen_envase.setText(input_volumen)
    ventana.input_distancia_centros.setText(input_distancia_centros)
    ventana.input_ancho_mitad.setText(input_ancho_mitad)
    ventana.input_mascaras_troqueles.setCurrentIndex(indice_desicion_mascaras_troqueles)
    
    ventana.input_postizos_cuerpo.setCurrentIndex(index_material_postizos_cuerpo)
    ventana.input_postizos_cuello.setCurrentIndex(index_material_postizos_cuello)
    ventana.input_postizos_fondo.setCurrentIndex(index_material_postizos_fondo)
    ventana.input_placas_respaldo.setCurrentIndex(index_material_placas_respaldo)
    ventana.input_prensamangas.setCurrentIndex(index_material_prensamangas)

    ventana.opcion_nivel_bajo.setChecked(hay_opcion_elegida)
    #if (ventana.lista_registros[0].tieneComoNombre("Aluminio 5083")): breakpoint()
    ventana.cotizar()


def ingresarInputsYCotizarSinElegirMateriales(ventana:Ventana, input_altura:str, input_volumen:str, 
                                              input_distancia_centros:str, input_ancho_mitad:str, 
                                              indice_desicion_mascaras_troqueles:int, hay_opcion_dificultad_elegida:bool):
    
    ingresarInputsYCotizar(ventana, input_altura, input_volumen, input_distancia_centros, 
                           input_ancho_mitad, indice_desicion_mascaras_troqueles, 0, 0, 0, 0, 0, hay_opcion_dificultad_elegida)

def verificarLanzamientoDeErrorAlIngresarInputsSinElegirMateriales(ventana:Ventana, input_altura:str, input_volumen:str, 
                                             input_distancia_centros:str,
                                             input_ancho_mitad:str, hay_opcion_dificultad_elegida:bool, 
                                             descripcion_de_error_esperada:str):
    
    ingresarInputsYCotizarSinElegirMateriales(ventana, input_altura, input_volumen, input_distancia_centros, 
                            input_ancho_mitad, hay_opcion_dificultad_elegida, hay_opcion_dificultad_elegida)

    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(ventana, descripcion_de_error_esperada)


def verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana:Ventana, input_altura:str, input_volumen:str, input_distancia_centros:str, 
                                           input_ancho_mitad:str, descripcion_de_error_esperada:str):
    
    verificarLanzamientoDeErrorAlIngresarInputsSinElegirMateriales(ventana, input_altura, input_volumen, 
                                                                   input_distancia_centros, 
                                          input_ancho_mitad, True, descripcion_de_error_esperada)


def verificarLanzamientoDeErrorAlIngresarAlturaInvalida(ventana:Ventana):
   
    verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "", "10", "10", "10", 
                                          cotizador.alturaDeEnvaseInvalidaDescripcionDeError(""))
                                                


def test_10_NoSePuedeCotizarConAlturaDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarAlturaInvalida(ventana))
    
def verificarLanzamientoDeErrorAlIngresarVolumenInvalido(ventana:Ventana):
    verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "-10", "10", "10", 
                                          cotizador.volumenDeEnvaseInvalidoDescripcionDeError("-10"))

def test_11_NoSePuedeCotizarConAlturaDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarVolumenInvalido(ventana))
    
def test_12_NoSePuedeCotizarConDistanciaEntreCentrosDelEnvaseInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "10", "1,", "10", 
                                                 cotizador.distanciaEntreCentrosInvalidaDescripcionDeError("1,")))
    
def test_13_NoSePuedeCotizarConAnchoPorMitadDelMoldeInvalida(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlIngresarMedidaInvalida(ventana, "10", "10", "10", "0", 
                                                 cotizador.anchoPorMitadDelMoldeInvalidoDescripcionDeError("0")))
    
def verificarLanzamientoDeErrorAlNoElegirNivelDeDificultad(ventana:Ventana):
    verificarLanzamientoDeErrorAlIngresarInputsSinElegirMateriales(ventana, "10", "10", "10", "10", False,
                            cotizador.NoSeEligioUnNivelDeDificultadDelEnvaseDescripcionDeError())
    

def test_14_NoSePuedeCotizarSinNivelDeDificultadDelEnvaseElegido(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: 
           verificarLanzamientoDeErrorAlNoElegirNivelDeDificultad(ventana))
    

def pasarContenidoComboBoxAListaStrings(comboBox:QComboBox):
   return [comboBox.itemText(i) for i in range(comboBox.count())]

def pasarListaRegistrosAListaNombresMateriales(lista_registros:list[RegistroDeCosto]):
    return [registro.nombre for registro in lista_registros if registro.esMaterial()]

def verificarQueMenusDesplegablesMuestrenMaterialesRegistrados(ventana:Ventana):
    ventana.empezarCotizacion()

    lista_nombres_materiales = pasarListaRegistrosAListaNombresMateriales(ventana.lista_registros)

    assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_postizos_cuerpo)
    assert  lista_nombres_materiales== pasarContenidoComboBoxAListaStrings(ventana.input_postizos_cuello)
    assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_postizos_fondo)
    assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_placas_respaldo)
    assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_prensamangas)

def test_15_VerificarQueLosComboBoxDeLosMaterialesAElegirMuestrenLosMaterialesCorrectos(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: verificarQueMenusDesplegablesMuestrenMaterialesRegistrados(ventana))


def obtener_widgets_layout(layout:QLayout) -> list[QWidget]:
    widgets = []

    for i in range(layout.count()):
        item = layout.itemAt(i)

        if item.widget():
            widgets.append(item.widget())

        elif item.layout():
            widgets.extend(obtener_widgets_layout(item.layout()))

    return widgets

def obtener_labels_layout(layout:QLayout) -> list[QWidget]:
    labels = []

    for i in range(layout.count()):
        item = layout.itemAt(i)

        if item.widget():
            if isinstance(item.widget(), QLabel):
                labels.append(item.widget())

        elif item.layout():
            labels.extend(obtener_labels_layout(item.layout()))

    return labels


def verificarQueSeMuestrenCorrectamenteLosResultadosDeCotizacionConLosMaterialesElegidos(ventana:Ventana, 
                                                    material_post_cuerpo:Material, material_post_cuello:Material, 
        material_post_fondo:Material, mat_placas_respaldo:Material, material_post_prensamangas:Material):
    
    hijos = obtener_widgets_layout(ventana.layout_general)
                
                             # boton guardar
    assert len(hijos) == 1 + 1
    assert type(hijos[0]) == QLabel

    hijo_datos = hijos[0].text()

    assert hijo_datos == cotizador.cotizarEnBaseA(1, 1, True, 10, 10, 10, 10, nivelDeDificultadBajo,
            material_post_cuerpo, material_post_cuello, material_post_fondo, mat_placas_respaldo,
            material_post_prensamangas, com_cot.lista_materiales_aceptada, 
            com_cot.mano_de_obra_aceptada).imprimirResultado()

def verificarQueLosResultadosDeLaCotizacionSeMuestrenCorrectamente(ventana:Ventana):

    ingresarInputsYCotizarSinElegirMateriales(ventana, "10", "10", "10", "10", 0, True)

    primer_material = com_cot.lista_materiales_aceptada[0]

    verificarQueSeMuestrenCorrectamenteLosResultadosDeCotizacionConLosMaterialesElegidos(ventana, primer_material, 
                                                                                         primer_material, primer_material, 
                                                                                         primer_material, primer_material)

  
def test_17VerificarQueAlPresionarCotizarSeMuestreElResultadoDeLaCotizacion(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: verificarQueLosResultadosDeLaCotizacionSeMuestrenCorrectamente(ventana))
    
def verificarQueResultadoCotizacionSeaCorrectoColocandoUnSoloAluminio5083(ventana):
    ingresarInputsYCotizar(ventana, "10", "10", "10", "10", 0, 1, 0, 0, 0, 0, True)

    primer_material = com_cot.lista_materiales_aceptada[0]
    aluminio_5083 = com_cot.lista_materiales_aceptada[1]

    verificarQueSeMuestrenCorrectamenteLosResultadosDeCotizacionConLosMaterialesElegidos(ventana, aluminio_5083, 
                                                primer_material, primer_material, primer_material, primer_material)


#Lo saqué porque depende del cálculo de cotización

# def yyy(ventana:Ventana, archivo:str):

#     #verificarQueAlCambiarElPrecioDeVariosRegistrosSeModificanSusPreciosEnElArchivo(ventana, archivo)
#     lista_registros_modificada = com_cot.lista_registros_aceptada.copy()

#     acero:Material = com_cot.lista_registros_aceptada[1]

#     ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
#                                                                 acero, Material(acero.nombre, acero.densidad_str(), "34"))
    
#     ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
#                                                                                  ManoDeObra_aceptada, ManoDeObra("42"))
    
#     acero_2:Material = com_cot.lista_registros_aceptada[2]
#     ingresarInputPrecioModificadoYCambiarElPrecioDelRegistroEnLaListaDeRegistros(ventana, lista_registros_modificada, 
#                                 acero_2, Material(acero_2.nombre, acero_2.densidad_str(), "33"))

#     verificarQueAlGuardarCambiosLasListasDeRegistrosYElContenidoDelArchivoSeaElEsperado(ventana, archivo, 
#                                                                                         lista_registros_modificada)
#     #fin funcion

#     #funcion
#     ventana.empezarCotizacion()

#     lista_nombres_materiales = pasarListaRegistrosAListaNombresMateriales(lista_registros_modificada)

#     assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_postizos_cuerpo)
#     assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_postizos_cuello)
#     assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_postizos_fondo)
#     assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_placas_respaldo)
#     assert lista_nombres_materiales == pasarContenidoComboBoxAListaStrings(ventana.input_prensamangas)

#     #fin funcion 

#     #verificarQueResultadoCotizacionSeaCorrectoColocandoUnSoloAluminio5083
#     ingresarInputsYCotizar(ventana, "10", "10", "10", "10", 0, 2, 0, 0, 0, 0, True)

#     primer_material = lista_registros_modificada[0]
#     acero_2 = lista_registros_modificada[2]

#     verificarQueSeMuestrenCorrectamenteLosResultadosDeCotizacionConLosMaterialesElegidos(ventana, acero_2, 
#                                                 primer_material, primer_material, primer_material, primer_material)


# def test_18_xxx(qtbot, tmpdir, monkeypatch):
#     ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
#             lambda ventana, archivo: yyy(ventana, archivo))



def verificarQueElResultadoDeCotizacionSeGuardeCorrectamente(ventana, tmpdir, monkeypatch):

    verificarQueLosResultadosDeLaCotizacionSeMuestrenCorrectamente(ventana)

    lista_labels:list[QWidget] = obtener_labels_layout(ventana.layout_general)
    
    impresion_resultado = lista_labels[0].text() 

    impresion_resultado = cotizador.cotizarEnBaseA(1, 1, True, 10, 10, 10, 10, nivelDeDificultadBajo,
        ventana.lista_materiales[0], ventana.lista_materiales[0], ventana.lista_materiales[0], 
        ventana.lista_materiales[0], ventana.lista_materiales[0], com_cot.lista_materiales_aceptada, 
        com_cot.mano_de_obra_aceptada).imprimirResultado()

    def mock_getSaveFileName(dialog_self, como_guardar_archivo:str, carpeta_inicial:str, filtros_iniciales:str):

        return (tmpdir/"archivito.txt", "Archivos de Texto (*.txt)")

    monkeypatch.setattr(QFileDialog, "getSaveFileName", mock_getSaveFileName)

    ventana.guardarEnArchivo()

    com_cot.assertarContenidoDeArchivoEsElEsperado(tmpdir/"archivito.txt", impresion_resultado.splitlines(keepends=True))


def test_19_VentanaResultadoDeCotizacionSeGuardaCorrectamente(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: verificarQueElResultadoDeCotizacionSeGuardeCorrectamente(ventana, tmpdir, monkeypatch))




def test_TestParaBuscarErrorColocarUnSoloAluminio5083(qtbot, tmpdir, monkeypatch):
    ui.abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch,                                     
            lambda ventana, archivo: verificarQueResultadoCotizacionSeaCorrectoColocandoUnSoloAluminio5083(ventana))

 
def test_TestParaBuscarErrorConArchivoPreciosReal(qtbot, tmpdir, monkeypatch):

    contenido = """Aluminio 5083,2.8,19.0
Aluminio 6061,2.8,21.5
Aluminio 7075,2.8,23.5
Acero Amutit,8.0,7.5
Acero Especial K,8.0,11.0
Acero Inoxidable,8.0,16.0
Acero SAE 4140,8.0,6.0
Cobre Berilio,9.0,110.0
Mano de obra,35.0"""

    archivo = ui.crearArchivoConContenido(tmpdir, "archivo_registros.txt", contenido)

    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    #breakpoint()
    #verificarQueResultadoCotizacionSeaCorrectoColocandoUnSoloAluminio5083(ventana)

    ingresarInputsYCotizar(ventana, "10", "10", "10", "10", 0, 0, 1, 1, 1, 1, True)

    primer_material = Material("Aluminio 6061", "2.8", "21.5")
    aluminio_5083 = Material("Aluminio 5083", "2.8", "19.0")

    verificarQueSeMuestrenCorrectamenteLosResultadosDeCotizacionConLosMaterialesElegidos(ventana, aluminio_5083, 
                                                primer_material, primer_material, primer_material, primer_material)
