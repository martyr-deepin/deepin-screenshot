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
    ctx.shadowColor = "black"
}
