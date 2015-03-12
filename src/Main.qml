import QtQuick 2.1
import QtMultimedia 5.0
import QtGraphicalEffects 1.0
import Deepin.Locale 1.0
import "calculateRect.js" as CalcEngine
import "drawing_utils.js" as DrawingUtils

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

    property var shortcutsViewerId

    function get_absolute_cursor_pos() {
        var pos_origin = windowView.get_cursor_pos()
        var pos_absolute = Qt.point(pos_origin.x - selectArea.x, pos_origin.y - selectArea.y)
        return pos_absolute
    }

    function saveScreenshot() {
        windowView.save_screenshot(selectFrame.x + 1,selectFrame.y + 1,
            selectFrame.width - 2,selectFrame.height - 2)
    }

    function share() {
        screen.saveScreenshot()
        windowView.share()
    }

    function colorCard(key) {
        switch (key) {
            case 0: return "#FFD903"
            case 1: return "#FF5E1A"
            case 2: return "#FF3305"
            case 3: return "#FF1C49"
            case 4: return "#FB00FF"
            case 5: return "#7700ED"
            case 6: return "#3D08FF"
            case 7: return "#3468FF"
            case 8: return "#00AAFF"
            case 9: return "#08FF77"
            case 10: return "#03A60E"
            case 11: return "#3C7D00"
            case 12: return "#FFFFFF"
            case 13: return "#666666"
            case 14: return "#2B2B2B"
            case 15: return "#000000"
        }
    }

    function showHotKeyOSD() {
        var osd = Qt.createQmlObject("import QtQuick 2.2; OSD {}", screen, "osd")
        osd.x = windowView.x + (windowView.width - osd.width) / 2
        osd.y = windowView.y + (windowView.height - osd.height) / 2
        osd.showTips()
    }

    function showShortcutsViewer() {
        if (!shortcutsViewerId) {
            shortcutsViewerId = Qt.createQmlObject("import QtQuick 2.2; ShortcutsViewer{}", screen, "shortcuts")
        }
        shortcutsViewerId.show()
    }

    function hideShortcutsViewer() {
        if (shortcutsViewerId) {
            shortcutsViewerId.hide()
        }
    }

    function dsTr(src) { return locale.dsTr(src) }

    DLocale { id: locale; domain: "deepin-screenshot" }

    Connections {
        target: _menu_controller
        onToolSelected: {
            switch(toolName) {
                case "_rectangle": {
                    button1.state = "on"
                    break
                }
                case "_ellipse": {
                    button2.state = "on"
                    break
                }
                case "_arrow": {
                    button3.state = "on"
                    break
                }
                case "_line": {
                    button4.state = "on"
                    break
                }
                case "_text": {
                    button5.state = "on"
                    break
                }
            }
        }
        onSaveSelected: {
            windowView.set_save_config("save", "save_op", saveOption + "")
            screen.saveScreenshot()
        }
        onShareSelected: screen.share()
        onExitSelected: windowView.closeWindow()
    }

    MouseArea {
        id: screenArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        cursorShape: windowView.set_cursor_shape("shape_start_cursor")

        property int pressX: 0
        property int pressY: 0
        onPressed: {
            if (mouse.button == Qt.RightButton && !firstRelease) windowView.closeWindow()

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

        onClicked: {
            if (mouse.button == Qt.RightButton)
                _menu_controller.show_menu(windowView.get_save_config("save", "save_op"))
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
                if ((pos.x >= selectArea.x && pos.x <= selectArea.x + selectArea.width) &&
                (pos.y >= selectArea.y && pos.y <= selectArea.y + selectArea.height )) {
                } else {
                    screenArea.cursorShape = windowView.set_cursor_shape("Qt.ArrowCursor")
                }
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

        onDoubleClicked: saveScreenshot()

        onWheel: {
            if (wheel.modifiers & Qt.ControlModifier) {
                if (wheel.angleDelta.y < 0) {
                    if (selectArea.width > 4) {
                        selectArea.x += 1
                        selectArea.width -= 2
                    }
                    if (selectArea.height > 4) {
                        selectArea.y += 1
                        selectArea.height -= 2
                    }
                } else {
                    selectArea.x = Math.max(0, selectArea.x - 1)
                    selectArea.y = Math.max(0, selectArea.y - 1)
                    selectArea.width = Math.min(selectArea.width + 2, screenWidth)
                    selectArea.height = Math.min(selectArea.height + 2, screenHeight)
                }
            }
        }
    }

    Image {
        id: background
        anchors.fill: parent
        source: "/tmp/deepin-screenshot.png"
        cache: true
        asynchronous: true
    }

    Rectangle {
        anchors.fill: screen
        color: "black"
        visible: true
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
            cache: true
            asynchronous: true
        }

        ShapeCanvas {
            id: shape_canvas
            onTextEditing: button5.state = "on"
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
            DrawingUtils.draw_point(ctx, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius)

            /* Top right */
            DrawingUtils.draw_point(ctx, width - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius)

            /* Bottom left */
            DrawingUtils.draw_point(ctx, selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius)

            /* Bottom right */
            DrawingUtils.draw_point(ctx, width - selectResizeCanvas.bigPointRadius, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.bigPointRadius)

            /* Top */
            DrawingUtils.draw_point(ctx, width / 2, selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius)

            /* Bottom */
            DrawingUtils.draw_point(ctx, width / 2, height - selectResizeCanvas.bigPointRadius, selectResizeCanvas.smallPointRadius)

            /* Left */
            DrawingUtils.draw_point(ctx, selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius)

            /* Right */
            DrawingUtils.draw_point(ctx, width - selectResizeCanvas.bigPointRadius, height / 2, selectResizeCanvas.smallPointRadius)
            ctx.restore()
        }
    }

    Rectangle {
        id: selectSizeTooltip
        x: Math.min(screenWidth - width, selectFrame.x)
        y: selectFrame.y < height * 1.5 ? selectFrame.y + outPadding : selectFrame.y - height - outPadding
        width: selectSizeTooltipText.width + 2 * padding
        height: 28

        color: Qt.rgba(0, 0, 0, 0.5)
        radius: 3
        visible: firstMove
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.2)
        property int outPadding: 4
        property int padding: 10
        Text {
            id: selectSizeTooltipText
            anchors.centerIn: parent
            anchors.margins: 3
            color: "white"
            text: selectArea.width + "X" + selectArea.height
            font.pixelSize: 12
        }
    }


    Rectangle {
        id: toolbar
        x: selectFrame.y < y && y < selectFrame.y + selectFrame.height ? selectFrame.x + selectFrame.width - width - 6 : Math.max(selectFrame.x + selectFrame.width - width,0)
        y: selectFrame.y + selectFrame.height > screen.height - height * 2 ? (selectFrame.y < height * 1.5 ? selectFrame.y + padding : selectFrame.y - height - padding) : selectFrame.y + selectFrame.height + padding
        width: 290
        height: 28
        radius: 4
        property bool bExtense: height == 56
        property var shape: shape_canvas
        property var linewidth: ""

        property color stop1Color: Qt.rgba(0, 0, 0, 0.7)
        property color stop2Color: Qt.rgba(0, 0, 0, 0.775)
        property color stop3Color: Qt.rgba(0, 0, 0, 0.776)
        property color stop4Color: Qt.rgba(0, 0, 0, 0.777)
        property color stop5Color: Qt.rgba(0, 0, 0, 0.778)
        property color stop6Color: Qt.rgba(0, 0, 0, 0.85)

        // this item is used to steal focus from other items
        MouseArea {
            anchors.fill: parent
            onClicked: toolbar.focus = true
        }
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
        function toolbarVisible() {
            if (toolbar.shape.shapeName == "rect" || toolbar.shape.shapeName == "ellipse") {
                setlw.visible = true
                dividingLine.visible = true
                blurType.visible = true
                mosaicType.visible = true
                colorChange.visible = false
                fontRect.visible = false
            }
            if (toolbar.shape.shapeName == "arrow" || toolbar.shape.shapeName == "line") {
                setlw.visible = true
                colorChange.visible = false
                dividingLine.visible = false
                blurType.visible = false
                mosaicType.visible = false
                fontRect.visible = false
            }
            if (toolbar.shape.shapeName == "text") {
                setlw.visible = false
                dividingLine.visible = false
                blurType.visible = false
                mosaicType.visible = false
                colorChange.visible = false
                fontRect.visible = true
            }
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

                shape_canvas.deselectAll()
                screen.focus = true
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
                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }

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

                    toolbar.shape.shapeName = "rect"
                    setlw.lineWidth = windowView.get_save_config(toolbar.shape.shapeName, "linewidth_index")
                    colorTool.colorOrder =  windowView.get_save_config(toolbar.shape.shapeName, "color_index")
                    colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                    setlw.checkOn()
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorOrder })
                }
            }
            ToolButton {
                id:button2
                group: row
                imageName: "ellipse"
                visible: ((button1.width*2 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true

                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }
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

                    toolbar.shape.shapeName = "ellipse"
                    setlw.lineWidth = windowView.get_save_config(toolbar.shape.shapeName, "linewidth_index")
                    colorTool.colorOrder =  windowView.get_save_config(toolbar.shape.shapeName, "color_index")
                    colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                    setlw.checkOn()
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorOrder })
                }
            }

            ToolButton {
                id:button3
                group: row
                imageName: "arrow"
                visible: ((button1.width*3 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }
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
                        colorChange.visible = false
                    }

                    toolbar.shape.shapeName = "arrow"
                    setlw.lineWidth = windowView.get_save_config(toolbar.shape.shapeName, "linewidth_index")
                    colorTool.colorOrder =  windowView.get_save_config(toolbar.shape.shapeName, "color_index")
                    colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                    setlw.checkOn()
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorOrder })
                }
            }

            ToolButton {
                id:button4
                group:row
                imageName: "line"
                visible: ((button1.width*4 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }
                    screenArea.enabled = false
                    toolbar.toggleToolbar("line")
                    if (toolbar.bExtense) {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = true
                        dividingLine.visible = true
                        straightLine.visible = true
                        colorChange.visible= false
                        fontRect.visible = false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        dividingLine.visible = false
                        straightLine.visible = false
                        colorChange.visible= false
                    }

                    toolbar.shape.shapeName = "line"
                    setlw.lineWidth = windowView.get_save_config(toolbar.shape.shapeName, "linewidth_index")
                    colorTool.colorOrder =  windowView.get_save_config(toolbar.shape.shapeName, "color_index")
                    colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                    setlw.checkOn()
                    toolbar.shape.linewidth = Qt.binding(function() { return setlw.lineWidth })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorOrder })
                }
            }
            ToolButton {
                group:row
                id:button5
                imageName: "text"
                visible: ((button1.width*5 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }
                    screenArea.enabled = false
                    toolbar.toggleToolbar("text")
                    if (toolbar.bExtense) {
                        blurType.visible = false
                        mosaicType.visible = false
                        setlw.visible = false
                        colorChange.visible= false
                        save_toolbar.visible = false
                    } else {
                        blurType.visible = false
                        mosaicType.visible = false
                        fontRect.visible = true
                        colorChange.visible= false
                        setlw.visible = false
                    }

                    toolbar.shape.shapeName = "text"
                    colorTool.colorOrder =  windowView.get_save_config(toolbar.shape.shapeName, "color_index")
                    colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                    toolbar.shape.fontSize = Qt.binding( function() { return fontRect.value })
                    toolbar.shape.paintColor = Qt.binding(function() { return colorTool.colorOrder })
                    fontRect.visible = !fontRect.visible
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
                colorStyle: screen.colorCard(colorOrder)
                visible: ((button1.width*6 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true
                property int colorOrder: windowView.get_save_config("common_color_linewidth","color_index")
                property bool isfirst: false
                onStateChanged: {
                    if (!isfirst) {
                        isfirst = true
                        if (state == "off") {
                            return
                        }
                    }
                    var originType = toolbar.buttonType
                    toolbar.toggleToolbar("color")
                    colorChange.visible = !colorChange.visible
                    if (toolbar.bExtense) {
                        colorChange.visible= true
                    } else {
                        colorChange.visible = false
                    }
                    setlw.visible = false
                    blurType.visible = false
                    straightLine.visible = false
                    mosaicType.visible = false
                    fontRect.visible = false
                    save_toolbar.visible = false
                    toolbar.buttonType = originType
                }
            }
            SaveButton {
                id: saveButton
                visible: ((button1.width*7 +10 + savetooltip.width*savetooltip.visible)>toolbar.width) ? false : true

                onStateChanged: {
                    if (state == "off") return

                    toolbar.visible = false
                    selectSizeTooltip.visible = false
                    screen.saveScreenshot()
                }

                onListIcon: {
                    save_toolbar.visible = !save_toolbar.visible
                    if (save_toolbar.visible) {
                        setlw.visible = false
                        blurType.visible = false
                        mosaicType.visible = false
                        colorChange.visible = false
                        fontRect.visible = false
                        save_toolbar.saveItem = windowView.get_save_config("save", "save_op")
                    }
                    toolbar.toggleToolbar("saveAction")
                }
            }
            ToolButton {
                id: shareButton
                visible: !savetooltip.visible
                imageName: "share"
                onStateChanged: {
                    if (state == "off") { return }

                    screen.share()
                }
            }
            ToolButton {
                visible: !savetooltip.visible
                imageName: "cancel"
                onPressed: {
                    windowView.closeWindow()
                }
            }
        }

        FontSizeSpinner {
            id: fontRect

            width: 120
            height: 20
            visible: false
            min: 6
            max: 24
            maximumLength: 3
            initValue: windowView.get_save_config("text", "fontsize_index")

            anchors.left: row.left
            anchors.leftMargin: 4
            anchors.top: row.bottom
            anchors.topMargin: 4
        }
        ColorRow {
            id: colorChange
            onColorOrderChanged: {
                colorTool.colorOrder = colorChange.colorOrder
                colorTool.colorStyle = screen.colorCard(colorTool.colorOrder)
                colorStyle = screen.colorCard(colorOrder)
                windowView.set_save_config("common_color_linewidth", "color_index", colorOrder)
                if (toolbar.shape != undefined && toolbar.shape.shapeName != undefined) {
                    windowView.set_save_config(toolbar.shape.shapeName, "color_index", colorOrder)
                }
                toolbar.toolbarVisible()
            }
        }

        Row {
            id: setlw
            anchors.top: row.bottom
            anchors.left: row.left
            anchors.leftMargin: 4
            anchors.bottom: parent.bottom
            visible: toolbar.bExtense
            property var lineWidth: windowView.get_save_config("common_color_linewidth", "linewidth_index")

            function checkOn() {
                for (var i=0; i<setlw.children.length - 1; i++) {
                    var childButton = setlw.children[i]
                    if (setlw.lineWidth == childButton.linewidth) {
                        setlw.children[i].state = "on"
                    }
                }
            }
            function setMosaicBlurState() {
                    if (toolbar.shape.isBlur) {
                        blurType.state = "off"
                        toolbar.shape.isBlur = false
                        toolbar.shape.processBlur = false
                    }
                    if (toolbar.shape.isMosaic) {
                        mosaicType.state = "off"
                        toolbar.shape.isMosaic =  false
                        toolbar.shape.processMosaic = false
                    }
            }
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
                property var linewidth: 2
                onStateChanged: {
                    if (state == "off") { return }
                    setlw.setMosaicBlurState()
                    setlw.lineWidth = linewidth
                }
            }
            ToolButton {
                id: setbutton2
                group: setlw
                imageName:"normal"
                dirImage: dirSizeImage
                property var linewidth: 4
                onStateChanged: {
                    if (state == "off") { return }
                    setlw.setMosaicBlurState()
                    setlw.lineWidth = linewidth
                }
            }
            ToolButton {
                id: setbutton3
                group: setlw
                imageName:"big"
                dirImage: dirSizeImage
                property var linewidth: 6
                onStateChanged: {
                    if (state == "off") { return }
                    setlw.setMosaicBlurState()
                    setlw.lineWidth = linewidth
                }
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
            function getlw() {
                for (var i=0; i<setlw.children.length; i++) {
                    if (setlw.children[i].state == "on") {
                        return i
                    }
                }
                return -1
            }

            property var num
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
                    toolbar.shape.isMosaic = false
                    toolbar.shape.processMosaic = false
                    toolbar.shape.isBlur = !toolbar.shape.isBlur
                    toolbar.shape.processBlur = !toolbar.shape.processBlur
                    if (toolbar.shape.isBlur) {
                        if (shapeEffect.getlw() >= 0) {
                            shapeEffect.num = shapeEffect.getlw()
                            setlw.children[shapeEffect.num].state = "off"
                        }
                    } else {
                        if (shapeEffect.num >= 0) {
                            setlw.children[shapeEffect.num].state = "on"
                        }
                    }
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
                    toolbar.shape.isBlur = false
                    toolbar.shape.processBlur = false
                    toolbar.shape.isMosaic =  !toolbar.shape.isMosaic
                    toolbar.shape.processMosaic = !toolbar.shape.processMosaic
                    if (toolbar.shape.isMosaic) {
                        if (shapeEffect.getlw() >= 0) {
                            shapeEffect.num = shapeEffect.getlw()
                            setlw.children[shapeEffect.num].state = "off"
                        }
                    } else {
                        if (shapeEffect.num >= 0) {
                            setlw.children[shapeEffect.num].state = "on"
                        }
                    }
                }
            }
        }
        ToolButton {
            id: straightLine
            width: 46
            anchors.top: row.bottom
            anchors.left: setlw.right
            anchors.leftMargin: 4
            anchors.bottom: parent.bottom
            dirImage: dirSizeImage
            selectDisArea.width: 40
            imageIcon.width: 40
            imageName: "straightline"
            visible: false
            onPressed: {
                screenArea.enabled = false
                toolbar.shape.isStraightLine = !toolbar.shape.isStraightLine
            }
        }
        SaveToolTip { id: savetooltip }

        Row {
            id: save_toolbar
            anchors.top: row.top
            anchors.topMargin: 28
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.bottom: parent.bottom
            visible: false
            property string saveId:"auto_save"
            property int saveItem: 0
            function last_select_saveItem() {
                return windowView.get_save_config("save","save_op")
            }

            ToolButton {
                id: save_to_desktop
                dirImage: dirSave
                imageName:"save_to_desktop"
                state: save_toolbar.saveItem == 0 ? "on": "off"
                onEntered: {
                    savetooltip.show()
                    savetooltip.text = "Save to Desktop"
                }
                onExited: {
                    savetooltip.hide()
                }
                onPressed: {
                    save_toolbar.saveId = "save_to_desktop"
                    windowView.set_save_config("save", "save_op","0")
                    toolbar.visible = false
                    selectSizeTooltip.visible = false

                    screen.saveScreenshot()
                }
            }
            ToolButton {
                id: auto_save

                imageName:"auto_save"
                dirImage: dirSave
                state: save_toolbar.saveItem == 1 ? "on": "off"
                onEntered: {
                    savetooltip.show()
                    savetooltip.text = "Auto Save"
                }
                onExited: {
                    savetooltip.hide()
                }
                onPressed: {
                    save_toolbar.saveId = "auto_save"
                    windowView.set_save_config("save","save_op","1")
                    toolbar.visible = false
                    selectSizeTooltip.visible = false

                    screen.saveScreenshot()
                }
            }
            ToolButton {
                id: save_to_dir

                imageName:"save_to_dir"
                dirImage: dirSave
                state: save_toolbar.saveItem == 2 ? "on": "off"
                onEntered: {
                    savetooltip.show()
                    savetooltip.text = "Save as"
                }
                onExited: {
                    savetooltip.hide()
                }
                onPressed: {
                    save_toolbar.saveId = "save_to_dir"
                    windowView.set_save_config("save","save_op","2")
                    toolbar.visible = false
                    selectSizeTooltip.visible = false

                    screen.saveScreenshot()
                }
            }
            ToolButton {
                id: save_ClipBoard

                imageName:"save_ClipBoard"
                dirImage: dirSave
                state: save_toolbar.saveItem == 3 ? "on": "off"
                onEntered: {
                    savetooltip.show()
                    savetooltip.text = "Save to Clipboard"
                }
                onExited: {
                    savetooltip.hide()
                }
                onPressed: {
                    save_toolbar.saveId = "save_ClipBoard"
                    windowView.set_save_config("save","save_op","3")
                    toolbar.visible = false
                    selectSizeTooltip.visible = false

                    screen.saveScreenshot()
                }
            }
            ToolButton {
                id: auto_save_ClipBoard
                imageName:"auto_save_ClipBoard"
                dirImage: dirSave
                state: save_toolbar.saveItem == 4 ? "on": "off"
                onEntered: {
                    savetooltip.show()
                    savetooltip.text = "Auto Save and Save to Clipboard"
                }
                onExited: {
                    savetooltip.hide()
                }
                onPressed: {
                    save_toolbar.saveId = "auto_save_ClipBoard"
                    windowView.set_save_config("save","save_op","4")
                    toolbar.visible = false
                    selectSizeTooltip.visible = false

                    screen.saveScreenshot()
                }
            }
        }
    }
    RectangularGlow {
        anchors.fill: toolbar
        glowRadius: toolbar.visible ? 3 : 0
        color: toolbar.visible ? Qt.rgba(0, 0, 0, 0.3) : "transparent"
        cornerRadius: toolbar.radius + glowRadius
    }
    Rectangle {
        id: zoomIndicator
        visible: firstMove && !firstRelease && !fontRect.visible

        width: 49
        height: 49
        color: Qt.rgba(1, 1, 1, 0)
        radius: 4
        border.width: 2
        border.color: Qt.rgba(1, 1, 1, 0.3)
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
    RectangularGlow {
        id: zoomIndicatorShadow
        anchors.fill: zoomIndicator
        glowRadius: zoomIndicator.visible ? 2 : 0
        color: zoomIndicator.visible ? Qt.rgba(0, 0, 0, 0.2) : "transparent"
        cornerRadius: zoomIndicator.radius + glowRadius
    }
    Item {
        id: zoomIndicatorItem
        anchors.fill: zoomIndicator
        visible: zoomIndicator.visible

        Rectangle {
            id: zoomIndicatorTooltip
            anchors.fill: parent
            anchors.margins: marginValue
            color: "black"
            radius: 4

            property int marginValue: 2

            Rectangle {
                id: zoomIndicatorClip
                clip: true
                color: "black"
                height: parent.height / zoomIndicatorClip.scaleValue
                width: parent.width / zoomIndicatorClip.scaleValue

                property int scaleValue: 4

                transform: Scale {
                    xScale: zoomIndicatorClip.scaleValue
                    yScale: zoomIndicatorClip.scaleValue
                }

                Image {
                    id: zoomIndicatorImage
                    // the -1 operation of x&y is non-sense, but it's necessary to make the indicator look right.
                    x: -zoomIndicator.cursorX + (zoomIndicator.width - zoomIndicatorTooltip.marginValue) / (2 * zoomIndicatorClip.scaleValue) - 1
                    y: -zoomIndicator.cursorY + (zoomIndicator.height - zoomIndicatorTooltip.marginValue) / (2 * zoomIndicatorClip.scaleValue) - 1
                    source: "/tmp/deepin-screenshot.png"
                    smooth: false
                    cache: true
                    asynchronous: true
                }
            }

            Rectangle {
                id: pointRect
                anchors.centerIn: parent
                color: "transparent"
                width: 14
                height: 14

                Rectangle {
                    id: pointColorRect
                    anchors.centerIn: parent
                    width: 10
                    height: 10
                    color: "transparent"
                    border.width: 1
                    border.color: Qt.rgba(1, 1, 1, 1)

                }
            }
            Glow {
                anchors.fill: pointRect
                radius: 2
                samples: 16
                color: Qt.rgba(0, 0, 0, 0.5)
                source: pointRect
            }
        }

        Rectangle {
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 2
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width - 4
            height: 14

            color: Qt.rgba(0, 0, 0, 0.5)
            Text {
                anchors.centerIn: parent
                text:zoomIndicator.cursorX + ", " + zoomIndicator.cursorY
                font.pixelSize: 8
                color: Qt.rgba(1, 1, 1, 0.6)
            }
        }
    }

    focus: true
    Keys.onEscapePressed: {
        windowView.closeWindow()
    }
    Keys.onDeletePressed: {
        var canvas = toolbar.shape
        for (var i = 0; i < canvas.shapes.length; i++) {
            if (canvas.shapes[i].selected == true || canvas.shapes[i].reSized == true
                || canvas.shapes[i].rotated == true) {
                var spliceElement = canvas.shapes.splice(i, 1)
                spliceElement[0].destroy()
            }
        }
        canvas.requestPaint()
    }

    function microAdjust(dir) {
        var canvas = toolbar.shape
        for (var i = 0; i < canvas.shapes.length; i++) {
            if (canvas.shapes[i].selected || canvas.shapes[i].reSized || canvas.shapes[i].rotated) {
                if (dir == "Left" || dir == "Right" || dir == "Up" || dir == "Down") {
                    var tempPoints = CalcEngine.pointMoveMicro(canvas.shapes[i].mainPoints[0], canvas.shapes[i].mainPoints[1],canvas.shapes[i].mainPoints[2],canvas.shapes[i].mainPoints[3], dir)
                } else {
                    var tempPoints = CalcEngine.pointResizeMicro(canvas.shapes[i].mainPoints[0], canvas.shapes[i].mainPoints[1],canvas.shapes[i].mainPoints[2],canvas.shapes[i].mainPoints[3], dir)
                }
                canvas.shapes[i].mainPoints[0] = tempPoints[0]
                canvas.shapes[i].mainPoints[1] = tempPoints[1]
                canvas.shapes[i].mainPoints[2] = tempPoints[2]
                canvas.shapes[i].mainPoints[3] = tempPoints[3]
                if (canvas.shapes[i].shape != "line" && canvas.shapes[i].shape != "arrow") {
                    canvas.requestPaint()
                } else {
                    if (canvas.shapes[i].portion.length == 0) {
                        for (var k = 0; k < canvas.shapes[i].points.length; k++) {
                            canvas.shapes[i].portion.push(CalcEngine.relativePostion(canvas.shapes[i].mainPoints[0], canvas.shapes[i].mainPoints[1],canvas.shapes[i].mainPoints[2], canvas.shapes[i].mainPoints[3], canvas.shapes[i].points[k]))
                        }
                    }
                    for (var j = 0; j < canvas.shapes[i].points.length; j++) {
                    canvas.shapes[i].points[j] = CalcEngine.getNewPostion(canvas.shapes[i].mainPoints[0], canvas.shapes[i].mainPoints[1],canvas.shapes[i].mainPoints[2], canvas.shapes[i].mainPoints[3], canvas.shapes[i].portion[j])
                    }
                    canvas.requestPaint()
                }
            }
        }
    }

    Keys.onPressed: {
        var keyActionMap = {
            "Return": "screen.saveScreenshot()",
            "Alt+1": "button1.state = 'on'",
            "Alt+2": "button2.state = 'on'",
            "Alt+3": "button3.state = 'on'",
            "Alt+4": "button4.state = 'on'",
            "Alt+5": "button5.state = 'on'",
            "Alt+6": "colorTool.state = 'on'",
            "Ctrl+S": "saveButton.state = 'on'",
            "Ctrl+Return": "shareButton.state = 'on'",
            "Ctrl+Shift+?": "screen.showShortcutsViewer()",
            "Left": "
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.x != 0) { selectArea.x = selectArea.x -1}
                } else { microAdjust('Left') }
            ",
            "Right":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.x+selectArea.width != screenWidth) { selectArea.x = selectArea.x + 1 }
                } else { microAdjust('Right') }
            ",
            "Up":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.y != 0) { selectArea.y = selectArea.y -1 }
                } else { microAdjust('Up') }
            ",
            "Down":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.y+selectArea.height != screenHeight) { selectArea.y = selectArea.y+1 }
                } else { microAdjust('Down') }
            ",
            "Ctrl+Left": "
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.x != 0) { selectArea.x = selectArea.x -1;selectArea.width=selectArea.width+1 }
                } else { microAdjust('Ctrl+Left') }
            ",
            "Ctrl+Right":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.x+selectArea.width != screenWidth) { selectArea.width = selectArea.width + 1 }
                } else { microAdjust('Ctrl+Right') }
            ",
            "Ctrl+Up":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.y != 0) { selectArea.y = selectArea.y -1;selectArea.height=selectArea.height+1 }
                } else { microAdjust('Ctrl+Up') }
            ",
            "Ctrl+Down":"
                if (toolbar.shape == undefined ||(toolbar.shape != undefined && toolbar.shape.shapes.length == 0)) {
                    if (selectArea.y+selectArea.height != screenHeight) { selectArea.height = selectArea.height+1 }
                } else { microAdjust('Ctrl+Down') }
            "
        }
        var keyStroke = windowView.keyEventToQKeySequenceString(event.modifiers, event.key)
        if (keyStroke in keyActionMap) eval(keyActionMap[keyStroke])
    }
    Keys.onReleased: {
        if (!event.isAutoRepeat) screen.hideShortcutsViewer()
    }
}
