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


    function bigDistract(p1, p2) {
        if( p1 >= Math.min(startPoint.x, endPoint.x) - 4*linewidth && p1 <= Math.max(startPoint.x, endPoint.x) + 4*linewidth
        && p2 >= Math.min(startPoint.y, endPoint.y) - 4*linewidth && p2 <= Math.max(startPoint.y, endPoint.y) + 4*linewidth )
                return true

        else
            return false
    }
    function smallDistract(p1, p2) {
        if( p1 >= Math.min(startPoint.x, endPoint.x) + 4*linewidth && p1 <= Math.max(startPoint.x, endPoint.x) - 4*linewidth
        && p2 >= Math.min(startPoint.y, endPoint.y) + 4*linewidth && p2 <= Math.max(startPoint.y, endPoint.y) - 4*linewidth )
            return true

        else
            return false
    }

    function moveDistract(p1,p2) {
        if(bigDistract(p1, p2) && !smallDistract(p1, p2))
            return true
        else
            return false
    }

    onPaint: {
        if(startPoint == Qt.point(0, 0) && endPoint == Qt.point(0, 0))
        return
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
            // var shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas { shapeName:shapeCanvas.shapeName }', shapeCanvas.parent, "shaperect")
            // shape.movePaint = Qt.binding(function () {  return shapeCanvas.movePaint })
            // shape.colorPaint = Qt.binding(function() { return shapeCanvas.colorPaint})
            // shape.linewidth = Qt.binding(function() { return shapeCanvas.linewidth})
        }

        onPositionChanged: {
            if (moveDistract(mouseX,mouseY))
                shapeCanvas.movePaint = true
            else
            shapeCanvas.movePaint = false
            if (shapeCanvas.paint) return

            if (shapeName == "line") {
                points.push(Qt.point(mouse.x,mouse.y))
            }
            shapeCanvas.endPoint = Qt.point(mouse.x,mouse.y)
            shapeCanvas.requestPaint()
        }

        drag.target: shapeCanvas.movePaint ? shapeCanvas : null
        drag.axis: Drag.XAndYAxis
        drag.minimumX: 0
        drag.maximumX: shapeCanvas.parent.width - shapeCanvas.width
        drag.minimumY: 0
        drag.maximumY: shapeCanvas.parent.height - shapeCanvas.height

    }

}

