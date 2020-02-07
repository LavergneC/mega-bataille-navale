import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "Attaque"
import "Defense"
import "Page_connexion"


RowLayout{
    Layout.margins : 20
    anchors.fill : parent
    spacing : 10
    Button{
        id: but_att
        text: "Attaque "
        onClicked: {
            Jeu.simulate();
        }
    }
    RowLayout{}
    CarteAttaque{
        id : attaq
    }
    RowLayout{}

    ToolSeparator {
        Layout.fillHeight : true
        Layout.maximumHeight : attaq.implicitHeight + 40
    }
    RowLayout{}

    CarteDefense{
        id : carteDef
        focus : true
    }

    RowLayout{}           
}           
