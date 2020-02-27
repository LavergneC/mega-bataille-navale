import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{

    property bool serveurOuvert : false

    id:joint
    Layout.fillWidth: true
    spacing: 10

    GridLayout {
        id: info
        columns: 2
        Layout.fillWidth: true
        rowSpacing: 20
        columnSpacing: 20
        Layout.margins: 20

        Text {
            id: addip
            text: ("Adress IP de l'hôte")
            font.pointSize: 14
        }

        TextField {
            enabled: false
            id:ip
            text : Jeu.getIP()
            Layout.fillWidth: true
        }
        Text {
            id: port
            text: ("Port d'acces à la partie")
            font.pointSize: 14
        }

        TextField {
            enabled: false
            id: saisiport
            text: Jeu.getPort()
            Layout.fillWidth: true
        }

    }
    RowLayout{
        RowLayout{
        }

        Button {
            Layout.minimumWidth: 200
            Layout.alignment: Qt.AlignRight
            text : "Mise en ligne du serveur"
            onClicked: {
                Jeu.set_nom(nom_joueur.text)
                popartie.open()
                Jeu.heberger()
            }
        }
        RowLayout{
        }
    }

}
