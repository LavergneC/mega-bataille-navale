import QtQuick.Layouts 1.14
import QtQuick 2.14

import "../Page_connexion"

ColumnLayout{
    property var touches: [0,0,0]
    property var impacts: [0,0,0]
    property var coules : [0,0,0]
    property int num
    property int nbtest: 0
    Layout.fillWidth : true
    
    Connections {
        target : Jeu
        onTir_feedback_received:{
            touches = Jeu.get_case_attaque(num)
            impacts = Jeu.get_case_impacts(num)
            coules = Jeu.get_case_coules(num)
        }
    }

    Rectangle{
        id : rect
        height : 35
        width : 35
        border.width : 1
        color : (mouseB.containsMouse) ? "#54647d" : "transparent"
        opacity : mouseB.containsMouse ? 0.5 : 1

        MouseArea {
            id : mouseB
            anchors.fill : parent
            acceptedButtons: Qt.LeftButton
            hoverEnabled : true
            onClicked: {
                nbtest ++
                if (Jeu.droit_de_tirer()) {
                    Jeu.tirer(num % 15, Math.trunc(num/15)) //console.log (num % 15 + " " + Math.trunc(num/15))
                }
                else {
                    if(nbtest == 1){
                        attenttontour.open()
                    }
                    else if(nbtest == 2){
                        attenttontour1.open()
                    }
                    else {
                        attenttontour2.open()
                    }
                }
            }
            onEntered: {
                if (Jeu.droit_de_tirer()) {
                    etattir = "<font color=\"black\">information du tir:<br> <font color=\"green\"> A ton tour de tirer</font>"
                }
                else {
                    etattir = "<font color=\"black\">information du tir:<br> <font color=\"red\"> En attente du tir adverse</font>"
                }
            }
        }
        ColumnLayout{
            anchors.fill : parent
            spacing : 2

            Repeater{
                model : 3
                Rectangle{
                    Layout.fillWidth : true
                    Layout.fillHeight : true
                    Layout.margins : 2
                    radius : 3

                    color : coules[index] ? "black" : (touches[index] ? "red": (impacts[index] ? "blue" : "transparent"))
                }
            }
        }
    }
    Ma_popup{
        id: attenttontour
        message : "Attends ton tour s'il te plait :)"
        bouton: true
    }
    Ma_popup{
        id: attenttontour1
        message : "Attends ton tour !!!!!"
        bouton: true
    }
    Ma_popup{
        id: attenttontour2
        message : "Tu comprends pas quoi dans : ATTENDS ?????"
        bouton: true
    }
}
