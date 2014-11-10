import QtQuick 2.1

Item {
	property bool selected: false
	property bool reSized: false
	property bool rotated: false
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
		reSized = false
		topRightLocal = false
		topLeftLocal = false
		bottomLeftLocal = false
		bottomRightLocal = false
		topLocal = false
		bottomLocal = false
		leftLocal = false
		rightLocal = false
		/*Top Left*/
		if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y >= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topLeftLocal = true
		}
		/*Top Right*/
		if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y >= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topRightLocal = true
		}
		/*Bottom Left*/
		if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y >= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			bottomLeftLocal = true
		}
		/*Bottom Right*/
		if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y >= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			bottomRightLocal = true
		}
		/* Top */
		if (point.x >= rect.x + rect.width / 2 - bigPointRadius / 2 && point.x <= rect.x + rect.width / 2 + bigPointRadius / 2 &&
			point.y >= rect.y - bigPointRadius / 2 && point.y <= rect.y + bigPointRadius / 2) {
			topLocal = true
		}
		/* Bottom */
		if (point.x >= rect.x + rect.width / 2 - bigPointRadius / 2 && point.x <= rect.x + rect.width / 2 + bigPointRadius / 2 &&
			point.y >= rect.y + rect.height - bigPointRadius / 2 && point.y <= rect.y + rect.height + bigPointRadius / 2) {
			bottomLocal = true
		}
		/* Left */
		if (point.x >= rect.x - bigPointRadius / 2 && point.x <= rect.x + bigPointRadius / 2 &&
			point.y >= rect.y + rect.height / 2 - bigPointRadius / 2 && point.y <= rect.y + rect.height / 2 + bigPointRadius / 2) {
			leftLocal = true
		}
		/* Right */
		if (point.x >= rect.x + rect.width - bigPointRadius / 2 && point.x <= rect.x + rect.width + bigPointRadius / 2 &&
			point.y >= rect.y + rect.height / 2 - bigPointRadius / 2 && point.y <= rect.y + rect.height / 2 + bigPointRadius / 2) {
			rightLocal = true
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
		var leftX = Math.min(startPoint.x, endPoint.x)
		var leftY = Math.min(startPoint.y, endPoint.y)
		var pWidth = Math.abs(startPoint.x - endPoint.x)
		var pHeight = Math.abs(startPoint.y - endPoint.y)

	    ctx.save()
	    ctx.beginPath()
	    ctx.roundedRect(leftX, leftY, pWidth, pHeight, 0, 0)
	    ctx.closePath()
	    ctx.stroke()
	    if (selected||reSized||rotated) {
	    	ctx.strokeStyle = "#00A0E9"
	    	ctx.fillStyle = "yellow"

	    	/* Rotate */
	    	ctx.beginPath()
	    	ctx.arc(leftX + pWidth / 2, leftY - 5*bigPointRadius, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	ctx.fillStyle = "white"
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
	    return Qt.rect(startPoint.x, startPoint.y, Math.abs(endPoint.x - startPoint.x), Math.abs(endPoint.y - startPoint.y))
	}
	function clickOnPoint(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		var result = _inRectCheck(p, Qt.rect(startPoint.x - 5, startPoint.y - 5, Math.abs(endPoint.x - startPoint.x) + 10, Math.abs(endPoint.y - startPoint.y) + 10))
					&& !_inRectCheck(p, Qt.rect(startPoint.x + 5, startPoint.y + 5, Math.abs(endPoint.x - startPoint.x) - 10, Math.abs(endPoint.y - startPoint.y) - 10))
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
		var result = _inEightPointsCheck(p,Qt.rect(Math.min(startPoint.x, endPoint.x),Math.min(startPoint.y, endPoint.y),Math.abs(endPoint.x - startPoint.x), Math.abs(endPoint.y - startPoint.y)))
		reSized = result

		clickedPoint = p
	}
	function handleResize(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var leftX = Math.min(startPoint.x, endPoint.x)
		var leftY = Math.min(startPoint.y, endPoint.y)
		var pWidth = Math.abs(startPoint.x - endPoint.x)
		var pHeight = Math.abs(startPoint.y - endPoint.y)
		var xq = leftX, yq = leftY, widthq = pWidth, heightq = pHeight
		if (topLeftLocal||leftLocal||bottomLeftLocal) {
			xq = Math.min(p.x, leftX + pWidth - smallPointRadius)
			widthq = Math.max(leftX + pWidth - p.x, smallPointRadius)
		}
		if (topRightLocal||rightLocal||bottomRightLocal) {
			widthq = Math.max(p.x - leftX, smallPointRadius)
		}
		if (topRightLocal||topLocal||topLeftLocal) {
			yq = Math.min(p.y, leftY + pHeight - smallPointRadius)
			heightq = Math.max(pHeight + leftY - p.y, smallPointRadius)
		}
		if (bottomRightLocal||bottomLocal||bottomLeftLocal) {
			heightq = Math.max(p.y - leftY, smallPointRadius)
		}
		points[0] = Qt.point(xq, yq)
		points[points.length - 1] = Qt.point(xq + widthq, yq + heightq)
	}
	function rotateOnPoint(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var leftX = Math.min(startPoint.x, endPoint.x)
		var leftY = Math.min(startPoint.y, endPoint.y)
		var pWidth = Math.abs(startPoint.x - endPoint.x)
		var pHeight = Math.abs(startPoint.y - endPoint.y)
		var result = _inRectCheck(p,Qt.rect(leftX + pWidth / 2 - smallPointRadius / 2 , leftY - 5*bigPointRadius - smallPointRadius / 2 , bigPointRadius, bigPointRadius))

		rotated = result

		clickedPoint = p
	}
	function square(p) {
		return ((p)*(p))
	}
	function rotateAngle(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var centerInPoint = Qt.point((startPoint.x + endPoint.x) / 2, (startPoint.y + endPoint.y) / 2)
		var angle = acos((square(clickedPoint.x - centerInPoint.x) + square(clickedPoint.y - centerInPoint.y) + square(p.x - centerInPoint.x) + square(p.y - centerInPoint.y) -
				square(p.x - clickedPoint.x) - square(p.y - clickedPoint.y))/ 2 * Math.sqrt(square(clickedPoint.x - centerInPoint.x) + square(clickedPoint.y - centerInPoint.y))*Math.sqrt(square(p.x - centerInPoint.x) + square(p.y - centerInPoint.y)))

		clickedPoint = p
		return angele
	}
	function pointRotate(point1,point2,angele) {
		var middlePoint = (point2.x - point1.x, point2.y - point1.y)
		var tmpPoint = (middlePoint.x * cos(angele) - middlePoint.y * sin(angele), middlePoint.x * sin(angle) + middlePoint.y * cos(angele))
		var point3 = (tmpPoint.x + point1.x, tmpPoint.y + point1.y)
		return point3
	}
	function handleRotate(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var angle = rotateAngle(p)
		points[0] = pointRotate(Qt.point((startPoint.x+endPoint.x) / 2, (startPoint.y+endPoint.y) / 2),startPoint,angle)
		points[points.length - 1] = pointRotate(Qt.point((startPoint.x+endPoint.x) / 2, (startPoint.y+endPoint.y) / 2),endPoint,angle)
	}

}