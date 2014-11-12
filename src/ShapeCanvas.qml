import QtQuick 2.1

Canvas {
    id: canvas
    width: parent.width
    height: parent.height

    property bool recording: false
    property bool wellPaint: false
    property var shapes: []
    property var currenRecordingShape
    /*test*/
    property bool roll: false
    onPaint: {
        var ctx = canvas.getContext("2d")
        ctx.clearRect(x, y, width, height)
        ctx.strokeStyle = "red"
        for (var i = 0; i < shapes.length; i++) {
            shapes[i].draw(ctx)
        }
    }

    function clickOnPoint(p) {
        var selectedShape = null
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].clickOnPoint(p)){
                selectedShape = i
            }
        }
        if (selectedShape != null ) {
            for (var i = 0; i < shapes.length && i != selectedShape; i++)
                shapes[i].selected = false
            return true
        } else {
            return false
        }
    }
    function resizeOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].resizeOnPoint(p)) {
                return true
            }
        }
        return false
    }
    function rotateOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].rotateOnPoint(p)) {
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
        id: canvasArea
        anchors.fill: parent
        onPressed: {
            if (!canvas.clickOnPoint(Qt.point(mouse.x, mouse.y))) {
                if (!roll) {
                    canvas.recording = true
                    canvas.currenRecordingShape = rect_component.createObject(canvas, {})
                    canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                    canvas.shapes.push(canvas.currenRecordingShape)
                } else {
                    canvas.rotateOnPoint(Qt.point(mouse.x, mouse.y))
                }

            } else {
                canvas.resizeOnPoint(Qt.point(mouse.x, mouse.y))
                canvas.rotateOnPoint(Qt.point(mouse.x, mouse.y))
            }
            canvas.requestPaint()
        }
        onReleased: {
            print("!",canvas.recording)
            if (canvas.recording) {
                canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                canvas.recording = false
                roll = true
            }

            canvas.requestPaint()
        }

        onPositionChanged: {
            if (canvas.recording) {
                canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
            } else {
                print(0)
                var selectedShape = null,adjustedShape = null,rotatedShape = null
                for (var i = 0; i < canvas.shapes.length; i++) {
                    if (canvas.shapes[i].reSized)  {
                        adjustedShape = canvas.shapes[i]
                    }
                    if (canvas.shapes[i].selected) {
                        selectedShape = canvas.shapes[i]
                    }
                    if (canvas.shapes[i].rotated && pressed) {
                        roll = true
                        rotatedShape = canvas.shapes[i]
                        rotatedShape.handleRotate(Qt.point(mouse.x, mouse.y))

                    }
                }
                if (selectedShape != null && selectedShape.rotateOnPoint(Qt.point(mouse.x, mouse.y))) {
                    canvasArea.cursorShape = Qt.ClosedHandCursor
                } else if (adjustedShape != null && adjustedShape.rotateOnPoint(Qt.point(mouse.x, mouse.y))) {
                    canvasArea.cursorShape = Qt.ClosedHandCursor
                } else {
                    canvasArea.cursorShape = Qt.ArrowCursor
                }

                if (canvasArea.cursorShape == Qt.ClosedHandCursor && onPressed) {
                    rotatedShape.handleRotate(Qt.point(mouse.x, mouse.y))
                }
                if (adjustedShape != null) {
                    adjustedShape.handleResize(Qt.point(mouse.x, mouse.y))
                }
                else {
                    if (selectedShape != null ) {
                        selectedShape.handleDrag(Qt.point(mouse.x, mouse.y))
                    }
                    if (rotatedShape != null) {
                        rotatedShape.handleRotate(Qt.point(mouse.x, mouse.y))
                    }
                }
            }
            canvas.requestPaint()
        }
    }
}