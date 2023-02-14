from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination)


class save2CSV(QgsProcessingAlgorithm):
    """
    Este algoritmo almacena los atributos de las entidades 
    de la capa activa en un fichero CSV
    """
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return save2CSV()

    def name(self):
        return 'save2CSV'

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'csv'

    def shortHelpString(self):
        return self.tr("Saves de active layer in a CSV file")

    def initAlgorithm(self, config=None):
        #Inicializa el input y el output del algoritmo para
        #recibir una capa vectorial y devolver un fichero CSV
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output File'),
                'CSV file(*.csv)',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        #guarda en source la capa de entrada
        source = self.parameterAsSource(parameters, self.INPUT, context)
        #guarda en csv el path al fichero donde guardar los datos de la capa
        csv = self.parameterAsFileOutput(parameters,self.OUTPUT,context)
        #Atributos que se van a almacenar
        nombre_atributos = [atri.name() for atri in source.fields()]
        
        #Los pasos que va a dar la progress bar
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
        
        #Abre y cierra el fichero CSV automaticamente
        with open(csv,'w') as f:
            #extraigo el nombre de los atributos
            nombre_atributos = [atri.name() for atri in source.fields()]
            line = '#'.join(name for name in nombre_atributos) + '\n'
            f.write(line)
            for current, feature in enumerate(features):
                # Stop the algorithm if cancel button has been clicked
                if feedback.isCanceled():
                    break
                #recorro todas las entidades almacenando en el CSV el valor de sus atributos
                line = '#'.join(str(feature[atributo]) for atributo in nombre_atributos) + '\n'
                f.write(line)
                # Update the progress bar
                feedback.setProgress(int(current * total))

        return {self.OUTPUT: csv}
