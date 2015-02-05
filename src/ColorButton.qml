import QtQuick 2.1

Rectangle {
    id: colorButton
    width: 12
    height: 12
    color: colorButton.colorStyle

    property int colorOrder: 3
    property string colorStyle: "red"
    signal clicked()

    Rectangle {
        id: selectArea
        color: "transparent"
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.3)

        anchors.fill: parent
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: windowView.set_cursor_shape("color_pen_purple")
        onEntered: {
            selectArea.border.color = Qt.rgba(1,1,1,0.7)
        }
        onExited: {
            selectArea.border.color = Qt.rgba(1,1,1,0.3)
        }

        onClicked:{
            selectArea.border.color = Qt.rgba(1,1,1,1)
            colorTool.colorStyle = colorStyle
            colorTool.colorOrder = colorOrder
            windowView.set_save_config("common_color_linewidth", "color_index", colorOrder)
        }
    }
}
