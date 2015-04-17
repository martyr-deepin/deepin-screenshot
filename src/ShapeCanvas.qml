import QtQuick 2.1
import "calculateRect.js" as CalcEngine

Canvas {
    id: canvas
    width: parent.width
    height: parent.height

    property bool recording: false
    property bool isShiftPressed: false
    property string shapeName
    property string cursorDirection
    property var shapes: []
    property var currenRecordingShape
    property int linewidth: 3
    property int paintColor: 3
    property alias canvasArea: canvasArea
    property url imageUrl: tmpImageFile
    property url rotateImage: "../image/mouse_style/shape/rotate.png"
    property string blurImage: blurImageFile
    property string mosaicImage: mosaicImageFile
    property bool isBlur: false
    property bool bluring:false
    property bool processBlur: false
    property var blurImageData

    property bool textFocus: false
    property bool isMosaic: false
    property bool mosaicing: false
    property bool processMosaic: false
    property var mosaicImageData
    property bool isStraightLine: false
    property int fontSize

    signal textEditing()

    function reLoadImage(image) { unloadImage(image); loadImage(image) }

    onPaintColorChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].selected || shapes[i].rotated || shapes[i].reSized) {
                shapes[i].drawColor = paintColor
                canvas.requestPaint()
            }
        }
    }
    onLinewidthChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].linewidth != undefined && shapes[i].selected || shapes[i].rotated || shapes[i].reSized) {
                if (!shapes[i].processBlur && !shapes[i].processMosaic) {
                    shapes[i].linewidth = canvas.linewidth
                    canvas.requestPaint()
                }
            }
        }
    }
    onTextFocusChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].text != undefined && shapes[i].text.focus) {
                selectUnique(shapes[i].numberOrder)
                canvas.requestPaint()
            }
        }
    }
    onFontSizeChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].isreadOnly != undefined && (shapes[i].selected || shapes[i].rotated)) {
                shapes[i].fontSize = fontSize
            }
        }
    }
    onIsBlurChanged: { if (isBlur) { reLoadImage(blurImage) } }
    onIsMosaicChanged: { if (isMosaic) { reLoadImage(mosaicImage) } }
    Component.onCompleted: reLoadImage(rotateImage)
    onImageLoaded: {
        if (isBlur) {
            bluring = true
        }
        if (isMosaic) {
            mosaicing = true
        }
        requestPaint()
    }

    onPaint: {
        var ctx = canvas.getContext("2d")
        ctx.reset()
        ctx.clearRect(0, 0, width, height)

        // clip the whole area to the stack for future usage
        ctx.beginPath()
        ctx.rect(0, 0, width, height)
        ctx.closePath()
        ctx.clip()

        // don't know why, but if the line below is not provided
        // the hover states will not even appear
        ctx.strokeStyle = "red"

        if(bluring || mosaicing) {
            if (bluring) {
                blurImageData = ctx.createImageData(blurImage)
                bluring = false
            } else {
                mosaicImageData = ctx.createImageData(mosaicImage)
                mosaicing = false
            }
        }
        for (var i = 0; i < shapes.length; i++) {
            shapes[i].draw(ctx)
        }
    }

    function clickOnPoint(p) {
        var selectedShape
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].clickOnPoint(p)){
                selectedShape = shapes[i].numberOrder
                break
            }
        }
        if (selectedShape != undefined) {
             selectUnique(selectedShape)
             return true
         } else {
            selectUnique(-1)
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
    function hoverOnShape(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].hoverOnShape(p)) {
                return true
            }
        }
        return false
    }
    function deselectAll() {
        for (var i = 0; i < shapes.length; i++) {
            shapes[i].deselect()
        }
    }

    function selectUnique(num) {
        var targetIndex = null
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].numberOrder == num && !targetIndex) {
                targetIndex = i
                continue
            } else {
                shapes[i].selected = false
                shapes[i].rotated = false
                shapes[i].reSized = false
            }
        }

        if (targetIndex != null && targetIndex != shapes.length - 1) {
            var _shape = shapes.splice(targetIndex, 1)
            shapes = shapes.concat(_shape)
        }
    }
    function mouse_style(shape,paint) {
        switch (shape) {
            case "rect": { return windowView.set_cursor_shape("shape_rect_mouse") }
            case "ellipse": { return windowView.set_cursor_shape("shape_ellipse_mouse") }
            case "arrow": { return windowView.set_cursor_shape("shape_arrow_mouse") }
            case "line": {
                if (paint == 0) { return windowView.set_cursor_shape("color_pen_yellow") }
                if (paint == 1) { return windowView.set_cursor_shape("color_pen_orange") }
                if (paint == 2) { return windowView.set_cursor_shape("color_pen_dark_orange") }
                if (paint == 3) { return windowView.set_cursor_shape("color_pen_pink_red") }
                if (paint == 4) { return windowView.set_cursor_shape("color_pen_light_purple") }
                if (paint == 5) { return windowView.set_cursor_shape("color_pen_purple") }
                if (paint == 6) { return windowView.set_cursor_shape("color_pen_dark_blue") }
                if (paint == 7) { return windowView.set_cursor_shape("color_pen_blue") }
                if (paint == 8) { return windowView.set_cursor_shape("color_pen_light_blue") }
                if (paint == 9) { return windowView.set_cursor_shape("color_pen_light_green") }
                if (paint == 10) { return windowView.set_cursor_shape("color_pen_grass_green") }
                if (paint == 11) { return windowView.set_cursor_shape("color_pen_dark_green") }
                if (paint == 12) { return windowView.set_cursor_shape("color_pen_white") }
                if (paint == 13) { return windowView.set_cursor_shape("color_pen_grey") }
                if (paint == 14) { return windowView.set_cursor_shape("color_pen_dark_grey") }
                if (paint == 15) { return windowView.set_cursor_shape("color_pen_black") }
            }
            case "text": { return windowView.set_cursor_shape("shape_text_mouse") }
        }
    }
    Component {
        id: rect_component
        RectangleCanvas {}
    }
    Component {
        id: ellipse_component
        EllipseCanvas {}
    }
    Component {
        id: arrow_component
        ArrowCanvas {}
    }
    Component {
        id: line_component
        LineCanvas {}
    }
    Component {
        id: text_component
        TextCanvas {}
    }
    MouseArea {
        id: canvasArea
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        cursorShape: windowView.set_cursor_shape("shape_start_cursor")
        enabled: canvas.shapeName
        hoverEnabled: canvas.shapeName

        onPressed: {
            if (!canvas.shapeName || mouse.button == Qt.RightButton) return
            if (mouse.modifiers & Qt.ShiftModifier) {
                canvas.isShiftPressed = true
            } else {
                canvas.isShiftPressed = false
            }
            var pos = screen.get_absolute_cursor_pos()
            if (!canvas.clickOnPoint(Qt.point(pos.x, pos.y))) {
                canvas.recording = true
                if (canvas.shapeName == "rect") {
                    canvas.currenRecordingShape = rect_component.createObject(canvas, {})
                    canvas.currenRecordingShape.processBlur = canvas.processBlur
                    canvas.currenRecordingShape.processMosaic = canvas.processMosaic
                    canvas.currenRecordingShape.isShiftPressed = canvas.isShiftPressed
                }
                if (canvas.shapeName == "ellipse") {
                    canvas.currenRecordingShape = ellipse_component.createObject(canvas, {})
                    canvas.currenRecordingShape.processBlur = canvas.processBlur
                    canvas.currenRecordingShape.processMosaic = canvas.processMosaic
                    canvas.currenRecordingShape.isShiftPressed = canvas.isShiftPressed
                }
                if (canvas.shapeName == "arrow") {
                    canvas.currenRecordingShape = arrow_component.createObject(canvas, {})
                    canvas.currenRecordingShape.isShiftPressed = canvas.isShiftPressed
                }
                if (canvas.shapeName == "line") {
                    canvas.currenRecordingShape = line_component.createObject(canvas, {})
                    canvas.currenRecordingShape.isShiftPressed = canvas.isShiftPressed
                    canvas.currenRecordingShape.isStraightLine = canvas.isStraightLine
                }
                if (canvas.shapeName == "text") {
                    var isReadOnly = false
                    for (var i = 0; i < canvas.shapes.length; i++) {
                        if (canvas.shapes[i].isreadOnly != undefined && canvas.shapes[i].isreadOnly == false) {
                            canvas.shapes[i].isreadOnly = true
                            canvas.shapes[i].selected = false
                            canvas.shapes[i].rotated = false
                            canvas.shapes[i].reSized = false
                            isReadOnly = true
                        }
                    }
                    if (!isReadOnly) {
                        canvas.currenRecordingShape = text_component.createObject(canvas, {})
                        canvas.currenRecordingShape.editing.connect(canvas.textEditing)
                        var pos = screen.get_absolute_cursor_pos()
                        canvas.currenRecordingShape.curX = pos.x
                        canvas.currenRecordingShape.curY = pos.y
                        canvas.currenRecordingShape.fontSize = fontSize
                        canvas.currenRecordingShape.numberOrder = canvas.shapes.length
                        canvas.shapes.push(canvas.currenRecordingShape)
                    }
                }
                canvas.currenRecordingShape.drawColor = canvas.paintColor
                windowView.set_save_config(canvas.currenRecordingShape.shape, "color_index", canvas.paintColor)
                if (canvas.shapeName != "text") {
                    canvas.currenRecordingShape.linewidth = canvas.linewidth
                    var pos = screen.get_absolute_cursor_pos()
                    canvas.currenRecordingShape.points.push(Qt.point(pos.x, pos.y))
                    canvas.currenRecordingShape.numberOrder = canvas.shapes.length
                    canvas.shapes.push(canvas.currenRecordingShape)
                }
            } else {
                if (canvas.shapeName == "text") {
                    canvas.recording = false
                    canvas.currenRecordingShape.firstDraw = true
                    var pos = screen.get_absolute_cursor_pos()
                    for (var i = 0; i < canvas.shapes.length; i++) {
                        if (canvas.shapes[i].isreadOnly != undefined && canvas.shapes[i].rotateOnPoint(Qt.point(pos.x, pos.y))) {
                            return
                        } else if (canvas.shapes[i].isreadOnly != undefined && canvas.shapes[i].isreadOnly == false) {
                            canvas.shapes[i].isreadOnly = true
                            canvas.shapes[i].selected = false
                            canvas.shapes[i].rotated = false
                            canvas.shapes[i].reSized = false
                            isReadOnly = true
                        }
                    }

                }
            }
            canvas.requestPaint()
        }
        onReleased: {
            if (!canvas.shapeName || mouse.button == Qt.RightButton) return

            if (!toolbar.visible) { toolbar.visible = true }
            if (canvas.recording && canvas.shapeName != "text") {
                var pos = screen.get_absolute_cursor_pos()
                canvas.currenRecordingShape.points.push(Qt.point(pos.x, pos.y))
                canvas.currenRecordingShape.firstDraw = true
                canvas.recording = false
                canvas.requestPaint()
            }
            if (canvas.recording) {
                for (var i = 0; i < canvas.shapes.length; i++) {
                    if (canvas.shapes[i].isRotating != undefined) {
                        canvas.shapes[i].isRotating = false
                    }
                }
            }
        }

        onDoubleClicked: saveScreenshot()

        onClicked: {
            if (mouse.button == Qt.RightButton)
                _menu_controller.show_menu(windowView.get_save_config("save", "save_op"))
        }
        onEntered: {
            canvasArea.cursorShape = canvas.mouse_style(canvas.shapeName, canvas.paintColor)
        }
        onPositionChanged: {
            if (!canvas.shapeName) return
            if (toolbar.visible && pressed) {
                var pos = screen.get_absolute_cursor_pos()
                if (pos.x+selectArea.x >= toolbar.x && pos.x+selectArea.x <= toolbar.x + toolbar.width &&
                pos.y+selectArea.y >= toolbar.y && pos.y+selectArea.y <= toolbar.y + toolbar.height) {
                    toolbar.visible = false
                }
            }
            if (canvas.recording && pressed) {
                var pos = screen.get_absolute_cursor_pos()
                canvas.currenRecordingShape.points.push(Qt.point(pos.x, pos.y))
                canvas.requestPaint()
            } else if(!canvas.recording && pressed) {
                var selectedShape = null,reSizedShape = null,rotatedShape = null
                for (var i = 0; i < canvas.shapes.length; i++) {
                    if (canvas.shapes[i].reSized||drag.active)  reSizedShape = canvas.shapes[i]
                    if (canvas.shapes[i].rotated||drag.active)  rotatedShape = canvas.shapes[i]
                    if (canvas.shapes[i].selected||drag.active)  selectedShape = canvas.shapes[i]
                }
                if (rotatedShape != null && pressed) {
                    if (rotatedShape.isreadOnly != undefined) {
                        rotatedShape.isRotating = true
                        var pos = screen.get_absolute_cursor_pos()
                        rotatedShape.handleRotate(Qt.point(pos.x, pos.y))
                        rotatedShape.isRotating = false
                    } else {
                        var pos = screen.get_absolute_cursor_pos()
                        rotatedShape.handleRotate(Qt.point(pos.x, pos.y))
                    }
                    canvas.requestPaint()
                }
                if (reSizedShape != null && pressed) {
                    var pos = screen.get_absolute_cursor_pos()
                    reSizedShape.handleResize(Qt.point(pos.x, pos.y), reSizedShape.clickedKey)
                    canvas.requestPaint()
                }
                if (selectedShape != null && pressed) {
                    if (selectedShape.isreadOnly == undefined) {
                        var pos = screen.get_absolute_cursor_pos()
                        selectedShape.handleDrag(Qt.point(pos.x, pos.y))
                    }
                    canvas.requestPaint()
                }

            } else {
                var pos = screen.get_absolute_cursor_pos()
                if (!canvas.recording) {
                    for (var i = 0; i < canvas.shapes.length;i++) {
                    if (canvas.shapes[i].hoverOnShape(pos)) {
                        if (canvas.cursorDirection == "TopLeft") {
                            canvasArea.cursorShape = Qt.SizeFDiagCursor
                        }
                        else if (canvas.cursorDirection == "Left") {
                            canvasArea.cursorShape = Qt.SizeHorCursor
                        }
                        else if (canvas.cursorDirection == "BottomLeft") {
                            canvasArea.cursorShape = Qt.SizeBDiagCursor
                        }
                        else if (canvas.cursorDirection == "TopRight") {
                            canvasArea.cursorShape = Qt.SizeBDiagCursor
                        }
                        else if (canvas.cursorDirection == "Right") {
                            canvasArea.cursorShape = Qt.SizeHorCursor
                        }
                        else if (canvas.cursorDirection == "BottomRight") {
                            canvasArea.cursorShape = Qt.SizeFDiagCursor
                        }
                        else if (canvas.cursorDirection == "Top") {
                            canvasArea.cursorShape = Qt.SizeVerCursor
                        }
                        else if (canvas.cursorDirection == "Bottom") {
                            canvasArea.cursorShape = Qt.SizeVerCursor
                        }
                        else {
                            canvasArea.cursorShape = Qt.ClosedHandCursor
                        }
                        canvas.requestPaint()
                        break
                    } else {
                        if ((canvas.shapes[i].selected || canvas.shapes[i].rotated || canvas.shapes[i].reSized) && canvas.shapes[i].hoverOnRotatePoint(pos))   {
                            canvasArea.cursorShape = windowView.set_cursor_shape("shape_rotate_mouse")
                        } else {
                            canvasArea.cursorShape = canvas.mouse_style(canvas.shapeName, canvas.paintColor)
                        }
                        canvas.requestPaint()
                        }
                    }
                    if (canvas.shapes.length == 0) {
                        canvasArea.cursorShape = canvas.mouse_style(canvas.shapeName, canvas.paintColor)
                    }
                } else {
                    for (var i = 0; i < canvas.shapes.length;i++) {
                        if (canvas.shapes[i].shape == "text") {
                            if ((canvas.shapes[i].selected || canvas.shapes[i].rotated || canvas.shapes[i].reSized) && (canvas.shapes[i].hoverOnRotatePoint(pos))) {
                                canvasArea.cursorShape = windowView.set_cursor_shape("shape_rotate_mouse")
                            } else {
                                canvasArea.cursorShape = canvas.mouse_style(canvas.shapeName, canvas.paintColor)
                            }
                        } else {
                            continue
                        }
                    }
                }
            }
        }
    }
}
