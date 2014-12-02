import QtQuick 2.1
import QtGraphicalEffects 1.0

Item {
	id:blurShape
	anchors.fill: blurItem

	property point startPoint: Qt.point(0, 0)
	property point endPoint: Qt.point(0, 0)
	property var points:[]

	property bool firstPressed: false
	property bool firstReleased: false
	property string blurStyle:""

	Item {
		id: blurBackgroud
		anchors.fill: parent

		FastBlur {
		  id: blur
		  anchors.fill: parent
		  visible: false
		  radius: 32
		  source: ShaderEffectSource { sourceItem: selectArea }
		}
		Item {
			id: mask_source
			anchors.fill: parent
			clip: true
			Canvas {
				id: blurCanvas
				width: parent.width
				height: parent.height

				function _measureRect() {
					var xmin = Math.min(blurShape.startPoint.x, blurShape.endPoint.x)
					var ymin = Math.min(blurShape.startPoint.y, blurShape.endPoint.y)
					var xmax = Math.max(blurShape.startPoint.x, blurShape.endPoint.x)
					var ymax = Math.max(blurShape.startPoint.y, blurShape.endPoint.y)

					for(var i=0;i<blurShape.points.length;i++) {
						xmin = Math.min(xmin, blurShape.points[i].x)
						ymin = Math.min(ymin, blurShape.points[i].y)
						xmax = Math.max(xmax, blurShape.points[i].x)
						ymax = Math.max(ymax,blurShape.points[i].y)
					}

					var width = xmax - xmin
					var height = ymax - ymin
					return Qt.rect(xmin, ymin, width, height)
				}

				function remap() {
					var rect = _measureRect()
					x = rect.x
					y = rect.y
					width = rect.width
					height = rect.height
					if (blurStyle == "line") {
						blurShape.startPoint.x = blurShape.startPoint.x - rect.x
						blurShape.startPoint.y = blurShape.startPoint.y - rect.y
						blurShape.endPoint.x = blurShape.endPoint.x - rect.x
						blurShape.endPoint.y = blurShape.endPoint.y - rect.y

						for(var i=0;i<blurShape.points.length;i++) {
							blurShape.points[i].x = blurShape.points[i].x - rect.x
							blurShape.points[i].y = blurShape.points[i].y - rect.y
						}
					}
					blurShape.startPoint.x = blurShape.startPoint.x - rect.x
					blurShape.startPoint.y = blurShape.startPoint.y - rect.y
					blurShape.endPoint.x = blurShape.endPoint.x - rect.x
					blurShape.endPoint.y = blurShape.endPoint.y- rect.y
					requestPaint()
				}

				onPaint: {
					var ctx = getContext("2d")

					ctx.save()
					ctx.lineWidth = 2
					ctx.strokeStyle =  "red"

					switch(blurStyle) {
						case "rect": {
							ctx.beginPath()
							ctx.rect(Math.min(blurShape.startPoint.x, blurShape.endPoint.x), Math.min(blurShape.startPoint.y, blurShape.endPoint.y), Math.abs(blurShape.endPoint.x - blurShape.startPoint.x), Math.abs(blurShape.endPoint.y - blurShape.startPoint.y))
							ctx.closePath()
							ctx.fill()
							ctx.stroke()
							break
						}
						case "ellipse": {
							ctx.beginPath()
							ctx.ellipse(Math.min(blurShape.startPoint.x, blurShape.endPoint.x), Math.min(blurShape.startPoint.y, blurShape.endPoint.y), Math.abs(blurShape.endPoint.x - blurShape.startPoint.x), Math.abs(blurShape.endPoint.y - blurShape.startPoint.y))
							ctx.closePath()
							ctx.fill()
							ctx.stroke()
							break
						}
						case "line": {
							ctx.lineWidth = 8
							ctx.beginPath()
							ctx.moveTo(blurShape.startPoint.x, blurShape.startPoint.y)
							for (var i=0;i<blurShape.points.length;i++) {
								ctx.lineTo(blurShape.points[i].x, blurShape.points[i].y)
							}
							ctx.lineTo(blurShape.endPoint.x, blurShape.endPoint.y)
							ctx.stroke()
							break
						}
					}
					ctx.save()
				}
				MouseArea {
					anchors.fill: parent

					onPressed: {
						if (firstPressed) return

						blurShape.startPoint = Qt.point(mouse.x,mouse.y)
						blurShape.endPoint = blurShape.startPoint
						firstPressed = true
					}

					onReleased: {
						if (firstReleased) return
						blurShape.endPoint = Qt.point(mouse.x,mouse.y)
						firstReleased = true
						blurCanvas.requestPaint()
						blurCanvas.remap()

						var blur = Qt.createQmlObject('import QtQuick 2.1; BlurShape { blurStyle: blurShape.blurStyle }', blurShape.parent, "blurrect")
					}

					onPositionChanged: {
			   			if (firstReleased) return

			   			if (blurStyle == "line") {
							points.push(Qt.point(mouse.x,mouse.y))
						}
							blurShape.endPoint = Qt.point(mouse.x,mouse.y)
							blurCanvas.requestPaint()
					}

					drag.target:  blurShape.firstReleased ? blurCanvas : null
					drag.axis: Drag.XAndYAxis
					drag.minimumX: 0
					drag.maximumX:  blurCanvas.parent.width - blurCanvas.width
				}
			}
		}

		OpacityMask {
			source: blur
			maskSource: mask_source
			anchors.fill: mask_source
		}
	}
}