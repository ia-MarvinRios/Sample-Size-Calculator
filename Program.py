import sys
from SampleSize import *
from PyQt6 import sip
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import *

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        central_widget = QWidget()
        self.validator = QIntValidator()
        self.sesion = SampleSize()
        self.layout = QHBoxLayout()
        
        window.setCentralWidget(self, central_widget)
        central_widget.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setWindowTitle("SampleSize Calculator")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(400, 500)
        self.setMaximumSize(400, 500)

        self.I = 1
        self.G = 1
        self.finiteLayout()
    
    #FUNCIÓN ENCARGADA DE TOMAR LOS DATOS DE LOS LINEEDITS
    def getData(self):
        if self.G == 1:
            if (self.check_input()):
                data = [self.population.text(), self.trust.text(), self.success.text()]
                new_data = []
                for value in data:
                    value = value.replace(" ", "").replace("-", "").replace("+","")
                    if value:
                        value = int(value)
                        new_data.append(value)
                    else:
                        value = 0
                        new_data.append(value)

                    print("NEW ENTRY | ", value, ": ",type(value))

                a, b, c = new_data[0], new_data[1], new_data[2]

                self.label_result.setText(str(round(self.sesion.finitePopulation(a,b,c), 2)))
            else:
                pass

        if self.G == 0:
            if (True):
                data = [self.trust.text(), self.success.text()]
                new_data = []
                for value in data:
                    value = value.replace(" ", "").replace("-", "").replace("+","")
                    if value:
                        value = int(value)
                        new_data.append(value)
                    else:
                        value = 0
                        new_data.append(value)

                    print("NEW ENTRY | ", value, ": ",type(value))

                a, b = new_data[0], new_data[1]

                self.label_result.setText(str(round(self.sesion.infinitePopulation(a,b), 2)))
    
    def check_input(self):
        if self.population.text().replace("-", "").replace("+", "") and int(self.population.text()) > 0:
            return True
        else:
            QMessageBox.warning(self, "Error", "INVALID POPULATION\nPOBLACIÓN INVÁLIDA.")
            return False
    
    def createObjects(self):
        if (hasattr(self, 'frame1') and isinstance(self.frame1, QFrame) or hasattr(self, 'frame2') and isinstance(self.frame2, QFrame)):
            sip.delete(self.frame1)
            sip.delete(self.frame2)

        #Establecer los 2 marcos de la ventana
        self.frame1, self.frame2 = QFrame(), QFrame()
        
        #Crear objetos de la ventana
        self.finit, self.infinite = QPushButton(self.frame1), QPushButton(self.frame1) #Crear los botones de tipo de cálculo
        self.trust, self.label_trust = QLineEdit(self.frame1), QLabel(self.frame1) #Nivel de confianza
        self.success, self.label_success = QLineEdit(self.frame1), QLabel(self.frame1) #Probabilidad de éxito
        self.label_result =  QLabel(self.frame2)
        self.lang = QPushButton(self.frame2)
        self.calculate = QPushButton(self.frame1)

        #Crear el comboBox y esconderlo
        self.combo = QComboBox(self.frame2)
        self.combo.addItem("English")
        self.combo.addItem("Español")
        self.combo.hide()

        #Agregar objetos al layout
        self.layout.addWidget(self.frame1)
        self.layout.addWidget(self.frame2)

        self.setUpFrames()

    def setUpFrames(self):
        #Definir el estilo y posición de los frames
        self.frame1.setGeometry(0,0,200,500)
        self.frame1.setStyleSheet("background-color: rgb(89, 214, 187);")
        self.frame2.setGeometry(200,0,200,500)
        self.frame2.setStyleSheet("background-color: rgb(223, 223, 223);")

        #BOTONES FINITO/INFINITO

        #FINITO
        self.finit.setGeometry(10,10,50,30)
        self.finit.setText("Finita")
        self.finit.setStyleSheet("background-color: white;")
        #INFINITO
        self.infinite.setGeometry(140,10,50,30)
        self.infinite.setText("Infinita")
        self.infinite.setStyleSheet("background-color: white;")

        #BOTÓN DE IDIOMA
        self.lang.setGeometry(150,10,40,30)
        self.lang.setText("LANG")

        #COMBO BOX
        self.combo.setGeometry(10,10,70,25)
        self.combo.setStyleSheet("background-color: #fff;")

        #Al presionar los botones dentro de la ventana:

        #Botón de Calcular
        self.calculate.clicked.connect(self.getData)
        #Botón finito
        self.finit.clicked.connect(self.finiteLayout)
        #Botón infinito
        self.infinite.clicked.connect(self.infiniteLayout)
        #Botón de idioma
        self.lang.clicked.connect(self.toggleComboBox)
        self.combo.setCurrentIndex(self.I)
        self.combo.currentIndexChanged.connect(self.changeLang)

    def finiteLayout(self):
        self.G = 1
        self.createObjects()
        self.population, self.label_population = QLineEdit(self.frame1), QLabel(self.frame1) #Población        

        #POBLACIÓN
        self.population.setGeometry(50,100,100,23)
        self.population.setStyleSheet("background-color: white;")
        self.population.setPlaceholderText("0")
        self.label_population.setGeometry(70,60,150,23)
        #self.label_population.setText("Población")

        #NIVEL DE CONFIANZA
        self.trust.setGeometry(50,200,100,23)
        self.trust.setStyleSheet("background-color: white;")
        self.trust.setPlaceholderText("99")
        self.label_trust.setGeometry(40,160,150,23)
        #self.label_trust.setText("Nivel de Confianza (%)")

        #POSIBILIDAD DE ÉXITOS
        self.success.setGeometry(50,300,100,23)
        self.success.setStyleSheet("background-color: white;")
        self.success.setPlaceholderText("50")
        self.label_success.setGeometry(35,260,150,23)
        #self.label_success.setText("Probabilidad de Éxito (%)")

        #BOTON
        self.calculate.setGeometry(65,350,60,30)
        self.calculate.setStyleSheet("background-color: white;")
        #self.calculate.setText("Calcular")

        #RESULTADO
        self.label_result.setGeometry(75,242,150,25)
        #self.label_result.setText("RESULTADO")

        self.changeLang()

        #Evitar caracteres no válidos:
        self.population.setValidator(self.validator)
        self.trust.setValidator(self.validator)
        self.success.setValidator(self.validator)

    def infiniteLayout(self):
        self.G = 0
        self.createObjects()

        #NIVEL DE CONFIANZA
        self.trust.setGeometry(50,200,100,23)
        self.trust.setStyleSheet("background-color: white;")
        self.trust.setPlaceholderText("99")
        self.label_trust.setGeometry(40,160,150,23)
        #self.label_trust.setText("Nivel de Confianza (%)")

        #POSIBILIDAD DE ÉXITOS
        self.success.setGeometry(50,300,100,23)
        self.success.setStyleSheet("background-color: white;")
        self.success.setPlaceholderText("50")
        self.label_success.setGeometry(35,260,150,23)
        #self.label_success.setText("Probabilidad de Éxito (%)")

        #BOTON
        self.calculate.setGeometry(65,350,60,30)
        self.calculate.setStyleSheet("background-color: white;")
        #self.calculate.setText("Calcular")

        #RESULTADO
        self.label_result.setGeometry(75,242,150,25)
        #self.label_result.setText("RESULTADO")

        self.changeLang()

        #Evitar caracteres no válidos:
        self.trust.setValidator(self.validator)
        self.success.setValidator(self.validator)
    
    def toggleComboBox(self):
        if self.combo.isHidden():
            self.combo.show()
        else:
            self.combo.hide()
    
    def changeLang(self):
        if (self.combo.currentIndex() == 0):
            self.I = 0
            self.finit.setText("Finite")
            self.infinite.setText("Infinite")

            self.label_trust.setText("Confidence Level (%)")
            self.label_success.setText("Success Probability (%)")
            self.calculate.setText("Calculate")
            
            self.label_result.setText("RESULT")

            if (self.G == 1):
                self.label_population.setText("Population")

        if (self.combo.currentIndex() == 1):
            self.I = 1
            self.finit.setText("Finita")
            self.infinite.setText("Infinita")

            self.label_trust.setText("Nivel de Confianza (%)")
            self.label_success.setText("Probabilidad de Éxito (%)")
            self.calculate.setText("Calcular")

            self.label_result.setText("RESULTADO")

            if (self.G == 1):
                self.label_population.setText("Población")

        else:
            pass

#EJECUTAR PROGRAMA
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec())