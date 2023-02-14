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
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return save2CSV()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm.
        """
        return 'save2CSV'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm.
        """
        return self.tr("Saves de active layer in a CSV file")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output File'),
                'CSV file(*.csv)',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        source = self.parameterAsSource(parameters, self.INPUT, context)
        csv = self.parameterAsFileOutput(parameters,self.OUTPUT,context)
        #Atributos que se van a almacenar
        nombre_atributos = [atri.name() for atri in source.fields()]
        
        #Los pasos que va a dar la progress bar
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
        
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
