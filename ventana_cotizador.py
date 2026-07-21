from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, #para imprimir texto
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QPushButton, QDialog, QApplication, QSizePolicy, QComboBox, QRadioButton,
    QLineEdit, QFileDialog) 

import os

from collections.abc import Callable
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import (Material, ManoDeObra, RegistroDeCosto, NivelDeDificultad,
            nivelDeDificultadBajo, nivelDeDificultadMedio, nivelDeDificultadAlto, nivelDeDificultadMuyAlto, 
            nivelDeDificultadEspeciales, ResultadoCotizacion)

ARCHIVO_REGISTROS = "precios.txt"


def esMedidaValida(medida_en_str:str):
    if(cotizador.es_float_estricto(medida_en_str)):
        return (float(medida_en_str) >0)
    else: 
        return False


def crearLineEdit(placeHolderText:str) -> QLineEdit:
    input = QLineEdit()
    input.setPlaceholderText(placeHolderText)
    input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)

    return input

def crearMenuDesplegable(opciones:list[str]) -> QComboBox:
    menu = QComboBox()
    menu.insertItems(0,opciones)
    
    return menu

def crearBoton(texto:str, accionProducidaPorBoton:Callable[[], None]):
        boton = QPushButton(texto)
        boton.clicked.connect(accionProducidaPorBoton)

        return boton

def seleccionarMateriales(lista_registros:list[RegistroDeCosto]) -> list[Material]:
    
    lista_materiales:list[Material] = []
    
    for registro in lista_registros:
        if (registro.esMaterial()):
            lista_materiales.append(registro)

    return lista_materiales

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cotizador para moldes de Soplado")

        # cargar_ventana debería estar integrado acá dentro pero hace que se abran en ventana cuando corren tests 
    
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

        self.cargarMaterialesRegistradosEInputsPrecios()

        # Botón para leer valores

        boton_guardar_cambios = crearBoton("Guardar Cambios", self.guardarCambios)
        self.layout_general.addWidget(boton_guardar_cambios)

        boton_empezar_cotizacion = crearBoton("Empezar cotización", self.empezarCotizacion)
        self.layout_general.addWidget(boton_empezar_cotizacion)

        # # 👉 IMPORTANTE: asignar layout al widget central
        central_widget.setLayout(self.layout_general)


    def ejecutarDialogCrearRegistros(self):
        self.dialogParaCrearRegistro = DialogCrearRegistros(self)
        self.dialogParaCrearRegistro.exec()

        # if self.dialogParaCrearRegistro.exec() == QDialog.DialogCode.Accepted:
        #     # Volvemos a leer el archivo ahora que tiene datos
        #     self.lista_registros = cotizador.crear_lista_registros_a_partir_de(ARCHIVO_REGISTROS)
        #     # Limpiamos los labels viejos (solo los encabezados) y redibujamos todo
        #     self.limpiar_layout(self.layout_materiales_registrados)
        #     self.agregarSeccionesCaracteristicasMaterial()
        #     self.cargarMaterialesRegistradosEInputsPrecios()

    def cargarMaterialesRegistradosEInputsPrecios(self):
        self.input_precios:dict[RegistroDeCosto, QLineEdit] = {}

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
            
            self.limpiar_layout(self.layout_materiales_registrados)
            self.cargarMaterialesRegistradosEInputsPrecios()

            cotizador.limpiarArchivoYRegistrarListaRegistros(self.lista_registros, ARCHIVO_REGISTROS)

    #de chatgpt -> este limpia widgets y layouts hijos
    def limpiar_layout(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            sub_layout = item.layout()

            # 1. Si el item es un widget, lo borramos de la memoria
            if widget is not None:
                widget.deleteLater()
            
            # 2. Si el item es un layout hijo, aplicamos recursividad
            elif sub_layout is not None:
                self.limpiar_layout(sub_layout)  # Limpia los hijos del sub-layout
                sub_layout.deleteLater()         # Borra el sub-layout en sí mismo
                
            # 3. Si es un SpacerItem (espaciador), simplemente lo eliminamos
            # (No tienen deleteLater, se eliminan al perder la referencia de C++)

        # Procesa todos los eventos pendientes una sola vez al final de la limpieza
        QApplication.processEvents()


    def crearCaracteristicaAElegirConMenuDesplegable(self, layout_padre:QGridLayout, 
                                        texto:str, opciones_desplegables:list[str], fila_en_layout:int) -> QLabel:
        label = QLabel(texto)
        menu_desplegable = crearMenuDesplegable(opciones_desplegables)

        layout_padre.addWidget(label, fila_en_layout , 0)
        layout_padre.addWidget(menu_desplegable, fila_en_layout , 1)

        return menu_desplegable


    def crearInputMedidaDelEnvase(self, layout_padre:QGridLayout, texto_label:str, fila_en_layout:int) -> QLabel:
        label = QLabel(texto_label)
        input = crearLineEdit("0 mm")

        layout_padre.addWidget(label, fila_en_layout, 0)
        layout_padre.addWidget(input, fila_en_layout, 1)

        return input

    def crearGroupBoxLayoutGeneral(self, titulo_del_grupo:str, fila_en_layout:int, columna_en_layout:int, rowspan_en_layout:int, 
            colspan_en_layout:int, asignarWidgetsAlLayout:Callable[[QGridLayout], None]):
        grupo = QGroupBox()
        grupo.setTitle(titulo_del_grupo)
        layout_grilla = QGridLayout()
        grupo.setLayout(layout_grilla)
        self.layout_grilla.addWidget(grupo, fila_en_layout, columna_en_layout,rowspan_en_layout,colspan_en_layout)
        
        asignarWidgetsAlLayout(layout_grilla)


    def crearGroupBoxEnPrimeraColumna(self, titulo_del_grupo:str, fila_en_layout:int, 
                      asignarWidgetsAlLayout:Callable[[QGridLayout], None]):
        
        self.crearGroupBoxLayoutGeneral(titulo_del_grupo, fila_en_layout, 0,1,1, asignarWidgetsAlLayout)

    def asignarInputsDetallesDeCavidadesAlLayout(self, layout_padre:QGridLayout):
        #cantidad de moldes a cotizar
        self.input_cantidad_moldes = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, 
                                                                                       "cantidad de moldes a cotizar: ",
                                                                                        ["1","2"], 0)
        
        #cantidad de cavidades
        self.input_cantidad_cavidades = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, 
                                                                                    "Cantidad de cavidades del molde: ", 
                                                          ["1","2","3","4","5","6","7","8","9","10"], 1)

        #mascaras y troqueles
        self.input_mascaras_troqueles = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, 
                                                                        "¿Incluye máscaras de transporte y troqueles?: ", 
                                                                        ["si","no"],2)

    def asignarInputsDeMedidasDelMoldeAlLayout(self, layout_padre:QGridLayout):
        #altura
        self.input_altura_envase = self.crearInputMedidaDelEnvase(layout_padre, "Altura del envase: ", 0)

        #volumen
        self.input_volumen_envase = self.crearInputMedidaDelEnvase(layout_padre, "Volumen del envase: ", 1)

        #distancia entre centros
        self.input_distancia_centros = self.crearInputMedidaDelEnvase(layout_padre, "Distancia entre centros que hay entre cavidades: ", 2)

        #ancho por mitad
        self.input_ancho_mitad = self.crearInputMedidaDelEnvase(layout_padre, "Ancho por mitad del molde: ", 3)

    def AsignarInputsDeEleccionDeMaterialesAlLayout(self, layout_padre:QGridLayout):
                
        self.lista_materiales:list[Material] = [registro for registro in self.lista_registros if registro.esMaterial()]
        lista_nombre_materiales:list[str] = [registro.nombre for registro in self.lista_registros if registro.esMaterial()]
             
        #postizos de cuerpo 
        self.input_postizos_cuerpo = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, "Postizos de cuerpo: ", 
                                                          lista_nombre_materiales, 0)

        #Postizos de cuello
        self.input_postizos_cuello = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, "Postizos de cuello: ", 
                                                          lista_nombre_materiales, 1)

        #Postizos de fondo
        self.input_postizos_fondo = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, "Postizos de fondo: ", 
                                                          lista_nombre_materiales, 2)
        
        #Placas de respaldo
        self.input_placas_respaldo = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, "Placas de respaldo: ", 
                                                          lista_nombre_materiales, 3)
        
        #Postizo prensamangas
        self.input_prensamangas = self.crearCaracteristicaAElegirConMenuDesplegable(layout_padre, "Postizo prensamangas: ",
                                                          lista_nombre_materiales, 4)

    def asignarRadioButtonsNivelesDeDificultad(self, layout_padre:QGridLayout):
        self.opcion_nivel_bajo = QRadioButton(nivelDeDificultadBajo.presentacion_en_str)
        self.opcion_nivel_medio = QRadioButton(nivelDeDificultadMedio.presentacion_en_str)
        self.opcion_nivel_alto = QRadioButton(nivelDeDificultadAlto.presentacion_en_str)
        self.opcion_nivel_muy_alto = QRadioButton(nivelDeDificultadMuyAlto.presentacion_en_str)
        self.opcion_nivel_especiales= QRadioButton(nivelDeDificultadEspeciales.presentacion_en_str)

        layout_padre.addWidget(self.opcion_nivel_bajo, 0, 0)
        layout_padre.addWidget(self.opcion_nivel_medio, 1, 0)
        layout_padre.addWidget(self.opcion_nivel_alto, 2, 0)
        layout_padre.addWidget(self.opcion_nivel_muy_alto, 3, 0)
        layout_padre.addWidget(self.opcion_nivel_especiales, 4, 0)

    def empezarCotizacion(self):
        self.limpiar_layout(self.layout_general) 

        self.layout_grilla = QGridLayout()
        self.layout_general.addLayout(self.layout_grilla)

        #Detalles de cavidades
        self.crearGroupBoxEnPrimeraColumna("Detalles de cavidades", 0, 
                                           lambda layout: self.asignarInputsDetallesDeCavidadesAlLayout(layout))

        #Caracteristicas del molde
        self.crearGroupBoxEnPrimeraColumna("medidas del molde", 1, 
                                           lambda layout: self.asignarInputsDeMedidasDelMoldeAlLayout(layout))
        

        #nivel de dificultad
        self.crearGroupBoxLayoutGeneral("Nivel de dificultad del envase:", 0, 1, 3, 3, lambda layout: 
                 self.asignarRadioButtonsNivelesDeDificultad(layout))

        # ingreso de tipo de material
        self.crearGroupBoxEnPrimeraColumna("Ingrese el material a utilizar", 2, lambda layout: 
                           self.AsignarInputsDeEleccionDeMaterialesAlLayout(layout))

        boton_cotizar = crearBoton("Cotizar", self.cotizar)
        self.layout_grilla.addWidget(boton_cotizar, 3, 0, 1, 4)

    def ejecutarDialogDeErrorSiInputNumericoInvalido(self, input:str, descripcion_de_error:str):
        cotizador.verificarAtributoNumericoValidoLanzando(input, 
            lambda: self.ejecutarDialogDeErrorConDescripcion(descripcion_de_error),
            lambda: self.ejecutarDialogDeErrorConDescripcion(descripcion_de_error))


    def seleccionarMaterialDelMenuDesplegable(self, menu_desplagable_con_materiales:QComboBox):
        nombre = menu_desplagable_con_materiales.currentText() 
        material_elegido:Material = None

        for material in self.lista_registros:
            if(material.tieneComoNombre(nombre) and material_elegido == None):
                material_elegido = material
            elif(material.tieneComoNombre(nombre) and material_elegido != None):
                raise ValueError(f"Hay dos materiales con el nombre {material_elegido.nombre} en ventana.lista_registros")

        return material_elegido

    def inputsSonCorrectos(self):
        todos_inputs_correctos:bool = True

        if (not esMedidaValida(self.input_altura_envase.text())):
            todos_inputs_correctos = False
        if (not esMedidaValida(self.input_volumen_envase.text())):
            todos_inputs_correctos = False
        if (not esMedidaValida(self.input_distancia_centros.text())):
            todos_inputs_correctos = False
        if (not esMedidaValida(self.input_distancia_centros.text())):
            todos_inputs_correctos = False
        if (not esMedidaValida(self.input_ancho_mitad.text())):
            todos_inputs_correctos = False

        self.ejecutarDialogDeErrorSiInputNumericoInvalido(self.input_altura_envase.text(), 
                cotizador.alturaDeEnvaseInvalidaDescripcionDeError(self.input_altura_envase.text()))

        self.ejecutarDialogDeErrorSiInputNumericoInvalido(self.input_volumen_envase.text(), 
                cotizador.volumenDeEnvaseInvalidoDescripcionDeError(self.input_volumen_envase.text()))
        
        self.ejecutarDialogDeErrorSiInputNumericoInvalido(self.input_distancia_centros.text(), 
                cotizador.distanciaEntreCentrosInvalidaDescripcionDeError(self.input_distancia_centros.text()))

        self.ejecutarDialogDeErrorSiInputNumericoInvalido(self.input_ancho_mitad.text(), 
                cotizador.anchoPorMitadDelMoldeInvalidoDescripcionDeError(self.input_ancho_mitad.text()))
        
        if(not self.opcion_nivel_bajo.isChecked() and 
           not self.opcion_nivel_medio.isChecked() and 
           not self.opcion_nivel_alto.isChecked() and
           not self.opcion_nivel_muy_alto.isChecked() and
           not self.opcion_nivel_especiales.isChecked()):
           todos_inputs_correctos = False
           self.ejecutarDialogDeErrorConDescripcion(cotizador.NoSeEligioUnNivelDeDificultadDelEnvaseDescripcionDeError())
        
        return todos_inputs_correctos

    def cotizar(self):

        if(self.inputsSonCorrectos()):

            if(self.input_mascaras_troqueles.currentText() == "si"):
                mascaras_troqueles:bool = True
            else: 
                mascaras_troqueles:bool = False

            #dificultad
            if(self.opcion_nivel_bajo.isChecked()):
                dificultad = nivelDeDificultadBajo
            if(self.opcion_nivel_medio.isChecked()):
                dificultad = nivelDeDificultadMedio
            if(self.opcion_nivel_alto.isChecked()):
                dificultad = nivelDeDificultadAlto
            if(self.opcion_nivel_muy_alto.isChecked()):
                dificultad = nivelDeDificultadMuyAlto
            if(self.opcion_nivel_especiales.isChecked()):
                dificultad = nivelDeDificultadEspeciales

            #opciones de materiales
            # nombre = self.input_postizos_cuerpo().currentText() 

            # for material in self.lista_registros:
            #     if(material.tieneComoNombre(nombre)):
            #         material_postizos_cuerpo = material
            #breakpoint()
            material_postizos_cuerpo:Material = self.seleccionarMaterialDelMenuDesplegable(self.input_postizos_cuerpo) 
            material_postizos_cuello:Material = self.seleccionarMaterialDelMenuDesplegable(self.input_postizos_cuello)
            material_postizos_fondo:Material = self.seleccionarMaterialDelMenuDesplegable(self.input_postizos_fondo)
            material_placas_respaldo:Material = self.seleccionarMaterialDelMenuDesplegable(self.input_placas_respaldo)
            material_prensamangas:Material = self.seleccionarMaterialDelMenuDesplegable(self.input_prensamangas)  

            mano_de_obra:ManoDeObra = None

            #breakpoint()
            for registro in self.lista_registros:
                if (registro.esManoDeObra()):
                    mano_de_obra = registro

            lista_materiales:list[Material] = seleccionarMateriales(self.lista_registros)


            self.resultado_cotizacion = cotizador.cotizarEnBaseA(int(self.input_cantidad_moldes.currentText()), 
                                    int(self.input_cantidad_cavidades.currentText()),
                                    mascaras_troqueles,
                                    float(self.input_altura_envase.text()),
                                    float(self.input_volumen_envase.text()),
                                    float(self.input_distancia_centros.text()),
                                    float(self.input_ancho_mitad.text()),
                                    dificultad,
                                    material_postizos_cuerpo,
                                    material_postizos_cuello,
                                    material_postizos_fondo,    
                                    material_placas_respaldo, 
                                    material_prensamangas,
                                    lista_materiales,
                                    mano_de_obra)
            
            #breakpoint()
            self.limpiar_layout(self.layout_general) 

            resultados_impresos = QLabel(self.resultado_cotizacion.imprimirResultado())

            self.layout_general.addWidget(resultados_impresos)

            #layout_guardar_archivo = QHBoxLayout()
            
            #label_guardar_en_archivo = QLabel("Guardar en archivo")
            #self.input_nombre_archivo = crearLineEdit("nombre archivo")
            #extension_txt = QLabel(".txt") 
            boton_guardar_en_archivo = crearBoton("guardar", self.guardarEnArchivo)
            self.layout_general.addWidget(boton_guardar_en_archivo)

            #layout_guardar_archivo.addWidget(label_guardar_en_archivo)
            #layout_guardar_archivo.addWidget(self.input_nombre_archivo)
            #layout_guardar_archivo.addWidget(extension_txt)
            #layout_guardar_archivo.addWidget(boton_guardar_en_archivo)
            
            #self.layout_general.addLayout(layout_guardar_archivo)
        
    def elNombreDelArchivoNoPuedeSerNuloDescripcionDeError(self) -> str:
        return "El nombre del archivo no puede estar vacío"

    def guardarEnArchivo(self):
        
        #if(self.input_nombre_archivo.text() == ""):
        #    self.ejecutarDialogDeErrorConDescripcion(self.elNombreDelArchivoNoPuedeSerNuloDescripcionDeError())

        #else:
            # archivo = open( + ".txt", "w")

            # archivo.write(self.resultado_cotizacion.imprimirResultado())

            # archivo.close()

        archivo, filtro = QFileDialog.getSaveFileName(
        self, 
        "Guardar archivo como", 
        ".", # Carpeta inicial
        "Archivos de texto (*.txt);;Todos los archivos (*.*)"
        )

        if archivo:
            #try:
                # Escribir el contenido en el archivo seleccionado
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(self.resultado_cotizacion.imprimirResultado())
                #     print(f"Archivo guardado exitosamente en: {archivo}")
                # except Exception as e:
                #     print(f"Error al guardar el archivo: {e}")

            # self.dialog_guardar_archivo = QFileDialog(self)
            # #self.dialog_guardar_archivo.setFileMode(QFileDialog.AnyFile)
            # #self.dialog_

            # if self.dialog_guardar_archivo.exec():
            #     nombre_archivo = self.dialog_guardar_archivo.selectedFiles()

    def cargar_lista_registros(self, nombre_archivo:str):
        try: 
            # 1. Si el archivo no existe o está vacío, abrimos el creador una única vez
            if not os.path.exists(nombre_archivo) or os.path.getsize(nombre_archivo) == 0:
                self.ejecutarDialogCrearRegistros()
                # Tras cerrarse el diálogo, intentamos cargar lo que el usuario guardó
                if os.path.exists(nombre_archivo) and os.path.getsize(nombre_archivo) > 0:
                    return cotizador.crear_lista_registros_a_partir_de(nombre_archivo)
                return []

            # 2. Si el archivo tiene contenido, intentamos procesarlo normalmente
            return cotizador.crear_lista_registros_a_partir_de(nombre_archivo)

        except (FileNotFoundError):
            self.ejecutarDialogCrearRegistros()
            return []

        except (ValueError) as descripcion_de_error:
            # Aquí cae tu Test 2: Muestra el error avisando que el archivo está corrupto
            self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))
            # Abre el diálogo para que el usuario cree datos nuevos y pise el archivo roto
            self.ejecutarDialogCrearRegistros()
            
            # Intentamos retornar los registros nuevos generados post-diálogo
            try:
                if os.path.exists(nombre_archivo) and os.path.getsize(nombre_archivo) > 0:
                    return cotizador.crear_lista_registros_a_partir_de(nombre_archivo)
            except Exception:
                pass
            
            return []

        # zzz:bool = False

        # while not zzz:
        #     zzz = self.xxx(nombre_archivo) 

        # try: 
        #     if(os.path.getsize(nombre_archivo) == 0):
        #         self.ejecutarDialogCrearRegistros()
        #     #     lista_registros:list[Material] = cotizador.crear_lista_registros_a_partir_de(nombre_archivo)
        #     #     #lista_registros:list[Material] = self.cargar_lista_registros(nombre_archivo)
        #         lista_registros:list[Material] = []
        #     else:
        #         lista_registros:list[Material] = cotizador.crear_lista_registros_a_partir_de(nombre_archivo)

        # except (FileNotFoundError):
            
        #     self.ejecutarDialogCrearRegistros()
        #     #lista_registros:list[Material] = self.cargar_lista_registros(nombre_archivo)
        #     lista_registros:list[Material] = []

        # except (ValueError) as descripcion_de_error:
        #     self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))

        #     self.ejecutarDialogCrearRegistros()
        #     #lista_registros:list[Material] = self.cargar_lista_registros(nombre_archivo)
        #     lista_registros:list[Material] = []

        #     #lista_registros:list[Material] = cotizador.crear_lista_registros_a_partir_de(nombre_archivo)

        # return lista_registros

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


    def registrarTodosLosRegistrosDeCostoAgregados(self, input_costo_mano_obra:str):
        materiales_a_agregar = self.materiales_agregados.copy()
        materiales_a_agregar.append(ManoDeObra(input_costo_mano_obra))
        cotizador.registrarListaRegistros(materiales_a_agregar, ARCHIVO_REGISTROS)

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

    def noSaltaErrorAlRegistrarRegistrosDeCosto(self) -> bool:
        input_costo_mano_obra = self.input_costo_mano_de_obra.text()

        if(self.materiales_agregados == []):
            self.ejecutarDialogDeErrorConDescripcion(
                DialogCrearRegistros.noHayMaterialesAgregadosParaRegistrarDescripcionDeError())
            return False
        
        elif(input_costo_mano_obra == ""):
            self.ejecutarDialogDeErrorConDescripcion(DialogCrearRegistros.noSePuedeGuardarSinUnPrecioDeManoDeObra())
            return False
        
        else:
            try:
                self.registrarTodosLosRegistrosDeCostoAgregados(input_costo_mano_obra)
                return True
            except (ValueError, TypeError) as descripcion_de_error:
                self.ejecutarDialogDeErrorConDescripcion(str(descripcion_de_error))
                return False
            
    def guardarTodoYCerrar(self):

        if (self.noSaltaErrorAlRegistrarRegistrosDeCosto()):
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
