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
	property int clickedKey: 0

	property bool firstDraw: false

	function draw(ctx) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		ctx.lineWidth = 5
	    ctx.save()
	    ctx.beginPath()
		ctx.moveTo(startPoint.x, startPoint.y)
		ctx.lineTo(endPoint.x, endPoint.y)
		ctx.stroke()
	    ctx.closePath()

	    if (endPoint.x - startPoint.x > 0 && endPoint.y - startPoint.y < 0)
	    {
	    	var add = CalcEngine.pointSplid(startPoint, endPoint, 3*ctx.lineWidth)
	    	var pointA = Qt.point(endPoint.x - add[0], endPoint.y + add[1])
	    	var angle = 20/180*Math.PI
	    	var pointB = CalcEngine.pointRotate(endPoint, pointA, angle)
	    	var distance = CalcEngine.pointTolineDistance(startPoint, endPoint, pointB)
	    	var splidistance = Math.sqrt(CalcEngine.square(3*ctx.lineWidth) - CalcEngine.square(distance))
	    	add = CalcEngine.pointSplid(startPoint, endPoint, splidistance)
	    	var pointC = Qt.point(endPoint.x - add[0], endPoint.y + add[1])
	    	var pointD = Qt.point(2*pointC.x - pointB.x, 2*pointC.y - pointB.y)
	    	var pointE = Qt.point((endPoint.x + pointA.x) / 2, (endPoint.y + pointA.y) / 2)

	    	ctx.fillStyle = "red"
	    	ctx.beginPath()

	    	ctx.moveTo(endPoint.x, endPoint.y)
	    	ctx.lineTo(pointB.x, pointB.y)
	    	ctx.lineTo(pointE.x, pointE.y)
	    	ctx.lineTo(pointD.x, pointD.y)
	    	ctx.lineTo(endPoint.x, endPoint.y)
	    	ctx.closePath()
	    	ctx.stroke()
	    	ctx.fill()

	    }
	    else if (endPoint.x - startPoint.x <= 0 && endPoint.y - startPoint.y <= 0)
	    {
	    	var add = CalcEngine.pointSplid(startPoint, endPoint, 20)
	    	var pointA = Qt.point(endPoint.x + add[0], endPoint.y + add[1])
	    	var angle = 20/180*Math.PI
	    	var pointB = CalcEngine.pointRotate(endPoint, pointA, angle)
	    	var distance = CalcEngine.pointTolineDistance(startPoint, endPoint, pointB)
	    	var splidistance = Math.sqrt(CalcEngine.square(20) - CalcEngine.square(distance))
	    	add = CalcEngine.pointSplid(startPoint, endPoint, splidistance)
	    	var pointC = Qt.point(endPoint.x + add[0], endPoint.y + add[1])
	    	var pointD = Qt.point(2*pointC.x - pointB.x, 2*pointC.y - pointB.y)
	    	var pointE = Qt.point((endPoint.x + pointA.x) / 2, (endPoint.y + pointA.y) / 2)

	    	ctx.fillStyle = "red"
	    	ctx.beginPath()

	    	ctx.moveTo(endPoint.x, endPoint.y)
	    	ctx.lineTo(pointB.x, pointB.y)
	    	ctx.lineTo(pointE.x, pointE.y)
	    	ctx.lineTo(pointD.x, pointD.y)
	    	ctx.lineTo(endPoint.x, endPoint.y)
	    	ctx.closePath()
	    	ctx.stroke()
	    	ctx.fill()
	    }
	    else if (endPoint.x - startPoint.x <= 0 && endPoint.y - startPoint.y > 0)
	    {var add = CalcEngine.pointSplid(startPoint, endPoint, 20)
	    	var pointA = Qt.point(endPoint.x + add[0], endPoint.y - add[1])
	    	var angle = 20/180*Math.PI
	    	var pointB = CalcEngine.pointRotate(endPoint, pointA, angle)
	    	var distance = CalcEngine.pointTolineDistance(startPoint, endPoint, pointB)
	    	var splidistance = Math.sqrt(CalcEngine.square(20) - CalcEngine.square(distance))
	    	add = CalcEngine.pointSplid(startPoint, endPoint, splidistance)
	    	var pointC = Qt.point(endPoint.x + add[0], endPoint.y - add[1])
	    	var pointD = Qt.point(2*pointC.x - pointB.x, 2*pointC.y - pointB.y)
	    	var pointE = Qt.point((endPoint.x + pointA.x) / 2, (endPoint.y + pointA.y) / 2)

	    	ctx.fillStyle = "red"
	    	ctx.beginPath()

	    	ctx.moveTo(endPoint.x, endPoint.y)
	    	ctx.lineTo(pointB.x, pointB.y)
	    	ctx.lineTo(pointE.x, pointE.y)
	    	ctx.lineTo(pointD.x, pointD.y)
	    	ctx.lineTo(endPoint.x, endPoint.y)
	    	ctx.closePath()
	    	ctx.stroke()
	    	ctx.fill()
	    }
	    else
	    {
	    	var add = CalcEngine.pointSplid(startPoint, endPoint, 20)
	    	var pointA = Qt.point(endPoint.x - add[0], endPoint.y - add[1])
	    	var angle = 20/180*Math.PI
	    	var pointB = CalcEngine.pointRotate(endPoint, pointA, angle)
	    	var distance = CalcEngine.pointTolineDistance(startPoint, endPoint, pointB)
	    	var splidistance = Math.sqrt(CalcEngine.square(20) - CalcEngine.square(distance))
	    	add = CalcEngine.pointSplid(startPoint, endPoint, splidistance)
	    	var pointC = Qt.point(endPoint.x - add[0], endPoint.y - add[1])
	    	var pointD = Qt.point(2*pointC.x - pointB.x, 2*pointC.y - pointB.y)
	    	var pointE = Qt.point((endPoint.x + pointA.x) / 2, (endPoint.y + pointA.y) / 2)

	    	ctx.fillStyle = "red"
	    	ctx.beginPath()

	    	ctx.moveTo(endPoint.x, endPoint.y)
	    	ctx.lineTo(pointB.x, pointB.y)
	    	ctx.lineTo(pointE.x, pointE.y)
	    	ctx.lineTo(pointD.x, pointD.y)
	    	ctx.lineTo(endPoint.x, endPoint.y)
	    	ctx.closePath()
	    	ctx.stroke()
	    	ctx.fill()
	    }

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

			if (key == 1) {
				startPoint = p
			}
			if (key == 2) {
				endPoint = p
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
}