import QtQuick 2.1
import QtGraphicalEffects 1.0

Item {
	id:mosaicShape
	anchors.fill: blurItem
	property string mosaicStyle: "rect"
	Item {
		id: background
		anchors.fill: parent
		visible: false
		Canvas {
			id: canvas
			anchors.fill: parent
			property url imageUrl: "/tmp/deepin-screenshot.png"

			Component.onCompleted: loadImage(imageUrl)
			onImageLoaded: requestPaint()

			onPaint: {
				if (!isImageLoaded(imageUrl)) return

				var ctx = canvas.getContext("2d")
				var imageData = ctx.createImageData("/tmp/deepin-screenshot.png")
				var mosaic = { x:5, y:5 }
				var image = { width: parent.width, height: parent.height }
				var pixelArray = imageData.data

				/* pixel assignment */
				for(var i = 0; i < image.height; i+= mosaic.y) {
					for(var j = 0; j < image.width; j+= mosaic.x) {
						var num = Math.random()
						var randomPixel = { x: Math.floor(num*mosaic.x+i), y: Math.floor(num*mosaic.y+j) }

						for(var k = j; k < j + mosaic.x; k++) {
							for( var l=i; l < i+mosaic.y; l++) {
								pixelArray[( l*image.width + k)*4] = pixelArray[( randomPixel.x*image.width + randomPixel.y)*4]
								pixelArray[( l*image.width + k)*4 + 1] = pixelArray[( randomPixel.x*image.width + randomPixel.y)*4 + 1]
								pixelArray[( l*image.width + k)*4 + 2] = pixelArray[( randomPixel.x*image.width + randomPixel.y)*4 + 2]
								pixelArray[( l*image.width + k)*4 + 3] = pixelArray[( randomPixel.x*image.width + randomPixel.y)*4 + 3]
							}
						}
					}
				}
				ctx.putImageData(imageData, 0, 0)
				/* fill the mosaic rectangle */
				for(var i = 0; i < image.height; i+= mosaic.y) {
					for(var j = 0;j < image.width; j+=mosaic.x) {
						var num = Math.random();
						var randomPixel = {x: Math.floor(num*mosaic.x+i), y: Math.floor(num*mosaic.y+j)}

						ctx.fillStyle = "rgba(" + pixelArray[( randomPixel.x*image.width + randomPixel.y )*4] + ","+
						pixelArray[( randomPixel.x*image.width + randomPixel.y )*4 + 1] + "," + pixelArray[(randomPixel.x*image.width+randomPixel.y)*4 + 2]
						+ "," + pixelArray[(randomPixel.x*image.width+randomPixel.y)*4 + 3] + ")"
						ctx.fillRect( j, i, mosaic.x, mosaic.y)

					}
				}
			}
		}
	}
	Item {
		id: mask_source
		anchors.fill: parent
		clip: true
		Canvas {
			id: mosaicCanvas
			width: parent.width
			height: parent.height
			   property bool recording: false
    property string shapeName: "rect"
    property var shapes: []
    property var currenRecordingShape

    onPaint: {
        var ctx = mosaicCanvas.getContext("2d")
        ctx.clearRect(x, y, width, height)
        ctx.strokeStyle = "red"
        for (var i = 0; i < shapes.length; i++) {
            shapes[i].draw(ctx)
        }
    }

    function clickOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].selected || shapes[i].reSized) {
                shapes[i].rotateOnPoint(p)
            }
        }

        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].clickOnPoint(p)){
                var selectedShape = i
            }
        }

        if (selectedShape != null ) {
            for (var i = 0; i < shapes.length && i != selectedShape; i++) {
                shapes[i].selected = false
                shapes[i].reSized = false
            }
            return true
        } else {
            for (var i = 0; i < shapes.length; i++) {
                shapes[i].selected = false
                shapes[i].reSized = false
                shapes[i].rotated = false
            }
            return false
        }
    }
    function resizeOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].resizeOnPoint(p)) {
                return true
            }
        }
        return false
    }
    function rotateOnPoint(p) {
        for (var i = 0; i < shapes.length; i++) {
            if (shapes[i].rotateOnPoint(p)) {
                return true
            }
        }
        return false
    }
    Component {
        id: rect_component
        RectangleCanvas {}
    }
    // Component {
    //     id: mosaic_component
    //     MosaicCanvas {}
    // }
    Component {
        id: ellipse_component
        EllipseCanvas {}
    }
    Component {
        id: arrow_component
        ArrowCanvas {}
    }
    // Rectangle {
    //     anchors.fill: parent
    //     color: Qt.rgba(0,1,1,0.2)
    // }
    MouseArea {
        id: canvasArea
        anchors.fill: parent

        onPressed: {

            if (!mosaicCanvas.clickOnPoint(Qt.point(mouse.x, mouse.y))) {
                    mosaicCanvas.recording = true
                    if (mosaicCanvas.shapeName == "rect") {
                        mosaicCanvas.currenRecordingShape = rect_component.createObject(canvas, {})

                    }
                    if (mosaicCanvas.shapeName == "ellipse") {
                        mosaicCanvas.currenRecordingShape = ellipse_component.createObject(canvas, {})
                    }
                    if (mosaicCanvas.shapeName == "arrow") {
                        mosaicCanvas.currenRecordingShape = arrow_component.createObject(canvas, {})
                    }
                    // if (canvas.shapeName == "mosaic") {
                    //     canvas.currenRecordingShape = mosaic_component.createObject(canvas, {})
                    // }
                    mosaicCanvas.currenRecordingShape.mosaicX = true
                    mosaicCanvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                    mosaicCanvas.shapes.push(mosaicCanvas.currenRecordingShape)
            }
            mosaicCanvas.requestPaint()
        }
        onReleased: {
            if (mosaicCanvas.recording) {
                mosaicCanvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
                mosaicCanvas.currenRecordingShape.firstDraw = true
                mosaicCanvas.recording = false
            }

            mosaicCanvas.requestPaint()
        }

        onPositionChanged: {
            if (mosaicCanvas.recording) {
                mosaicCanvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
            } else {
                var selectedShape = null,reSizedShape = null,rotatedShape = null
                for (var i = 0; i < mosaicCanvas.shapes.length; i++) {
                    if (mosaicCanvas.shapes[i].reSized||drag.active)  reSizedShape = mosaicCanvas.shapes[i]
                    if (mosaicCanvas.shapes[i].rotated||drag.active) rotatedShape = mosaicCanvas.shapes[i]
                    if (mosaicCanvas.shapes[i].selected||drag.active)  selectedShape = mosaicCanvas.shapes[i]
                }

                if (selectedShape != null) {
                    selectedShape.handleDrag(Qt.point(mouse.x, mouse.y))
                }
                if (reSizedShape != null) {
                    reSizedShape.handleResize(Qt.point(mouse.x, mouse.y), reSizedShape.clickedKey)
                }
                if (rotatedShape != null) {
                    rotatedShape.handleRotate(Qt.point(mouse.x, mouse.y))
                }
            }
            mosaicCanvas.requestPaint()
        }


    }
		}
	}
	OpacityMask {
		source: background
		maskSource: mask_source
		anchors.fill: mask_source
	}
}
