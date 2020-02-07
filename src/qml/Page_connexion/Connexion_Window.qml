import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{
    property bool attente: false
    property bool attente1: false
    property bool rechercheadv: true

    spacing: 30
    Layout.rightMargin: 10
    Layout.leftMargin: 10

    Text {
        id: titre
        text: qsTr("Connexion méga bataille navale")
        font.pointSize: 22
        Layout.alignment: Qt.AlignCenter
        Layout.leftMargin: 22
        Layout.rightMargin: 22
        Layout.topMargin: 10
    }

    TabBar {
        id: bar
        Layout.alignment: Qt.AlignTop
        Layout.fillWidth: true

        TabButton {
            text: qsTr("Rejoindre")
        }
        TabButton {
            text: qsTr("Héberger")
        }
    }
    SwipeView{
        id:vuconnexion
        currentIndex: bar.currentIndex
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignTop
        interactive: false

        Rejoindre{
        }
        Heberger{
        }
    }

    Ma_popup{
        id:pop
        image:"../Images/attention.svg"
        message : "Veuillez vérifier les information rentrées ..."
        bouton: true
    }

    Ma_popup{
        id:popartie
        back:"../Images/bateau.jpg"
        message : "En attente d'adversaire !! Préparez-vous à la bataille"
        bouton: false
        busyindi: true
    }
}
