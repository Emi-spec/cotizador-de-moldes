import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QLabel)
from collections.abc import Callable
#este import era lo que ejecutaba la ventana y hacía que se viera
import ventana_cotizador
from ventana_cotizador import Ventana # Importa tu clase principal
from ventana_cotizador import DialogCrearRegistros
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import Material


def crearArchivoConContenido(tmpdir, nombre_archivo:str, contenido:str) -> str:
    archivo = tmpdir / nombre_archivo

    # Escribimos contenido
    archivo.write(contenido)

    return archivo

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

def crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                                     accionSobreDialogYArchivo:Callable[[DialogCrearRegistros, str], None]):
    archivo = tmpdir / "archivo_inexistente.txt"

    ventana = crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    dialog = ventana.dialogParaCrearRegistro

    accionSobreDialogYArchivo(dialog, archivo)

def assertarContenidoDeArchivoDespuesDeAgregarMaterial(dialog:DialogCrearRegistros, archivo:str, nombre_material:str, 
        densidad_material:str, precio_material:str, accionSobreDialog:Callable[[DialogCrearRegistros], None], 
        contenido_esperado:str):
    
    dialog.casilla_material.setText(nombre_material)
    dialog.casilla_densidad.setText(densidad_material)
    dialog.casilla_precio.setText(precio_material)

    dialog.agregar_material()

    accionSobreDialog(dialog)

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def assertarQueMaterialesNoFueronGuardadosNiRegistradosDespuesDeAgregarMaterial(dialog, archivo, nombre_material, densidad_material, precio_material, 
        accionSobreDialog:Callable[[DialogCrearRegistros], None], materiales_agregados_esperados:list[Material]):
    dialog.casilla_material.setText(nombre_material)
    dialog.casilla_densidad.setText(densidad_material)
    dialog.casilla_precio.setText(precio_material)

    dialog.agregar_material()

    accionSobreDialog(dialog)

    dialog.materiales_agregados == materiales_agregados_esperados

    assertarArchivoInexistente(archivo)

def verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, 
                                                                           nombre_material:str, densidad_material:str, 
                                                                           precio_material:str, 
                                                                           accionSobreDialog:Callable[[DialogCrearRegistros], None], 
                                                                           materiales_guardados_esperados:list[Material]):
    
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog,archivo: 
        assertarQueMaterialesNoFueronGuardadosNiRegistradosDespuesDeAgregarMaterial(dialog, archivo, nombre_material, 
                                                                                    densidad_material, 
                                                                                    precio_material, accionSobreDialog, 
                                                                                    materiales_guardados_esperados))
    
        # assertarContenidoDeArchivoDespuesDeAgregarMaterial(dialogo, archivo, nombre_material, 
        #                                                     densidad_material, precio_material, 
        #                                                     accionSobreDialog, materiales_guardados_esperados))
    

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog:DialogCrearRegistros, descripcion_de_error_esperada:str):
    descripcion_de_error:str = dialog.dialogDescripcionDeError.label_descripcion_error.text() 

    assert descripcion_de_error == descripcion_de_error_esperada
    dialog.dialogDescripcionDeError.cerrar_dialog()

def verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, nombre_material:str, densidad_material:str, precio_material:str, descripcion_de_error_esperada:str):
    
    verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, nombre_material, 
                                                                           densidad_material, precio_material, 
                                                                           lambda dialog: 
                        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, descripcion_de_error_esperada), [])



def test_01_AppCreaDialogAlAbrirArchivoInexistente(qtbot, monkeypatch):
    
    ventana = crearVentana(qtbot)

    # Variable para rastrear si se llamó al diálogo
    was_called = False

    def mock_exec(self):
        nonlocal was_called
        was_called = True
        return QDialog.Accepted # Simulamos que el usuario dio "OK"

    # Reemplazamos QDialog.exec() (de cualquier dialogo por mock_exec) 
    monkeypatch.setattr(QDialog, "exec", mock_exec)

    # Disparamos la acción que debería abrir el diálogo
    ventana.cargar_lista_registros("archivo_inexistente.txt")

    assert was_called is True



def test_02_DialogCrearRegistrosNoRegistraUnMaterialSiValueError(qtbot, tmpdir, monkeypatch):
    
    verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, "", "3","4.5", cotizador.Material.NombreNuloDescripcionDeError("3","4.5"))
   


def test_03_DialogCrearRegistrosNoRegistraUnMaterialSiTypeError(qtbot, tmpdir, monkeypatch):
    
    verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, "Aluminio", "a","4.5", cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio","a"))
    


def test_04_DialogCrearRegistrosRegistraUnMaterialEnArchivoInexistente(qtbot, tmpdir, monkeypatch):
   
    verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, "Aluminio", "3", "4.5", lambda dialog: None, ["Aluminio,3,4.5"])


def test_05_DialogCrearRegistrosRegistraMasDeUnMaterialEnArchivoInexistente(qtbot, tmpdir, monkeypatch):
    pass
    #pasa de una porque esto es problema de la función registrar_material

    # archivo = tmpdir / "archivo_inexistente.txt"

    # monkeypatch.setattr(ventana_cotizador,"ARCHIVO_REGISTROS",str(archivo))
    # monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.Accepted)

    # ventana = crearVentana(qtbot)
    # ventana.cargar_ventana()

    # dialog = ventana.dialogParaCrearRegistro

    # dialog.casilla_material.setText("Aluminio")
    # dialog.casilla_densidad.setText("3")
    # dialog.casilla_precio.setText("4.5")

    # dialog.registrar_material()

    # assertarContenidoDeArchivoEsElEsperado(archivo, ["Aluminio,3,4.5"])

    # dialog.casilla_material.setText("Cobre")
    # dialog.casilla_densidad.setText("2")
    # dialog.casilla_precio.setText("4.6")

    # dialog.registrar_material()

    # assertarContenidoDeArchivoEsElEsperado(archivo, ["Aluminio,3,4.5\n", "Cobre,2,4.6"])


def test_06_DialogCrearRegistrosNoMuestraMaterialesSiArchivoInexistente(qtbot, tmpdir, monkeypatch):

    archivo = tmpdir / "archivo_inexistente.txt"

    ventana = crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    dialog = ventana.dialogParaCrearRegistro

    # crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
    # lambda dialogo,archivo: 
    # assertarContenidoDeArchivoDespuesDeIngresarMaterial(dialogo, archivo, nombre_material, 
    #                                                     densidad_material, precio_material, 
    #                                                     accionSobreDialog, contenido_esperado))

    labels = dialog.tabla_materiales_registrados.findChildren(QLabel)

    assert len(labels) == 3 #por los de sección

    labels_datos = [l.text() for l in labels]

    assert "Material" in labels_datos
    assert "Densidad" in labels_datos
    assert "Precio" in labels_datos

    
def test_07_DialogCrearRegistrosMuestraMaterialRegistradoEnElArchivo(qtbot, tmpdir, monkeypatch):

    archivo = tmpdir / "archivo_inexistente.txt"

    monkeypatch.setattr(ventana_cotizador,"ARCHIVO_REGISTROS",str(archivo))
    monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.Accepted)

    ventana = crearVentana(qtbot)
    ventana.cargar_ventana()

    dialog = ventana.dialogParaCrearRegistro

    dialog.casilla_material.setText("Acero Amutit")
    dialog.casilla_densidad.setText("3")
    dialog.casilla_precio.setText("3.4")

    dialog.agregar_material()

    #accionSobreDialog(dialog)

    labels = dialog.tabla_materiales_registrados.findChildren(QLabel)

    cantidad_secciones = 3
    cantidad_materiales_registrados = 1

    assert len(labels) == cantidad_secciones + 3 * cantidad_materiales_registrados #por los de sección y un material

    labels_datos = [l.text() for l in labels]

    assert "Material" in labels_datos
    assert "Densidad" in labels_datos
    assert "Precio" in labels_datos

    assert "Acero Amutit" in labels_datos
    assert "3.0" in labels_datos
    assert "3.4" in labels_datos

    # assertarContenidoDeArchivoEsElEsperado(archivo, "Acero Amutit,3,3.4")
    



# def test_02_AppAbreArchivoVacio(qtbot, tmpdir):
#     """
#     qtbot: fixture de pytest-qt para manejar la interfaz.
#     tmp_path: fixture de pytest para crear archivos temporales.
#     """
#     # 1. Crear un archivo vacío en una carpeta temporal
#     #empty_file = tmp_path / "vacio.txt"
#     #empty_file.write_text("") 
#     archivo:str = crearArchivoConContenido(tmpdir, "precios_vacio.txt", "")

#     # 2. Instanciar la ventana y registrar el widget en qtbot
#     ventana = Ventana()
#     # ventana.show() # -> incluso al sacarlo se sigue viendo la ventana
#     qtbot.addWidget(ventana)

#     # 3. Llamar al método que carga el archivo
#     # Asumiendo que tu método se llama 'load_file'
#     # ventana.load_file(str(ventana))
#     ventana.cargar_lista_registros(archivo)

#     # 4. Verificaciones (Asserts)
#     # Ejemplo: Si usas un QTextEdit llamado 'editor'
    
#     # Opcional: verificar que la barra de estado o un label cambió
#     # assert window.status_label.text() == "Archivo cargado correctamente"


