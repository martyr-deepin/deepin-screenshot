import QtQuick 2.2

MouseArea {
    width: img.implicitWidth
    height: img.implicitHeight
    hoverEnabled: true
    state: "normal"

    property string type: "+"

    states: [
        State {
            name: "normal"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_normal.png".arg(type)
            }
        },
        State {
            name: "hover"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_hover.png".arg(type)
            }
        },
        State {
            name: "pressed"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_press.png".arg(type)
            }
        }
    ]

    onEntered: state = "hover"
    onExited: state = "normal"
    onPressed: state = "pressed"
    onReleased: state = "hover"

    Image { id: img }
}