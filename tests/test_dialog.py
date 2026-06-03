import tests.funciones_comunes_cotizador as com_cot
import tests.funciones_comunes_UI as ui

from . import (QDialog, QLabel, Callable, Ventana, RegistroDeCosto,
DialogCrearRegistros, cotizador, Material, ManoDeObra, ventana_cotizador)


def crearDialogSobreArchivoYEjecutarAccion(qtbot, monkeypatch, archivo:str, 
                                           accionSobreDialogYArchivo:Callable[[DialogCrearRegistros, str], None]):

    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    dialog = ventana.dialogParaCrearRegistro

    accionSobreDialogYArchivo(dialog, archivo)

def crearDialogSobreArchivoVacioYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                        accionSobreDialogYArchivo:Callable[[DialogCrearRegistros, str], None]):
    archivo = ui.crearArchivoConContenido(tmpdir, "archivo_vacio.txt", "")

    crearDialogSobreArchivoYEjecutarAccion(qtbot, monkeypatch, archivo, accionSobreDialogYArchivo)


def crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                                accionSobreDialogYArchivo:Callable[[DialogCrearRegistros, str], None]):
    archivo = ui.crearArchivoInexistenteConDireccion(tmpdir)

    crearDialogSobreArchivoYEjecutarAccion(qtbot, monkeypatch, archivo, accionSobreDialogYArchivo)
      

def ingresarInputYEjecutarDialog(dialog:DialogCrearRegistros, input_nombre:str, input_densidad:str, input_precio:str, 
        accionesSobreDialog:Callable[[DialogCrearRegistros], None]):
    
    ui.ingresarInputMaterial(dialog, input_nombre, input_densidad, input_precio)

    accionesSobreDialog(dialog)


# def agregarMaterial(dialog:DialogCrearRegistros, material:Material):
#     ingresarInputMaterial(dialog, material.nombre, material.densidad_str(), material.precio_str())

def agregarMaterialYRealizarAcciones(dialog:DialogCrearRegistros, material:Material, 
                                     accionesSobreDialog:Callable[[DialogCrearRegistros], None]):

    ingresarInputYEjecutarDialog(dialog, material.nombre, material.densidad_str(), 
                                 material.precio_str(), accionesSobreDialog)    


def assertarContenidoDeArchivoDespuesDeAgregarMaterial(dialog:DialogCrearRegistros, archivo:str, material:Material, 
                                                       accionesSobreDialog:Callable[[DialogCrearRegistros], None], 
                                                       contenido_esperado:str):
    
    agregarMaterialYRealizarAcciones(dialog, material, accionesSobreDialog)

    com_cot.assertarContenidoDeArchivoEsElEsperado(archivo, contenido_esperado)

def verificarQueNoHayaMaterialesRegistradosPeroEstenAgregadosLosEsperados(dialog:DialogCrearRegistros, 
                                                                          materiales_agregados_esperados:list[Material], 
                                                                          archivo:str):
    dialog.materiales_agregados == materiales_agregados_esperados

    ui.assertarArchivoInexistente(archivo)

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

def verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog:DialogCrearRegistros, descripcion_de_error_esperada:str):
    ui.verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog.dialogDescripcionDeError, 
                                                             descripcion_de_error_esperada)

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

#test data
def lista_materiales_aceptados() -> list[Material]:
    material_1 = Material("Acero Amutit", "3", "3.4")
    material_2 = Material("Cobre berilio", "3", "4.5")
    material_3 = Material("Aluminio 5083", "4", "2.3")

    return [material_1, material_2, material_3]



def test_01_AppCreaDialogAlAbrirArchivoInexistente(qtbot, monkeypatch):
    
    ventana = ui.crearVentana(qtbot)

    ui.verificarQueDialogCrearRegistrosSeEjecuteHaciendo(monkeypatch, 
                                                lambda: ventana.cargar_lista_registros("archivo_inexistente.txt") )



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



def test_06_DialogCrearRegistrosNoMuestraMaterialesSiArchivoInexistente(qtbot, tmpdir, monkeypatch):

    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
                                                     lambda dialog, archivo: 
                        ui.verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog, 0))


def verificarQueSeMuestranLosMaterialesAgregados(dialog, materiales_agregados_esperados:list[Material]):
    labels_datos = ui.verificarQueSeMuestrenSeccionesYCantidadDeMaterialesMostrados(dialog, 
                                                                                    len(materiales_agregados_esperados))

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
    agregarMaterialesYVerificarQueFueronGuardadosYMostrados(dialog, archivo, com_cot.lista_materiales_aceptada)

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



def test_11_DialogCrearRegistroRegistraMaterialesAgregadosYManoDeObra(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: ui.verificarQueLosRegistrosDeCostoAceptadosSeRegistrenCorrectamente(dialog, archivo))



def verificarQueDialogNoSeCierreYLanceDialogDeErrorAlIngresarInput(qtbot, dialog:DialogCrearRegistros, 
                                                                   lista_registros:list[RegistroDeCosto], archivo:str, 
        input_costo_mano_de_obra:str, descripcion_de_dialog_de_error_esperada:str):
    
    with qtbot.assertNotEmitted(dialog.accepted):

        ui.registrarListaMaterialesEInputManoDeObra(dialog, lista_registros, input_costo_mano_de_obra)

        verificarQueDialogDeErrorDeDialogTengaComoDescripcion(dialog, 
                                        descripcion_de_dialog_de_error_esperada)

        ui.assertarArchivoInexistente(archivo)

def verificarQueAlIngresarInputInvalidoDeManoDeObraDialogLanceDialogDeError(qtbot, dialog, archivo, 
                                                                            input_invalido_costo_mano_de_obra: str):
    lista_registros = [Material("Aluminio 5083", "3", "3"), Material("Aluminio","3.4","3"), Material("Acero","3.4","4")]

    verificarQueDialogNoSeCierreYLanceDialogDeErrorAlIngresarInput(qtbot, dialog, lista_registros, archivo, 
                                                                   input_invalido_costo_mano_de_obra, 
        ManoDeObra.PrecioInvalidoDescripcionDeError(input_invalido_costo_mano_de_obra))

def test_12_DialogCrearRegistroNoCreaRegistroYLevantaDialogDeErrorAlIngresarCostoDeManoDeObraValueError(qtbot, 
                                                                                                       tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: 
        verificarQueAlIngresarInputInvalidoDeManoDeObraDialogLanceDialogDeError(qtbot, dialog, archivo, "-3"))


def test_13_DialogCrearRegistroNoCreaRegistroLevantaDialogDeErrorAlIngresarCostoDeManoDeObraTypeError(qtbot, 
                                                                                                      tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: 
        verificarQueAlIngresarInputInvalidoDeManoDeObraDialogLanceDialogDeError(qtbot, dialog, archivo, "a"))


def test_14_DialogCrearRegistroReseteaLaTablaDeMaterialesAlGuardarTodo(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: ui.verificarQueSeReseteaLaTablaDeMaterialesAlGuardar(qtbot, dialog, archivo))

def test_15_DialogCrearRegistrosSeAbreAlAbrirArchivoVacio(qtbot, tmpdir, monkeypatch):
    
    archivo = ui.crearArchivoConContenido(tmpdir, "archivo_vacio.txt", "")

    ventana = ui.crearVentanaParaTestLeyendoDeArchivo(qtbot, archivo, monkeypatch)

    dialog = ventana.dialogParaCrearRegistro

    ui.verificarQueSeReseteaLaTablaDeMaterialesAlGuardar(qtbot, dialog, archivo)
    
#No hacer el scroll porque no hace falta, max 10 materiales 


def verificarQueDialogLanceErrorAlRegistrarSinAluminio5083(qtbot, dialog:DialogCrearRegistros, archivo:str, ):

    lista_registros = [Material("Aluminio","3.4","3"), Material("Acero","3.4","4")]

    verificarQueDialogNoSeCierreYLanceDialogDeErrorAlIngresarInput(qtbot, dialog, 
                                                                   lista_registros, archivo, "4", 
                                                            cotizador.noSePuedeRegistrarSiElAluminio5083NoEstaAgregado())


def test_16_DialogCrearRegistrosNoCreaRegistroYLevantaDialogDeErrorAlNoIngresarAluminio5083(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: 
        verificarQueDialogLanceErrorAlRegistrarSinAluminio5083(qtbot, dialog, archivo))

def verificarQueDialogLanceErrorSinAluminio5083DosVecesAlApretarGuardarTodoDosVeces(qtbot, dialog, archivo):
    verificarQueDialogLanceErrorAlRegistrarSinAluminio5083(qtbot, dialog, archivo)

    verificarQueDialogLanceErrorAlRegistrarSinAluminio5083(qtbot, dialog, archivo)

def test_17_DialogCrearRegistrosLanzaElMismoErrorAlNoPonerElAluminioyGuardarDosVeces(qtbot, tmpdir, monkeypatch):
    crearDialogSobreArchivoInexistenteYAplicarAccion(qtbot, tmpdir, monkeypatch, 
        lambda dialog, archivo: 
        verificarQueDialogLanceErrorSinAluminio5083DosVecesAlApretarGuardarTodoDosVeces(qtbot, dialog, archivo))

