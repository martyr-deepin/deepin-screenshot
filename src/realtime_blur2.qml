import QtQuick 2.2
import QtGraphicalEffects 1.0

Item {
    width: img.implicitWidth
    height: img.implicitHeight

    Image {
        id: img
        // source: "/home/hualet/Pictures/DeepinScreenshot20140805174517.png"
        source: "/tmp/deepin-screenshot.png"
    }

    Item {
        anchors.fill: img

        FastBlur {
            id: blur
            visible: false
            source: img
            radius: 32
            anchors.fill: parent
        }

        Item {
            id: mask_source
            anchors.fill: parent

            Rectangle {
                id: round
                width: 200
                height: 200
                radius: 100
            }
        }

        OpacityMask {
            source: blur
            maskSource: mask_source
            anchors.fill: mask_source
        }

        MouseArea {
            anchors.fill: parent
            drag.target: round
            drag.axis: Drag.XAndYAxis
            drag.minimumX: 0
            drag.maximumX: round.parent.width - round.width
        }
    }
}