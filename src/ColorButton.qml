 import QtQuick 2.1

 Item {
    id: colorButton
    width: 13
    height: 15

    property string colorStyle: "red"
    signal clicked()

    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 13
        height: 13


        color: colorButton.colorStyle
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.2)
    }



    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            selectArea.border.color = Qt.rgba(1,1,1,0.6)
        }
        onExited: {
            selectArea.border.color = Qt.rgba(1,1,1,0.2)
        }

        onClicked:{
            selectArea.border.color = Qt.rgba(1,1,1,1)
            colorTool.colorStyle = colorStyle
        }
    }
}