import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

GridLayout{
    rowSpacing : 0
    columnSpacing : 0
    Layout.alignment : Qt.alignHCenter | Qt.alignVCenter
    Layout.margins : 20

    columns : 15
    Repeater{
        model : 225
        CaseAtt {
            num : index
        }
    }

}
