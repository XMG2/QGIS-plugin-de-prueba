from qgis.utils import *
from qgis.core import QgsProcessingAlgorithm, QgsApplication
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
import os
import webbrowser
import inspect
import processing
from .save2CSV_provider import save2CSV_provider

class pluginTest:

    def __init__(self,iface):
        self.iface = iface
        self.provider = None
    
    def initProcessing(self):
        #Instancia el algoritmo de procesamiento
        self.provider = save2CSV_provider()
        QgsApplication.processingRegistry().addProvider(self.provider)
    
    def initGui(self):
        #Añade un boton para ir a la api de qgis 
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(cmd_folder,'house.svg'))
        self.accion = QAction(icon,'Documentacion',self.iface.mainWindow())
        self.accion.triggered.connect(self.abrir_buscador)
        self.iface.addToolBarIcon(self.accion)
        
        #Algoritmo de procesamiento
        self.initProcessing()
        self.accion2 = QAction(icon,'Guardar atributos en CSV',self.iface.mainWindow())
        self.accion2.triggered.connect(self.run)
        self.iface.addPluginToMenu('Guardar Atributos',self.accion2)
        self.iface.addToolBarIcon(self.accion2)
    
    def unload(self):
        #Eliminar boton de documentacion
        self.iface.removeToolBarIcon(self.accion)
        del self.accion
        
        #Eliminar algoritmo de procesamiento
        QgsApplication.processingRegistry().removeProvider(self.provider)
        self.iface.removeToolBarIcon(self.accion2)
        self.iface.removePluginMenu('Guardar Atributos',self.accion2)
        del self.accion2
    
    def run(self):
        #Es una funcion aparte para iniciar la ejecucion del algoritmo de procesamiento
        processing.execAlgorithmDialog('save_attributes:save2CSV')
    
    def abrir_buscador(self):
        webbrowser.open('https://api.qgis.org/api/')