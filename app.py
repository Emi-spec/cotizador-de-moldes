from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, #para imprimir texto
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QFormLayout, QDoubleSpinBox, QPushButton, QMessageBox) 

import cotizador_para_moldes_de_soplado as cotizador

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cotizador para moldes de Soplado")

        # 👉 Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        form = QFormLayout()

        # Diccionario de materiales
        self.campos = {}

        materiales = cotizador.crear_dic_materiales()
        # {
        #     "Aluminio 5083": 19.0,
        #     "Aluminio 6061": 21.5,
        #     "Aluminio 7075": 23.5,
        #     "Acero Amutit": 7.5,
        #     "Acero Especial K": 11.0,
        #     "Acero Inoxidable": 16.0,
        #     "Acero SAE 4140": 6.0,
        #     "Cobre Berilio": 110.0,
        #     "Hora molde soplado": 35.0
        # }

        # Crear campos editables
        for letra, caract_material in materiales.items():
            spin = QDoubleSpinBox()
            spin.setRange(0, 1000)
            spin.setValue(caract_material[2])
            spin.setSuffix(" US$")
            spin.setDecimals(2)

            form.addRow(caract_material[0] + ":", spin)
            self.campos[caract_material[0]] = spin

        layout.addLayout(form)
        

        # Botón para leer valores
        boton = QPushButton("Guardar / Mostrar valores")
        #boton.clicked.connect(self.mostrar_valores)
        layout.addWidget(boton)

        # 👉 IMPORTANTE: asignar layout al widget central
        central_widget.setLayout(layout)

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

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])


# Create a Qt widget, which will be our window.
window = Ventana()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.