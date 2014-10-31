import QtQuick 2.1

Item {
    id: bigColor
    width: 30
    height: 28

    property string colorStyle: "red"
    signal pressed()

    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 24
        height: 22
        radius: 4

        color: bigColor.colorStyle
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

        onPressed:{
            bigColor.pressed()
            selectArea.border.color = Qt.rgba(1,1,1,1)
        }

    }

}