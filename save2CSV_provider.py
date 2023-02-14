import os
import inspect
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from .save2CSV import save2CSV

class save2CSV_provider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)
    
    def unload(self):
        pass
    
    def loadAlgorithms(self):
        self.addAlgorithm(save2CSV())
    
    def id(self):
        return 'save_attributes'
    
    def name(self):
        return self.tr('save attributes')
    
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder,'house.svg')))
        return icon
    
    def longName(self):
        return self.name()