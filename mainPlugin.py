from qgis.utils import *
from qgis.core import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
from .resources import abrir_buscador

class pluginTest:

    def __init__(self,iface):
        self.iface = iface
    
    def initGui(self):
        #Añadir una herramienta que lleva directamente a la documentacion de la api en el buscador
        #Añade un boton para ir a la api de qgis 
        icon = os.path.join(os.path.expanduser('~'),'Pictures','house.svg')
        self.accion = QAction(QIcon(icon),'Documentacion',self.iface.mainWindow())
        self.accion.triggered.connect(abrir_buscador)
        self.iface.addToolBarIcon(self.accion)
    
    def unload(self):
        #esto deberia remover el boton de accion para ir a la api de QGIS
        self.iface.removeToolBarIcon(self.accion)
        del self.accion

    
