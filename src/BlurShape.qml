import QtQuick 2.2
import QtGraphicalEffects 1.0

Item {
    id:blurShape
    width: img.implicitWidth
    height: img.implicitHeight

    property point startPoint: Qt.point(0, 0)
    property point endPoint: Qt.point(0, 0)

    Image {
        id: img
        source: "/tmp/deepin-screenshot.png"
        clip:true
    }

    Item {
        anchors.fill: img
        x: startPoint.x
        y: startPoint.y

        FastBlur {
            id: blur
            anchors.fill: parent

            visible: false
            radius: 32
            source: img

        }

        Item {
            id: mask_source
            anchors.fill: parent

            Rectangle {
                id: round

                width: Math.abs(startPoint.x - endPoint.x)
                height: Math.abs(startPoint.y - endPoint.y)

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

            onPressed: {
                blurShape.startPoint = Qt.point(mouse.x, mouse.y)
                print(blurShape.startPoint,blur.x,blur.y,round.x,round.y)
            }
            onReleased: {
                blurShape.endPoint = Qt.point(mouse.x, mouse.y)
            }
            onPositionChanged: {
                blurShape.endPoint = Qt.point(mouse.x, mouse.y)
            }

            drag.target: round
            drag.axis: Drag.XAndYAxis
            drag.minimumX: 0
            drag.maximumX: round.parent.width - round.width
        }
    }
}