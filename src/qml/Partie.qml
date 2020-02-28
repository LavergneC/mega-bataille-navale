import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "Attaque"
import "Defense"
import "Page_connexion"
import "Placement_navires"


RowLayout{

    property int navireRestant: 18

    Layout.margins : 20
    anchors.fill : parent
    spacing : 10

    property string etattir: "A toi de jouer !"

    Button{
        onClicked: attaqueswipe.currentIndex ++
    }
    RowLayout{
        ColumnLayout{
            Layout.margins: 20
            ColumnLayout{}
            Text {
                id: placementnavires
                text: qsTr("Veuillez placer vos navires :")
                Layout.alignment: Qt.AlignHCenter
                font.pointSize: 24
            }
            Text {
                id: infopartie
                text: {
                    if(Jeu.droit_de_tirer())
                        ""

                    else {
                        "En attente du tir adverse"
                    }
                }
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
                }
                Fin_jeu{
                    sourceimage :"Images/defeat.jpg"
                }

                onCurrentIndexChanged: carteDef.focus = true
            }
            ColumnLayout{}
        }
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
