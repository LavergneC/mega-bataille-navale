import sys

from PySide2.QtCore import QObject, Signal, Property
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtQml import QQmlApplicationEngine
from jeu import *

if __name__ == "__main__":
    jeu = Jeu()
    jeu.connection = Reseau()

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Expose the Python object to QML
    context = engine.rootContext()
    context.setContextProperty("Jeu", jeu)

    engine.load("src/qml/main.qml")
    sys.exit(app.exec_())
