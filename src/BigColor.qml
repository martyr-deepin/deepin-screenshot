import QtQuick 2.1

Item {
    id: bigColor
    width: 30
    height: 28

    property string imageName: ""
    signal pressed()

    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 24
        height: 22
        radius: 4

        visible: false
        color: "white"
        opacity: 0.2
    }

    Image {
        id:colorImage
        anchors.centerIn: parent

        width: 18
        height: 18
        source: "../image/color_big/" + bigColor.imageName + ".png"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            selectArea.visible = true
        }

        onExited: {
            selectArea.visible = false
        }

        onPressed:{
            bigColor.pressed()
        }

    }

}