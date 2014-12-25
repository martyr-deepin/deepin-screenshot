import QtQuick 2.1
import "calculateRect.js" as CalcEngine

Rectangle {
	x: curX
	y: curY
	width: Math.max(8, text.contentWidth + 10)
	height: Math.max(18, text.contentHeight + 10)
    
    property int curX
    property int curY
    property int fontSize: 12 
    
    property bool selected: false
    property bool reSized: false
    property bool rotated: false
	property bool isrotatedPoint: true
	property bool firstDraw: false
	property bool isHovered: false
    property bool isreadOnly: false
	property point clickedPoint
	property var points: []
	property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
	property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

	property var bigPointRadius: 3
	property var smallPointRadius: 2
	property int clickedKey: 0
	property int linewidth: 3
	property color drawColor: "red"

    color: isreadOnly ? "transparent": Qt.rgba(1, 1, 1, 0.2)
    function _getMainPoints() {

		mainPoints[0] = Qt.point(curX, curY)
		mainPoints[1] = Qt.point(curX, curY + height)
		mainPoints[2] = Qt.point(curX + width, curY)
		mainPoints[3] = Qt.point(curX + width, curY + height)

		var tmpPoints = CalcEngine.fourPoint_dir(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
		return tmpPoints
	}
    
    function draw(ctx) {
	    if (!firstDraw) {
			mainPoints = _getMainPoints()
		}

        ctx.lineWidth = 1
        ctx.strokeStyle = isreadOnly ? "transparent" : "white"
		ctx.beginPath()
		ctx.moveTo(curX, curY+ 3)
        ctx.lineTo(curX, curY)
        ctx.lineTo(curX + 5, curY)
		ctx.stroke()
        for (var k = curX + 8;k + 10 <= curX + width;k = k + 10) {
			ctx.beginPath()
			ctx.moveTo(k, curY)
			ctx.lineTo(k + 5, curY)
			ctx.stroke()
		}
		for (var j = curY;j + 10 <= curY+ height;j = j + 10) {
			ctx.beginPath()
			ctx.moveTo( curX + width, j)
			ctx.lineTo( curX + width,j + 5)
			ctx.stroke()
		}
		for (var l = curX + width;l - 10 >= curX;l = l-10) {
			ctx.beginPath()
			ctx.moveTo(l, height + y)
			ctx.lineTo(l-5, height + y)
			ctx.stroke()
		}
		for (var h = curY+ height;h - 10 >= curY;h = h-10) {
			ctx.beginPath()
			ctx.moveTo(curX, h)
			ctx.lineTo(curX, h-5)
			ctx.stroke()
        }
        if (isrotatedPoint) {
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
        }
        ctx.restore()

    }
    function clickOnPoint(p) {
        if (p.x >= curX -5 && p.x <= curX + width &&
        p.y >= curY - 5 && p.y <= curY + height) {
            return true 
        } else {
            return false
        }
    } 
    Rectangle {
       id: textRect
       clip: true
       anchors.fill: parent
       anchors.leftMargin: 6
       anchors.rightMargin: 6
       anchors.topMargin: 3
       anchors.bottomMargin: 3
       color: "transparent"
       TextEdit {
    	    id:text
            textMargin: 3
            width: Math.floor((canvas.width - curX - 10) / font.pixelSize)*font.pixelSize
            height: Math.floor((canvas.height - curY - 10) / font.pixelSize)*font.pixelSize
            color: drawColor
            font.pixelSize: fontSize
            wrapMode: TextEdit.Wrap

            readOnly: isreadOnly
            cursorVisible: !isreadOnly
            onContentWidthChanged: {canvas.requestPaint()}
            Component.onCompleted: forceActiveFocus()
        }
    }
    function handleDrag(p) {

		var delX = p.x - clickedPoint.x
		var delY = p.y - clickedPoint.y
        curX = curX + delX
        curY = curY + delY

		clickedPoint = p
	}
    function handleResize(p, key) {}
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
        curX = mainPoints[0].x
        curY = mainPoints[0].y
		clickedPoint = p
	}

    function hoverOnRotatePoint(p) {
       rotateOnPoint(p)
	}
	function hoverOnShape(p) {
        var result
        result = clickOnPoint(p) 
		isHovered = result
			return result
	}

}
