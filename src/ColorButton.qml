 import QtQuick 2.1

 Item {
    id: colorButton
    width: 13
    height: 15

    property string colorStyle: "red"
    signal clicked()

    Rectangle {
        id: selectcolor
        anchors.centerIn: parent
        width: 13
        height: 15
        color: colorButton.colorStyle

    }
    Rectangle {
        id: selectArea
        width: 13
        height: 14
        color: "transparent"
        border.width: 2
        border.color: Qt.rgba(1,1,1,0.3)
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            selectArea.border.color = Qt.rgba(1,1,1,0.7)
        }
        onExited: {
            selectArea.border.color = Qt.rgba(1,1,1,0.3)
        }

        onClicked:{
            selectArea.border.color = Qt.rgba(1,1,1,1)
            colorTool.colorStyle = colorStyle
        }
    }
}