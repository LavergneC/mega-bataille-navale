import QtQuick 2.6
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14


RowLayout{
    ColumnLayout{
        Layout.margins : 20
        ColumnLayout{}
        SwipeView {
            orientation : Qt.Vertical
            interactive : false
            clip : true
            id : stacklayout
            Repeater{
                model : 3
                GridLayout {
                    id : defGrid
                    rowSpacing : 0
                    columnSpacing : 0
                    columns : 15
                    Repeater{
                        model : 225
                        CaseDef {
                            num : index
                        }
                    }
                }
            }
        }
        ColumnLayout{}
    }

    CustomPageIndicator {
        Layout.rightMargin : 10
        Layout.alignment : Qt.AlignVCenter
        currentIndex: stacklayout.currentIndex
        count: stacklayout.count
    }
    onVisibleChanged:{
        focus = true
    }

    Keys.onPressed: {
        console.log(event.key)
        if (event.key == Qt.Key_1 || event.key == 38) {
            stacklayout.currentIndex = 0
            event.accepted = true;
        }
        else if (event.key == Qt.Key_2 || event.key == 201) {
            event.accepted = true;
            stacklayout.currentIndex = 1
        }
        else if (event.key == Qt.Key_3 || event.key == 34) {
            stacklayout.currentIndex = 2
            event.accepted = true;
        }
        else if (event.key == 16777235 && stacklayout.currentIndex > 0){
            stacklayout.currentIndex --
            event.accepted = true;
        }
        else if (event.key == 16777237 && stacklayout.currentIndex < 2){
            stacklayout.currentIndex ++
            event.accepted = true;
        }
        console.log(stacklayout.currentIndex)
    }
}