import QtQuick 2.1

Canvas {
    id: canvas
    width: parent.width
    height: parent.height

    property bool recording: false
    property var shapes: []
    property var currenRecordingShape

    onPaint: {
        var ctx = canvas.getContext("2d")
        ctx.clearRect(x, y, width, height)
        ctx.strokeStyle = "red"
        for (var i = 0; i < shapes.length; i++) {
            shapes[i].draw(ctx)
        }
    }

    function clickOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].clickOnPoint(p)) {
                return true
            }
        }

        return false
    }

    Component {
        id: rect_component
        RectangleCanvas {}
    }
    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0,1,1,0.2)
    }
    MouseArea {
        anchors.fill: parent

        onPressed: {
            if (!canvas.clickOnPoint(Qt.point(mouse.x, mouse.y))) {
                canvas.recording = true
                canvas.currenRecordingShape = rect_component.createObject(canvas, {})
                canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                canvas.shapes.push(canvas.currenRecordingShape)

            }
                canvas.requestPaint()
        }

        onReleased: {
            if (canvas.recording) {
                canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                canvas.recording = false
                canvas.requestPaint()
            }
        }

        onPositionChanged: {
            if (canvas.recording) {
                canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
            } else {
                var selectedShape = null
                for (var i = 0; i < canvas.shapes.length; i++) {
                    if (canvas.shapes[i].selected) selectedShape = canvas.shapes[i]
                }

                selectedShape.handleDrag(Qt.point(mouse.x, mouse.y))
            }

            canvas.requestPaint()
        }
    }
}