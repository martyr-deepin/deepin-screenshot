import QtQuick 2.1
import QtGraphicalEffects 1.0
Rectangle {
	id:textRect
	color:"transparent"

	property point startPoint: Qt.point(0, 0)
	property point seClikPoint: Qt.point(0, 0)
	property bool firstClicked: false
	property color textColor: "red"
	property int fontSIZE: 16

	function isEmpty() {
        if (startPoint == Qt.point(0,0) && seClikPoint == Qt.point(0,0)) {
            return true
        }

        else {
            return false
        }
    }
	function _calculateIntext(p1,p2) {
		if(p1 >= textDistract.x && p1 <= textDistract.x + textDistract.width
		&& p2 >= textDistract.y && p2 <= textDistract.y + textDistract.height) {
			return true
		}
		else {
			return false
		}
	}
	function _remapRect() {

		textRect.x = startPoint.x
		textRect.y = startPoint.y
		startPoint.x = startPoint.x - textDistract.x
		startPoint.y = startPoint.y - textDistract.y
		textRect.width =  textDistract.width
		textRect.height = textDistract.height

	}
	function _thirdmapRect() {
		var p1 = textRect.x
		var p2 = textRect.y

		textRect.x = 0
		textRect.y = 0
		textRect.width = textRect.parent.width
		textRect.height = textRect.parent.height
		startPoint.x = p1
		startPoint.y = p2
	}
	MouseArea {
		id:textArea
		hoverEnabled: true
		anchors.fill: parent

		onClicked: {
			if(!firstClicked) {

				startPoint = Qt.point(mouse.x, mouse.y)
				textDistract.visible = true
				firstClicked = true
			}
			else {
				seClikPoint = Qt.point(mouse.x,mouse.y)
				if(!_calculateIntext(seClikPoint.x, seClikPoint.y) && text.text != "") {
						text.readOnly = true
						textDistract.color = "transparent"
						textDistract.border.color = "transparent"
						textCanvas.visible = false
						textRect._remapRect()
				} else if (!_calculateIntext(seClikPoint.x, seClikPoint.y) && text.text == "") {
						textDistract.visible = false
				}
			}
		}
	}
	Rectangle {
		id: textDistract

		x: startPoint.x
		y: startPoint.y
		width: Math.max(12, text.contentWidth)
		height: Math.max(22, text.contentHeight)

		color: Qt.rgba(1, 1 , 1, 0.2)
		visible: false

		Canvas {
			id: textCanvas
			width: parent.width
			height: parent.height

			visible: true
			onPaint: {

				var ctx = getContext("2d")

				ctx.strokeStyle = "white"
				ctx.lineWidth = 1
				ctx.beginPath()
				ctx.moveTo(0,8)
				ctx.lineTo(0,0)
				ctx.lineTo(8,0)
				ctx.stroke()

				for (var k=8;k + 12<=width;k = k+12) {
					ctx.strokeStyle = "white"
					ctx.beginPath()
					ctx.moveTo(k,0)
					ctx.lineTo(k + 8,0)
					ctx.closePath()
					ctx.stroke()
				}
				for (var j=4;j + 12<=width;j = j+12) {
					ctx.strokeStyle = "white"
					ctx.beginPath()
					ctx.moveTo(width,j)
					ctx.lineTo(width,j+8)
					ctx.closePath()
					ctx.stroke()
				}
				for (var l=width;l - 12>=0;l = l-12) {
					ctx.strokeStyle = "white"
					ctx.beginPath()
					ctx.moveTo(l, height)
					ctx.lineTo(l-8, height)
					ctx.closePath()
					ctx.stroke()
				}
				for (var h=height;h - 12>=0;h = h-12) {
					ctx.strokeStyle = "white"
					ctx.beginPath()
					ctx.moveTo(0, h)
					ctx.lineTo(0, h-8)
					ctx.closePath()
					ctx.stroke()
				}

			}
		}

		TextEdit {
			id:text
			width: Math.floor((selectArea.width - startPoint.x)/font.pixelSize)*font.pixelSize
		 	height: Math.floor((selectArea.height - startPoint.y)/font.pixelSize)*font.pixelSize
			color:textRect.textColor
			font.pixelSize: textRect.fontSIZE
			wrapMode: TextEdit.Wrap
			anchors.margins: 3
			onTextChanged: {
				if(text.length>=(selectArea.height - startPoint.y)/font.pixelSize*(selectArea.width-startPoint.x)/font.pixelSize) {
					readOnly = true
				}
			}
			Component.onCompleted: forceActiveFocus()
		}



		Rectangle {
			id:textQuilt
			anchors.fill:parent
			color: "steelblue"
			border.color: "#00A0E9"
			opacity: 0.2
			visible:false
		}

		MouseArea {
			id: moveText
			anchors.fill: textDistract
			enabled: text.readOnly
			hoverEnabled: true

			onEntered: {
				/* To unbind the width and height of text */
				text.width = text.width
				text.height = text.height
				textQuilt.visible = true
				cursorShape = Qt.ClosedHandCursor
			}
			onExited: textQuilt.visible = false || drag.active

			onDoubleClicked: {
				text.readOnly = false
				textQuilt.visible = false
				textCanvas.visible = true
				textDistract.color = Qt.rgba(1,1,1,0.2)
				textRect._thirdmapRect()
			}

		drag.target: textQuilt.visible ? textRect : null
		drag.axis: Drag.XAndYAxis
		drag.minimumX: 0
		drag.maximumX: textRect.parent.width - textDistract.width
		drag.minimumY: 0
		drag.maximumY: textRect.parent.height - textDistract.height

		}
	}

}
