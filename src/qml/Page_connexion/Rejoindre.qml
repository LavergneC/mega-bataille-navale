import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{

    property bool coencours: false
    property bool entreescorrects: saisiport.acceptableInput && ip.acceptableInput

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
            text: ("Adresse IP de l'hôte ")
            font.pointSize: 14
        }

        TextField {
            id:ip
            placeholderText: qsTr("255.255.255.255")
            Layout.fillWidth: true
            validator: RegularExpressionValidator { regularExpression: /(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/ }
        }
        Text {
            id: port
            text: ("Port d'acces à la partie")
            font.pointSize: 14
        }

        TextField {
            id: saisiport
            placeholderText: qsTr("554")
            Layout.fillWidth: true
            validator: RegularExpressionValidator { regularExpression: /[0-9]{1,4}/ }
        }

    }
    RowLayout{
        RowLayout{

        }

        Button {
            Layout.minimumWidth: 200
            Layout.alignment: Qt.AlignRight
            text : "Connexion"
            onClicked: {
                if (entreescorrects)
                    coencours = !coencours
                else
                    pop.open()
            }
        }
        Indication_Connexion{
            tickState: entreescorrects
            displayBusy: joint.coencours
            Layout.minimumHeight: 70
            Layout.minimumWidth: 70
        }

        RowLayout{

        }
    }



}
