import QtQuick 2.1

Item {
    id: fillShape
    width: 32
    height: 32
    state: "off"

    property string imageName: ""

    states: [
            State {
                    name : "on"
                    PropertyChanges {
                        target: imageShape
                        source: "../image/size/" + fillShape.imageName + "_fill_hover.png"
                    }
            },
            State {
                    name : "off"
                    PropertyChanges {
                        target: imageShape
                        source: "../image/size/" + fillShape.imageName + "_fill.png"
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
        color: "yellow"
        opacity: 0.2
    }

    Image {
        id: imageShape
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            selectArea.visible = true
            fillShape.state = "on"
        }
        onExited: {
            selectArea.visible = false
            fillShape.state = "off"
        }

        onClicked:{

        }

    }

}