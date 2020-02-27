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

    Button{
        onClicked: attaqueswipe.currentIndex ++
    }
    RowLayout{
        ColumnLayout{
            Layout.margins: 20
            ColumnLayout{}
            
            Text {
                id: placementnavires
                text: qsTr("Veulliez placer vos navires :")
                Layout.alignment: Qt.AlignHCenter
                font.pointSize: 24
            }
            StackLayout {

                id: attaqueswipe
                Placement_navires{
                    id : placementNavires
                }
                CarteAttaque{
                    id : attaq
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
