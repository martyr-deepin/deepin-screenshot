import QtQuick 2.1
import QtMultimedia 5.0
import QtGraphicalEffects 1.0

Item {
    id: screen
    property bool firstMove: false
    property bool firstPress: false
    property bool firstRelease: false
    property bool firstEdit: false

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
        cursorShape: windowView.set_cursor_shape("../image/mouse_style/shape/start_cursor.png", -1, -1)

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
                screenArea.cursorShape = Qt.ArrowCursor
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectArea.handleRelease(pos)
                }
            }
            if (selectArea.x == 0 && selectArea.y == 0 && selectArea.width == screenWidth - 1 && selectArea.height == screenHeight - 1) {
                selectSizeTooltip.visible = false
                toolbar.visible = false
            } else {
                selectSizeTooltip.visible = true
                toolbar.visible = true
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
                pointColorRect.color = Qt.rgba(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, 1)
            }
        }
        onDoubleClicked: {
            save_toolbar.saveId = "auto_save"
            toolbar.visible = false
            selectSizeTooltip.visible = false
            windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2,selectFrame.height - 2)
            count.running = true
            cameraSound.play()
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
        visible: true
        opacity: 0.8
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
        clip: true
        anchors.fill: selectArea
        color: "transparent"
        border.color: "#01bdff"
        border.width: 1
        visible: firstMove
    }
    Item {
        id: blurItem
        anchors.fill: selectFrame
    }
    Canvas  {
        id: selectResizeCanvas
        visible: false

        property int bigPointRadius: 4
        property int smallPointRadius: 3
        property string system: system
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
            ctx.strokeStyle = "white"
            ctx.fillStyle = "white"

            /* Top left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Top right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Top */
            ctx.beginPath()
            ctx.arc(width / 2, selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Bottom */
            ctx.beginPath()
            ctx.arc(width / 2, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Left */
            ctx.beginPath()
            ctx.arc(selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()

            /* Right */
            ctx.beginPath()
            ctx.arc(width - selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius, 0, Math.PI * 2, false)
            ctx.shadowOffsetY = 1
            ctx.shadowBlur = 2
            ctx.shadowColor = Qt.rgba(0, 0, 0, 0.2)
            ctx.closePath()
            ctx.fill()
            ctx.stroke()
            ctx.restore()
            windowView.save_overload("system", selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2, selectFrame.height - 2)
        }
    }

    Rectangle {
        id: selectSizeTooltip
        x: Math.min(screenWidth - width - padding, selectFrame.x + padding)
        y: selectFrame.y < height * 1.5 ? selectFrame.y + padding : selectFrame.y - height - padding
        width: 100
        height: 32

        color: Qt.rgba(0, 0, 0, 0.5)
        radius: 3
        visible: firstMove
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.2)
        property int padding: 4

        Text {
            id: selectSizeTooltipText
            anchors.centerIn: parent
            color: "white"
            text: selectArea.width + "x" + selectArea.height
            font.pixelSize: 12
        }
    }

    Rectangle {
        id: toolbar
        x: Math.max(selectFrame.x + selectFrame.width - width - padding, padding)
        y: selectFrame.y + selectFrame.height > screen.height - height * 2 ? (selectFrame.y < height * 1.5 ? selectFrame.y + padding : selectFrame.y - height - padding) : selectFrame.y + selectFrame.height + padding
        width: 288
        height: 28

        radius: 4

        property bool bExtense: height == 56
        property bool hasShapeCanvas: false
        property bool hasMosaicCanvas: false
        property bool hasBlurCanvas: false

        property var shape
        property var linewidth: ""

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
        property string buttonType: ""

        function tryHideSizeTooltip() {
            if (firstMove && firstRelease) {
                if (x <= selectSizeTooltip.x + selectSizeTooltip.width && selectSizeTooltip.y <= y && y <= selectSizeTooltip.y + selectSizeTooltip.height) {
                    selectSizeTooltip.visible = false
                    } else {
                        selectSizeTooltip.visible = true
                    }
                }
            }

        function toggleToolbar(type) {
            if (toolbar.buttonType != type) {
                toolbar.expandToolbar()
                toolbar.buttonType = type
            } else {
                    toolbar.shrinkToolbar()
                    toolbar.buttonType = ""
            }
        }

        function expandToolbar() {
            toolbar.height = 56
            toolbar.stop1Color = Qt.rgba(0, 0, 0, 0.6)
            toolbar.stop2Color = Qt.rgba(0, 0, 0, 0.75)
            toolbar.stop3Color = Qt.rgba(1, 1, 1, 0.5)
            toolbar.stop4Color = Qt.rgba(1, 1, 1, 0.5)
            toolbar.stop5Color = Qt.rgba(0, 0, 0, 0.75)
            toolbar.stop6Color = Qt.rgba(0, 0, 0, 0.6)
        }

        function shrinkToolbar() {
            toolbar.height = 28
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
            id: row
            anchors.left: savetooltip.visible ? savetooltip.right:parent.left
            anchors.leftMargin: 4

            function checkState(id) {
                for (var i=0; i<row.children.length; i++) {
                    var childButton = row.children[i]
                    if (childButton.imageName != id.imageName) {
                        childButton.state = "off"
                    }
                }
            }

            function _destroyCanvas() {
                var theTopChild = selectArea.children[selectArea.children.length - 1]

                if (theTopChild != undefined && theTopChild.firstPress ) {

                    theTopChild.destroy()
                }
            }

            ToolButton {
                id:button1
                group: row
                imageName: "rect"
                visible: ((button1.width + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                onPressed:
                {
                    screenArea.enabled = false
                    toolbar.toggleToolbar("rect")

                    if (toolbar.bExtense) {
                        blurType.visible = true
                        mosaicType.visible = true
                        setlw.visible = true
                        dividingLine.visible = true
                        colorChange.visible = false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        colorChange.visible = false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    }

                    if (!toolbar.hasShapeCanvas) {
                        toolbar.shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas {}', selectArea, "shaperect")
                        toolbar.hasShapeCanvas = true
                    }
                    toolbar.shape.shapeName = "rect"
                    toolbar.shape.isBlur = false
                    toolbar.shape.isMosaic = false
                    toolbar.shape.processBlur = false
                    toolbar.shape.processMosaic = false
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorStyle })

                }
            }
            ToolButton {
                id:button2
                group: row
                imageName: "ellipse"
                visible: ((button1.width*2 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true

                onPressed: {
                    screenArea.enabled = false
                    toolbar.toggleToolbar("ellipse")
                    if (toolbar.bExtense) {
                        blurType.visible = true
                        mosaicType.visible = true
                        setlw.visible = true
                        dividingLine.visible = true
                        colorChange.visible= false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        colorChange.visible= false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    }
                    if (!toolbar.hasShapeCanvas) {
                        toolbar.shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas {}', selectArea, "shaperect")
                        toolbar.hasShapeCanvas = true
                    }
                    toolbar.shape.shapeName = "ellipse"
                    toolbar.shape.isBlur = false
                    toolbar.shape.isMosaic = false
                    toolbar.shape.processBlur = false
                    toolbar.shape.processMosaic = false
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorStyle })
                }
            }

            ToolButton {
                id:button3
                group: row
                imageName: "arrow"
                visible: ((button1.width*3 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                onPressed: {
                    screenArea.enabled = false
                    toolbar.toggleToolbar("arrow")
                    if (toolbar.bExtense) {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = true
                        dividingLine.visible = false
                        colorChange.visible = false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        setlw.visible = false
                    }
                    if (!toolbar.hasShapeCanvas) {
                        toolbar.shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas {}', selectArea, "shaperect")
                        toolbar.hasShapeCanvas = true
                    }
                    toolbar.shape.shapeName = "arrow"
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorStyle })
                }
            }

            ToolButton {
                id:button4
                group:row
                imageName: "line"
                visible: ((button1.width*4 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                onPressed: {
                    screenArea.enabled = false
                    toolbar.toggleToolbar("line")
                    if (toolbar.bExtense) {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = true
                        dividingLine.visible = false
                        colorChange.visible= false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        dividingLine.visible = false
                    }
                    if (!toolbar.hasShapeCanvas) {
                        toolbar.shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas {}', selectArea, "shaperect")
                        toolbar.hasShapeCanvas = true
                    }
                    toolbar.shape.shapeName = "line"
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorStyle })
                }
            }
            ToolButton {
                group:row
                id:button5
                imageName: "text"
                visible: ((button1.width*5 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                onPressed: {
                    screenArea.enabled = false
                    toolbar.toggleToolbar("text")
                    if (toolbar.bExtense) {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        colorChange.visible= false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                    }
                     if (!toolbar.hasShapeCanvas) {
                        toolbar.shape = Qt.createQmlObject('import QtQuick 2.1; ShapeCanvas {}', selectArea, "shaperect")
                        toolbar.hasShapeCanvas = true
                    }
                    toolbar.shape.shapeName = "text"

                    toolbar.shape.fontSize = Qt.binding( function() { return fontRect.fontText.font_size})
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorStyle })
                    fontRect.visible = fontRect.visible == false ? true : false
                    if (fontRect.visible) {
                        setlw.visible = false
                        colorChange.visible = false
                        save_toolbar.visible = false
                    }
                }
            }
            function _ColorXLineXText() {
                if (setlw.visible) {
                    fontRect.visible = false
                    colorChange.visible = false
                }
                else if(colorChange.visible) {
                    fontRect.visible = false
                    setlw.visible = false
                }
                else if(fontRect.visible) {
                    colorChange.visible = false
                    setlw.visible = false
                }
            }
            BigColor {
                id: colorTool
                colorStyle: "#FF1C49"

                visible: ((button1.width*6 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true

                onPressed: {
                    toolbar.toggleToolbar("color")
                    fontRect.visible = false

                    colorChange.visible = colorChange.visible == false ? true : false
                    if (colorChange.visible) {
                        setlw.visible = false
                        blurType.visible = false
                        mosaicType.visible = false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    }
                }
            }
            SaveButton {
                id: saveButton
                visible: ((button1.width*7 +10 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true

                onSaveIcon: {
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2, selectFrame.height - 2)
                    windowView.close()
                }
                onListIcon: {
                    save_toolbar.visible = save_toolbar.visible == false ? true : false
                    if (save_toolbar.visible) {
                        setlw.visible = false
                        blurType.visible = false
                        mosaicType.visible = false
                        colorChange.visible = false
                        fontRect.visible = false
                    }
                    toolbar.toggleToolbar("saveAction")
                }
            }
            ToolButton {
                visible: !savetooltip.visible
                imageName: "share"
            }
            ToolButton {
                visible: !savetooltip.visible
                imageName: "cancel"
                onPressed: {
                    windowView.close()
                }
            }
        }

        Rectangle {
            id: fontRect
            anchors.left: row.left
            anchors.leftMargin: 4
            anchors.top: row.bottom
            anchors.topMargin: 4
            width: 80
            height: 18

            radius: 4
            opacity: 0.2
            color: "transparent"

            border.width:1
            border.color: "white"
            visible: false
            property alias fontText: fontText
            TextInput {
                id:fontText
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.top: parent.top
                anchors.topMargin: 3
                width: parent.width / 2 - 10
                height: parent.height
                property int font_size: 12
                text: font_size
                font.pixelSize: 12
                color: "white"
            }

            Rectangle {
                id:fontSizeAdd
                width: 20
                height: 18
                anchors.left: fontText.right
                color: "transparent"
                border.width: 1
                border.color: Qt.rgba(1,1,1,0.2)
                TextInput {
                    id: addFontSize
                    anchors.left: parent.left
                    anchors.leftMargin: 5
                    text: "+"
                    color: "white"
                    readOnly: true
                    MouseArea {
                        anchors.fill: parent
                        onPressed: {
                            if (fontText.font_size >=72) {
                                return
                            } else {
                                fontText.font_size = fontText.font_size + 1
                            }
                        }
                    }
                }

            }
            Rectangle {
                id: fontSizeMinux
                width: 20
                height: 18
                anchors.left: fontSizeAdd.right
                color: "transparent"
                TextInput {
                    id: minusFontSize
                    anchors.left: parent.left
                    anchors.leftMargin: 5
                    text: "-"
                    color: "white"
                    readOnly: true
                    MouseArea {
                        anchors.fill: parent
                        onPressed: {
                            if (fontText.font_size <= 8) {
                                return
                            } else {
                                fontText.font_size = fontText.font_size - 1
                            }
                        }
                    }
                }
            }
        }
        Rectangle {
            id: colorChange
            anchors.left: row.left
            anchors.leftMargin: 4
            anchors.top: row.bottom
            anchors.topMargin: 6
            color:"black"

            visible: false
            Row {
                id:colorGrid
                spacing: 5
                ColorButton{
                    id: black
                    colorStyle: "#FFD903"
                }
                ColorButton{
                    id: gray_dark
                    colorStyle: "#FF5E1A"
                }
                ColorButton{
                    id: red
                    colorStyle: "#FF3305"
                }
                ColorButton{
                    id: yellow_dark
                    colorStyle:"#FF1C49"
                }
                ColorButton{
                    id: yellow
                    colorStyle: "#FB00FF"
                }
                ColorButton{
                    id: green
                    colorStyle: "#7700ED"
                }
                ColorButton{
                    id: green_dark
                    colorStyle: "#3D08FF"
                }
                ColorButton{
                    id: wathet_dark
                    colorStyle: "#3468FF"
                }
                ColorButton{
                    id: white
                    colorStyle: "#00AAFF"
                }

                ColorButton{
                    id: gray
                    colorStyle: "#08FF77"
                }

                ColorButton{
                    id: red_dark
                    colorStyle: "#03A60E"
                }
                ColorButton{
                    id: pink
                    colorStyle: "#3C7D00"
                }
                ColorButton{
                    id: pink_dark
                    colorStyle: "#FFFFFF"
                }
                ColorButton{
                    id: blue_dark
                    colorStyle: "#666666"
                }
                ColorButton{
                    id: blue
                    colorStyle: "#2B2B2B"
                }
                ColorButton{
                    id: wathet
                    colorStyle: "#000000"
                }
            }
        }

        Row {
            id: setlw
            anchors.top: row.bottom
            anchors.left: parent.left
            anchors.leftMargin: 4
            anchors.bottom: parent.bottom

            visible: toolbar.bExtense
            property var lineWidth: 3

            function checkState(id) {
                for (var i=0; i<setlw.children.length; i++) {
                    var childButton = setlw.children[i]
                    if (childButton.imageName != id.imageName) {
                        childButton.state = "off"
                    }
                }
            }
            ToolButton {
                id: setbutton1
                group: setlw
                imageName:"small"
                dirImage: dirSizeImage
                state: "on"
                onPressed: setlw.lineWidth = 3
            }
            ToolButton {
                id: setbutton2
                group: setlw
                imageName:"normal"
                dirImage: dirSizeImage

                onPressed: setlw.lineWidth = 5
            }
            ToolButton {
                id: setbutton3
                group: setlw
                imageName:"big"
                dirImage: dirSizeImage
                onPressed: setlw.lineWidth = 7
            }
            Rectangle {
                id: dividingLine
                x: 5
                y: 5
                width: 1
                height: 20
                color: Qt.rgba(1, 1, 1, 0.1)
            }
        }
        Row {
            id: shapeEffect
            anchors.top: row.bottom
            anchors.left: setlw.right
            anchors.leftMargin: 4
            anchors.bottom: parent.bottom
            property string imageName: "blur"
            function checkState(id) {
                for (var i=0; i<shapeEffect.children.length; i++) {
                    var childButton = shapeEffect.children[i]
                    if (childButton.imageName != id.imageName) {
                        childButton.state = "off"
                    }
                }
            }


            ToolButton {
                id: blurType
                group: shapeEffect
                dirImage: dirSizeImage
                imageName: "blur"
                visible: false
                onPressed: {
                    screenArea.enabled = false
                    shapeEffect.imageName = "blur"
                    windowView.save_overload("blur", selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2, selectFrame.height - 2)
                    toolbar.shape.isBlur = true
                    toolbar.shape.processBlur = true
                }
            }
            ToolButton {
                id: mosaicType
                group: shapeEffect
                dirImage: dirSizeImage
                imageName:"mosaic"
                visible: false
                onPressed: {
                    screenArea.enabled = false
                    shapeEffect.imageName = "mosaic"
                    windowView.save_overload("mosaic", selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2, selectFrame.height - 2)
                    toolbar.shape.isMosaic = true
                    toolbar.shape.processMosaic = true
                }
            }
        }
        SaveToolTip {
            id: savetooltip
            visible: false
        }
        Row {
            id: save_toolbar
            anchors.top: row.top
            anchors.topMargin: 28
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.bottom: parent.bottom
            visible: false
            property string saveId:"auto_save"

            SoundEffect {
                id: cameraSound
                source: "../sound/camera.wav"
            }
            Timer {
                id: count
                interval: 500
                running: false
                onTriggered: {
                    running = false
                    windowView.close()
                }
            }
            ToolButton {
                id: save_to_desktop
                dirImage: dirSave
                imageName:"save_to_desktop"
                state: "on"
                onEntered: {
                    savetooltip.visible = true
                    savetooltip.text = "Save to Desktop"
                }
                onExited: {
                    savetooltip.visible = false
                }
                onPressed: {
                    save_toolbar.saveId = "save_to_desktop"
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2,selectFrame.height - 2)
                    cameraSound.play()
                    count.running = true
                }
            }
            ToolButton {
                id: auto_save

                imageName:"auto_save"
                dirImage: dirSave
                onEntered: {
                    savetooltip.visible = true
                    savetooltip.text = "Auto Save"
                }
                onExited: {
                    savetooltip.visible = false
                }
                onPressed: {
                    save_toolbar.saveId = "auto_save"
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2,selectFrame.height - 2)
                    count.running = true
                    cameraSound.play()
                }
            }
            ToolButton {
                id: save_to_dir

                imageName:"save_to_dir"
                dirImage: dirSave
                onEntered: {
                    savetooltip.visible = true
                    savetooltip.text = "Save as"
                }
                onExited: {
                    savetooltip.visible = false
                }
                onPressed: {
                    save_toolbar.saveId = "save_to_dir"
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2 ,selectFrame.height - 2)
                    count.running = true
                    cameraSound.play()
                }
            }
            ToolButton {
                id: save_ClipBoard

                imageName:"save_ClipBoard"
                dirImage: dirSave
                onEntered: {
                    savetooltip.visible = true
                    savetooltip.text = "Save to Clipboard"
                }
                onExited: {
                    savetooltip.visible = false
                }
                onPressed: {
                    save_toolbar.saveId = "save_ClipBoard"
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2,selectFrame.height - 2)
                    count.running = true
                    cameraSound.play()
                }
            }
            ToolButton {
                id: auto_save_ClipBoard

                imageName:"auto_save_ClipBoard"
                dirImage: dirSave
                onEntered: {
                    savetooltip.visible = true
                    savetooltip.text = "Auto Save and Save to Clipboard"
                }
                onExited: {
                    savetooltip.visible = false
                }
                onPressed: {
                    save_toolbar.saveId = "auto_save_ClipBoard"
                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    windowView.save_screenshot(save_toolbar.saveId,selectFrame.x + 1,selectFrame.y + 1, selectFrame.width - 2,selectFrame.height - 2)
                    count.running = true
                    cameraSound.play()
                }
            }
        }
    }

    Rectangle {
        id: zoomIndicator
        visible: firstMove && !firstRelease && !fontRect.visible

        width: 49
        height: 49
        color: Qt.rgba(1, 1, 1, 0)
        radius: 4
        border.width:2
        border.color: Qt.rgba(1, 1, 1, 0.3)
        property int cursorWidth: 8
        property int cursorHeight: 18

        property int cursorX: 0
        property int cursorY: 0
        DropShadow {
            anchors.fill: parent
            horizontalOffset: 0
            verticalOffset: 1
            radius: 10
            samples: 16
            color: Qt.rgba(0, 0, 0, 0.2)
            source: parent
        }
        function updatePosition(pos) {
            cursorX = pos.x
            cursorY = pos.y

            x = pos.x + width + cursorWidth > screenWidth ? pos.x - width : pos.x + cursorWidth
            y = pos.y + height + cursorHeight > screenHeight ? pos.y - height : pos.y + cursorHeight
        }
    }
    Item {
        id: zoomIndicatorItem
        anchors.fill: zoomIndicator
        visible: zoomIndicator.visible

        Column {
            id: zoomIndicatorTooltip

            anchors.fill: parent
            anchors.margins: marginValue
            property int marginValue: 3

            Rectangle {
                width: parent.width
                height: 35

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

                    x: (zoomIndicator.width - width) / 2 - 2
                    y:  (zoomIndicator.height - height) / 2
                    width: 12
                    height: width
                    color: "white"

                    Rectangle {
                        id: pointColorRect
                        anchors.fill: parent
                        anchors.margins: 1
                        DropShadow {
                            anchors.fill: parent
                            horizontalOffset: 0
                            verticalOffset: 1
                            radius: 10
                            samples: 16
                            color: Qt.rgba(0, 0, 0, 0.2)
                            source: parent
                        }
                    }
                }
            }

            Text {
                x:  (parent.width - width) / 2
                text:zoomIndicator.cursorX + ", " + zoomIndicator.cursorY
                font.pixelSize: 8
                color: "white"
            }
        }
    }

    focus: true
    Keys.onEscapePressed: {
        windowView.close()
    }
    Keys.onDeletePressed: {

        var canvas = toolbar.shape
        for (var i = 0; i < canvas.shapes.length; i++) {
        print(i, canvas.shapes[i].selected, canvas.shapes[i].reSized, canvas.shapes[i].rotated)
            if (canvas.shapes[i].selected == true || canvas.shapes[i].reSized == true
                || canvas.shapes[i].rotated == true) {
                print(i, canvas.shapes[i].selected, canvas.shapes[i].reSized, canvas.shapes[i].rotated)
                var spliceElement = canvas.shapes.splice(i, 1)
                spliceElement[0].destroy()
            }
        }
        canvas.requestPaint()
    }
}
