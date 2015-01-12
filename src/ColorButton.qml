import QtQuick 2.1

Item {
    id: colorButton
    width: 12
    height: 15

    property string colorStyle: "red"
    signal clicked()

    Rectangle {
        id: selectcolor
        anchors.centerIn: parent
        width: 14
        height: 14
        color: colorButton.colorStyle

        border.width: 1
        border.color: "transparent"
    }
    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 12
        height: 12
        color: "transparent"
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.3)
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: windowView.set_cursor_shape("color_pen_purple")
        onEntered: {
            selectcolor.border.color = "#01bdff"
            selectArea.border.color = Qt.rgba(1,1,1,0.7)
        }
        onExited: {
            selectcolor.border.color = "transparent"
            selectArea.border.color = Qt.rgba(1,1,1,0.3)
        }

        onClicked:{
            selectArea.border.color = Qt.rgba(1,1,1,1)
            colorTool.colorStyle = colorStyle
        }
    }
}
