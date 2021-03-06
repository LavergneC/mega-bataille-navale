import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

Item {
    property int rota: bateau.rotation
    property string color : "grey"
    property int nbRestant
    signal bateauDroped

    Action {
        enabled : bateau.parent == root
        id: rotate
        shortcut: "R"
        onTriggered: {
            bateau.rotation = bateau.rotation == 90? 0 : 90
        }
    }

    id: root
    height: largeur * 35
    width: longueur * 35

    Rectangle {
        width: longueur * 35
        height: largeur * 35
        color: "gray"
        visible : nbRestant > 1
    }

    MouseArea {
        id: dragArea
        anchors.fill: parent
        drag.target: bateau
        onReleased: {
            root.color = "gray"
            if(mouse.button === Qt.LeftButton){
                parent = bateau.Drag.target !== null ? bateau.Drag.target : root
                if (bateau.Drag.target === null){
                    parent = root
                    bateau.parent = root
                }
                else if (!bateau.Drag.target.positionDisponible(longueur, largeur, rota)){
                    parent = root
                    bateau.parent = root
                }
                else {
                    bateau.Drag.drop()
                    bateauDroped()
                    parent = root
                    bateau.parent = root
                    navireRestant --
                    if (navireRestant == 0){
                        attaqueswipe.currentIndex ++
                    }
                }
                bateau.rotation = 0
            }
        }

        Rectangle {
            z : 10
            id: bateau
            width: longueur * 35
            height: largeur * 35
            color: root.color
            Drag.active: dragArea.drag.active
            Drag.hotSpot.x: 15
            Drag.hotSpot.y: 15
            Drag.source: root
            Drag.onTargetChanged:{
                if (bateau.Drag.target !== null)
                    root.color = Drag.target.positionDisponible(longueur, largeur, rota) ? "grey" : "red"
            }
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            states: State {
                when: dragArea.drag.active
                ParentChange { target: bateau; parent: root }
                AnchorChanges { target: bateau; anchors.verticalCenter: undefined; anchors.horizontalCenter: undefined }
            }
        }
    }
}
