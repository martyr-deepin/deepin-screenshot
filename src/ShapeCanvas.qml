import QtQuick 2.1
import "graphicProcess.js" as CalcGraphic

Canvas {
	id: canvas
	width: parent.width
	height: parent.height

	property bool recording: false
	property string shapeName: "rect"
	property var shapes: []
	property var currenRecordingShape
	property var linewidth: 3
	property color paintColor: "red"
	property url imageUrl: "/tmp/deepin-screenshot.png"
	property string blurImage:"/tmp/deepin-screenshot-blur.png"
	property string mosaicImage: "/tmp/deepin-screenshot-mosaic.png"
	property bool isBlur: false
	property bool bluring:false
	property bool processBlur: false
	property var blurImageData

	property bool isMosaic: false
	property bool mosaicing: false
	property bool processMosaic: false
	property var mosaicImageData

	function reLoadImage(image) { unloadImage(image); loadImage(image) }

	onIsBlurChanged: { if (isBlur) { reLoadImage(blurImage) } }
	onIsMosaicChanged: { if (isMosaic) { reLoadImage(mosaicImage) } }

	onImageLoaded: {
		if (isBlur) {
			bluring = true
		}
		if (isMosaic) {
			mosaicing = true
		}
			requestPaint()
	}
	onPaint: {

		var ctx = canvas.getContext("2d")
		ctx.clearRect(x, y, width, height)
		if ( processBlur || processMosaic ) {
			ctx.beginPath()
			ctx.rect(x, y, width, height)
			ctx.clip()
		}
		if(bluring || mosaicing) {
			if (bluring) {
				var imageData = ctx.createImageData(blurImage)
				imageData = CalcGraphic.gaussianBlur(imageData, 1)
				blurImageData = imageData
				bluring = false
			} else {
				var imageData = ctx.createImageData(mosaicImage)
				imageData = CalcGraphic.mosaic(imageData, 5)
				mosaicImageData = imageData
				mosaicing = false
			}
		} else {
			ctx.strokeStyle = "red"
			for (var i = 0; i < shapes.length; i++) {
				shapes[i].draw(ctx)
			}
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
	Component {
		id: ellipse_component
		EllipseCanvas {}
	}
	Component {
		id: arrow_component
		ArrowCanvas {}
	}
	Component {
		id: line_component
		LineCanvas {}
	}
	MouseArea {
		id: canvasArea
		anchors.fill: parent

		onPressed: {

			if (!canvas.clickOnPoint(Qt.point(mouse.x, mouse.y))) {
					canvas.recording = true
					if (canvas.shapeName == "rect") {
						canvas.currenRecordingShape = rect_component.createObject(canvas, {})

					}
					if (canvas.shapeName == "ellipse") {
						canvas.currenRecordingShape = ellipse_component.createObject(canvas, {})
					}
					if (canvas.shapeName == "arrow") {
						canvas.currenRecordingShape = arrow_component.createObject(canvas, {})
					}
					if (canvas.shapeName == "line") {
						canvas.currenRecordingShape = line_component.createObject(canvas, {})
					}
					canvas.currenRecordingShape.linewidth = canvas.linewidth
					canvas.currenRecordingShape.drawColor = canvas.paintColor
					canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
					canvas.shapes.push(canvas.currenRecordingShape)

			}

			canvas.requestPaint()
		}
		onReleased: {
			if (canvas.recording) {
				canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
				canvas.currenRecordingShape.firstDraw = true
				canvas.recording = false
			}

			canvas.requestPaint()

		}

		onPositionChanged: {
			if (canvas.recording) {
				canvas.currenRecordingShape.points.push(Qt.point(mouse.x, mouse.y))
			} else {
				var selectedShape = null,reSizedShape = null,rotatedShape = null
				for (var i = 0; i < canvas.shapes.length; i++) {
					if (canvas.shapes[i].reSized||drag.active)  reSizedShape = canvas.shapes[i]
					if (canvas.shapes[i].rotated||drag.active) rotatedShape = canvas.shapes[i]
					if (canvas.shapes[i].selected||drag.active)  selectedShape = canvas.shapes[i]
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
			canvas.requestPaint()
		}

	}


}