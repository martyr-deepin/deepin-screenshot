import QtQuick 2.1

Item {
    id: toolButton
    width: 30
    height: 28
    state: "off"

    property url dirAction: "../image/action/"
    property url dirActionMenu: "../image/action_menu/"
    property url dirSizeImage: "../image/size/"
    property url dirColor_big: "../image/color_big/"
    property url dirShareImage:"../image/share/"
    property url dirSave: "../image/save/"

    property string imageName: ""
    property string dirImage:dirAction

    property var group: null

    signal clicked()
    signal pressed()
    signal entered()
    signal exited()
    states: [
            State {
                    name : "on"
                    PropertyChanges {
                        target:toolImage
                        source: toolButton.dirImage + toolButton.imageName + "_press.png"
                     }
            },
            State {
                    name : "off"
                    PropertyChanges {
                        target:toolImage
                        source: toolButton.dirImage + toolButton.imageName + ".png"
                    }
        }
    ]

    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 24
        height: 20
        radius: 2
        visible: false

        color: "white"
        opacity: 0.2
    }

    Image {
        id: toolImage
        width: 22
        height: 22
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            selectArea.visible = true
            toolImage.source = toolButton.dirImage + toolButton.imageName + "_hover.png"
            toolButton.entered()
        }

        onExited: {
            selectArea.visible = false
            if (toolButton.state == "on") {
               toolImage.source = toolButton.dirImage + toolButton.imageName + "_press.png"
            } else {
               toolImage.source = toolButton.dirImage + toolButton.imageName+".png"
            }
            toolButton.exited()
        }

        onPressed:{
            toolButton.state = toolButton.state == "on" ? "off" : "on"
            toolButton.pressed()
            if (toolButton.group&&toolButton.state == "on")
               group.checkState(toolButton)
        }

    }

}
