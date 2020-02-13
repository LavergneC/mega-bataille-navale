import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{
    property bool drop: false
    id: infobat
    Layout.leftMargin: 20
    Layout.rightMargin: 20
    Layout.topMargin: 50
    Layout.fillWidth: true
    spacing: 10

    ListView {
        orientation: ListView.Vertical
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        spacing: 3

        model: ModelBateaux{}
        delegate: GridLayout {
            columns: 2
            id: boot
            visible: nbRestant > 0

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
            Repeater {
                model: nb
                Rectangle {
                    Layout.column: 0
                    Layout.row: 1
                    id: bateau
                    width: longueur * 35
                    height: largeur * 35
                    color: "grey"
                    Drag.active: dragArea.drag.active
                    Drag.keys: "fr"
                    Drag.hotSpot.x: 15
                    Drag.hotSpot.y: 15
                    Drag.source: infobat

                    MouseArea {
                        id: dragArea
                        anchors.fill: parent
                        acceptedButtons: Qt.AllButtons
                        drag.target: bateau

                        onReleased: {
                            if(mouse.button  == Qt.RightButton){
                                bateau.rotation = bateau.rotation == 90? 0 : 90
                                console.log("on released : right")
                            }
                            if(mouse.button == Qt.LeftButton){
                                drop = true
                                parent = bateau.Drag.target !== null ? bateau.Drag.target : boot
                                bateau.Drag.drop()
                                bateau.visible = false
                                nbRestant --
                                console.log("on released : left")
                            }
                        }
                        states: State {
                            when: dragArea.drag.active
                            ParentChange { target: bateau; parent: boot }
                            AnchorChanges { target: bateau }
                        }
                    }
                }
            }
        }
    }
}
