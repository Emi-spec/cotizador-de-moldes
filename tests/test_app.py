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


def ingresarInputMaterial(dialog:DialogCrearRegistros, input_nombre:str, input_densidad:str, input_precio:str):
    dialog.input_material.setText(input_nombre)
    dialog.input_densidad.setText(input_densidad)
    dialog.input_precio.setText(input_precio)

    dialog.agregar_material()      

def ingresarInputYEjecutarDialog(dialog:DialogCrearRegistros, input_nombre:str, input_densidad:str, input_precio:str, 
        accionesSobreDialog:Callable[[DialogCrearRegistros], None]):
    
    ingresarInputMaterial(dialog, input_nombre, input_densidad, input_precio)

    accionesSobreDialog(dialog)


def agregarMaterial(dialog:DialogCrearRegistros, material:Material):
    ingresarInputMaterial(dialog, material.nombre, material.densidad_str(), material.precio_str())

def agregarMaterialYRealizarAcciones(dialog:DialogCrearRegistros, material:Material, 
                                     accionesSobreDialog:Callable[[DialogCrearRegistros], None]):

    ingresarInputYEjecutarDialog(dialog, material.nombre, material.densidad_str(), 
                                 material.precio_str(), accionesSobreDialog)    


def assertarContenidoDeArchivoDespuesDeAgregarMaterial(dialog:DialogCrearRegistros, archivo:str, material:Material, 
                                                       accionesSobreDialog:Callable[[DialogCrearRegistros], None], 
                                                       contenido_esperado:str):
    
    agregarMaterialYRealizarAcciones(dialog, material, accionesSobreDialog)

    assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)

def assertarArchivoInexistente(archivo:str):
    assert not archivo.exists()

def verificarQueNoHayaMaterialesRegistradosPeroEstenAgregadosLosEsperados(dialog:DialogCrearRegistros, 
                                                                          materiales_agregados_esperados:list[Material], 
                                                                          archivo:str):
    dialog.materiales_agregados == materiales_agregados_esperados

    assertarArchivoInexistente(archivo)

def verificarQueMaterialesFueronGuardadosPeroNoRegistradosDespuesDeAgregarMaterial(dialog:DialogCrearRegistros, 
                                                                                   archivo:str, material:Material, 
        accionesSobreDialog:Callable[[DialogCrearRegistros], None], materiales_agregados_esperados:list[Material]):

    agregarMaterialYRealizarAcciones(dialog, material, accionesSobreDialog)

    verificarQueNoHayaMaterialesRegistradosPeroEstenAgregadosLosEsperados(dialog, materiales_agregados_esperados, archivo)


def verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, 
                                                                           material:Material, 
                                                                           accionSobreDialog:Callable[[DialogCrearRegistros], None], 
                                                                           materiales_guardados_esperados:list[Material]):
    
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog,archivo: 
        verificarQueMaterialesFueronGuardadosPeroNoRegistradosDespuesDeAgregarMaterial(dialog, archivo, material, 
                                                                                       accionSobreDialog, 
                                                                                       materiales_guardados_esperados))
    
        # assertarContenidoDeArchivoDespuesDeAgregarMaterial(dialogo, archivo, nombre_material, 
        #                                                     densidad_material, precio_material, 
        #                                                     accionSobreDialog, materiales_guardados_esperados))
    

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog:DialogCrearRegistros, descripcion_de_error_esperada:str):
    descripcion_de_error:str = dialog.dialogDescripcionDeError.label_descripcion_error.text() 

    assert descripcion_de_error == descripcion_de_error_esperada
    dialog.dialogDescripcionDeError.cerrar_dialog()


def verificarQueNoSeAgregaronMaterialesNiExistaArchivo(dialog:DialogCrearRegistros, archivo:str, input_nombre:str, 
                                                       input_densidad:str, input_precio:str, 
                                                       descripcion_de_error_esperada:str):
    
    ingresarInputYEjecutarDialog(dialog, input_nombre, input_densidad, input_precio, 
                                 lambda dialog: 
                    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, descripcion_de_error_esperada))

    verificarQueNoHayaMaterialesRegistradosPeroEstenAgregadosLosEsperados(dialog, [], archivo)

def verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, input_nombre:str, input_densidad:str, 
                                   input_precio:str, descripcion_de_error_esperada:str):
    
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog,archivo: 
        verificarQueNoSeAgregaronMaterialesNiExistaArchivo(dialog, archivo, input_nombre, input_densidad, input_precio, 
                                            descripcion_de_error_esperada))



    # verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, nombre_material, 
    #                                                                        densidad_material, precio_material, 
    #                                                                        lambda dialog: 
    #                     verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, descripcion_de_error_esperada), [])


#test data
def lista_materiales_aceptados() -> list[Material]:
    material_1 = Material("Acero Amutit", "3", "3.4")
    material_2 = Material("Cobre berilio", "3", "4.5")
    material_3 = Material("Aluminio 5083", "4", "2.3")

    return [material_1, material_2, material_3]



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
    
    verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, "", "3","4.5", 
                                   cotizador.Material.NombreNuloDescripcionDeError("3","4.5"))
   


def test_03_DialogCrearRegistrosNoRegistraUnMaterialSiTypeError(qtbot, tmpdir, monkeypatch):
    
    verificarQueNoSeAgregoMaterial(qtbot, tmpdir, monkeypatch, "Aluminio", "a","4.5", 
                                   cotizador.Material.DensidadInvalidaDescripcionDeError("Aluminio","a"))
    

def test_04_DialogCrearRegistrosAgregaUnMaterialEnArchivoInexistente(qtbot, tmpdir, monkeypatch):
   
    material = Material("Aluminio", "3", "4.5")
    verificarQueAlAgregarMaterialYAccionarDialogLosMaterialesAgregadosSean(qtbot, tmpdir, monkeypatch, 
                                                                           material, 
                                                                           lambda dialog: None, [material])


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


def test_06_DialogCrearRegistrosNoMuestraMaterialesSiArchivoInexistente(qtbot, tmpdir, monkeypatch):

    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                                     lambda dialog, archivo: 
                        verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog, 0))


def verificarQueSeMuestranLosMaterialesAgregados(dialog, materiales_agregados_esperados:list[Material]):
    labels_datos = verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog, len(materiales_agregados_esperados))

    for material in materiales_agregados_esperados:
        assert material.nombre in labels_datos
        assert material.densidad_str() in labels_datos
        assert material.precio_str() in labels_datos


def agregarMaterialesYVerificarQueFueronGuardadosYMostrados(dialog:DialogCrearRegistros, archivo:str, 
                                                            materiales_a_agregar:list[Material]):

    for index,material in enumerate(materiales_a_agregar):
        verificarQueMaterialesFueronGuardadosPeroNoRegistradosDespuesDeAgregarMaterial(dialog, 
                                                                                   archivo, 
                                                                                   material,
                                                                                   lambda dialog: None, 
                                                                                   materiales_a_agregar[:index+1])
        
        verificarQueSeMuestranLosMaterialesAgregados(dialog,  materiales_a_agregar[:index+1])

def agregarMaterialesAceptadosYVerificarQueSonGuardadosYMostrados(dialog:DialogCrearRegistros, archivo:str):
    agregarMaterialesYVerificarQueFueronGuardadosYMostrados(dialog, archivo, lista_materiales_aceptados())

def test_07_DialogCrearRegistrosMuestraMaterialesAgregados(qtbot, tmpdir, monkeypatch):

    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                                     lambda dialog, archivo:
                                    agregarMaterialesAceptadosYVerificarQueSonGuardadosYMostrados(dialog, archivo)) 


def verificarQueNoSePuedenAgregarDosMaterialesDeMismoNombre(dialog:DialogCrearRegistros, archivo:str):
    material = Material("Acero Amutit", "3", "3.4")

    verificarQueMaterialesFueronGuardadosPeroNoRegistradosDespuesDeAgregarMaterial(dialog, 
                                                                                   archivo, 
                                                                                   material,
                                                                                   lambda dialog: None, 
                                                                                   [material])
    
    verificarQueMaterialesFueronGuardadosPeroNoRegistradosDespuesDeAgregarMaterial(dialog, archivo,
                                                                                   material,
                    lambda dialog: 
                    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, 
                    DialogCrearRegistros.materialYaRegistradoDeMismoNombreDescripcionDeError(material.nombre)), 
                                                                        [material])

def test_08_DialogCrearRegistrosNoRegistraDosMaterialesDelMismoNombre(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: verificarQueNoSePuedenAgregarDosMaterialesDeMismoNombre(dialog, archivo))

def VerificarQueSaltaDialogDeErrorConDescripcionAlGuardar(dialog:DialogCrearRegistros, descripcion_de_error_esperada:str):
    dialog.guardarTodoYCerrar()
    verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, descripcion_de_error_esperada)


def test_09_DialogCrearRegistroNoRegistraSinMaterialesAgregados(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: 
        VerificarQueSaltaDialogDeErrorConDescripcionAlGuardar(dialog, 
                                    DialogCrearRegistros.noHayMaterialesAgregadosParaRegistrarDescripcionDeError()))


def verificarQueDialogLanceErrorAlGuardarMaterialesSinPrecioManoDeObra(dialog:DialogCrearRegistros, archivo:str):
    agregarMaterialesAceptadosYVerificarQueSonGuardadosYMostrados(dialog, archivo)
    VerificarQueSaltaDialogDeErrorConDescripcionAlGuardar(dialog, 
                                                          DialogCrearRegistros.noSePuedeGuardarSinUnPrecioDeManoDeObra())


def test_10_DialogCrearRegistroNoRegistraSinPrecioDeManoDeObraAsignado(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: verificarQueDialogLanceErrorAlGuardarMaterialesSinPrecioManoDeObra(dialog, archivo))


# def yyy(dialog, archivo):
#     agregarMaterial(dialog, Material("Aluminio","3.4","3"))
#     agregarMaterial(dialog, Material("Acero","3.4","4"))

#     dialog.input_costo_mano_de_obra.setText("3")

#     dialog.guardarTodoYCerrar()

#     assertarContenidoDeArchivoEsElEsperado(archivo, ["Aluminio,3.4,3\n","acero,3.4,4\n","mano de obra,3"])

# def test_11_DialogCrearRegistroRegistraMaterialesAgregadosYManoDeObra(qtbot, tmpdir, monkeypatch):
#     crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
#         lambda dialog, archivo: yyy(dialog, archivo))


#def test_09_DialogCrearRegistrosRegistraSinAgregarMaterial():
    
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


#No hacer el scroll porque no hace falta, max 10 materiales 