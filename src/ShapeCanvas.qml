import QtQuick 2.1

Canvas {
    id: shapeCanvas
    width: parent.width
    height: parent.height

    property bool movePaint: false
    property bool paint: false
    property string shapeName: ""
    property point startPoint: Qt.point(0, 0)
    property point endPoint: Qt.point(0, 0)
    property color colorPaint: "red"
    property var linewidth: 1
    property var points:[]

    function isEmpty() {
        if (startPoint == Qt.point(0, 0) && endPoint == Qt.point(0, 0)) {
            return true
        }
        else if (startPoint == endPoint) {
            return true
        }
        else {
            return false
        }
    }

    function _measureRect() {
        var xmin = Math.min(startPoint.x, endPoint.x) - 3
        var ymin = Math.min(startPoint.y, endPoint.y) - 4
        var xmax = Math.max(startPoint.x, endPoint.x) + 15
        var ymax = Math.max(startPoint.y, endPoint.y) + 15
        for(var i=0;i<points.length;i++) {
            xmin = Math.min(xmin, points[i].x)
            ymin = Math.min(ymin, points[i].y)
            xmax = Math.max(xmax, points[i].x)
            ymax = Math.max(ymax,points[i].y)
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
        if (shapeName == "line") {
            startPoint.x = startPoint.x - rect.x
            startPoint.y = startPoint.y - rect.y
            endPoint.x = endPoint.x - rect.x
            endPoint.y = endPoint.y - rect.y

            for(var i=0;i<points.length;i++) {
                points[i].x = points[i].x - rect.x
                points[i].y = points[i].y - rect.y
            }
        }
        else {
            startPoint.x = startPoint.x - rect.x
            startPoint.y = startPoint.y - rect.y
            endPoint.x = endPoint.x - rect.x
            endPoint.y = endPoint.y- rect.y
        }
        requestPaint()
    }

    function moveDistract(p1,p2) {
        var rect = _measureRect()
        if(p1 >= rect.x - 8*linewidth && p1 <= rect.x + 8*linewidth + rect.width
        && p2 >= rect.y - 8*linewidth && p2 <= rect.y + 8*linewidth + rect.height)
            return true
        else
            return false
    }

    onPaint: {
        if(startPoint == Qt.point(0, 0) && endPoint == Qt.point(0, 0))
        return

        onXChanged: requestPaint()
        onYChanged: requestPaint()
        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()

        var ctx = getContext("2d")
        ctx.clearRect(0, 0, width, height)
        ctx.save()
        ctx.lineWidth = shapeCanvas.linewidth
        ctx.strokeStyle =  shapeCanvas.colorPaint

        switch(shapeName)  {
            case "rect": {
                ctx.beginPath()
                ctx.rect(Math.min(startPoint.x, endPoint.x), Math.min(startPoint.y, endPoint.y), Math.abs(endPoint.x - startPoint.x), Math.abs(endPoint.y - startPoint.y))
                ctx.closePath()
                ctx.stroke()
                break
            }
            case "ellipse": {
                ctx.beginPath()
                ctx.ellipse(Math.min(startPoint.x,endPoint.x), Math.min(startPoint.y,endPoint.y), Math.abs(endPoint.x - startPoint.x), Math.abs(endPoint.y - startPoint.y))
                ctx.closePath()
                ctx.stroke()
                break
            }
            case "arrow": {
                ctx.beginPath()
                ctx.moveTo(startPoint.x, startPoint.y)
                ctx.lineTo(endPoint.x, endPoint.y)
                ctx.closePath()

                ctx.stroke()
                ctx.fillStyle = shapeCanvas.colorPaint
                ctx.beginPath()
                var angle = Math.atan2(Math.abs(endPoint.y - startPoint.y), Math.abs(endPoint.x - startPoint.x))
                var leftx, lefty, rightx, righty
                if (endPoint.x - startPoint.x > 0 && endPoint.y - startPoint.y < 0)
                {
                    leftx = endPoint.x + 15*Math.cos( Math.PI + angle - Math.PI/8)
                    lefty = endPoint.y -15*Math.sin(Math.PI + angle - Math.PI/8)
                    rightx = endPoint.x + 15*Math.cos( Math.PI + angle + Math.PI/8)
                    righty = endPoint.y - 15*Math.sin(Math.PI + angle + Math.PI/8)
                }
                else if (endPoint.x - startPoint.x <= 0 && endPoint.y - startPoint.y <= 0)
                {
                    leftx = endPoint.x - 15*Math.cos( Math.PI + angle - Math.PI/8)
                    lefty = endPoint.y -15*Math.sin(Math.PI + angle - Math.PI/8)
                    rightx = endPoint.x - 15*Math.cos( Math.PI + angle + Math.PI/8)
                    righty = endPoint.y - 15*Math.sin(Math.PI + angle + Math.PI/8)
                }
                else if (endPoint.x - startPoint.x <= 0 && endPoint.y - startPoint.y > 0)
                {
                    leftx = endPoint.x - 15*Math.cos( Math.PI + angle - Math.PI/8)
                    lefty = endPoint.y + 15*Math.sin(Math.PI + angle - Math.PI/8)
                    rightx = endPoint.x - 15*Math.cos( Math.PI + angle + Math.PI/8)
                    righty = endPoint.y + 15*Math.sin(Math.PI + angle + Math.PI/8)
                }
                else
                {
                    leftx = endPoint.x + 15*Math.cos( Math.PI + angle - Math.PI/8)
                    lefty = endPoint.y + 15*Math.sin(Math.PI + angle - Math.PI/8)
                    rightx = endPoint.x + 15*Math.cos( Math.PI + angle + Math.PI/8)
                    righty = endPoint.y + 15*Math.sin(Math.PI + angle + Math.PI/8)
                }
                ctx.moveTo(endPoint.x,endPoint.y)
                ctx.lineTo(leftx, lefty)
                ctx.lineTo( (endPoint.x + (leftx + rightx)/2)/2, (endPoint.y +(lefty + righty)/2)/2)
                ctx.lineTo(rightx,righty)
                ctx.lineTo(endPoint.x,endPoint.y)
                ctx.closePath()
                ctx.fill()
                ctx.stroke()
                ctx.fill()
                break
            }
            case "line": {
                ctx.beginPath()
                ctx.moveTo(startPoint.x, startPoint.y)
                for (var i=0;i<points.length;i++) {
                    ctx.lineTo(points[i].x, points[i].y)
                }
                ctx.lineTo(endPoint.x, endPoint.y)
                ctx.stroke()
                break
            }
        }
    ctx.restore()
    }
    Canvas {
    id: selectResizeShape
    anchors.fill: shapeCanvas
    visible: false

    property int bigPointRadius: 4
    property int smallPointRadius: 3

    x: shapeCanvas.x - bigPointRadius
    y: shapeCanvas.y - bigPointRadius
    width: shapeCanvas.width + bigPointRadius * 2
    height: shapeCanvas.height + bigPointRadius * 2

        onPaint: {
            var ctx = getContext("2d")
            ctx.save()
            ctx.clearRect(0, 0, width, height)

            ctx.lineWidth = 1
            ctx.strokeStyle = "width"
            ctx.fillStyle = "white"

            /* Top left */
            ctx.beginPath()
            ctx.arc(selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Top right */
            ctx.beginPath()
            ctx.arc(width - selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom left */
            ctx.beginPath()
            ctx.arc(selectResizeShape.bigPointRadius, height - selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom right */
            ctx.beginPath()
            ctx.arc(width - selectResizeShape.bigPointRadius, height - selectResizeShape.bigPointRadius, selectResizeShape.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Top */
            ctx.beginPath()
            ctx.arc(width / 2, selectResizeShape.bigPointRadius, selectResizeShape.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom */
            ctx.beginPath()
            ctx.arc(width / 2, height - selectResizeShape.bigPointRadius, selectResizeShape.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Left */
            ctx.beginPath()
            ctx.arc(selectResizeShape.bigPointRadius, height / 2, selectResizeShape.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Right */
            ctx.beginPath()
            ctx.arc(width - selectResizeShape.bigPointRadius, height / 2, selectResizeShape.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            ctx.restore()
        }
    }
    Rectangle {
        id:ret
        anchors.fill: parent
        color:Qt.rgba(1,0,0,0.2)
    }

    MouseArea {
        id: markPaint
        anchors.fill: parent


        onPressed: {
            if (shapeCanvas.paint)  return
            shapeCanvas.startPoint = Qt.point(mouse.x,mouse.y)

        }

        onReleased: {
            if (shapeCanvas.paint)  return
            shapeCanvas.endPoint = Qt.point(mouse.x,mouse.y)
            shapeCanvas.requestPaint()
            shapeCanvas.remap()
            shapeCanvas.paint = true

        }

        onPositionChanged: {

            if (moveDistract(mouseX,mouseY) || drag.actives) {
                shapeCanvas.movePaint = true
                selectResizeShape.visible = true
                markPaint.cursorShape = Qt.CrossCursor
            }
            else {
                shapeCanvas.movePaint = false
                selectResizeShape.visible = false
                markPaint.cursorShape = Qt.ArrowCursor
            }

            if (shapeCanvas.paint) return

            if (shapeName == "line") {
                points.push(Qt.point(mouse.x,mouse.y))
            }
            shapeCanvas.endPoint = Qt.point(mouse.x,mouse.y)
            shapeCanvas.requestPaint()
        }
        onDoubleClicked: {
            shapeCanvas.paint = false
        }

        drag.target: shapeCanvas.movePaint ? shapeCanvas : null
        drag.axis: Drag.XAndYAxis
        drag.minimumX: 0
        drag.maximumX: shapeCanvas.parent.width - shapeCanvas.width
        drag.minimumY: 0
        drag.maximumY: shapeCanvas.parent.height - shapeCanvas.height

    }

}



