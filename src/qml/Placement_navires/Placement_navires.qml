import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{
    id: infobat
    Layout.leftMargin: 20
    Layout.rightMargin: 20
    Layout.topMargin: 2
    Layout.fillWidth: true
    spacing: 3

    ListView {
        id : listBat
        orientation: ListView.Vertical
        Layout.fillWidth: true
        Layout.fillHeight: true


        model: ModelBateaux{}

        delegate: GridLayout {
            columns: 2
            id: boot
            visible: nbRestant > 0
            Layout.alignment: Qt.AlignTop

            property int nbRestant : nb

            Text {
                Layout.column: 0
                Layout.row: 0
                text: name
                font.pointSize: 11
                style: Text.Outline
                styleColor: "blue"
                Layout.alignment: Qt.AlignVCenter
            }

            Text {
                Layout.column: 1
                Layout.row: 1
                text: "x " + nbRestant
                font.pointSize: 14
                style: Text.Sunken
                styleColor: "blue"
                Layout.alignment: Qt.AlignVCenter
            }

            Drag_navires{
                id: gestionnavire
                Layout.column: 0
                Layout.row: 1
                nbRestant: boot.nbRestant
                onBateauDroped: boot.nbRestant --
            }
        }
    }
}
