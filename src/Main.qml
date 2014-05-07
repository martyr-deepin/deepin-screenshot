import QtQuick 2.1

Item {
    id: screen

    property bool firstMove: false
    property bool firstPress: false
    property bool firstRelease: false
    property bool firstEdit: false

    property alias pointColor: pointColor
    property alias pointColorRect: pointColorRect
    property alias selectArea: selectArea
    property alias selectResizeCanvas: selectResizeCanvas
    property alias zoomIndicator: zoomIndicator
    property alias selectSizeTooltip: selectSizeTooltip
    property alias toolbar: toolbar
    
    MouseArea {
        id: screenArea
        anchors.fill: parent
        hoverEnabled: true

        property int pressX: 0
        property int pressY: 0

        onPressed: {
            var pos = windowView.get_cursor_pos()
            pressX = pos.x
            pressY = pos.y

            if (!firstPress) {
                firstPress = true
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectArea.handlePress(pos)
                }
            }
        }

        onReleased: {
            var pos = windowView.get_cursor_pos()
            
            if (!firstRelease) {
                firstRelease = true
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectArea.handleRelease(pos)
                }
            }
        }

        onPositionChanged: {
            var pos = windowView.get_cursor_pos()

            if (!firstMove) {
                firstMove = true
            }

            if (!firstPress) {
                var window_info = windowView.get_window_info_at_pointer()
                if (window_info != undefined) {
                    selectArea.x = window_info[0]
                    selectArea.y = window_info[1]
                    selectArea.width = window_info[2]
                    selectArea.height = window_info[3]
                }
            }

            if (firstPress) {
                if (!firstRelease) {
                    if (pos.x != screenArea.pressX && pos.y != screenArea.pressY) {
                        selectArea.x = Math.min(pos.x, screenArea.pressX)
                        selectArea.y = Math.min(pos.y, screenArea.pressY)
                        selectArea.width = Math.abs(pos.x - screenArea.pressX)
                        selectArea.height = Math.abs(pos.y - screenArea.pressY)
                    }
                }
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectArea.handlePositionChange(pos)
                }
            }

            if (firstMove && !firstRelease) {
                zoomIndicator.updatePosition(pos)
                
                var rgb = windowView.get_color_at_point(pos.x, pos.y)
                pointColor.text = "[" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + "]"
                pointColorRect.color = Qt.rgba(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1)
            }
        }
    }

    Image {
        id: background
        anchors.fill: parent
        source: "/tmp/deepin-screenshot.png"
    }

    Rectangle {
        anchors.fill: screen
        color: "black"
        opacity: 0.5
    }

    Rectangle {
        id: selectArea
        clip: true
        visible: firstMove

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
                    
                    screenArea.cursorShape = Qt.ClosedHandCursor
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
                        screenArea.cursorShape = Qt.OpenHandCursor
                        
                        selectResizeCanvas.visible = false
                    } else if (x + dndSize >= pos.x) {
                        if (y + dndSize >= pos.y) {
                            screenArea.cursorShape = Qt.SizeFDiagCursor
                        } else if (y + height - dndSize <= pos.y) {
                            screenArea.cursorShape = Qt.SizeBDiagCursor
                        } else {
                            screenArea.cursorShape = Qt.SizeHorCursor
                        }
                        
                        selectResizeCanvas.visible = true
                    } else if (x + width - dndSize <= pos.x) {
                        if (y + dndSize >= pos.y) {
                            screenArea.cursorShape = Qt.SizeBDiagCursor
                        } else if (y + height - dndSize <= pos.y) {
                            screenArea.cursorShape = Qt.SizeFDiagCursor
                        } else {
                            screenArea.cursorShape = Qt.SizeHorCursor
                        }
                        
                        selectResizeCanvas.visible = true
                    } else {
                        screenArea.cursorShape = Qt.SizeVerCursor
                        
                        selectResizeCanvas.visible = true
                    }
                } else {
                    screenArea.cursorShape = Qt.ArrowCursor
                    
                    selectResizeCanvas.visible = false
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
                        screenArea.cursorShape = Qt.OpenHandCursor
                    }
                }                
            }
        }

        Image {
            x: -selectArea.x
            y: -selectArea.y
            source: "/tmp/deepin-screenshot.png"
        }
    }
    
    Rectangle {
        id: selectFrame
        anchors.fill: selectArea
        color: "transparent"
        border.color: "#00A0E9"
        border.width: 1
        visible: firstMove
    }

    Canvas {
        id: selectResizeCanvas
        visible: false

        property int bigPointRadius: 4
        property int smallPointRadius: 3
        
        x: selectArea.x - bigPointRadius
        y: selectArea.y - bigPointRadius
        width: selectArea.width + bigPointRadius * 2
        height: selectArea.height + bigPointRadius * 2
        
        onXChanged: requestPaint()
        onYChanged: requestPaint()
        onWidthChanged: requestPaint()
        onHeightChanged: requestPaint()
        
        onPaint: {
            var ctx = getContext("2d")
            ctx.save()
            ctx.clearRect(0, 0, width, height)
            
            ctx.lineWidth = 1
            ctx.strokeStyle = "#00A0E9"
            ctx.fillStyle = "white"
            
            /* Top left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            
            /* Top right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            
            /* Bottom right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            
            /* Top */
            ctx.beginPath()
            ctx.arc(width / 2, selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom */
            ctx.beginPath()
            ctx.arc(width / 2, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            
            /* Left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            ctx.restore()
        }
    }

    Rectangle {
        id: selectSizeTooltip
        x: Math.min(screenWidth - width - padding, selectFrame.x + padding)
        y: selectFrame.y < height * 1.5 ? selectFrame.y + padding : selectFrame.y - height - padding
        color: "black"
        opacity: 0.7
        width: 100
        height: 32
        radius: 3
        visible: firstMove

        property int padding: 4

        Text {
            id: selectSizeTooltipText
            anchors.centerIn: parent
            color: "white"
            text: selectArea.width + "x" + selectArea.height
        }
    }

    Rectangle {
        id: toolbar
        x: Math.max(selectFrame.x + selectFrame.width - width - padding, padding)
        y: selectFrame.y + selectFrame.height > screen.height - height * 2 ? (selectFrame.y < height * 1.5 ? selectFrame.y + padding : selectFrame.y - height - padding) : selectFrame.y + selectFrame.height + padding
        width: 315
        height: 32
        
        radius: 3
        
        property color stop1Color: Qt.rgba(0, 0, 0, 0.6)
        property color stop2Color: Qt.rgba(0, 0, 0, 0.675)
        property color stop3Color: Qt.rgba(0, 0, 0, 0.676)
        property color stop4Color: Qt.rgba(0, 0, 0, 0.677)
        property color stop5Color: Qt.rgba(0, 0, 0, 0.678)
        property color stop6Color: Qt.rgba(0, 0, 0, 0.75)
        
        gradient: Gradient {
            GradientStop {id: stop1; position: 0.0; color: toolbar.stop1Color}
            GradientStop {id: stop2; position: 0.5; color: toolbar.stop2Color}
            GradientStop {id: stop3; position: 0.51; color: toolbar.stop3Color}
            GradientStop {id: stop4; position: 0.5100001; color: toolbar.stop4Color}
            GradientStop {id: stop5; position: 0.52; color: toolbar.stop5Color}
            GradientStop {id: stop6; position: 1.0; color: toolbar.stop6Color}
        }
        
        border.color:  Qt.rgba(1, 1, 1, 0.2)
        
        visible: firstMove && firstRelease

        property int padding: 4
        
        function tryHideSizeTooltip() {
            if (firstMove && firstRelease) {
                if (x <= selectSizeTooltip.x + selectSizeTooltip.width && selectSizeTooltip.y <= y && y <= selectSizeTooltip.y + selectSizeTooltip.height) {
                    selectSizeTooltip.visible = false
                } else {
                    selectSizeTooltip.visible = true
                }
            }
        }
        
        function expandToolbar() {
            toolbar.height = 64
            toolbar.stop1Color = Qt.rgba(0, 0, 0, 0.6)
            toolbar.stop2Color = Qt.rgba(0, 0, 0, 0.75)
            toolbar.stop3Color = Qt.rgba(1, 1, 1, 0.1)
            toolbar.stop4Color = Qt.rgba(1, 1, 1, 0.1)
            toolbar.stop5Color = Qt.rgba(0.1, 0.1, 0.1, 0.8)
            toolbar.stop6Color = Qt.rgba(0.1, 0.1, 0.1, 0.8)
        }
        
        function shrinkToolbar() {
            toolbar.height = 32
            toolbar.stop1Color = Qt.rgba(0, 0, 0, 0.6)
            toolbar.stop2Color = Qt.rgba(0, 0, 0, 0.675)
            toolbar.stop3Color = Qt.rgba(0, 0, 0, 0.676)
            toolbar.stop4Color = Qt.rgba(0, 0, 0, 0.677)
            toolbar.stop5Color = Qt.rgba(0, 0, 0, 0.677)
            toolbar.stop6Color = Qt.rgba(0, 0, 0, 0.75)
        }

        onXChanged: {
            tryHideSizeTooltip()
        }

        onYChanged: {
            tryHideSizeTooltip()
        }
        
        Row {
            anchors.left: parent.left
            anchors.leftMargin: 8
            
            ToolButton {
                imageName: "rect"
            }
            
            ToolButton {
                imageName: "ellipse"
            }
            
            ToolButton {
                imageName: "arrow"
            }
            
            ToolButton {
                imageName: "line"
            }
            
            ToolButton {
                imageName: "text"
            }
        }
        
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 8
            
            ToolButton {
                imageName: "color"
            }
            
            ToolButton {
                imageName: "undo"
            }
            
            SaveButton {
            }
            
            ToolButton {
                imageName: "share"
            }            
        }
    }

    Rectangle {
        id: zoomIndicator
        visible: firstMove && !firstRelease

        width: 130
        height: 130
        color: "black"
        opacity: 0.7

        property int cursorWidth: 8
        property int cursorHeight: 18

        property int cursorX: 0
        property int cursorY: 0

        function updatePosition(pos) {
            cursorX = pos.x
            cursorY = pos.y

            x = pos.x + width + cursorWidth > screenWidth ? pos.x - width : pos.x + cursorWidth
            y = pos.y + height + cursorHeight > screenHeight ? pos.y - height : pos.y + cursorHeight
        }

        
    }
    
    Item {
        anchors.fill: zoomIndicator
        visible: zoomIndicator.visible
        
        Column {
            id: zoomIndicatorTooltip

            anchors.fill: parent
            anchors.margins: marginValue

            property int marginValue: 3

            Rectangle {
                width: parent.width
                height: 68

                Rectangle {
                    id: zoomIndicatorClip
                    clip: true
                    height: parent.height / zoomIndicatorClip.scaleValue
                    width: parent.width / zoomIndicatorClip.scaleValue
                    
                    property int scaleValue: 4

                    transform: Scale {
                        xScale: zoomIndicatorClip.scaleValue
                        yScale: zoomIndicatorClip.scaleValue
                    }

                    Image {
                        id: zoomIndicatorImage
                        x: -zoomIndicator.cursorX + (zoomIndicator.width - zoomIndicatorTooltip.marginValue) / (2 * zoomIndicatorClip.scaleValue) 
                        y: -zoomIndicator.cursorY + parent.height / 2
                        source: "/tmp/deepin-screenshot.png"
                        smooth: false
                    }
                }
                
                Rectangle {
                    color: "black"
                    opacity: 0.5
                    height: 1
                    width: parent.width
                    x: parent.x
                    y: parent.y + parent.height / 2
                }
                Rectangle {
                    color: "white"
                    opacity: 0.5
                    height: 1
                    width: parent.width
                    x: parent.x
                    y: parent.y + parent.height / 2 + 1
                }
                
                Rectangle {
                    color: "black"
                    opacity: 0.5
                    width: 1
                    height: parent.height
                    x: parent.x + parent.width / 2
                    y: parent.y
                }
                Rectangle {
                    color: "white"
                    opacity: 0.5
                    width: 1
                    height: parent.height
                    x: parent.x + parent.width / 2 + 1
                    y: parent.y
                }
            }


            Text {
                text: "(" + zoomIndicator.cursorX + ", " + zoomIndicator.cursorY + ")"
                color: "white"
            }

            Text {
                id: pointColor
                color: "white"
                width: parent.width
                
                Rectangle {
                    width: 12
                    height: width
                    x: parent.width - width
                    y: (parent.height - height) / 2
                    color: "grey"
                    
                    Rectangle {
                        id: pointColorRect
                        anchors.fill: parent
                        anchors.margins: 1
                    }
                }
            }
            
            Text {
                text: "拖动可自由选区"
                color: "white"
            }
        }
    }
    
    focus: true
    Keys.onEscapePressed: {
        windowView.close()
    }
}
