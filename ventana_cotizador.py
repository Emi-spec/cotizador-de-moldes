from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, #para imprimir texto
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QPushButton, QDialog, QApplication, QSizePolicy,
    QLineEdit) 

import os

from collections.abc import Callable
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import (Material, ManoDeObra, RegistroDeCosto)

ARCHIVO_REGISTROS = "precios.txt"

def crearLineEdit(placeHolderText:str) -> QLabel:
    input = QLineEdit()
    input.setPlaceholderText(placeHolderText)
    input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    return input

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cotizador para moldes de Soplado")
       

    def cargar_ventana(self):
        
        # 👉 Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout_general = QVBoxLayout()

        # Diccionario de materiales
        self.campos = {}

        self.lista_registros:list[Material] = self.cargar_lista_registros(ARCHIVO_REGISTROS)

        self.tabla_materiales_registrados = QGroupBox()
        self.tabla_materiales_registrados.setTitle("materiales registrados")

        self.layout_materiales_registrados = QGridLayout()

        self.tabla_materiales_registrados.setLayout(self.layout_materiales_registrados)
        self.layout_general.addWidget(self.tabla_materiales_registrados)

        self.agregarSeccionesCaracteristicasMaterial()

        self.input_precios:dict[str, QLineEdit] = {}

        for index,registro in enumerate(self.lista_registros):
            if(registro.esMaterial()):
                nombre_del_material = QLabel(registro.nombre)
                self.layout_materiales_registrados.addWidget(nombre_del_material, index+1, 0)

                densidad_del_material = QLabel(registro.densidad_str())
                self.layout_materiales_registrados.addWidget(densidad_del_material, index+1, 1)

                precio_del_material = crearLineEdit(registro.precio_str())
                self.layout_materiales_registrados.addWidget(precio_del_material, index+1, 2)

                self.input_precios[registro] = precio_del_material
            
            if(registro.esManoDeObra()):
                nombre_mano_de_obra = QLabel(registro.nombre)
                self.layout_materiales_registrados.addWidget(nombre_mano_de_obra, index+1, 0)

                precio_mano_de_obra = crearLineEdit(registro.precio_str())
                self.layout_materiales_registrados.addWidget(precio_mano_de_obra, index+1, 2)

                self.input_precios[registro] = precio_mano_de_obra

        # Botón para leer valores
        boton_guardar_cambios = QPushButton("Guardar Cambios")
        boton_guardar_cambios.clicked.connect(self.guardarCambios)
        self.layout_general.addWidget(boton_guardar_cambios)

        central_widget.setLayout(self.layout_general)

        # # 👉 IMPORTANTE: asignar layout al widget central
        # central_widget.setLayout(layout)
    def ejecutarDialogCrearRegistros(self):
        self.dialogParaCrearRegistro = DialogCrearRegistros(self)
        self.dialogParaCrearRegistro.exec()

    def inputsPreciosSonValidos(self) -> bool:
        for registro in self.input_precios:
            if(self.input_precios[registro].text() != ""):
                precio_a_modificar = self.input_precios[registro].text()

                if(not registro.esPrecioValido(precio_a_modificar)):    
                    registro.lanzarErrorPrecioInvalidoEnVentana(self, precio_a_modificar)
                    return False
        
        return True

    def guardarCambios(self):
    
        if(self.inputsPreciosSonValidos()):
            for indice, registro in enumerate(self.input_precios):
                if(self.input_precios[registro].text() != ""):
            
                    precio_a_modificar = self.input_precios[registro].text()
                    
                    registro.agregarseALaListaConElPrecioModificado(self, indice, precio_a_modificar)


            cotizador.limpiarArchivoYRegistrarListaRegistros(self.lista_registros, ARCHIVO_REGISTROS)





    def cargar_lista_registros(self, nombre_archivo:str):

        try: 
            if(os.path.getsize(nombre_archivo) == 0):
                self.ejecutarDialogCrearRegistros()
                lista_registros:list[Material] = []
            else:
                lista_registros:list[Material] = cotizador.crear_lista_registros_a_partir_de(nombre_archivo)

        except (FileNotFoundError):
            
            self.ejecutarDialogCrearRegistros()

            lista_registros:list[Material] = []

        except (ValueError) as descripcion_de_error:
            self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))

            self.ejecutarDialogCrearRegistros()

            lista_registros:list[Material] = []

        return lista_registros

    def agregarSeccionesCaracteristicasMaterial(self):
        seccion_nombre_material = QLabel("Material")
        seccion_nombre_material.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        seccion_densidad_material = QLabel("Densidad (Kg/dm3)")
        seccion_densidad_material.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        seccion_precio_material = QLabel("Precio (US$)")
        seccion_precio_material.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.layout_materiales_registrados.addWidget(seccion_nombre_material, 0,0)
        self.layout_materiales_registrados.addWidget(seccion_densidad_material,0,1)
        self.layout_materiales_registrados.addWidget(seccion_precio_material,0,2)

    def ejecutarDialogDeErrorConDescripcion(self, descripcion_de_error:str):
        self.dialogDescripcionDeError = DialogDescripcionDeError(descripcion_de_error,self)
        self.dialogDescripcionDeError.exec()

    def lanzarDialogDeErrorConDescripcionSiFalla(self, codigoQueAlFallarSeDebeMostrarDialogDeError:Callable[[],None]):
        try:
            codigoQueAlFallarSeDebeMostrarDialogDeError()

        except (ValueError, TypeError) as descripcion_de_error:
            self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))

class DialogDescripcionDeError(QDialog):
    def __init__(self, mensajeDeError:str, parent ):
        super(DialogDescripcionDeError, self).__init__(parent)
        self.setWindowTitle("Error")
        
        self.label_descripcion_error = QLabel(mensajeDeError)
        self.label_descripcion_error.setAlignment(Qt.AlignCenter)
        self.label_descripcion_error.setWordWrap(True) 
        self.label_descripcion_error.setStyleSheet("font-weight: bold; margin: 10px;")

        self.boton_OK = QPushButton("OK")
        self.boton_OK.clicked.connect(self.cerrar_dialog)

        layout_general = QVBoxLayout(self)
        layout_general.addWidget(self.label_descripcion_error)
        layout_general.addWidget(self.boton_OK)

    def cerrar_dialog(self):
        self.accept()

#class tablaDeMateriales (QAbstractScrollArea):


class DialogCrearRegistros(QDialog):
    def __init__(self, parent):
        super(DialogCrearRegistros, self).__init__(parent)
        self.setWindowTitle("Crear un registro nuevo")

        descripcion_error = QLabel("No existe un registro de materiales y precios para iniciar la cotización. Usted está por crear uno.", self)
        descripcion_error.setAlignment(Qt.AlignCenter)
        # Opcional: hacer que el texto sea más visible o use varias líneas
        descripcion_error.setWordWrap(True) 
        descripcion_error.setStyleSheet("font-weight: bold; margin: 10px;")

        #grilla que va mostrando los materiales
        
        self.tabla_materiales_registrados = QGroupBox()
        self.tabla_materiales_registrados.setTitle("materiales registrados")
        self.tabla_materiales_registrados.resize(800,900)


        self.materiales_agregados:list[Material] = []

        self.layout_materiales_registrados = QGridLayout()

        self.agregarSeccionesCaracteristicasMaterial()

        self.tabla_materiales_registrados.setLayout(self.layout_materiales_registrados)

        #creo un atributo llamado input_material
        self.input_material = crearLineEdit("Material")

        self.input_densidad = crearLineEdit("Densidad (Kg/dm3)") 

        self.input_precio = crearLineEdit("Precio (US$)")

        self.boton_agregar_material = QPushButton("Agregar material")
        self.boton_agregar_material.clicked.connect(self.agregar_material)

        label_ingresar_costo_mano_de_obra = QLabel("Ingresar costo de mano de obra:")
        self.input_costo_mano_de_obra = crearLineEdit("Costo (US$)")

        layout_ingresar_costo_mano_de_obra = QHBoxLayout()
        layout_ingresar_costo_mano_de_obra.addWidget(label_ingresar_costo_mano_de_obra)
        layout_ingresar_costo_mano_de_obra.addWidget(self.input_costo_mano_de_obra)

        # Quitamos el 'self' del paréntesis para que no intente ser el layout principal todavía
        layout_ingresar_material = QHBoxLayout()
        layout_ingresar_material.addWidget(self.input_material)
        layout_ingresar_material.addWidget(self.input_densidad)
        layout_ingresar_material.addWidget(self.input_precio)
        layout_ingresar_material.addWidget(self.boton_agregar_material)

        self.boton_guardar = QPushButton("Guardar todo")
        self.boton_guardar.clicked.connect(self.guardarTodoYCerrar)

        layout_general = QVBoxLayout(self) # Este SI lleva self porque es el principal
        layout_general.addWidget(descripcion_error)
        layout_general.addWidget(self.tabla_materiales_registrados)
        layout_general.addStretch() # Agregamos un pequeño espacio o "stretch" si quieres que el texto esté bien arriba
        layout_general.addLayout(layout_ingresar_material) # Agrega el grupo de inputs abajo
        layout_general.addLayout(layout_ingresar_costo_mano_de_obra)
        layout_general.addWidget(self.boton_guardar)
        
        self.setLayout(layout_general)
        self.resize(900, 600)

    @staticmethod
    def materialYaRegistradoDeMismoNombreDescripcionDeError(nombre_duplicado:str) -> str:
        return f"Ya hay un material de nombre {nombre_duplicado} agregado"
    
    @staticmethod
    def noHayMaterialesAgregadosParaRegistrarDescripcionDeError() -> str:
        return f"No se puede guardar materiales que no fueron agregados"
    
    @staticmethod
    def noSePuedeGuardarSinUnPrecioDeManoDeObra() -> str:
        return f"No se puede guardar materiales sin un precio asignado a la mano de obra"

    def agregarSeccionesCaracteristicasMaterial(self):
        seccion_nombre_material = QLabel("Material")
        seccion_densidad_material = QLabel("Densidad (Kg/dm3)")
        seccion_precio_material = QLabel("Precio (US$)")

        self.layout_materiales_registrados.addWidget(seccion_nombre_material, 0,0)
        self.layout_materiales_registrados.addWidget(seccion_densidad_material,0,1)
        self.layout_materiales_registrados.addWidget(seccion_precio_material,0,2)

    def ejecutarDialogDeErrorConDescripcion(self, descripcion_de_error:str):
        self.dialogDescripcionDeError = DialogDescripcionDeError(descripcion_de_error,self)
        self.dialogDescripcionDeError.exec()

    def lanzarDialogDeErrorConDescripcionSiFalla(self, codigoQueAlFallarSeDebeMostrarDialogDeError:Callable[[],None]):
        try:
            codigoQueAlFallarSeDebeMostrarDialogDeError()

        except (ValueError, TypeError) as descripcion_de_error:
            self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))


    def registrarTodosLosRegistrosDeCostoAgregados(self, input_costo_mano_obra:str, ):
        self.materiales_agregados.append(ManoDeObra(input_costo_mano_obra))
        cotizador.registrarListaRegistros(self.materiales_agregados, ARCHIVO_REGISTROS)

        #CHEQUEAR
        self.limpiar_layout(self.layout_materiales_registrados)
        self.agregarSeccionesCaracteristicasMaterial()

        self.input_material.clear()
        self.input_densidad.clear()
        self.input_precio.clear()
        self.input_costo_mano_de_obra.clear()

        


    #de chatgpt
    def limpiar_layout(self, layout):
    # Recorremos el layout desde el último índice hasta el 0
    # Es importante recorrer al revés para no perder el orden mientras borramos
    # borra tambien los widgets de los layouts hijos
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # Borra el widget de la memoria
                widget.deleteLater()
        # Procesa todos los eventos pendientes (borrado de widgets, repintado, etc.)
        QApplication.processEvents()

    def guardarTodoYCerrar(self):

        input_costo_mano_obra = self.input_costo_mano_de_obra.text()

        if(self.materiales_agregados == []):
            self.ejecutarDialogDeErrorConDescripcion(
                DialogCrearRegistros.noHayMaterialesAgregadosParaRegistrarDescripcionDeError())

        elif(input_costo_mano_obra == ""):
            self.ejecutarDialogDeErrorConDescripcion(DialogCrearRegistros.noSePuedeGuardarSinUnPrecioDeManoDeObra())

        else:
            self.lanzarDialogDeErrorConDescripcionSiFalla(lambda: 
                                            self.registrarTodosLosRegistrosDeCostoAgregados(input_costo_mano_obra))

        self.accept()



    def agregarMaterialAMaterialesAgregadosYMostrarlo(self, nombre_material:str, densidad_material:str, precio_material:str):
        material = Material(nombre_material, densidad_material, precio_material)

        for material_agregado in self.materiales_agregados:
            if(material_agregado.tieneComoNombre(nombre_material)):
                raise ValueError(DialogCrearRegistros.materialYaRegistradoDeMismoNombreDescripcionDeError(nombre_material))
                
        self.materiales_agregados.append(material)
        self.mostrarMaterialAgregado()


    def agregar_material(self):
        nombre_material:str = self.input_material.text()
        densidad_material:str = self.input_densidad.text()
        precio_material:str = self.input_precio.text()
        
        self.lanzarDialogDeErrorConDescripcionSiFalla(lambda:
                self.agregarMaterialAMaterialesAgregadosYMostrarlo(nombre_material, densidad_material, precio_material))
        



    def mostrarMaterialAgregado(self):

        ultima_posicion_lista = len(self.materiales_agregados) -1
        ultimo_material_agregado = self.materiales_agregados[ultima_posicion_lista]

        nombre_del_material = QLabel(ultimo_material_agregado.nombre)
        self.layout_materiales_registrados.addWidget(nombre_del_material, ultima_posicion_lista+1, 0)

        densidad_del_material = QLabel(str(ultimo_material_agregado.densidad))
        self.layout_materiales_registrados.addWidget(densidad_del_material, ultima_posicion_lista+1, 1)

        precio_del_material = QLabel(str(ultimo_material_agregado.precio))
        self.layout_materiales_registrados.addWidget(precio_del_material, ultima_posicion_lista+1, 2)
       

    # def mostrar_valores(self):
    #     resultado = ""
    #     for letra, campo in self.campos.items():
    #         resultado += f"{letra}: {campo.value()} US$\n"

    #     QMessageBox.information(self, "Valores actuales", resultado)

        # texto_inicial = QLabel("____________________\n\nPROGRAMA DE COTIZACIÓN PARA MOLDES DE SOPLADO\n____________________\n")

        # texto_inicial.setAlignment(
        # Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        # )
        
        # text_edit = QTextEdit()
        # text_edit.setReadOnly(True)
        # text_edit.setPlainText(texto_inicial)

        # self.setCentralWidget(texto_inicial)
        #button = QPushButton("Press Me!")

        #self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        #self.setCentralWidget(button)
