import QtQuick.Layouts 1.14
import QtQuick 2.14

ColumnLayout{

    id: test
    property int num
    property int depth
    property bool touche: false
    property bool navire: false
    Layout.fillWidth : true



    Connections {
        target : Jeu
        onTir_subit:{
            touche = Jeu.get_defense_touche(num, depth)
        }
    }

    DropArea {

        id: dropArea
        width: 35
        height: 35
        onDropped: console.log(num + " " + depth + " " + drag.source.height/35 + " " + drag.source.width/35 + " " + drag.source.rotation)

        Rectangle {
            id : rect
            height : 35
            width : 35
            color : (navire || mouseA.containsMouse) ? "#54647d" : "transparent"
            border.width : 1
            opacity : mouseA.containsMouse ? 0.5 : 1

            states: [
                State {
                    when: dropArea.containsDrag
                    PropertyChanges {
                        target: rect
                        color: "yellow"
                    }
                }
            ]

            Image{
                id : img
                source : navire ? "../Images/cross.png" : "../Images/close.png"
                width : navire ? (parent.width * 0.85) : (parent.width * 0.65)
                height : width
                anchors.centerIn: parent
                opacity : touche

                Behavior on opacity{
                    NumberAnimation{
                        duration : 420
                    }
                }

            }
            MouseArea {
                id : mouseA
                anchors.fill : parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                hoverEnabled : true
                onClicked:{
                    if(mouse.button == Qt.LeftButton){
                        navire = !navire
                    }
                    if(mouse.button  == Qt.RightButton){
                        touche = !touche
                    }
                    console.log("index: " + num + " depth : " + depth)
                }
            }
        }
    }
}
