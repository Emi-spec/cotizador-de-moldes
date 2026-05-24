from . import (QDialog, QLabel, Callable, Ventana, RegistroDeCosto, DialogDescripcionDeError,
DialogCrearRegistros, cotizador, Material, ManoDeObra, ventana_cotizador)


def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = tmpdir / nombre_archivo

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def assertarContenidoDeArchivoEsElEsperado(archivo:str, contenido_esperado:list[str]):
    
    archivo_modificado = open(archivo,"r")
    lineas_archivo:list[str] = archivo_modificado.readlines()
    archivo_modificado.close() #CERRE EL ARCHIVO

    assert lineas_archivo == contenido_esperado

def crearVentana(qtbot) -> Ventana:
    ventana = Ventana()
    # ventana.show() # -> incluso al sacarlo se sigue viendo la ventana
    qtbot.addWidget(ventana)

    return ventana

def crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo:str, monkeypatch):
    
    monkeypatch.setattr(ventana_cotizador,"ARCHIVO_REGISTROS",str(archivo))
    monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.Accepted)

    ventana = crearVentana(qtbot)
    ventana.cargar_ventana()

    #tiene que devolver la ventana y no el dialogo poruqe si destruye la ventana destruye el dialogo también
    return ventana

def verificarQueDialogCrearRegistrosSeEjecuteHaciendo(monkeypatch, accionQueDisparaDialog:Callable[[], None]):
# Variable para rastrear si se llamó al diálogo
    was_called = False

    def mock_exec(self):
        nonlocal was_called
        was_called = True
        return DialogCrearRegistros.Accepted # Simulamos que el usuario dio "OK"

    # Reemplazamos QDialog.exec() (de cualquier dialogo por mock_exec) 
    monkeypatch.setattr(DialogCrearRegistros, "exec", mock_exec)

    # Disparamos la acción que debería abrir el diálogo
    accionQueDisparaDialog()

    assert was_called

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialogDescripcionDeError:DialogDescripcionDeError, descripcion_de_error_esperada:str):
    descripcion_de_error:str = dialogDescripcionDeError.label_descripcion_error.text() 

    assert descripcion_de_error == descripcion_de_error_esperada
    dialogDescripcionDeError.cerrar_dialog()
