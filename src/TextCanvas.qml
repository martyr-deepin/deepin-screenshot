import QtQuick 2.1
import QtGraphicalEffects 1.0
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

Rectangle {
    id: rect
    x: curX
    y: curY
    width: Math.max(18, text.contentWidth + 10)
    height: text.contentHeight + 10

    property int curX
    property int curY
    property int fontSize: 12
    property int numberOrder
    property string shape: "text"
    property bool selected: true
    property bool reSized: false
    property bool rotated: false

    property bool isRotating: false
    property bool isDraging: false
    property bool afterRotated: false
    property bool firstDraw: false
    property bool isHovered: false
    property alias isreadOnly: text.readOnly
    property alias text: text
    property point clickedPoint
    property point convertRotatePoint
    property point rotatePoint
    property var points: []
    property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
    property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

    property var bigPointRadius: 3
    property var smallPointRadius: 2
    property var angleGlobal: 0
    property int clickedKey: 0
    property int linewidth: 1
    property var reX: width / 2
    property var reY: height / 2
    property int drawColor: 3
    property  string state: "off"

    signal editing()

    onDrawColorChanged: { windowView.set_save_config(shape, "color_index", drawColor)}
    onFontSizeChanged: { windowView.set_save_config(shape, "fontsize_index", fontSize)}
    transform: Rotation {
        origin.x: (isRotating || isDraging) ? width / 2 : reX
        origin.y: (isRotating || isDraging) ? height / 2 : reY
        angle: angleGlobal/Math.PI*180
    }
    color: (selected || rotated) ? Qt.rgba(1, 1, 1, 0.2) : "transparent"

    onWidthChanged: { _expandByWidth(width) }
    onHeightChanged: { _expandByHeight(height) }

    function _initMainPoints() {
        mainPoints[0] = Qt.point(curX, curY)
        mainPoints[1] = Qt.point(curX, curY + height)
        mainPoints[2] = Qt.point(curX + width, curY)
        mainPoints[3] = Qt.point(curX + width, curY + height)

        CalcEngine.changePointsOrder(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
    }

    function _mergeTwoCenters() {
        var textAreaCenter = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
        curX = textAreaCenter.x - width / 2
        curY = textAreaCenter.y - height / 2
    }

    function _expandByWidth(addWidth) {
        if (addWidth == 0 || mainPoints == undefined) return

        var add = CalcEngine.pointSplid(mainPoints[0], mainPoints[2], addWidth)
        if (mainPoints[0].x <= mainPoints[2].x) {
            if (mainPoints[0].y >= mainPoints[2].y) {
                mainPoints[2] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y - add[1])
            } else {
                mainPoints[2] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y + add[1])
            }
        } else {
            if (mainPoints[0].y >= mainPoints[2].y) {
                mainPoints[2] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y - add[1])
            } else {
                mainPoints[2] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y + add[1])
            }
        }
        mainPoints[3] = Qt.point(mainPoints[1].x + mainPoints[2].x - mainPoints[0].x,
            mainPoints[1].y + mainPoints[2].y - mainPoints[0].y)

        rotated && _mergeTwoCenters()
    }

    function _expandByHeight(addHeight) {
        if (addHeight == 0 || mainPoints == undefined) return

        var add = CalcEngine.pointSplid(mainPoints[0], mainPoints[1], addHeight)
        if (mainPoints[0].x <= mainPoints[1].x) {
            if (mainPoints[0].y >= mainPoints[1].y) {
                mainPoints[1] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y - add[1])
            } else {
                mainPoints[1] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y + add[1])
            }
        } else {
            if (mainPoints[0].y >= mainPoints[1].y) {
                mainPoints[1] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y - add[1])
            } else {
                mainPoints[1] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y + add[1])
            }
        }
        mainPoints[3] = Qt.point(mainPoints[1].x + mainPoints[2].x - mainPoints[0].x,
            mainPoints[1].y + mainPoints[2].y - mainPoints[0].y)

        rotated && _mergeTwoCenters()
    }

    function dashLine(ctx, point0, point3) {
        var startPoint = Qt.point(0, 0), endPoint = Qt.point(0, 0)
        var opposite = false
        if (point0.x <= point3.x && point0.y <= point3.y) {
            startPoint = point0
            endPoint = point3
        }
        if (point3.x < point0.x && point3.y < point0.y) {
            startPoint = point3
            endPoint = point0
        }
        if (point0.x > point3.x && point0.y <= point3.y) {
            opposite = true
            startPoint = point3
            endPoint = point0
        }
        if (point0.x <= point3.x && point0.y > point3.y) {
            opposite = true
            startPoint = point0
            endPoint = point3
        }
        if (startPoint == Qt.point(0, 0) && endPoint == Qt.point(0, 0)) {}
        else {
            var distance = 8,dist = 0, dashpoints = []
            var total_distance = Math.sqrt(CalcEngine.square(startPoint.x - endPoint.x) + CalcEngine.square(startPoint.y - endPoint.y))
            var count = Math.floor(total_distance /  distance)
            for (var i = 0; i < count - 1; i++) {
                dist = (i + 1)*distance
                var tmp =  CalcEngine.pointSplid(startPoint, endPoint, dist)
                if (!opposite) { var tmpPoint = Qt.point(startPoint.x + tmp[0], startPoint.y + tmp[1])}
                else { var tmpPoint = Qt.point(startPoint.x + tmp[0], startPoint.y - tmp[1]) }
                dashpoints.push(tmpPoint)
            }
            ctx.beginPath()
            ctx.moveTo(startPoint.x, startPoint.y)
            ctx.lineTo(dashpoints[0].x, dashpoints[0].y)
            ctx.closePath()
            ctx.stroke()
            for (var i = 1; i < dashpoints.length - 1; i+= 2) {
                ctx.beginPath()
                ctx.moveTo(dashpoints[i].x, dashpoints[i].y)
                ctx.lineTo(dashpoints[i + 1].x, dashpoints[i + 1].y)
                ctx.shadowOffsetX = 1
                ctx.shadowOffsetY = 2
                ctx.shadowColor = Qt.rgba(0, 0, 0, 0.5)
                ctx.closePath()
                ctx.stroke()
            }
        }
    }

    function deselect() {
        selected = false
        rotated = false
        reSized = false
        text.focus = false
    }

    function draw(ctx) {
        if (!firstDraw) { _initMainPoints() }

        if (rect.selected || rect.rotated) {
            ctx.lineWidth = 1
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.5)

            dashLine(ctx, mainPoints[0], mainPoints[2])
            dashLine(ctx, mainPoints[2], mainPoints[3])
            dashLine(ctx, mainPoints[3], mainPoints[1])
            dashLine(ctx, mainPoints[1], mainPoints[0])

            /* Rotate point*/
            ctx.lineWidth = 1
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.6)
            var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
            var middlePoint = Qt.point((mainPoints[0].x + mainPoints[2].x) / 2,(mainPoints[0].y + mainPoints[2].y) / 2)
            ctx.moveTo(rotatePoint.x, rotatePoint.y)
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, middlePoint.x, middlePoint.y)
            ctx.stroke()
            ctx.drawImage(canvas.rotateImage, rotatePoint.x - 12, rotatePoint.y - 12)
        }
    }
    function clickOnPoint(p) {
        var result = false
        if (CalcEngine.textClickOnPoint(p, mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])) {
            result = true
            selected = result
        }
        if (rotateOnPoint(p)) {
            result = true
            rotated = result
        }
        if (result) {
            canvas.selectUnique(numberOrder)
        }

        clickedPoint = p
        return result
    }
    Rectangle {
        id: textRect
        clip: true
        anchors.fill: parent
        anchors.leftMargin: 3
        anchors.rightMargin: 3
        color: "transparent"

        TextEdit {
            id:text
        //  width: Math.floor((canvas.width - curX - 10) / font.pixelSize)*font.pixelSize
        //  height: Math.floor((canvas.height - curY - 10) / font.pixelSize)*font.pixelSize
            color: screen.colorCard(drawColor)
            selectedTextColor: readOnly ? color : "white"
            selectionColor: readOnly ? "transparent" : "#01bdff"
            selectByMouse: !readOnly
            font.pixelSize: fontSize
            wrapMode: TextEdit.Wrap
            cursorDelegate: Rectangle {
                width: 1
                height: parent.height
                color: text.color
                visible: !text.readOnly && blink_timer.cursorVisible
            }

            anchors.verticalCenter: parent.verticalCenter

            onFocusChanged: {
                if (focus) {
                    canvas.selectUnique(numberOrder)
                } else {
                    readOnly = true
                    rect.firstDraw = true
                }
                canvas.requestPaint()
            }

            onTextChanged: { blink_timer.cursorVisible = true, blink_timer.restart() }
            onContentWidthChanged: { canvas.requestPaint()}
            Component.onCompleted: forceActiveFocus()

            Timer {
                id: blink_timer
                running: !text.readOnly
                repeat: true
                interval: 700

                property bool cursorVisible

                onTriggered: cursorVisible = !cursorVisible
            }
        }

        Glow {
            anchors.fill: text
            fast: true
            radius: 3
            samples: 16
            spread: 0.5
            color: "black"
            source: text
            visible: text.readOnly && (selected || rotated || reSized)
        }
    }
    /* click on the text is difficult to handle , add an MouseArea */
    MouseArea {
        id: moveText
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: windowView.set_cursor_shape("shape_text_mouse")
        onPressed: {
            if (!text.readOnly) {
                mouse.accepted = false
                return
            }

            var pos = screen.get_absolute_cursor_pos()
            clickedPoint = Qt.point(pos.x, pos.y)
            rect.selected = true
            text.forceActiveFocus()
            canvas.requestPaint()
        }
        onEntered: {
            if (text.readOnly) {
                moveText.cursorShape = Qt.ClosedHandCursor
            } else {
                moveText.cursorShape = windowView.set_cursor_shape("shape_text_mouse")
            }
        }
        onReleased: {
            if (!text.readOnly) {
                mouse.accepted = false
                return
            }
        }

        onPositionChanged: {
            if (!text.readOnly) {
                mouse.accepted = false
                return
            }

            if (rect.selected && pressed) {
                cursorShape = Qt.ClosedHandCursor

                var pos = screen.get_absolute_cursor_pos()
                isDraging = true
                handleDrag(Qt.point(pos.x, pos.y))
                isDraging = false
            }
            canvas.requestPaint()
        }
        onDoubleClicked: {
            if (!text.readOnly) {
                mouse.accepted = false
                return
            }

            rect.selected = true
            text.readOnly = false
            text.forceActiveFocus()
            rect.editing()
            canvas.requestPaint()
        }

    }
    function handleDrag(p) {
    /* keep the text's width & height the same as before drag*/
       // width = width
       // height = height
        var delX = p.x - clickedPoint.x
        var delY = p.y - clickedPoint.y
        for (var i = 0; i < mainPoints.length; i++) {
            mainPoints[i].x = mainPoints[i].x + delX
            mainPoints[i].y = mainPoints[i].y + delY
        }
        _mergeTwoCenters()

        reX = width / 2
        reY = height / 2
        clickedPoint = p
    }
    function handleResize(p, key) {}
    function rotateOnPoint(p) {
        var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        if (p.x >= rotatePoint.x - 15 && p.x <= rotatePoint.x + 15 && p.y >= rotatePoint.y - 15 && p.y <= rotatePoint.y + 15) {
            rotated = true
        } else {
            rotated = false
        }
        clickedPoint = rotatePoint
        return rotated
    }

    function handleRotate(p) {
        _mergeTwoCenters()

        var centerInPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
        var angle = CalcEngine.calcutateAngle(clickedPoint, p, centerInPoint)
        angleGlobal += angle
        for (var i = 0; i < mainPoints.length; i++) {
            mainPoints[i] = CalcEngine.pointRotate(centerInPoint, mainPoints[i], angle)
        }
        reX = width / 2
        reY = height / 2
        clickedPoint = p
    }
    function hoverOnRotatePoint(p) {
        var result =  false
        result = rotateOnPoint(p)
        return result
    }
    function hoverOnShape(p) {
        var result = false
        isHovered = result
        return result
    }

}
