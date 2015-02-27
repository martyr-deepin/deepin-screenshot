import QtQuick 2.1
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

Item {
    property bool selected: false
    property bool reSized: false
    property bool rotated: false
    property bool firstDraw: false
    property bool isHovered: false

    property point clickedPoint
    property var points: []
    property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
    property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

    property int numberOrder
    property string shape: "arrow"
    property var bigPointRadius: 2
    property var smallPointRadius: 1
    property int clickedKey: 0
    property int linewidth: 3
    property int drawColor: 2
    property int arrowSize: 16
    property int arrowAngle: 40
    property bool isShiftPressed: false

    onDrawColorChanged: { windowView.set_save_config(shape, "color_index", drawColor)}
    onLinewidthChanged: { windowView.set_save_config(shape, "linewidth_index", linewidth)}
    function deselect() {
        selected = false
        rotated = false
        reSized = false
    }

    function draw(ctx) {
        var startPoint = points[0]
        var endPoint = points[points.length - 1]
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

        clickedPoint = p
    }
    function handleResize(p, key) {
        var startPoint = points[0]
        var endPoint = points[points.length - 1]
        if (isShiftPressed) {
            if (key == 1) {
                if (Math.atan2(Math.abs(endPoint.y - p.y), Math.abs(endPoint.x - p.x))*180/Math.PI < 45 ) {
                    startPoint = Qt.point(p.x, endPoint.y)
                } else {
                    startPoint = Qt.point(endPoint.x, p.y)
                }

            }
            if (key == 2) {
                endPoint = p
                if (Math.atan2(Math.abs(endPoint.y - startPoint.y), Math.abs(endPoint.x - startPoint.x))*180/Math.PI < 45 ) {
                    points[points.length - 1] = Qt.point(endPoint.x, startPoint.y)
                    endPoint = points[points.length - 1]
                } else {
                    points[points.length - 1] = Qt.point(startPoint.x, endPoint.y)
                    endPoint = points[points.length - 1]
                }
            }
        } else {
            if (key == 1) {
                startPoint = p
            }
            if (key == 2) {
                endPoint = p
            }
        }
        points[0] = startPoint
        points[points.length - 1] = endPoint

        clickedPoint = p
    }
    function rotateOnPoint(p) {
        if (reSized) {
            rotated = true
        }
        return rotated
    }

    function handleRotate(p, key) {
        handleResize(p)
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
