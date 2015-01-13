import QtQuick 2.1
import QtGraphicalEffects 1.0
import "calculateRect.js" as CalcEngine

Rectangle {
	id: rect
	x: curX
	y: curY
	width: Math.max(18, text.contentWidth + 10)
	height: Math.max(18, text.contentHeight + 10)

	property int curX
	property int curY
	property int fontSize: 12
    property int numberOrder
	property bool selected: true
	property bool reSized: false
	property bool rotated: false

    property bool isRotating: false
    property bool isDraging: false
    property bool afterRotated: false
	property bool firstDraw: false
	property bool isHovered: false
	property bool isreadOnly: false
    property alias text: text
	property point clickedPoint
	property point convertRotatePoint
	property point rotatePoint
	property var points: []
	property var mainPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]
	property var minorPoints: [Qt.point(0, 0), Qt.point(0, 0), Qt.point(0, 0), Qt.point(0,0)]

	property var bigPointRadius: 3
	property var smallPointRadius: 2
	property var angleGlobal: 0
	property int clickedKey: 0
	property int linewidth: 1
	property var reX
	property var reY
	property color drawColor: "red"
    property  string state: "off"
    transform: Rotation { origin.x: (isRotating||isDraging) ? width/2 : reX ;origin.y: (isRotating||isDraging) ? height/2 : reY; angle: angleGlobal/Math.PI*180;}
    color: (selected || rotated) ? Qt.rgba(1, 1, 1, 0.2) : "transparent"

    onWidthChanged: { mainPoints = _expandByWidth(width);}
	onHeightChanged: { mainPoints = _expandByHeight(height);}

	function _initMainPoints() {
		mainPoints[0] = Qt.point(curX, curY)
		mainPoints[1] = Qt.point(curX, curY + height)
        mainPoints[2] = Qt.point(curX + width, curY)
        mainPoints[3] = Qt.point(curX + width, curY + height)

        CalcEngine.changePointOrder(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
	}
	function _getbeginPoint() {
		var tmpPoint, centerInPoint
		var rotatAngle = Math.PI*2-angleGlobal
		centerInPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
		tmpPoint = CalcEngine.pointRotate(centerInPoint, mainPoints[0], rotatAngle)
		return tmpPoint
	}
	function _expandByWidth(addWidth) {
		if (addWidth == 0) {
			return
		} else {
			mainPoints[0] = mainPoints[0]
			mainPoints[1] = mainPoints[1]
			var add = CalcEngine.pointSplid(mainPoints[0], mainPoints[2], addWidth)
			if (mainPoints[0].x < mainPoints[2].x && mainPoints[0].y > mainPoints[2].y) {
				mainPoints[2] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y - add[1])

			}
			if (mainPoints[0].x > mainPoints[2].x && mainPoints[0].y > mainPoints[2].y ) {
				mainPoints[2] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y - add[1])

			}
			if (mainPoints[0].x < mainPoints[2].x && mainPoints[0].y < mainPoints[2].y) {
				mainPoints[2] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y + add[1])

			}
			if (mainPoints[0].x > mainPoints[2].x && mainPoints[0].y < mainPoints[2].y) {
				mainPoints[2] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y + add[1])

			}
			mainPoints[3] = Qt.point(mainPoints[1].x + mainPoints[2].x - mainPoints[0].x, mainPoints[1].y + mainPoints[2].y - mainPoints[0].y)
			var tmpPoints =  [mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3]]
			return tmpPoints
		}
	}
	function _expandByHeight(addHeight) {
		if (addHeight == 0) {
			return
		} else {
			mainPoints[0] = mainPoints[0]
			mainPoints[2] = mainPoints[2]
			var add = CalcEngine.pointSplid(mainPoints[0], mainPoints[1], addHeight)
			if (mainPoints[0].x <= mainPoints[1].x && mainPoints[0].y < mainPoints[1].y) {
				mainPoints[1] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y + add[1])
			}
			if (mainPoints[0].x < mainPoints[1].x && mainPoints[0].y > mainPoints[1].y) {
				mainPoints[1] = Qt.point(mainPoints[0].x + add[0], mainPoints[0].y - add[1])
			}
			if (mainPoints[0].x > mainPoints[1].x && mainPoints[0].y < mainPoints[1].y) {
				mainPoints[1] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y + add[1])
			}
			if (mainPoints[0].x > mainPoints[1].x && mainPoints[0].y > mainPoints[1].y) {
				mainPoints[1] = Qt.point(mainPoints[0].x - add[0], mainPoints[0].y - add[1])
			}

			mainPoints[3] = Qt.point(mainPoints[1].x + mainPoints[2].x - mainPoints[0].x, mainPoints[1].y + mainPoints[2].y - mainPoints[0].y)
			var tmpPoints =  [mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3]]
			return tmpPoints
		}
	}
	function _getConvertRotatePoint() {
		if (isRotating) {
			convertRotatePoint = Qt.point(width / 2, height / 2)
		} else {
			convertRotatePoint = Qt.point(reX, reY)
		}
	}
	function dashLine(ctx, point0, point3) {
		var startPoint = Qt.point(0, 0), endPoint = Qt.point(0, 0)
		var opposite = false
		if (point0.x <= point3.x && point0.y <= point3.y) {
			startPoint = point0
			endPoint = point3
		}
		if (point3.x < point0.x && point3.y < point0.y) {
			startPoint = point3
			endPoint = point0
		}
		if (point0.x > point3.x && point0.y <= point3.y) {
			opposite = true
			startPoint = point3
			endPoint = point0
		}
		if (point0.x <= point3.x && point0.y > point3.y) {
			opposite = true
			startPoint = point0
			endPoint = point3
		}
		if (startPoint == Qt.point(0, 0) && endPoint == Qt.point(0, 0)) {}
		else {
			var distance = 8,dist = 0, dashpoints = []
			var total_distance = Math.sqrt(CalcEngine.square(startPoint.x - endPoint.x) + CalcEngine.square(startPoint.y - endPoint.y))
			var count = Math.floor(total_distance /  distance)
			for (var i = 0; i < count - 1; i++) {
				dist = (i + 1)*distance
				var tmp =  CalcEngine.pointSplid(startPoint, endPoint, dist)
				if (!opposite) { var tmpPoint = Qt.point(startPoint.x + tmp[0], startPoint.y + tmp[1])}
				else { var tmpPoint = Qt.point(startPoint.x + tmp[0], startPoint.y - tmp[1]) }
				dashpoints.push(tmpPoint)
			}
			ctx.beginPath()
			ctx.moveTo(startPoint.x, startPoint.y)
			ctx.lineTo(dashpoints[0].x, dashpoints[0].y)
			ctx.closePath()
			ctx.stroke()
			for (var i = 1; i < dashpoints.length - 1; i+= 2) {
				ctx.beginPath()
				ctx.moveTo(dashpoints[i].x, dashpoints[i].y)
				ctx.lineTo(dashpoints[i + 1].x, dashpoints[i + 1].y)
				ctx.closePath()
				ctx.stroke()
			}
			ctx.restore()
		}
	}
	function draw(ctx) {
		if (!firstDraw) { _initMainPoints() }

		if (rect.selected || rect.rotated) {
        ctx.lineWidth = 1
		ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.5)

		dashLine(ctx, mainPoints[0], mainPoints[2])
		dashLine(ctx, mainPoints[2], mainPoints[3])
		dashLine(ctx, mainPoints[3], mainPoints[1])
		dashLine(ctx, mainPoints[1], mainPoints[0])

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
	}
	function clickOnPoint(p) {
        var result = false
        if (CalcEngine.textClickOnPoint(p, mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])) {
            result = true
            selected = result
        }
        if (rotateOnPoint(p)) {
            result = true
            rotated = result
        }
        if (result) {
            canvas.selectUnique(numberOrder)
        }

        clickedPoint = p
        return result
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
        border.width: 1
        border.color: "#01bdff"
		TextEdit {
			id:text
			textMargin: 3
		//	width: Math.floor((canvas.width - curX - 10) / font.pixelSize)*font.pixelSize
		//	height: Math.floor((canvas.height - curY - 10) / font.pixelSize)*font.pixelSize
			color: drawColor
            onColorChanged: { select(0, 0)}
            font.pixelSize: fontSize
			wrapMode: TextEdit.Wrap
			readOnly: isreadOnly
			cursorVisible: !isreadOnly
            onFocusChanged: { if (focus) { canvas.selectUnique(numberOrder); canvas.requestPaint()}}

            onCursorVisibleChanged: { canvas.requestPaint()}
			onContentWidthChanged: { canvas.requestPaint()}
			Component.onCompleted: forceActiveFocus()
            // DropShadow {
           //     anchors.fill: parent
           //     horizontalOffset: 0
           //     verticalOffset: 1
           //     radius: 10
           //     samples: 16
           //     color: Qt.rgba(0, 0, 0, 0.2)
           //     source: parent
           // }
        }

	}
	/* click on the text is difficult to handle , add an MouseArea */
	MouseArea {
		id: moveText
		anchors.fill: parent
		hoverEnabled: true

		onEntered: {
			/* To unbind the width and height of text */
			cursorShape = Qt.ClosedHandCursor
		}
		onPressed: {
            var pos = screen.get_absolute_cursor_pos()
            clickedPoint = Qt.point(pos.x, pos.y)
            rect.selected = true
            text.forceActiveFocus()
			canvas.requestPaint()
		}
		onPositionChanged: {
            if (rect.selected && pressed) {
                var pos = screen.get_absolute_cursor_pos()
                isDraging = true
                handleDrag(Qt.point(pos.x, pos.y))
                isDraging = false
			}
			canvas.requestPaint()
		}
        onDoubleClicked: {
			rect.selected = true
            rect.isreadOnly = false
            text.readOnly = false
			text.cursorVisible = true
            text.forceActiveFocus()
            canvas.requestPaint()

        }
	}
	function handleDrag(p) {
    /* keep the text's width & height the same as before drag*/
       // width = width
       // height = height
		var delX = p.x - clickedPoint.x
		var delY = p.y - clickedPoint.y
		for (var i = 0; i < mainPoints.length; i++) {
			mainPoints[i].x = mainPoints[i].x + delX
			mainPoints[i].y = mainPoints[i].y + delY
		}
		var destCentralPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
		curX = destCentralPoint.x - rect.width / 2
		curY = destCentralPoint.y - rect.height / 2
        reX = width / 2
        reY = height / 2
		clickedPoint = p
	}
	function handleResize(p, key) {}
	function rotateOnPoint(p) {

		var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
		if (p.x >= rotatePoint.x - 15 && p.x <= rotatePoint.x + 15 && p.y >= rotatePoint.y - 15 && p.y <= rotatePoint.y + 15) {
			rotated = true
		} else {
			rotated = false
		}
		clickedPoint = rotatePoint
		return rotated
	}
	function handleRotate(p) {
        var beginPoint = _getbeginPoint()
		curX = beginPoint.x
		curY = beginPoint.y

		var centerInPoint = Qt.point((mainPoints[0].x + mainPoints[3].x) / 2, (mainPoints[0].y + mainPoints[3].y) / 2)
		var rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])
        var angle = CalcEngine.calcutateAngle(clickedPoint, p, centerInPoint)
        angleGlobal += angle
		for (var i = 0; i < 4; i++) {
            mainPoints[i] = CalcEngine.pointRotate(centerInPoint, mainPoints[i], angle)
		}
        rotatePoint = CalcEngine.getRotatePoint(mainPoints[0], mainPoints[1], mainPoints[2], mainPoints[3])

		reX = width / 2
		reY = height / 2
		clickedPoint = p
    }
	function hoverOnRotatePoint(p) {
		var result =  false
		result = rotateOnPoint(p)
		return result
	}
	function hoverOnShape(p) {
		var result = false
		isHovered = result
        return result
	}

}
