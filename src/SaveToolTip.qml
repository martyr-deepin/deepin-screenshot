import QtQuick 2.1
import QtGraphicalEffects 1.0
Item {
	id: savetooltip
	anchors.left: parent.left
	width: 170
	height: 28
	visible: false

	property string text:"Autosave"
	Image {
		id: tipbackground
		anchors.fill: parent
		source: "../image/save/imgo.jpg"
		visible: false

		InnerShadow {
			id:innerShadow
			anchors.fill: tipbackground
			radius: 0
			color: Qt.rgba(1, 1, 1, 0.1)
			source: tipbackground
		}


	}

	Item {
		id: tooltipItem
		anchors.fill: parent
		clip: true

		Canvas {
			id: tooltipCanvas
			width: parent.width
			height: parent.height

			onPaint: {
				var ctx = getContext("2d")
				ctx.strokeStyle = Qt.rgba(0, 0, 0, 0.6)
				ctx.linewidth = 5
				ctx.beginPath()
				ctx.moveTo(savetooltip.x, savetooltip.y + 4)
				ctx.arcTo(savetooltip.x, savetooltip.y,savetooltip.x + 4, savetooltip.y,4)
				ctx.moveTo(savetooltip.x + 4, savetooltip.y)
				ctx.lineTo(savetooltip.x + savetooltip.width,savetooltip.y)
				ctx.moveTo(savetooltip.x + savetooltip.width,savetooltip.y)
				ctx.lineTo(savetooltip.x + savetooltip.width,savetooltip.y + savetooltip.height)
				ctx.moveTo(savetooltip.x + savetooltip.width,savetooltip.y + savetooltip.height)
				ctx.lineTo(savetooltip.x, savetooltip.y + savetooltip.height)
				ctx.moveTo(savetooltip.x, savetooltip.y + savetooltip.height)
				ctx.lineTo(savetooltip.x, savetooltip.y+4)
				ctx.closePath()
				ctx.stroke()
			}
		}
	}

	OpacityMask {
		source: tipbackground
		maskSource: tooltipItem
		anchors.fill: tooltipItem
	}

	TextInput {
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