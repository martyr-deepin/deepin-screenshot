function isPointsSameX(points) {
    if (points.length < 2) {
        return true
    } else {
        for (var i = 1; i < points.length; i++) {
            if (points[i].x != points[0].x) {
                return false
            }
        }
        return true
    }
}

function isPointsSameY(points) {
    if (points.length < 2) {
        return true
    } else {
        for (var i = 1; i < points.length; i++) {
            if (points[i].y != points[0].y) {
                return false
            }
    }
        return true
    }
}

function shiftMainPoints(startPoint, endPoint, isShift) {
    var leftX = Math.min(startPoint.x, endPoint.x)
    var leftY = Math.min(startPoint.y, endPoint.y)
    var pWidth = Math.max(Math.abs(startPoint.x - endPoint.x), minPadding)
    var pHeight = Math.max(Math.abs(startPoint.y - endPoint.y), minPadding)
    var mainPoints = [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0)]
    if (isShift) {
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
    return mainPoints
}

function draw_point(ctx, startX, startY, radius) {
    ctx.beginPath()
    ctx.arc(startX, startY, radius, 0, Math.PI * 2, false)
    ctx.shadowBlur = 2
    ctx.shadowColor = "black"
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
    ctx.beginPath()
    ctx.arc(startX, startY, radius, 0, Math.PI * 2, false)
    ctx.shadowBlur =0
    ctx.shadowColor = "transparent"
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
}

function draw_line(isShadow, ctx, endX, endY) {
    ctx.lineTo(endX, endY)
    ctx.shadowBlur = 2
    ctx.shadowColor = isShadow ? "black": "transparent"
}
