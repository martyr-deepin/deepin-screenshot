import QtQuick 2.1
import "calculateRect.js" as CalcEngine

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
	property var bigPointRadius: 3
	property var smallPointRadius: 2
	property int clickedKey: 0
	property int linewidth: 3
	property color drawColor: "red"
	property int arrowSize: 16
	property int arrowAngle: 40

    onSelectedChanged: { if (selected) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}
    onRotatedChanged: { if (rotated) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}
    onReSizedChanged: { if (reSized) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}

	function draw(ctx) {
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		ctx.lineWidth = linewidth
		ctx.strokeStyle = drawColor
		ctx.save()
		ctx.beginPath()
		ctx.moveTo(startPoint.x, startPoint.y)
		ctx.lineTo(endPoint.x, endPoint.y)
		ctx.stroke()
		ctx.closePath()

		if (isHovered) {
			ctx.lineWidth = 1
			ctx.strokeStyle = "#01bdff"
			ctx.stroke()
		}

		var xMultiplier = (startPoint.x - endPoint.x) / Math.abs(startPoint.x - endPoint.x)
		var yMultiplier = (startPoint.y - endPoint.y) / Math.abs(startPoint.y - endPoint.y)

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

		ctx.fillStyle =  drawColor
		ctx.strokeStyle = drawColor
		ctx.beginPath()
		ctx.moveTo(endPoint.x, endPoint.y)
		ctx.lineTo(pointB.x, pointB.y)
		ctx.lineTo(pointE.x, pointE.y)
		ctx.lineTo(pointD.x, pointD.y)
		ctx.lineTo(endPoint.x, endPoint.y)
		ctx.closePath()
		ctx.stroke()
		ctx.fill()

		if (selected||reSized||rotated) {
			ctx.lineWidth = 1
			ctx.strokeStyle = "white"
			ctx.fillStyle = "white"

			/* Top left */
			ctx.beginPath()
			ctx.arc(startPoint.x, startPoint.y, smallPointRadius + linewidth/2, 0, Math.PI * 2, false)
			ctx.closePath()
			ctx.fill()
			ctx.stroke()
			/* Top right */
			ctx.beginPath()
			ctx.arc(endPoint.x, endPoint.y, smallPointRadius + linewidth/2, 0, Math.PI * 2, false)
			ctx.closePath()
			ctx.fill()
			ctx.stroke()

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
	function hoverOnRotatePoint(p) {
		var result = true
		return  result
	}
	function hoverOnShape(p) {
		var result
		var startPoint = points[0]
		var endPoint = points[points.length - 1]

		if  (CalcEngine.pointOnLine(startPoint, endPoint, p)) {
			result = true
		} else {
			result = false
		}
			isHovered = result
			return result
	}
}
