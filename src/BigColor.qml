import QtQuick 2.1

Rectangle {
    id: bigColor
    width: 15
    height: 15


    property string imageName: ""

    signal pressed()
    Rectangle {

       anchors.centerIn: parent
       width: 20
       height: 20
       radius: 2

       visible: false
       color: "white"
       opacity: 0.2
    }

    Image {
        id:colorImage
        anchors.centerIn: parent

        width: 20
        height: 20
        source: "../image/color_big/" + bigColor.imageName + ".png"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onPressed:{
            bigColor.pressed()
        }

    }

}