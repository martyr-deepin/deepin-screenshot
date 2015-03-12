import QtQuick 2.1
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

Item {
    id: root
    property bool selected: false
    property bool reSized: false
    property bool rotated: false
    property bool firstDraw: false
    property bool firstRelativeCalculate: false
    property bool isHovered: false

    property point clickedPoint
    property var points: []
    property var portion: []
    property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
    property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

    property int numberOrder
    property string shape: "line"
    property var bigPointRadius: 2
    property var smallPointRadius: 1
    property var minPadding: 10
    property int clickedKey: 0
    property int linewidth: 3
    property int drawColor: 3
    property bool isStraightLine: false
    property bool isShiftPressed: false
    onDrawColorChanged: { windowView.set_save_config(shape, "color_index", drawColor)}
    onLinewidthChanged: { windowView.set_save_config(shape, "linewidth_index", linewidth)}

    function _initMainPoints() {
        var startPoint = points[0]
        var endPoint = points[points.length - 1]
        var leftX = points[0].x
        var leftY = points[0].y
        var rightX = points[0].x
        var rightY = points[0].y

        for (var i = 1; i < points.length; i++) {

            leftX = Math.min(leftX, points[i].x)
            leftY = Math.min(leftY, points[i].y)
            rightX = Math.max(rightX, points[i].x)
            rightY = Math.max(rightY, points[i].y)
        }
        if (!isShiftPressed || !isStraightLine) {
            mainPoints[0] = Qt.point(Math.max(leftX - minPadding, 0), Math.max(leftY - minPadding, 0))
            mainPoints[1] = Qt.point(Math.max(leftX - minPadding, 0), Math.min(rightY + minPadding, screenHeight))
            mainPoints[2] = Qt.point(Math.min(rightX + minPadding, screenWidth), Math.max(leftY - minPadding, 0))
            mainPoints[3] = Qt.point(Math.min(rightX + minPadding, screenWidth), Math.min(rightY + minPadding, screenHeight))

            CalcEngine.changePointsOrder(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        }
    }

    function deselect() {
        selected = false
        rotated = false
        reSized = false
    }
    function _minPadding() {
        switch (linewidth) {
            case 2: { minPadding = 20;}
            case 4: { minPadding = 15;}
            case 6: { minPadding = 19;}
        }
    }

    function draw(ctx) {
        _minPadding()
        if (!firstDraw) { _initMainPoints() }
        if (isShiftPressed || isStraightLine) { minorPoints = CalcEngine.getAnotherFourPoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3]) }

        var startPoint = points[0]
        var endPoint = points[points.length - 1]

        if ((isShiftPressed || isStraightLine) && (!reSized || !rotated)) {
            if (startPoint.x != endPoint.x) {
                if (isShiftPressed) {
                    if (Math.atan2(Math.abs(endPoint.y - startPoint.y), Math.abs(endPoint.x - startPoint.x))*180/Math.PI < 45 ) {
                        points[points.length - 1] = Qt.point(endPoint.x, startPoint.y)
                        points.splice(1, points.length -2)
                        endPoint = points[points.length - 1]
                    } else {
                        points[points.length - 1] = Qt.point(startPoint.x, endPoint.y)
                        var popPoints = points.splice(1, points.length -2)
                        endPoint = points[points.length - 1]
                    }
                } else {
                    points.splice(1, points.length -2)
                }
            }

            ctx.lineWidth = linewidth
            ctx.strokeStyle = screen.colorCard(drawColor)
            ctx.beginPath()
            ctx.moveTo(points[0].x, points[0].y)
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, endPoint.x, endPoint.y)
            ctx.stroke()
            ctx.closePath()
        } else {
            ctx.lineWidth = linewidth
            ctx.strokeStyle = screen.colorCard(drawColor)

            var content = ""
            var lastPointTake = points[0]
            for(var i = 1; i < points.length; i++) {
                // NOTE:
                // 1, reducing the point length, thus to prevent too much calculations
                // 2, we take every last point to ensure that when the drawing's very slow,
                //    the drawing doesn't seem to be intermittent.
                if (CalcEngine.getDistance(lastPointTake, points[i]) > 15 || i == points.length - 1) {
                    lastPointTake = points[i]
                    content += "PathCurve {x: %1; y: %2}".arg(points[i].x).arg(points[i].y)
                }
            }

            var curve_path = Qt.createQmlObject("import QtQuick 2.2; Path {%1}".arg(content), root, "curve_path")
            curve_path.startX = points[0].x
            curve_path.startY = points[0].y

            ctx.path = curve_path
            ctx.stroke()
            // don't forget to release the memory
            curve_path.destroy()
        }
        if (isHovered) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "#01bdff"
            ctx.stroke()
        }
        if (selected||reSized||rotated) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "black"
            ctx.fillStyle = "yellow"
            if (isStraightLine||isShiftPressed) {
                ctx.lineWidth = 1
                ctx.strokeStyle = "white"
                ctx.fillStyle = "white"

                /* Top left */
                DrawingUtils.draw_point(ctx, points[0].x, points[0].y, bigPointRadius + linewidth/2)
                /* Top right */
                DrawingUtils.draw_point(ctx, points[points.length - 1].x, points[points.length - 1].y, bigPointRadius + linewidth/2)
            } else {
                /* Rotate point*/
                var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
                ctx.lineWidth = 1
                ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.6)
                var middlePoint = Qt.point((mainPoints[0].x + mainPoints[2].x) / 2,(mainPoints[0].y + mainPoints[2].y) / 2)
                ctx.moveTo(rotatePoint.x, rotatePoint.y)
                DrawingUtils.draw_line((selected || reSized || rotated), ctx, middlePoint.x, middlePoint.y)
                ctx.stroke()
                ctx.drawImage(canvas.rotateImage, rotatePoint.x - 12, rotatePoint.y - 12)

                /* Top left */
                DrawingUtils.draw_point(ctx, mainPoints[0].x, mainPoints[0].y,bigPointRadius + linewidth / 2)

                /* Top right */
                DrawingUtils.draw_point(ctx, mainPoints[3].x, mainPoints[3].y, bigPointRadius + linewidth / 2)

                /* Bottom left */
                DrawingUtils.draw_point(ctx, mainPoints[1].x, mainPoints[1].y, bigPointRadius + linewidth / 2)

                /* Bottom right */
                DrawingUtils.draw_point(ctx, mainPoints[2].x, mainPoints[2].y, bigPointRadius + linewidth / 2)

                minorPoints = CalcEngine.getAnotherFourPoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
                /* Top */
                DrawingUtils.draw_point(ctx, minorPoints[0].x, minorPoints[0].y, linewidth / 2)

                /* Bottom */
                DrawingUtils.draw_point(ctx, minorPoints[1].x, minorPoints[1].y, linewidth / 2)

                /* Left */
                DrawingUtils.draw_point(ctx, minorPoints[2].x, minorPoints[2].y, linewidth / 2)

                /* Right */
                DrawingUtils.draw_point(ctx, minorPoints[3].x, minorPoints[3].y, linewidth / 2)
                ctx.lineWidth = 1
                ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.6)
                ctx.beginPath()
                ctx.moveTo(mainPoints[0].x, mainPoints[0].y)
                DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[2].x, mainPoints[2].y)
                DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[3].x, mainPoints[3].y)
                DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[1].x, mainPoints[1].y)
                DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[0].x, mainPoints[0].y)
                ctx.closePath()
                ctx.stroke()
            }
        }
    }
    function clickOnPoint(p) {
        selected = false
        reSized = false
        rotated = false
        clickedPoint = Qt.point(0, 0)

        if (isStraightLine||isShiftPressed) {
            if (CalcEngine.pointClickIn(points[0], p)) {
                canvas.cursorDirection = ""
                reSized = true
                rotated = true
                clickedKey = 1
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(points[points.length -1], p)) {
                canvas.cursorDirection = ""
                reSized = true
                rotated = true
                clickedKey = 2
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointOnLine(points[0], points[points.length - 1], p)) {
                canvas.cursorDirection = ""
                selected = true
                clickedPoint = p
                return true
            }
        } else {
            if (CalcEngine.pointClickIn(mainPoints[0], p)) {
                reSized = true
                clickedKey = 1
                canvas.cursorDirection = "TopLeft"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(mainPoints[1], p)) {
                reSized = true
                clickedKey = 2
                canvas.cursorDirection = "BottomLeft"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(mainPoints[2], p)) {
                reSized = true
                clickedKey = 3
                canvas.cursorDirection = "TopRight"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(mainPoints[3], p)) {
                reSized = true
                clickedKey = 4
                canvas.cursorDirection = "BottomRight"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(minorPoints[0], p)) {
                reSized = true
                clickedKey = 5
                canvas.cursorDirection = "Left"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(minorPoints[1], p)) {
                reSized = true
                clickedKey = 6
                canvas.cursorDirection = "Top"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(minorPoints[2], p)) {
                reSized = true
                clickedKey = 7
                canvas.cursorDirection = "Right"
                clickedPoint = p
                return true
            }
            if (CalcEngine.pointClickIn(minorPoints[3], p)) {
                reSized = true
                clickedKey = 8
                canvas.cursorDirection = "Bottom"
                clickedPoint = p
                return true
            }
        }
        if (rotateOnPoint(p)) {
            rotated = true
            clickedPoint = p
            return true
        }
        for (var i = 0; i < points.length; i++) {
            if (CalcEngine.pointClickIn(points[i], p)) {
                selected = true
                if (isStraightLine||isShiftPressed) {
                    reSized = true
                }
                clickedPoint = p
                return true

            }
        }
        return false
    }

    function handleDrag(p) {
        var delX = p.x - clickedPoint.x
        var delY = p.y - clickedPoint.y
        if (isStraightLine||isShiftPressed) {
            for (var i = 0; i < points.length; i++) {
                points[i] = Qt.point(points[i].x + delX, points[i].y + delY)
            }
            _initMainPoints()
            for (var i = 0; i < portion.length; i++) {
                portion.pop()
            }
        } else {
            for(var i = 0; i < 4; i++) {
                mainPoints[i] = Qt.point(mainPoints[i].x + delX, mainPoints[i].y + delY)
            }
            for (var i = 0; i < points.length; i++) {
                points[i] = Qt.point(points[i].x + delX, points[i].y + delY)
            }
        }
        clickedPoint = p
    }
    function handleResize(p, key) {
        if (isStraightLine||isShiftPressed) {
            var startPoint = points[0]
            var endPoint = points[points.length - 1]
            if (key == 1) {
                if (isShiftPressed) {
                    if (Math.atan2(Math.abs(endPoint.y - p.y), Math.abs(endPoint.x - p.x))*180/Math.PI < 45 ) {
                        startPoint = Qt.point(p.x, endPoint.y)
                    } else {
                        startPoint = Qt.point(endPoint.x, p.y)
                    }
                } else {
                    startPoint = p
                }

            }
            if (key == 2) {
                if (isShiftPressed) {
                    if (Math.atan2(Math.abs(p.y - startPoint.y), Math.abs(p.x - startPoint.x))*180/Math.PI < 45 ) {
                        endPoint = Qt.point(p.x, startPoint.y)
                    } else {
                        endPoint = Qt.point(startPoint.x, p.y)
                    }
                } else {
                    endPoint = p
                }
            }

            points[0] = startPoint
            points[points.length - 1] = endPoint
            _initMainPoints()
            for (var i = 0; i < portion.length; i++) {
                portion.pop()
            }
            clickedPoint = p
        } else {
            if (reSized) {
                if (!firstRelativeCalculate) {
                    for(var i = 0; i < points.length; i++) {
                        portion.push(CalcEngine.relativePostion(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], points[i]))

                    }
                    firstRelativeCalculate = true
                }
                var points1 = CalcEngine.reSizePointPosition(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], p, key, minPadding)
                for (var i = 0; i < 4; i ++) { mainPoints[i] = points1[i] }
                for (var i = 0; i < points.length; i++) {
                    points[i] = CalcEngine.getNewPostion(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], portion[i])
                }
            }
        }
        clickedPoint = p
    }

    function rotateOnPoint(p) {
        return hoverOnRotatePoint(p)
    }

    function handleRotate(p) {
        if (!isShiftPressed && !isStraightLine) {
            var centerInPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
            var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
            var angle = CalcEngine.calcutateAngle(clickedPoint, p, centerInPoint)
            for (var i = 0; i < 4; i++) {
                mainPoints[i] = CalcEngine.pointRotate(centerInPoint, mainPoints[i], angle)
            }
            for(var i = 0; i < points.length; i++) {
                points[i] = CalcEngine.pointRotate(centerInPoint, points[i], angle)
            }
        }
        clickedPoint = p
    }

    function hoverOnRotatePoint(p) {
        if (isStraightLine||isShiftPressed) {
            var startPoint = points[0]
            var endPoint = points[points.length - 1]
            /* don't know why when hover on the rotatepoint, the cursor is on the lower coordinate*/
            startPoint = Qt.point(startPoint.x - 5, startPoint.y - 5)
            endPoint = Qt.point(endPoint.x - 5, endPoint.y - 5)
            if (CalcEngine.pointClickIn(startPoint, p) || CalcEngine.pointClickIn(endPoint, p)) {
                var result = true
            } else {
                var result = false
            }
            clickedPoint = p
        } else {
            var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
            rotatePoint = Qt.point(rotatePoint.x - 5, rotatePoint.y - 5)
            if (p.x >= rotatePoint.x - 12 && p.x <= rotatePoint.x + 12 && p.y >= rotatePoint.y - 12 && p.y <= rotatePoint.y + 12) {
                var result = true
            } else {
                var result = false
            }
            clickedPoint = rotatePoint
        }
        return  result
    }
    function hoverOnShape(p) {
        var result = false
        var startPoint = points[0]
        var endPoint = points[points.length -1]
        for (var i = 0; i < points.length; i++) {
            if (CalcEngine.pointClickIn(points[i], p)) {
                canvas.cursorDirection = ""
                var result = true
            }
        }
        if (isStraightLine||isShiftPressed) {
            if (CalcEngine.pointOnLine(points[0], points[points.length - 1], p) && !(CalcEngine.pointClickIn(startPoint, p) || CalcEngine.pointClickIn(endPoint, p))) {
                canvas.cursorDirection = ""
                result = true
            } else {
                result = false
            }
        } else {
            if (selected || reSized || rotated) {
                if (CalcEngine.pointClickIn(mainPoints[0], p)) {
                    result =  true
                    clickedKey = 1
                    canvas.cursorDirection = "TopLeft"
                    clickedPoint = p
                    return result
                }
                else if (CalcEngine.pointClickIn(mainPoints[1], p)) {
                    result =  true
                    clickedKey = 2
                    canvas.cursorDirection = "BottomLeft"
                    clickedPoint = p
                    return result
                }
                else if (CalcEngine.pointClickIn(mainPoints[2], p)) {
                    result =  true
                    clickedKey = 3
                    canvas.cursorDirection = "TopRight"
                    clickedPoint = p
                    return result
                }
                else if (CalcEngine.pointClickIn(mainPoints[3], p)) {
                    result =  true
                    clickedKey = 4
                    canvas.cursorDirection = "BottomRight"
                    clickedPoint = p
                    return result
                } else {
                    if (CalcEngine.pointClickIn(minorPoints[0], p)) {
                        result =  true
                        clickedKey = 5
                        canvas.cursorDirection = "Left"
                        clickedPoint = p
                        return result
                    }
                    else if (CalcEngine.pointClickIn(minorPoints[1], p)) {
                        result =  true
                        reSized = result
                        clickedKey = 6
                        canvas.cursorDirection = "Top"
                        clickedPoint = p
                        return result
                    }
                    else if (CalcEngine.pointClickIn(minorPoints[2], p)) {
                        result =  true
                        clickedKey = 7
                        canvas.cursorDirection = "Right"
                        clickedPoint = p
                        return result
                    }
                    else if (CalcEngine.pointClickIn(minorPoints[3], p)) {
                        result =  true
                        clickedKey = 8
                        canvas.cursorDirection = "Bottom"
                        clickedPoint = p
                        return result
                    }
                }
            }
        }
        isHovered = result
        return result
    }
}
