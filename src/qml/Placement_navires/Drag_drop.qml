import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.0

//ColumnLayout {
//    Rectangle {
//        anchors.centerIn: parent
//        width: text.implicitWidth + 20; height: text.implicitHeight + 10
//        color: "green"
//        radius: 5
//        Drag.active: dragArea.drag.active
//        Drag.dragType: Drag.Automatic
//        Drag.supportedActions: Qt.CopyAction
//        Drag.mimeData: {
//            "text/plain": "Copied text"
//        }

//        MouseArea {
//            id: dragArea
//            anchors.fill: parent
//            drag.target: parent
//            onPressed: parent.grabToImage(function(result) {
//                parent.Drag.imageSource = result.url
//            })

//        }
//    }
//}
