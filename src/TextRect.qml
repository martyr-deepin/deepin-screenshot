import QtQuick 2.1

Rectangle {
	id:textRect
	color:"transparent"

	property point startPoint: Qt.point(0, 0)
	property point seClikPoint: Qt.point(0, 0)
	property bool firstClicked: false
	property color textColor: "red"
	property int fontSIZE: 12

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


		border.color: "black"
		color: "white"
		visible: false

		TextEdit {
			id:text
			width: Math.floor((textRect.width - textDistract.x)/font.pixelSize)*font.pixelSize
		 	height: Math.floor((textRect.height - textDistract.y)/font.pixelSize)*font.pixelSize
			clip: true
			color:textRect.textColor
			font.pointSize: textRect.fontSIZE
			wrapMode: TextEdit.Wrap
			anchors.margins: 0.1

			Component.onCompleted: forceActiveFocus()
		}

		Rectangle {
			id:textQuilt
			anchors.fill:parent
			color: "#00A0E9"
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
				textDistract.color = "white"
				textDistract.border.color = "black"
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

