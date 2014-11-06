import QtQuick 2.1

Item {
	property bool selected: false
	property bool reSized: false
	property point clickedPoint

	property var points: []
	property int bigPointRadius: 6
	property int smallPointRadius: 4

	property bool topRightLocal: false
	property bool topLeftLocal: false
	property bool bottomLeftLocal: false
	property bool bottomRightLocal: false
	property bool topLocal: false
	property bool bottomLocal: false
	property bool leftLocal: false
	property bool rightLocal: false

	function _inRectCheck(point, rect) {
	    return rect.x <= point.x && point.x <= rect.x + rect.width && rect.y <= point.y && point.y <= rect.y + rect.height
	}
	function _inEightPointsCheck(point, rect) {
		/*Top Left*/
		if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y <= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topLeftLocal = true
		}
		/*Top Right*/
		else if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y <= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topRightLocal = true
		}
		/*Bottom Left*/
		else if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y <= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			topLeftLocal = true
		}
		/*Bottom Right*/
		else if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y <= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			topRightLocal = true
		}
		/* Top */
		if (point.x >= rect.x + rect.width / 2 - bigPointRadius / 2 && point.x <= rect.x + rect.width / 2 + bigPointRadius / 2 &&
			point.y <= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topLeftLocal = true
		}
		/* Bottom */
		else if (point.x >= rect.x + rect.width / 2 - bigPointRadius / 2 && point.x <= rect.x + rect.width / 2 + bigPointRadius / 2 &&
			point.y <= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			topRightLocal = true
		}
		/* Left */
		if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y <= rect.y + rect.height / 2 - bigPointRadius / 2 && point.y <= rect.y + rect.height / 2 + bigPointRadius / 2) {
			topLeftLocal = true
		}
		/* Right */
		else if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y <= rect.y + rect.height / 2 - bigPointRadius / 2 && point.y <= rect.y + rect.height / 2 + bigPointRadius / 2) {
			topRightLocal = true
		}
		if (topRightLocal || topLeftLocal || bottomLeftLocal || bottomRightLocal || topLocal || bottomLocal || leftLocal || rightLocal) {
			return true
		} else {
			return false
		}
	}
	function draw(ctx) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

	    ctx.save()
	    ctx.beginPath()
	    ctx.roundedRect(startPoint.x, startPoint.y, endPoint.x - startPoint.x, endPoint.y - startPoint.y, 0, 0)
	    ctx.closePath()
	    ctx.stroke()
	    if (selected) {
	    	ctx.strokeStyle = "#00A0E9"
	    	ctx.fillStyle = "white"
	    	var leftX = Math.min(startPoint.x, endPoint.x)
	    	var leftY = Math.min(startPoint.y, endPoint.y)
	    	var pWidth = Math.abs(startPoint.x - endPoint.x)
	    	var pHeight = Math.abs(startPoint.y - endPoint.y)

	    	/* Top left */
	    	ctx.beginPath()
	    	ctx.arc(leftX, leftY, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()
	    	/* Top right */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth, leftY, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom left */
	    	ctx.beginPath()
	    	ctx.arc(leftX, leftY + pHeight, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom right */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth, leftY + pHeight, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Top */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth / 2, leftY, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth / 2, leftY + pHeight, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Left */
	    	ctx.beginPath()
	    	ctx.arc(leftX, leftY + pHeight / 2, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Right */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth, leftY + pHeight / 2, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()
	    }
	    ctx.restore()
	    return Qt.rect(startPoint.x, startPoint.y, endPoint.x - startPoint.x, endPoint.y - startPoint.y)
	}
	function clickOnPoint(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		var result = _inRectCheck(p, Qt.rect(startPoint.x - 5, startPoint.y - 5, endPoint.x - startPoint.x + 10, endPoint.y - startPoint.y + 10))
					&& !_inRectCheck(p, Qt.rect(startPoint.x + 5, startPoint.y + 5, endPoint.x - startPoint.x - 10, endPoint.y - startPoint.y - 10))
		selected = result
		clickedPoint = p

		return result
	}

	function handleDrag(p) {
	    var delX = p.x - clickedPoint.x
	    var delY = p.y - clickedPoint.y
	    for (var i = 0; i < points.length; i++) {
	    	points[i] = Qt.point(points[i].x + delX, points[i].y + delY)
	    }

	    clickedPoint = p
	}
	function resizeOnPoint(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var local = _inEightPointsCheck(p,Qt.rect(startPoint.x - bigPointRadius,startPoint.y - bigPointRadius,endPoint.x - startPoint.x + 2*bigPointRadius, endPoint.y - startPoint.y + 2*bigPointRadius))
		reSized = local
		clickedPoint = p
	}
	function handleResize(p,rect) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		if (topLeftLocal||leftLocal) {}
	}

}