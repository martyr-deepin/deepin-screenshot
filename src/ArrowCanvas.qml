import QtQuick 2.1
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

Item {
    property bool selected: false
    property bool reSized: false
    property bool rotated: false
    property bool firstDraw: false
    property bool isHovered: false
    property bool firstRelativeCalculate: false

    property point clickedPoint
    property var points: []
    property var portion: []
    property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
    property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

    property int numberOrder
    property string shape: "arrow"
    property var bigPointRadius: 2
    property var smallPointRadius: 1
    property var minPadding: 10
    property int clickedKey: 0
    property int linewidth: 3
    property int drawColor: 2
    property int arrowSize: 16
    property int arrowAngle: 40
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
    function _draw(ctx, startPoint, endPoint) {
        if (isShiftPressed && (!reSized || !rotated)) {
            if (startPoint.x != endPoint.x) {
                if (Math.atan2(Math.abs(endPoint.y - startPoint.y), Math.abs(endPoint.x - startPoint.x))*180/Math.PI < 45 ) {
                    points[points.length - 1] = Qt.point(endPoint.x, startPoint.y)
                    endPoint = points[points.length - 1]
                } else {
                    points[points.length - 1] = Qt.point(startPoint.x, endPoint.y)
                    endPoint = points[points.length - 1]
                }
            }
        }
        ctx.lineWidth = linewidth
        ctx.strokeStyle = screen.colorCard(drawColor)
        ctx.save()
        ctx.beginPath()
        ctx.moveTo(startPoint.x, startPoint.y)
        DrawingUtils.draw_line((selected || reSized || rotated), ctx, endPoint.x, endPoint.y)
        ctx.stroke()
        ctx.closePath()

        if (isHovered) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "#01bdff"
            ctx.stroke()
        }
        ctx.lineWidth = linewidth
        ctx.strokeStyle = screen.colorCard(drawColor)
        if (startPoint.x == endPoint.x) { var xMultiplier = 1} else {
            var xMultiplier = (startPoint.x - endPoint.x) / Math.abs(startPoint.x - endPoint.x)
        }
        if (startPoint.y == endPoint.y) { var yMultiplier = -1} else {
            var yMultiplier = (startPoint.y - endPoint.y) / Math.abs(startPoint.y - endPoint.y)
        }
        var add = CalcEngine.pointSplid(startPoint, endPoint, arrowSize)
        var pointA = Qt.point(endPoint.x + xMultiplier * add[0], endPoint.y + yMultiplier * add[1])
        var angle = arrowAngle / 2 / 180 * Math.PI
        var pointB = CalcEngine.pointRotate(endPoint, pointA, angle)
        var distance = CalcEngine.pointTolineDistance(startPoint, endPoint, pointB)
        var splidistance = Math.sqrt(CalcEngine.square(arrowSize) - CalcEngine.square(distance))
        add = CalcEngine.pointSplid(startPoint, endPoint, splidistance)
        var pointC = Qt.point(endPoint.x + xMultiplier * add[0], endPoint.y + yMultiplier * add[1])
        var pointD = Qt.point(2*pointC.x - pointB.x, 2*pointC.y - pointB.y)
        var pointE = Qt.point((endPoint.x + pointA.x) / 2, (endPoint.y + pointA.y) / 2)

        ctx.fillStyle =  screen.colorCard(drawColor)
        ctx.strokeStyle = screen.colorCard(drawColor)
        ctx.beginPath()
        ctx.moveTo(endPoint.x, endPoint.y)
        DrawingUtils.draw_line((selected || reSized || rotated), ctx, pointB.x, pointB.y)
        DrawingUtils.draw_line((selected || reSized || rotated), ctx, pointE.x, pointE.y)
        DrawingUtils.draw_line((selected || reSized || rotated), ctx, pointD.x, pointD.y)
        DrawingUtils.draw_line((selected || reSized || rotated), ctx, endPoint.x, endPoint.y)
        ctx.closePath()
        ctx.stroke()
        ctx.fill()

        if (selected||reSized||rotated) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "white"
            ctx.fillStyle = "white"

            /* Top left */
            DrawingUtils.draw_point(ctx, startPoint.x, startPoint.y, bigPointRadius + linewidth/2)
            /* Top right */
            DrawingUtils.draw_point(ctx, endPoint.x, endPoint.y, bigPointRadius + linewidth/2)

        }
        ctx.restore()
    }
    function draw(ctx) {
        if (!firstDraw) { _initMainPoints() }
        if (!isShiftPressed) { minorPoints = CalcEngine.getAnotherFourPoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3]) }

        var startPoint = points[0]
        var endPoint = points[points.length - 1]
        _minPadding()
        if (points.length < 2) {
            return
        } else if (points.length == 2 && CalcEngine.getDistance(startPoint, endPoint) < 5) {
            return
        } else if (!CalcEngine.startDraw(startPoint, endPoint, minPadding)){
            if (startPoint.x < endPoint.x) {
                if (startPoint.y < endPoint.y) {
                    endPoint = Qt.point(startPoint.x + minPadding, startPoint.y + minPadding)
                } else {
                    endPoint = Qt.point(startPoint.x + minPadding, startPoint.y - minPadding)
                }
            } else {
                if (startPoint.y < endPoint.y) {
                    endPoint = Qt.point(startPoint.x - minPadding, startPoint.y + minPadding)
                } else {
                    endPoint = Qt.point(startPoint.x - minPadding, startPoint.y - minPadding)
                }
            }
            points[points.length -1] = endPoint
            _draw(ctx, startPoint, endPoint)
        } else {
            _draw(ctx, startPoint, endPoint)
        }
    }
    function clickOnPoint(p) {
        selected = false
        reSized = false
        rotated = false
        clickedPoint = Qt.point(0, 0)
        var startPoint = points[0]
        var endPoint = points[points.length - 1]

        if (CalcEngine.pointClickIn(startPoint, p)) {
            var result =  true
            reSized = result
            rotated = result
            clickedKey = 1
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(endPoint, p)) {
            var result =  true
            reSized = result
            rotated = result
            clickedKey = 2
            clickedPoint = p
            return result
        }

        if (CalcEngine.pointOnLine(startPoint, endPoint, p)) {
            var result = true
            selected = result
            clickedPoint = p
            return result
        }
    }

    function handleDrag(p) {

        var delX = p.x - clickedPoint.x
        var delY = p.y - clickedPoint.y
        for (var i = 0; i < points.length; i++) {
            points[i] = Qt.point(points[i].x + delX, points[i].y + delY)
        }
        _initMainPoints()
        for(var i = 0; i < portion.length; i++) {
            portion.pop()
        }

        clickedPoint = p
    }
    function handleResize(p, key) {
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
        for(var i = 0; i < portion.length; i++) {
            portion.pop()
        }
        clickedPoint = p
    }
    function rotateOnPoint(p) {
        if (reSized) {
            rotated = true
        }
        clickedPoint = p
        return rotated
    }

    function handleRotate(p) {
        clickedPoint = p
    }
    function hoverOnRotatePoint(p) {
        var startPoint = points[0]
        var endPoint = points[points.length - 1]
        if (CalcEngine.pointClickIn(startPoint, p) || CalcEngine.pointClickIn(endPoint, p)) {
            var result = true
        } else {
            var result = false
        }
        return  result
    }
    function hoverOnShape(p) {
        var result
        var startPoint = points[0]
        var endPoint = points[points.length - 1]

        if (CalcEngine.pointOnLine(startPoint, endPoint, p) && !(CalcEngine.pointClickIn(startPoint, p) ||CalcEngine.pointClickIn(endPoint, p))) {
            canvas.cursorDirection = ""
            result = true
        } else {
            result = false
        }
        isHovered = result
        return result
    }
}
