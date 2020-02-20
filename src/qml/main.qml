import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import QtQuick.Window 2.14

import "Page_connexion"

ApplicationWindow{
    visible: true
    minimumWidth : connecte ? jeuWin.implicitWidth : connecWin.implicitWidth
    minimumHeight : connecte ? jeuWin.implicitHeight : connecWin.implicitHeight

    property bool connecte: false
    
    Connexion_Window{
        id : connecWin
        visible: !connecte
        anchors.fill : parent
    }

<<<<<<< Updated upstream
    Partie{
=======
    Jeujeu{
>>>>>>> Stashed changes
        id : jeuWin
        visible : connecte
        anchors.fill : parent
    }

    Button{
        onClicked : connecte = true
    }
}