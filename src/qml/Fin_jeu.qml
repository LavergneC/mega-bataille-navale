import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

ColumnLayout{
    Layout.leftMargin: 20
    Layout.rightMargin: 20
    Layout.topMargin: 2
    Layout.fillWidth: true
    spacing: 3

    Image{
        id : img
        source : "../qml/Images/victoire.jpg"
        Layout.fillWidth: parent
    }

}
