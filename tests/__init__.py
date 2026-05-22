import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit)
from collections.abc import Callable
#este import era lo que ejecutaba la ventana y hacía que se viera
import ventana_cotizador
from ventana_cotizador import (Ventana, DialogCrearRegistros, DialogDescripcionDeError) 
import cotizador_para_moldes_de_soplado as cotizador
from cotizador_para_moldes_de_soplado import (RegistroDeCosto, Material, ManoDeObra)


__all__ = ['pytest','Qt', 'QDialog', 'QLabel', 'QLineEdit', 'Callable', 'ventana_cotizador',
            'Ventana', 'RegistroDeCosto', 'DialogCrearRegistros', 'cotizador', 
            'test_cot', 'Material', 'ManoDeObra', 'DialogDescripcionDeError']

