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
function draw_point(ctx, startX, startY, radius) {
    ctx.beginPath()
    ctx.arc(startX, startY, radius, 0, Math.PI * 2, false)
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 1
    ctx.shadowBlur = 2
    ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
    ctx.beginPath()
    ctx.arc(startX, startY,radius - 1, 0, Math.PI * 2, false)
    ctx.shadowBlur =0
    ctx.shadowColor = "transparent"
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
}

function draw_line(isShadow, ctx, endX, endY, offsetX, offsetY,shadowBlur, shadowColor) {
    offsetX = typeof offsetX !== 'undefined' ? offsetX : 0
    offsetY = typeof offsetY !== 'undefined' ? offsetY : 1
    shadowBlur = typeof shadowBlur !== 'undefined' ? shadowBlur : 2
    shadowColor = typeof shadowColor !== 'undefined' ? shadowColor : Qt.rgba(0, 0, 0, 0.2)
    ctx.lineTo(endX, endY)
    ctx.shadowOffsetX = isShadow ? offsetX : 0
    ctx.shadowOffsetY = isShadow ? offsetY : 0
    ctx.shadowBlur = isShadow ? shadowBlur : 0
    ctx.shadowColor = isShadow ? shadowColor : "transparent"
}
