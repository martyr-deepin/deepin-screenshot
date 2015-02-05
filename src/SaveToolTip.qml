import QtQuick 2.1
import QtGraphicalEffects 1.0
Item {
	id: savetooltip
	width: text.contentWidth + 20
	height: 28
	visible: false

	property string text:"Autosave"
	Image {
		id: tipbackground
		anchors.fill: parent
		source: "../image/save/imgo.jpg"
		visible: false
	}
	InnerShadow {
	    id:innerShadow
		anchors.fill: tipbackground
		radius: 10
		samples: 16
		color: Qt.rgba(0, 0, 0, 0.5)
		horizontalOffset: -1
		verticalOffset: -1
		source: tipbackground
		visible: false
	}

	Item {
		id: tooltipItem
		anchors.fill: parent
		clip: true
		visible: false
		Canvas {
			id: tooltipCanvas
			width: parent.width
			height: parent.height

			onPaint: {
				var ctx = getContext("2d")
				ctx.strokeStyle = "white"
				ctx.beginPath()
				ctx.moveTo(0, 4)
				ctx.arcTo(0, 0, 4, 0, 4)
				ctx.lineTo(width, 0)
				ctx.lineTo(width, height)
				ctx.lineTo(0, height)
				ctx.lineTo(0, 4)
				ctx.closePath()
				ctx.fillStyle = "white"
				ctx.fill()
			}
		}
	}

	OpacityMask {

		source: innerShadow
		maskSource: tooltipItem
		anchors.fill: tooltipItem
	}

	TextInput {
		id: text
		anchors.fill: parent
		anchors.leftMargin: 10
		anchors.rightMargin: 10
		anchors.topMargin: 8
		anchors.bottomMargin: 8
		text: savetooltip.text
		color: "#FDA825"
		font.pixelSize: 11
		readOnly: true
	}

}
