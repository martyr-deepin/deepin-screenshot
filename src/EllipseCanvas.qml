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
	property int bigPointRadius: 3
	property int smallPointRadius: 2
	property int clickedKey: 0
	property int linewidth: 3
    property color drawColor: "red"
    
    onSelectedChanged: { if (selected) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}
    onRotatedChanged: { if (rotated) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}
    onReSizedChanged: { if (reSized) {canvas.selectUnique(numberOrder); canvas.requestPaint()}}


	function _getMainPoints() {

		var startPoint = points[0]
		var endPoint = points[points.length - 1]
		var leftX = Math.min(startPoint.x, endPoint.x)
		var leftY = Math.min(startPoint.y, endPoint.y)
		var pWidth = Math.abs(startPoint.x - endPoint.x)
		var pHeight = Math.abs(startPoint.y - endPoint.y)
		mainPoints[0] = Qt.point(leftX, leftY)
		mainPoints[1] = Qt.point(leftX + pWidth, leftY)
		mainPoints[2] = Qt.point(leftX, pHeight + leftY)
		mainPoints[3] = Qt.point(leftX + pWidth, leftY + pHeight)

		var tmpPoints = CalcEngine.fourPoint_dir(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
		return tmpPoints
	}

	function draw(ctx) {
		if (!firstDraw) {
			mainPoints = _getMainPoints()
		}
		minorPoints = CalcEngine.getAnotherFourPoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
	    var points1 = CalcEngine.getEightControlPoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])

	    ctx.lineWidth = linewidth
	    ctx.strokeStyle = drawColor
	    ctx.fillStyle = "transparent"
	    ctx.save()
		ctx.beginPath()
		ctx.moveTo(minorPoints[0].x, minorPoints[0].y);
		ctx.bezierCurveTo(points1[0].x, points1[0].y, points1[1].x, points1[1].y, minorPoints[1].x, minorPoints[1].y);
		ctx.bezierCurveTo(points1[4].x, points1[4].y, points1[5].x, points1[5].y , minorPoints[2].x, minorPoints[2].y );
		ctx.bezierCurveTo(points1[6].x, points1[6].y, points1[7].x, points1[7].y, minorPoints[3].x, minorPoints[3].y);
		ctx.bezierCurveTo(points1[3].x, points1[3].y, points1[2].x, points1[2].y, minorPoints[0].x, minorPoints[0].y);
		ctx.closePath()

		if (processBlur||processMosaic) {
			ctx.fill()
			ctx.stroke()
			ctx.clip()
			if (processBlur) {
				ctx.putImageData(parent.blurImageData, 0, 0)
			} else {
				ctx.putImageData(parent.mosaicImageData, 0, 0)
			}
			ctx.restore()
		} else {
			ctx.stroke()
		}
	    if (selected||reSized||rotated) {
	    	ctx.lineWidth = 1
	    	ctx.strokeStyle = "black"
	    	ctx.fillStyle = "yellow"

	    	/* Rotate */

	    	var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])

	    	ctx.beginPath()
	    	ctx.arc(rotatePoint.x, rotatePoint.y, bigPointRadius + linewidth/2, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	ctx.lineWidth = linewidth
	    	ctx.strokeStyle = "white"
	    	ctx.fillStyle = "white"
	    	/* Top left */
	    	ctx.beginPath()
	    	ctx.arc(mainPoints[1].x, mainPoints[1].y, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()
	    	/* Top right */
	    	ctx.beginPath()
	    	ctx.arc(mainPoints[3].x, mainPoints[3].y, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom left */
	    	ctx.beginPath()
	    	ctx.arc(mainPoints[0].x, mainPoints[0].y, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom right */
	    	ctx.beginPath()
	    	ctx.arc(mainPoints[2].x, mainPoints[2].y, bigPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Top */
	    	ctx.beginPath()
	    	ctx.arc(minorPoints[0].x, minorPoints[0].y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Bottom */
	    	ctx.beginPath()
	    	ctx.arc(minorPoints[1].x, minorPoints[1].y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Left */
	    	ctx.beginPath()
	    	ctx.arc(minorPoints[2].x, minorPoints[2].y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	/* Right */
	    	ctx.beginPath()
	    	ctx.arc(minorPoints[3].x, minorPoints[3].y, smallPointRadius, 0, Math.PI * 2, false)
	    	ctx.closePath()
	    	ctx.fill()
	    	ctx.stroke()

	    	ctx.lineWidth = 0.5
	    	ctx.strokeStyle = "white"
	    	ctx.beginPath()
	    	ctx.moveTo(mainPoints[0].x, mainPoints[0].y)
	    	ctx.lineTo(mainPoints[2].x, mainPoints[2].y)
	    	ctx.lineTo(mainPoints[3].x, mainPoints[3].y)
	    	ctx.lineTo(mainPoints[1].x, mainPoints[1].y)
	    	ctx.lineTo(mainPoints[0].x, mainPoints[0].y)
	    	ctx.closePath()
	    	ctx.stroke()
        }
        if (isHovered) {
        ctx.lineWidth = 1
	    ctx.strokeStyle = "#01bdff"
	    ctx.save()
		ctx.beginPath()
		ctx.moveTo(minorPoints[0].x, minorPoints[0].y);
		ctx.bezierCurveTo(points1[0].x, points1[0].y, points1[1].x, points1[1].y, minorPoints[1].x, minorPoints[1].y);
		ctx.bezierCurveTo(points1[4].x, points1[4].y, points1[5].x, points1[5].y , minorPoints[2].x, minorPoints[2].y );
		ctx.bezierCurveTo(points1[6].x, points1[6].y, points1[7].x, points1[7].y, minorPoints[3].x, minorPoints[3].y);
		ctx.bezierCurveTo(points1[3].x, points1[3].y, points1[2].x, points1[2].y, minorPoints[0].x, minorPoints[0].y);
		ctx.closePath()
        ctx.stroke()
        }

		if (!(processBlur||processMosaic)) {
			ctx.restore()
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
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(mainPoints[1], p)) {
			var result =  true
			reSized = result
			clickedKey = 2
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(mainPoints[2], p)) {
			var result =  true
			reSized = result
			clickedKey = 3
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(mainPoints[3], p)) {
			var result =  true
			reSized = result
			clickedKey = 4
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(minorPoints[0], p)) {
			var result =  true
			reSized = result
			clickedKey = 5
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(minorPoints[1], p)) {
			var result =  true
			reSized = result
			clickedKey = 6
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(minorPoints[2], p)) {
			var result =  true
			reSized = result
			clickedKey = 7
			clickedPoint = p
			return result
		}
		if (CalcEngine.pointClickIn(minorPoints[3], p)) {
			var result =  true
			reSized = result
			clickedKey = 8
			clickedPoint = p
			return result
		}
		if (rotateOnPoint(p)) {
			var result = true
			rotated = true
			clickedPoint = p
			return result
		}

		if (CalcEngine.pointOnEllipse(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], p)) {
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
			var points = CalcEngine.reSizePointPosititon(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], p, key)
			for (var i = 0; i < 4; i ++) { mainPoints[i] = points[i] }
		}
		clickedPoint = p

	}
	function rotateOnPoint(p) {
		var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
		if (p.x >= rotatePoint.x - 5 && p.x <= rotatePoint.x + 5 &&
			p.y >= rotatePoint.y - 5 && p.y <= rotatePoint.y + 5) {

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
        var result
    	if  (CalcEngine.pointOnEllipse(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3], p)) {
			result = true
        } else {
            result = false 
        }
        isHovered = result
        return result
    }

}
