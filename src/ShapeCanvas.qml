import QtQuick 2.1
import "graphicProcess.js" as CalcGraphic
import "calculateRect.js" as CalcEngine

Canvas {
    id: canvas
    width: parent.width
    height: parent.height

    property bool recording: false
    property string shapeName: "text"
    property var shapes: []
    property var currenRecordingShape
    property var linewidth: 3
    property color paintColor: "red"
    property alias canvasArea: canvasArea
    property url imageUrl: "/tmp/deepin-screenshot.png"
    property string blurImage:"/tmp/deepin-screenshot-blur.png"
    property string mosaicImage: "/tmp/deepin-screenshot-mosaic.png"
    property bool isBlur: false
    property bool bluring:false
    property bool processBlur: false
    property var blurImageData

    property bool textFocus: false
    property bool isMosaic: false
    property bool mosaicing: false
    property bool processMosaic: false
    property var mosaicImageData

    property int fontSize

    function reLoadImage(image) { unloadImage(image); loadImage(image) }
    
    onPaintColorChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].selected || shapes[i].rotated || shapes[i].reSized) {
                shapes[i].drawColor = paintColor
            } 
        }
    }
    onLinewidthChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].linewidth != undefined && shapes[i].selected || shapes[i].rotated || shapes[i].reSized) {
                shapes[i].linewidth = canvas.linewidth
            } 
        }
    }
    onTextFocusChanged: {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].text != undefined && shapes[i].text.focus) {
                selectUnique(shapes[i].numberOrder)
            } 
        }
        canvas.requestPaint()
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
        ctx.clearRect(x, y, width, height)
        if ( processBlur || processMosaic ) {
            ctx.beginPath()
            ctx.rect(x, y, width, height)
            ctx.clip()
        }
        if(bluring || mosaicing) {
            if (bluring) {
                var imageData = ctx.createImageData(blurImage)
                imageData = CalcGraphic.gaussianBlur(imageData, 1)
                blurImageData = imageData
                bluring = false
            } else {
                var imageData = ctx.createImageData(mosaicImage)
                imageData = CalcGraphic.mosaic(imageData, 5)
                mosaicImageData = imageData
                mosaicing = false
            }
        } else {
            ctx.strokeStyle = "red"
            for (var i = 0; i < shapes.length; i++) {
                shapes[i].draw(ctx)
            }
        }
    }

    function clickOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
                if (shapes[i].clickOnPoint(p)){
                var selectedShape = i
            }
        }
        if (selectedShape != undefined) {
             selectUnique(selectedShape)
         } else {
            var selectedShape = shapes.length + 1
            selectUnique(selectedShape)
        }
        if (selectedShape >= 0 && selectedShape < shapes.length) {
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
    function hoverOnShape(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].hoverOnShape(p)) {
                return true
            }
        }
        return false
    }

    function selectUnique(num) {
        for (var i = 0; i < shapes.length; i++) {
            if (i == num) {
                continue
            } else {
                shapes[i].selected = false
                shapes[i].rotated = false
                shapes[i].reSized = false
            }
        }
    }

    function mouse_style(shape,paint) {
        switch (shape) {
            case "rect": { return windowView.set_cursor_shape("shape_rect_mouse") }
            case "ellipse": { return windowView.set_cursor_shape("shape_ellipse_mouse") }
            case "arrow": { return windowView.set_cursor_shape("shape_arrow_mouse") }
            case "line": {
                if (paint == "#ffd903") { return windowView.set_cursor_shape("color_pen_yellow") }
                if (paint == "#ff5e1a") { return windowView.set_cursor_shape("color_pen_orange") }
                if (paint == "#ff3305") { return windowView.set_cursor_shape("color_pen_dark_orange") }
                if (paint == "#ff1c49") { return windowView.set_cursor_shape("color_pen_pink_red") }
                if (paint == "#fb00ff") { return windowView.set_cursor_shape("color_pen_light_purple") }
                if (paint == "#7700ed") { return windowView.set_cursor_shape("color_pen_purple") }
                if (paint == "#3d08ff") { return windowView.set_cursor_shape("color_pen_dark_blue") }
                if (paint == "#3468ff") { return windowView.set_cursor_shape("color_pen_blue") }
                if (paint == "#00aaff") { return windowView.set_cursor_shape("color_pen_light_blue") }
                if (paint == "#08ff77") { return windowView.set_cursor_shape("color_pen_light_green") }
                if (paint == "#03a60e") { return windowView.set_cursor_shape("color_pen_grass_green") }
                if (paint == "#3c7d00") { return windowView.set_cursor_shape("color_pen_dark_green") }
                if (paint == "#ffffff") { return windowView.set_cursor_shape("color_pen_white") }
                if (paint == "#666666") { return windowView.set_cursor_shape("color_pen_grey") }
                if (paint == "#2b2b2b") { return windowView.set_cursor_shape("color_pen_dark_grey") }
                if (paint == "#000000") { return windowView.set_cursor_shape("color_pen_black") }
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
        hoverEnabled: true
        cursorShape: canvas.mouse_style(canvas.shapeName, canvas.paintColor)
        onPressed: {
            var pos = screen.get_absolute_cursor_pos()
            if (!canvas.clickOnPoint(Qt.point(pos.x, pos.y))) {
                canvas.recording = true
                if (canvas.shapeName == "rect") {
                    canvas.currenRecordingShape = rect_component.createObject(canvas, {})
                    canvas.currenRecordingShape.processBlur = canvas.processBlur
                    canvas.currenRecordingShape.processMosaic = canvas.processMosaic
                }
                if (canvas.shapeName == "ellipse") {
                    canvas.currenRecordingShape = ellipse_component.createObject(canvas, {})
                    canvas.currenRecordingShape.processBlur = canvas.processBlur
                    canvas.currenRecordingShape.processMosaic = canvas.processMosaic
                }
                if (canvas.shapeName == "arrow") {
                    canvas.currenRecordingShape = arrow_component.createObject(canvas, {})
                }
                if (canvas.shapeName == "line") {
                    canvas.currenRecordingShape = line_component.createObject(canvas, {})
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
                        var pos = screen.get_absolute_cursor_pos()
                        canvas.currenRecordingShape.curX = pos.x
                        canvas.currenRecordingShape.curY = pos.y
                        canvas.currenRecordingShape.fontSize = fontSize
                        canvas.currenRecordingShape.numberOrder = canvas.shapes.length
                        canvas.shapes.push(canvas.currenRecordingShape)
                    }
                }
                canvas.currenRecordingShape.drawColor = canvas.paintColor
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
                        //canvas.shapes[i].rotated = false
                        canvas.shapes[i].isRotating = false
                    }
                }
            }
        }

        onPositionChanged: {
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
                        canvasArea.cursorShape =windowView.set_cursor_shape("shape_rotate_mouse")
                        var pos = screen.get_absolute_cursor_pos()
                        rotatedShape.handleRotate(Qt.point(pos.x, pos.y))
                        rotatedShape.isRotating = false
                    } else {
                        canvasArea.cursorShape = windowView.set_cursor_shape("shape_rotate_mouse")
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
                        print("selectedShape:", selectedShape)
                        var pos = screen.get_absolute_cursor_pos()
                        selectedShape.handleDrag(Qt.point(pos.x, pos.y))
                    }
                    canvas.requestPaint()
                }

            } else {
                for (var i = 0; i < canvas.shapes.length;i++) {
                    if (canvas.shapes[i].reSized || canvas.shapes[i].selected || canvas.shapes[i].rotated) {
                        var pos = screen.get_absolute_cursor_pos()
                        if (canvas.shapes[i].hoverOnRotatePoint(Qt.point(pos.x, pos.y))) {
                            canvasArea.cursorShape = windowView.set_cursor_shape("shape_rotate_mouse")
                        } else {
                            canvasArea.cursorShape = canvas.mouse_style(canvas.shapeName, canvas.paintColor)
                        }
                    }
                    if (canvas.shapes[i].isreadOnly == undefined) {
                        var pos = screen.get_absolute_cursor_pos()
                        canvas.hoverOnShape(Qt.point(pos.x, pos.y))
                        canvas.requestPaint()
                    }
                }
            }
        }
    }
}
