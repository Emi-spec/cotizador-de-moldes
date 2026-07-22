from . import (QDialog, QLabel, Callable, Ventana, RegistroDeCosto, DialogDescripcionDeError, QFileDialog, 
DialogCrearRegistros, cotizador, Material, ManoDeObra, ventana_cotizador)

import tests.funciones_comunes_cotizador as com_cot

def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = tmpdir / nombre_archivo

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def crearVentana(qtbot) -> Ventana:
    ventana = Ventana()
    # ventana.show() # -> incluso al sacarlo se sigue viendo la ventana
    qtbot.addWidget(ventana)

    return ventana

def crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo:str, monkeypatch) -> Ventana:
    
    monkeypatch.setattr(ventana_cotizador,"ARCHIVO_REGISTROS",str(archivo))
    monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.Accepted)

    ventana = crearVentana(qtbot)
    ventana.cargar_ventana()

    #tiene que devolver la ventana y no el dialogo poruqe si destruye la ventana destruye el dialogo también
    return ventana

def crearArchivoInexistenteConDireccion(tmpdir) -> str:
    return tmpdir / "archivo_inexistente.txt"

def simularExecDeDialogCrearRegistrosCon(monkeypatch, reemplazo_de_exec:Callable[[], None]):
    # Interceptamos el método exec del diálogo para simular la carga del usuario
    def mock_exec(dialog_self):
        reemplazo_de_exec(dialog_self)
        return QDialog.Accepted # Simulamos que el usuario dio "OK"

   # # Reemplazamos QDialog.exec() (de cualquier dialogo por mock_exec)
    monkeypatch.setattr(DialogCrearRegistros, "exec", mock_exec)


def verificarQueDialogCrearRegistrosSeEjecuteHaciendo(monkeypatch, accionQueDisparaDialog:Callable[[], None]):
    # Variable para rastrear si se llamó al diálogo
    was_called = False

    # 1. Definimos una función normal en lugar de la lambda
    def registrar_llamada():
        nonlocal was_called
        was_called = True

    simularExecDeDialogCrearRegistrosCon(monkeypatch, lambda dialog_self: registrar_llamada())

    # Disparamos la acción que debería abrir el diálogo
    accionQueDisparaDialog()

    assert was_called

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialogDescripcionDeError:DialogDescripcionDeError, descripcion_de_error_esperada:str):
    descripcion_de_error:str = dialogDescripcionDeError.label_descripcion_error.text() 

    assert descripcion_de_error == descripcion_de_error_esperada
    dialogDescripcionDeError.cerrar_dialog()


ManoDeObra_aceptada:ManoDeObra = ManoDeObra("35")

def abrirVentanaLeyendoDeArchivoConRegistrosAceptadosYRealizar(qtbot, tmpdir, monkeypatch, 
                                                               accionesYVerificaciones:Callable[[Ventana, str], None]):
    archivo = crearArchivoConContenido(tmpdir, "archivo_registros.txt", 
                                          com_cot.pasarListaRegistrosATexto(com_cot.lista_registros_aceptada))

    ventana = crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    accionesYVerificaciones(ventana, archivo)


#dialog
def ingresarInputMaterial(dialog:DialogCrearRegistros, input_nombre:str, input_densidad:str, input_precio:str):
    dialog.input_material.setText(input_nombre)
    dialog.input_densidad.setText(input_densidad)
    dialog.input_precio.setText(input_precio)

    dialog.agregar_material()    

def agregarMaterial(dialog:DialogCrearRegistros, material:Material):
    ingresarInputMaterial(dialog, material.nombre, material.densidad_str(), material.precio_str())


def registrarListaMaterialesEInputManoDeObra(dialog, lista_materiales:list[Material], input_costo_de_mano_de_obra:str):

    if(lista_materiales == []): raise ValueError("No se puede ingresar lista vacia en registrarListaMaterialesEInputManoDeObra")

    for material in lista_materiales:
        agregarMaterial(dialog, material)

    dialog.input_costo_mano_de_obra.setText(input_costo_de_mano_de_obra)

    dialog.guardarTodoYCerrar()


def verificarQueLosRegistrosDeCostoAceptadosSeRegistrenCorrectamente(dialog, archivo):

    registrarListaMaterialesEInputManoDeObra(dialog, com_cot.lista_materiales_aceptada, 
                                             com_cot.mano_de_obra_aceptada.precio_str())

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, 
                                com_cot.pasarListaRegistrosALineasParaArchivo(com_cot.lista_registros_aceptada))


def verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog:DialogCrearRegistros, 
                                                        cantidad_de_materiales_agregados_esperados:int) -> list[str]:
    labels = dialog.tabla_materiales_registrados.findChildren(QLabel)

    cantidad_secciones = 3

    assert len(labels) == cantidad_secciones + 3 * cantidad_de_materiales_agregados_esperados #por los de sección y un material

    labels_datos = [l.text() for l in labels]

    assert "Material" in labels_datos
    assert "Densidad (Kg/dm3)" in labels_datos
    assert "Precio (US$)" in labels_datos

    return labels_datos

def verificarQueSeReseteaLaTablaDeMaterialesAlGuardar(qtbot, dialog, archivo):
    verificarQueLosRegistrosDeCostoAceptadosSeRegistrenCorrectamente(dialog, archivo)
    qtbot.wait(10)
    verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog, 0)

    assert dialog.input_material.text() == ""
    assert dialog.input_densidad.text() == ""
    assert dialog.input_precio.text() == ""
    assert dialog.input_costo_mano_de_obra.text() == ""

    assert dialog.accepted 