import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

Popup{
    id: pop
    visible: false
    modal : true
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)
    background: Rectangle {
        Image {
        anchors.fill: parent
        source: back
    }
 }


    property string message
    property string image
    property bool bouton : false
    property bool busyindi: false
    property string back : ""

    ColumnLayout{
        spacing: 10
        anchors.fill : parent

        RowLayout{
            spacing: 10
            Layout.fillWidth: true

            Image {
                source: image
                sourceSize.width: 80
                sourceSize.height: 80
            }

            Text {
                wrapMode: Text.Wrap
                text : message
                font.pixelSize: 18
            }
        }

        Button {
            opacity: bouton
            text : "Ok"
            onClicked: pop.close()
            Layout.alignment: Qt.AlignCenter
        }

        ProgressBar {
            visible: busyindi
            indeterminate:true
            Layout.alignment: Qt.AlignCenter
        }
    }
}
