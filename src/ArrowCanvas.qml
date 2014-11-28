import QtQuick 2.1
import "calculateRect.js" as CalcEngine

Item {
	property bool selected: false
	property bool reSized: false
	property bool rotated: false
	property point clickedPoint

	property var points: []
 	property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
	property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

	property int bigPointRadius: 6
	property int smallPointRadius: 4

	property bool firstDraw: false

	function draw(ctx) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		ctx.lineWidth = 7
	    ctx.save()

	    ctx.beginPath()
		ctx.moveTo(startPoint.x, startPoint.y)
		ctx.lineTo(endPoint.x, endPoint.y)
		ctx.stroke()
	    ctx.closePath()

	    if (selected||reSized||rotated) {
	    	ctx.strokeStyle = "#00A0E9"
	    	ctx.fillStyle = "white"

	    	/* Top left */
	    	ctx.beginPath()
	    	ctx.arc(startPoint.x, startPoint.y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()
	    	/* Top right */
	    	ctx.beginPath()
	    	ctx.arc(endPoint.x, endPoint.y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

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

		if (CalcEngine.pointClickIn(startPoint, p) || CalcEngine.pointClickIn(endPoint, p)) {
			var result =  true
			reSized = result
			rotated = result
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
	function handleResize(p) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		if (reSized) {
			if (CalcEngine.pointClickIn(startPoint, p)) {
				startPoint = p
			}
			if (CalcEngine.pointClickIn(endPoint, p)) {
				endPoint = p
			}
			points[0] = startPoint
			points[points.length - 1] = endPoint
		}
		clickedPoint = p
	}
	function rotateOnPoint(p) {
		if (reSized) {
			rotated = true
		}
		return rotated
	}

	function handleRotate(p) {
		handleResize(p)
	}
}