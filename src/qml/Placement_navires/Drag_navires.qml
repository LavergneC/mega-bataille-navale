import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

Item {
visible : nbRestant > 1
    property int nbRestant
    signal bateauDroped

    id: root
    height: largeur * 35
    width: longueur * 35

    Rectangle {

        width: longueur * 35
        height: largeur * 35
        color: "grey"

    }

    MouseArea {
        property string commetuveux: "vzrvz"

        id: dragArea
        anchors.fill: parent
        acceptedButtons: Qt.AllButtons
        drag.target: bateau

        onReleased: {
            if(mouse.button  === Qt.RightButton){
                bateau.rotation = bateau.rotation == 90? 0 : 90
                console.log("on released : right")
            }
            if(mouse.button === Qt.LeftButton){
                parent = bateau.Drag.target !== null ? bateau.Drag.target : root
                if (bateau.Drag.target === null){
                    parent = root
                    bateau.parent = root

                }
                else {
                    bateau.Drag.drop()
                    //   bateau.visible = false
                    bateauDroped()
                    parent = root
                    bateau.parent = root
                }

            }

        }

        Rectangle {
            id: bateau
            width: longueur * 35
            height: largeur * 35
            color: "grey"
            Drag.active: dragArea.drag.active
            Drag.hotSpot.x: 15
            Drag.hotSpot.y: 15
            Drag.source: root
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }


        states: State {
            when: dragArea.drag.active
            ParentChange { target: bateau; parent: root }
            AnchorChanges { target: bateau; anchors.verticalCenter: undefined; anchors.horizontalCenter: undefined }
        }

        // }
        //   }
    }
}
