import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "Attaque"
import "Defense"
import "Page_connexion"
import "Placement_navires"

RowLayout{

    property int navireRestant: 18
    property string etattir

    Layout.margins : 20
    anchors.fill : parent
    spacing : 10

    Button{
        onClicked: attaqueswipe.currentIndex ++
    }

    Text {
        id: infopartie
        text: etattir

    }
    RowLayout{
        ColumnLayout{
            Layout.margins: 20
            ColumnLayout{}

        }
        Connections{
            target: Jeu
            onPartie_en_cours_changed:
            {
                if (Jeu.get_partie_gagnee())
                    attaqueswipe.currentIndex ++
                else
                    attaqueswipe.currentIndex +=2
            }
        }
        ColumnLayout{}
        StackLayout {
            id: attaqueswipe
            Placement_navires{
                id : placementNavires
            }
            CarteAttaque{
                id : attaq
            }
            Fin_jeu{
                sourceimage :"Images/victoire.jpg"
                taillelarg: 500
                taillelong: 500
            }
            Fin_jeu{
                sourceimage :"Images/defeat2.jpg"
                taillelarg: 500
                taillelong: 500
            }

            onCurrentIndexChanged: carteDef.focus = true
        }
        ColumnLayout{}
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
