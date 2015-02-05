import QtQuick 2.2

MouseArea {
    width: 20
    height: 20
    hoverEnabled: true
    state: "normal"

    property alias text: label.text

    states: [
        State {
            name: "normal"
            PropertyChanges {
                target: background
                color: "transparent"
            }
            PropertyChanges {
                target: label
                color: "#979797"
            }
        },
        State {
            name: "hover"
            PropertyChanges {
                target: background
                color: Qt.rgba(1, 1, 1, 0.1)
            }
            PropertyChanges {
                target: label
                color: "white"
            }
        },
        State {
            name: "pressed"
            PropertyChanges {
                target: background
                color: "transparent"
            }
            PropertyChanges {
                target: label
                color: "#01bdff"
            }
        }
    ]

    onEntered: state = "hover"
    onExited: state = "normal"
    onPressed: state = "pressed"
    onReleased: state = "hover"

    Rectangle {
        id: background
        anchors.fill: parent

        Text {
            id: label
            font.pixelSize: 24
            anchors.centerIn: parent
        }
    }
}