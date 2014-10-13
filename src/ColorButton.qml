import QtQuick 2.1

Item {
    id: colorButton
    width: 15
    height: 15


    property string imageName: ""

    signal clicked()

    Rectangle {
       id: selectArea
       anchors.centerIn: parent
       width: 13
       height: 13
       radius: 2

       visible: false
       color: "white"
       opacity: 0.2
    }

    Image {
        id:colorImage
        source: "../image/color/" + colorButton.imageName + ".png"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            colorImage.source = "../image/color/" + colorButton.imageName + "_hover.png"
        }
        onExited: {
            colorImage.source = "../image/color/" + colorButton.imageName + ".png"
        }

        onClicked:{
            colorTool.imageName = imageName
        }

    }

}