from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, #para imprimir texto
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QFormLayout, QDoubleSpinBox, QPushButton, QDialog, QTextEdit) 

import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import Material

ARCHIVO_REGISTROS = "nada.txt"

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cotizador para moldes de Soplado")
       

    def cargar_ventana(self):
        
        # 👉 Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        form = QFormLayout()

        # Diccionario de materiales
        self.campos = {}

        lista_registros:list[Material] = self.cargar_lista_registros(ARCHIVO_REGISTROS)

        # Crear campos editables
        for  registro in lista_registros:
            spin = QDoubleSpinBox()
            spin.setRange(0, 1000)
            spin.setValue(registro.precio)
            spin.setSuffix(" US$")
            spin.setDecimals(2)

            form.addRow(registro.nombre + ":", spin)
            self.campos[registro.nombre] = spin

        layout.addLayout(form)
        

        # Botón para leer valores
        boton = QPushButton("Guardar / Mostrar valores")
        #boton.clicked.connect(self.mostrar_valores)
        layout.addWidget(boton)

        # 👉 IMPORTANTE: asignar layout al widget central
        central_widget.setLayout(layout)

    def cargar_lista_registros(self, nombre_archivo:str):

        try: 
            lista_registros:list[Material] = cotizador.crear_lista_materiales_a_partir_de(nombre_archivo)

        except (FileNotFoundError, ValueError):

            self.dialogParaCrearRegistro = DialogCrearRegistros(self)
            self.dialogParaCrearRegistro.exec()

            lista_registros:list[Material] = []

        return lista_registros

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
        #hacer una funcion en cotizador que agarre el contenido del archivo y lo pasa a texto(?)
        # si el archivo no existe entonces que pase algo vacío

        seccion_nombre_material = QLabel("Material")
        seccion_densidad_material = QLabel("Densidad")
        seccion_precio_material = QLabel("Precio")
        
        self.tabla_materiales_registrados = QGroupBox()
        self.tabla_materiales_registrados.setTitle("materiales registrados")

        self.materiales_agregados:list[Material] = []

        self.layout_materiales_registrados = QGridLayout()
        self.layout_materiales_registrados.addWidget(seccion_nombre_material, 0,0)
        self.layout_materiales_registrados.addWidget(seccion_densidad_material,0,1)
        self.layout_materiales_registrados.addWidget(seccion_precio_material,0,2)

        # layout_materiales_registrados = QGridLayout() 
        # apartado_secciones = QHBoxLayout()
        # apartado_secciones.addWidget(seccion_nombre_material)
        # apartado_secciones.addWidget(seccion_densidad_material)
        # apartado_secciones.addWidget(seccion_precio_material)

        # layout_materiales_registrados.addLayout(apartado_secciones)

        self.tabla_materiales_registrados.setLayout(self.layout_materiales_registrados)


        #creo un atributo llamado casilla_material
        self.casilla_material = QTextEdit()
        self.casilla_material.setPlaceholderText("Material")

        self.casilla_densidad = QTextEdit()
        self.casilla_densidad.setPlaceholderText("Densidad (Kg/dm3)")

        self.casilla_precio = QTextEdit()
        self.casilla_precio.setPlaceholderText("Precio (US$)")

        self.boton_agregar_material = QPushButton("Agregar material")
        self.boton_agregar_material.clicked.connect(self.agregar_material)

        # Quitamos el 'self' del paréntesis para que no intente ser el layout principal todavía
        layout_ingresar_material = QHBoxLayout()
        layout_ingresar_material.addWidget(self.casilla_material)
        layout_ingresar_material.addWidget(self.casilla_densidad)
        layout_ingresar_material.addWidget(self.casilla_precio)
        layout_ingresar_material.addWidget(self.boton_agregar_material)

        layout_general = QVBoxLayout(self) # Este SI lleva self porque es el principal
        layout_general.addWidget(descripcion_error)
        layout_general.addWidget(self.tabla_materiales_registrados)
        layout_general.addStretch() # Agregamos un pequeño espacio o "stretch" si quieres que el texto esté bien arriba
        layout_general.addLayout(layout_ingresar_material) # Agrega el grupo de inputs abajo
        

        self.setLayout(layout_general)

        """ un label que diga No existe un registro de materiales y precios para iniciar la cotización. Usted está por crear uno."""

        self.resize(900, 600)

    def agregar_material(self):
        nombre_material:str = self.casilla_material.toPlainText()
        densidad_material:str = self.casilla_densidad.toPlainText()
        precio_material:str = self.casilla_precio.toPlainText()

        try:
            self.materiales_agregados.append(Material(nombre_material, densidad_material, precio_material))
        except (ValueError, TypeError) as descripcion_de_error:
            self.dialogDescripcionDeError = DialogDescripcionDeError(str(descripcion_de_error),self)
            self.dialogDescripcionDeError.exec()

        #try:
        #     cotizador.registrar_material(nombre_material, densidad_material, precio_material, ARCHIVO_REGISTROS)

        # except (ValueError, TypeError) as descripcion_de_error:
        #     self.dialogDescripcionDeError = DialogDescripcionDeError(str(descripcion_de_error),self)
        #     self.dialogDescripcionDeError.exec()

        self.xxx()

    def xxx(self):
       
        for index,registro in enumerate(self.materiales_agregados):
           #for i in enumerate(range(3)):
            nombre_del_material = QLabel(registro.nombre)
            self.layout_materiales_registrados.addWidget(nombre_del_material, index, 0)

            densidad_del_material = QLabel(str(registro.densidad))
            self.layout_materiales_registrados.addWidget(densidad_del_material, index, 1)

            precio_del_material = QLabel(str(registro.precio))
            self.layout_materiales_registrados.addWidget(precio_del_material, index, 2)

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
