import QtQuick 2.1

Item {
    id: shapeItem

    width: parent.width
    height: parent.height
    property bool firstMove: false
    property bool firstPress: false
    property bool firstRelease: false
    property bool firstEdit: false

    property alias selectshape: selectshape
    property alias selectResizeShape: selectResizeShape

    property string shapeName: ""
    property int linewidth: 1
    property string colorPaint: "red"

    property point startPoint: Qt.point(0, 0)
    property point endPoint: Qt.point(0, 0)

    function _calculateRect() {
        var x = selectshape.x - selectResizeShape.bigPointRadius / 2
        var y = selectshape.y - selectResizeShape.bigPointRadius / 2
        var width = selectshape.width + selectResizeShape.bigPointRadius
        var height = selectshape.height + selectResizeShape.bigPointRadius

        return Qt.rect(x, y, width, height)
    }
    function remap() {

        var rect =  _calculateRect()
        shapeItem.x = rect.x
        shapeItem.y = rect.y
        shapeItem.width = rect.width
        shapeItem.height = rect.height


    }

    MouseArea {
        id: shapeArea
        anchors.fill: parent

        property int pressX: 0
        property int pressY: 0

        onPressed: {
            shapeItem.startPoint = Qt.point(mouse.x, mouse.y)
            pressX = shapeItem.startPoint.x
            pressY = shapeItem.startPoint.y

            if (!firstPress) {
                firstPress = true
                hoverEnabled = true
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectshape.handlePress(shapeItem.startPoint)
                }
            }
        }
        onReleased: {
            shapeItem.endPoint = Qt.point(mouse.x,mouse.y)

            if (!firstRelease) {
                firstRelease = true
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectshape.handleRelease(shapeItem.endPoint)

                    shapeItem.remap()
                    // var shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas { shapeName: toolbar.paintShape }', shapeItem.parent, "shaperect")
                    // shape.colorPaint = Qt.binding(function() { return colorTool.colorStyle })
                    // shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                }
            }
        }
        onPositionChanged: {
            shapeItem.endPoint = Qt.point(mouse.x,mouse.y)

            if (!firstMove) {
                firstMove = true
            }

            if (!firstPress) {
                var window_info = windowView.get_window_info_at_pointer()
                if (window_info != undefined) {
                    selectshape.x = window_info[0]
                    selectshape.y = window_info[1]
                    selectshape.width = window_info[2]
                    selectshape.height = window_info[3]
                }
            }

            if (firstPress) {
                if (!firstRelease) {
                    if (shapeItem.endPoint.x != shapeArea.pressX && shapeItem.endPoint.y != shapeArea.pressY) {
                        selectshape.x = Math.min(shapeItem.endPoint.x, shapeArea.pressX)
                        selectshape.y = Math.min(shapeItem.endPoint.y, shapeArea.pressY)
                        selectshape.width = Math.abs(shapeItem.endPoint.x - shapeArea.pressX)
                        selectshape.height = Math.abs(shapeItem.endPoint.y - shapeArea.pressY)
                    }
                }
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectshape.handlePositionChange(shapeItem.endPoint)
                }
            }
        }
    }

    Rectangle {
        id: selectshape
        clip: true
        visible: false
        property int startX: 0
        property int startY: 0
        property int startWidth: 0
        property int startHeight: 0
        property int pressX: 0
        property int pressY: 0
        property int dndSize: 5
        property int minSize: 10
        property bool hasPress: false
        property bool pressAtCenter: false
        property bool pressAtLeft: false
        property bool pressAtRight: false
        property bool pressAtTop: false
        property bool pressAtBottom: false
        property bool pressAtTopLeft: false
        property bool pressAtTopRight: false
        property bool pressAtBottomLeft: false
        property bool pressAtBottomRight: false
        border.width: 4
        border.color: "red"
        function handlePress(pos) {
            if (x <= pos.x && pos.x <= x + width && y <= pos.y && pos.y <= y + height) {
                hasPress = true
                startX = x
                startY = y
                startWidth = width
                startHeight = height
                pressX = pos.x
                pressY = pos.y

                if (x + dndSize < pos.x && pos.x < x + width - dndSize && y + dndSize < pos.y && pos.y < y + height - dndSize) {
                    pressAtCenter = true
                } else if (x + dndSize >= pos.x) {
                    if (y + dndSize >= pos.y) {
                        pressAtTopLeft = true
                    } else if (y + height - dndSize <= pos.y) {
                        pressAtBottomLeft = true
                    } else {
                      pressAtLeft = true
                    }
                } else if (x + width - dndSize <= pos.x) {
                    if (y + dndSize >= pos.y) {
                        pressAtTopRight = true
                    } else if (y + height - dndSize <= pos.y) {
                        pressAtBottomRight = true
                    } else {
                      pressAtRight = true
                    }
                } else if (y + dndSize >= pos.y) {
                    pressAtTop = true
                } else if (y + height - dndSize <= pos.y) {
                    pressAtBottom = true
                }
            }
        }

        function handlePositionChange(pos) {
            if (hasPress) {
                if (pressAtCenter) {
                    x = Math.max(Math.min(startX + pos.x - pressX, screenWidth - width), 0)
                    y = Math.max(Math.min(startY + pos.y - pressY, screenHeight - height), 0)

                    shapeArea.cursorShape = Qt.ClosedHandCursor
                } else {
                    if (pressAtLeft || pressAtTopLeft || pressAtBottomLeft) {
                        x = Math.min(pos.x, startX + startWidth - minSize)
                         width = Math.max(startWidth + startX - pos.x, minSize)
                    }

                    if (pressAtRight || pressAtTopRight || pressAtBottomRight) {
                        width = Math.max(pos.x - startX, minSize)
                        x = Math.max(pos.x - width, startX)
                    }

                    if (pressAtTop || pressAtTopLeft || pressAtTopRight) {
                        y = Math.min(pos.y, startY + startHeight - minSize)
                        height = Math.max(startHeight + startY - pos.y, minSize)
                    }

                    if (pressAtBottom || pressAtBottomLeft || pressAtBottomRight) {
                        height = Math.max(pos.y - startY, minSize)
                        y = Math.max(pos.y - height, startY)
                    }
                }
            } else {
                if (x <= pos.x && pos.x <= x + width && y <= pos.y && pos.y <= y + height) {
                    if (x + dndSize < pos.x && pos.x < x + width - dndSize && y + dndSize < pos.y && pos.y < y + height - dndSize) {
                        shapeArea.cursorShape = Qt.OpenHandCursor
                        selectResizeShape.visible = false
                } else if (x + dndSize >= pos.x) {
                    if (y + dndSize >= pos.y) {
                        shapeArea.cursorShape = Qt.SizeFDiagCursor
                    } else if (y + height - dndSize <= pos.y) {
                        shapeArea.cursorShape = Qt.SizeBDiagCursor
                    } else {
                        shapeArea.cursorShape = Qt.SizeHorCursor
                    }

                    selectResizeShape.visible = true
                } else if (x + width - dndSize <= pos.x) {
                    if (y + dndSize >= pos.y) {
                        shapeArea.cursorShape = Qt.SizeBDiagCursor
                    } else if (y + height - dndSize <= pos.y) {
                        shapeArea.cursorShape = Qt.SizeFDiagCursor
                    } else {
                        shapeArea.cursorShape = Qt.SizeHorCursor
                    }

                        selectResizeShape.visible = true
                    } else {
                        shapeArea.cursorShape = Qt.SizeVerCursor
                        selectResizeShape.visible = true
                    }
                } else {
                    shapeArea.cursorShape = Qt.ArrowCursor
                    selectResizeShape.visible = false
                }
            }
        }
        function handleRelease(pos) {
            if (hasPress) {
                hasPress = false
                pressAtCenter = false
                pressAtLeft = false
                pressAtRight = false
                pressAtTop = false
                pressAtBottom = false
                pressAtTopLeft = false
                pressAtTopRight = false
                pressAtBottomLeft = false
                pressAtBottomRight = false
                startX = 0
                startY = 0
                startWidth = 0
                startHeight = 0
                pressX = 0
                pressY = 0

                if (x <= pos.x && pos.x <= x + width && y <= pos.y && pos.y <= y + height) {
                    if (x + dndSize < pos.x && pos.x < x + width - dndSize && y + dndSize < pos.y && pos.y < y + height - dndSize) {
                        shapeArea.cursorShape = Qt.OpenHandCursor
                    }
                }
            }
        }
    }
    Canvas {
        id: shapeCanvas
        x: selectshape.x
        y: selectshape.y
        width: selectshape.width
        height: selectshape.height
        visible: true
        onXChanged: requestPaint()
        onYChanged: requestPaint()
        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()

        onPaint: {
            var ctx = getContext("2d")
            ctx.save()
            ctx.clearRect(0, 0, width, height)

            ctx.lineWidth = shapeItem.linewidth
            ctx.strokeStyle = shapeItem.colorPaint
            ctx.fillStyle = "transparent"

            switch(shapeItem.shapeName) {
                case "rect": {
                   ctx.beginPath()
                   //ctx.rect(shapeItem.startPoint.x, shapeItem.startPoint.y, shapeItem.endPoint.x - shapeItem.startPoint.x, shapeItem.endPoint.y - shapeItem.startPoint.y)
                   ctx.rect(0, 0, width, height)
                   ctx.closePath()
                   ctx.fill()
                   ctx.stroke()
                    break
                }
                case "ellipse": {
                    ctx.beginPath()
                    ctx.ellipse(0,0, width, height)
                    ctx.closePath()
                    ctx.fill()
                    ctx.stroke()
                    break
                }
                case "arrow": {
                    break
                }
                case "line": {
                    break
                }

            }
        ctx.restore()
        }
    }
    Canvas  {
        id: selectResizeShape
        visible: false

        property int bigPointRadius: 4
        property int smallPointRadius: 3

        x: selectshape.x - bigPointRadius
        y: selectshape.y - bigPointRadius
        width: selectshape.width + bigPointRadius * 2
        height: selectshape.height + bigPointRadius * 2

        onXChanged: requestPaint()
        onYChanged: requestPaint()
        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()

        onPaint: {
            var ctx = getContext("2d")
            ctx.save()
            ctx.clearRect(0, 0, width, height)

            ctx.lineWidth = 1
            //ctx.strokeStyle = "#00A0E9"
            ctx.strokeStyle = "yellow"
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




}
