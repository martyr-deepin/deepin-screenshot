import QtQuick 2.1
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

Item {

    property bool selected: false
    property bool reSized: false
    property bool rotated: false
    property bool firstDraw: false
    property bool mosaicX: false
    property bool isHovered: false

    property point clickedPoint
    property var points: []
    property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
    property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

    property int numberOrder
    property string shape: "rect"
    property var bigPointRadius: 2
    property var smallPointRadius: 2
    property int clickedKey: 0
    property int linewidth: 3
    property int drawColor: 2

    property bool processBlur: false
    property bool processMosaic: false
    property bool isShiftPressed: false

    onDrawColorChanged: windowView.set_save_config("rect", "color_index", drawColor)
    onLinewidthChanged: windowView.set_save_config("rect", "linewidth_index", linewidth)

    function _initMainPoints() {
        var startPoint = points[0]
        var endPoint = points[points.length - 1]
        var leftX = Math.min(startPoint.x, endPoint.x)
        var leftY = Math.min(startPoint.y, endPoint.y)
        var pWidth = Math.abs(startPoint.x - endPoint.x)
        var pHeight = Math.abs(startPoint.y - endPoint.y)
        if (isShiftPressed) {
            var shiftWidth = Math.min(pWidth, pHeight)
            if (endPoint.x >= startPoint.x) {
                if (endPoint.y >= startPoint.y) {
                    mainPoints[0]=startPoint
                    mainPoints[1]=Qt.point(startPoint.x, startPoint.y + shiftWidth)
                    mainPoints[2]=Qt.point(startPoint.x + shiftWidth, startPoint.y)
                    mainPoints[3]=Qt.point(startPoint.x + shiftWidth, startPoint.y+ shiftWidth)
                } else {
                    mainPoints[0] = Qt.point(startPoint.x, startPoint.y - shiftWidth)
                    mainPoints[1] = startPoint
                    mainPoints[2] = Qt.point(startPoint.x + shiftWidth, startPoint.y - shiftWidth)
                    mainPoints[3] = Qt.point(startPoint.x + shiftWidth, startPoint.y)
                }
            } else {
                if (endPoint.y >= startPoint.y) {
                    mainPoints[0] = Qt.point(startPoint.x- shiftWidth, startPoint.y)
                    mainPoints[1] = Qt.point(startPoint.x - shiftWidth, startPoint.y + shiftWidth)
                    mainPoints[2] = startPoint
                    mainPoints[3] = Qt.point(startPoint.x, startPoint.y + shiftWidth)
                } else {
                    mainPoints[0] = Qt.point(startPoint.x - shiftWidth, startPoint.y - shiftWidth)
                    mainPoints[1] = Qt.point(startPoint.x - shiftWidth, startPoint.y)
                    mainPoints[2] = Qt.point(startPoint.x, startPoint.y - shiftWidth)
                    mainPoints[3] = startPoint
                }
            }
        } else {
            mainPoints[0] = Qt.point(leftX, leftY)
            mainPoints[1] = Qt.point(leftX + pWidth, leftY)
            mainPoints[2] = Qt.point(leftX, pHeight + leftY)
            mainPoints[3] = Qt.point(leftX + pWidth, leftY + pHeight)
        }
        CalcEngine.changePointsOrder(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
    }

    function deselect() {
        selected = false
        rotated = false
        reSized = false
    }

    function draw(ctx) {
        if (!firstDraw) { _initMainPoints() }

        ctx.lineWidth = linewidth
        ctx.fillStyle = "transparent"
        ctx.strokeStyle =  ((processBlur||processMosaic)&& !(selected || reSized || rotated)) ? "transparent": screen.colorCard(drawColor)
        ctx.beginPath()
        ctx.moveTo(mainPoints[0].x, mainPoints[0].y)
        if (DrawingUtils.isPointsSameX(mainPoints)) {
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[1].x, mainPoints[1].y)
        } else if (DrawingUtils.isPointsSameY(mainPoints)) {
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[2].x, mainPoints[2].y)
        } else {
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[2].x, mainPoints[2].y)
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[3].x, mainPoints[3].y)
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[1].x, mainPoints[1].y)
            DrawingUtils.draw_line((selected || reSized || rotated), ctx, mainPoints[0].x, mainPoints[0].y)
        }
        ctx.closePath()
        ctx.stroke()
        if (isHovered) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "#01bdff"
            ctx.stroke()
        }
        if (processBlur||processMosaic) {
            ctx.save()
            ctx.clip()
            if (processBlur) {
                ctx.putImageData(parent.blurImageData, 0, 0)
            } else {
                ctx.putImageData(parent.mosaicImageData, 0, 0)
            }
            ctx.restore()
        }

        if (selected||reSized||rotated) {
            ctx.lineWidth = 1
            ctx.strokeStyle = "black"
            ctx.fillStyle = "yellow"
            /* Rotate */
            var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
            ctx.drawImage(canvas.rotateImage, rotatePoint.x - 12, rotatePoint.y - 12)
            ctx.lineWidth = 1
            ctx.strokeStyle = "white"
            ctx.fillStyle = "white"
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
        }
    }
    function clickOnPoint(p) {
        selected = false
        reSized = false
        rotated = false
        clickedPoint = Qt.point(0, 0)
        if (CalcEngine.pointClickIn(mainPoints[0], p)) {
            var result =  true
            reSized = result
            clickedKey = 1
            canvas.cursorDirection = "TopLeft"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(mainPoints[1], p)) {
            var result =  true
            reSized = result
            clickedKey = 2
            canvas.cursorDirection = "BottomLeft"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(mainPoints[2], p)) {
            var result =  true
            reSized = result
            clickedKey = 3
            canvas.cursorDirection = "TopRight"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(mainPoints[3], p)) {
            var result =  true
            reSized = result
            clickedKey = 4
            canvas.cursorDirection = "BottomRight"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(minorPoints[0], p)) {
            var result =  true
            reSized = result
            clickedKey = 5
            canvas.cursorDirection = "Left"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(minorPoints[1], p)) {
            var result =  true
            reSized = result
            clickedKey = 6
            canvas.cursorDirection = "Top"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(minorPoints[2], p)) {
            var result =  true
            reSized = result
            clickedKey = 7
            canvas.cursorDirection = "Right"
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointClickIn(minorPoints[3], p)) {
            var result =  true
            reSized = result
            clickedKey = 8
            canvas.cursorDirection = "Bottom"
            clickedPoint = p
            return result
        }
        if (rotateOnPoint(p)) {
            var result = true
            rotated = true
            clickedPoint = p
            return result
        }
        if (CalcEngine.pointOnLine(mainPoints[0], mainPoints[1], p) || CalcEngine.pointOnLine(mainPoints[1], mainPoints[3], p) ||
            CalcEngine.pointOnLine(mainPoints[3], mainPoints[2], p) || CalcEngine.pointOnLine(mainPoints[2], mainPoints[0], p)) {
            var result = true
            selected = result
            clickedPoint = p
            return result
        }
        if ((processBlur||processMosaic) && CalcEngine.textClickOnPoint(p, mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])) {
            var result = true
            selected = result
            clickedPoint = p
            return result
        }
    }

    function handleDrag(p) {
        var delX = p.x - clickedPoint.x
        var delY = p.y - clickedPoint.y
        for (var i = 0; i < mainPoints.length; i++) {
            mainPoints[i] = Qt.point(mainPoints[i].x + delX, mainPoints[i].y + delY)
        }

        clickedPoint = p
    }
    function handleResize(p, key) {

        if (reSized) {
            var Newpoints = CalcEngine.reSizePointPosititon(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], p, key, isShiftPressed)
            for (var i = 0; i < 4; i ++) { mainPoints[i] = Newpoints[i] }
        }

        clickedPoint = p
    }
    function rotateOnPoint(p) {
        var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        if (p.x >= rotatePoint.x - 5 && p.x <= rotatePoint.x + 5 && p.y >= rotatePoint.y - 5 && p.y <= rotatePoint.y + 5) {
            rotated = true
        } else {
            rotated = false
        }
        clickedPoint = rotatePoint
        return rotated
    }
    function handleRotate(p) {
        var centerInPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
        var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        var angle = CalcEngine.calcutateAngle(clickedPoint, p, centerInPoint)
        for (var i = 0; i < 4; i++) {
            mainPoints[i] = CalcEngine.pointRotate(centerInPoint, mainPoints[i], angle)
        }

        clickedPoint = p
    }
    function hoverOnRotatePoint(p) {
        var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        if (p.x >= rotatePoint.x - 5 && p.x <= rotatePoint.x + 5 && p.y >= rotatePoint.y - 5 && p.y <= rotatePoint.y + 5) {
            var result = true
        } else {
            var result = false
        }
        clickedPoint = rotatePoint
        return  result
    }
    function hoverOnShape(p) {
        var result = false
        if (selected || rotated || reSized) {
            if (CalcEngine.pointClickIn(mainPoints[0], p)) {
                result =  true
                clickedKey = 1
                canvas.cursorDirection = "TopLeft"
                clickedPoint = p
                isHovered = result
                return result
            }
            else if (CalcEngine.pointClickIn(mainPoints[1], p)) {
                result =  true
                clickedKey = 2
                canvas.cursorDirection = "BottomLeft"
                clickedPoint = p
                isHovered = result
                return result
            }
            else if (CalcEngine.pointClickIn(mainPoints[2], p)) {
                result =  true
                clickedKey = 3
                canvas.cursorDirection = "TopRight"
                clickedPoint = p
                isHovered = result
                return result
            }
            else if (CalcEngine.pointClickIn(mainPoints[3], p)) {
                result =  true
                clickedKey = 4
                canvas.cursorDirection = "BottomRight"
                clickedPoint = p
                isHovered = result
                return result
            } else {
                if (CalcEngine.pointClickIn(minorPoints[0], p)) {
                    result =  true
                    clickedKey = 5
                    canvas.cursorDirection = "Left"
                    clickedPoint = p
                    isHovered = result
                    return result
                }
                else if (CalcEngine.pointClickIn(minorPoints[1], p)) {
                    result =  true
                    clickedKey = 6
                    canvas.cursorDirection = "Top"
                    clickedPoint = p
                    isHovered = result
                    return result
                }
                else if (CalcEngine.pointClickIn(minorPoints[2], p)) {
                    result =  true
                    clickedKey = 7
                    canvas.cursorDirection = "Right"
                    clickedPoint = p
                    isHovered = result
                    return result
                }
                else if (CalcEngine.pointClickIn(minorPoints[3], p)) {
                    result =  true
                    clickedKey = 8
                    canvas.cursorDirection = "Bottom"
                    clickedPoint = p
                    isHovered = result
                    return result
                }
                else {
                    if (CalcEngine.pointOnLine(mainPoints[0], mainPoints[1], p) || CalcEngine.pointOnLine(mainPoints[1], mainPoints[3], p) ||
                        CalcEngine.pointOnLine(mainPoints[3], mainPoints[2], p) || CalcEngine.pointOnLine(mainPoints[2], mainPoints[0], p)) {
                        result = true
                        canvas.cursorDirection = ""
                    }
                }
            }
        } else {
            if (CalcEngine.pointOnLine(mainPoints[0], mainPoints[1], p) || CalcEngine.pointOnLine(mainPoints[1], mainPoints[3], p) ||
                CalcEngine.pointOnLine(mainPoints[3], mainPoints[2], p) || CalcEngine.pointOnLine(mainPoints[2], mainPoints[0], p)) {
                result = true
                canvas.cursorDirection = ""
            }
        }
        isHovered = result
        return result
    }
}
