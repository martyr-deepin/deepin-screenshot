import QtQuick 2.1

Item {
    id: screen

    property bool firstMove: false
    property bool firstPress: false
    property bool firstRelease: false
    property bool firstEdit: false

    property alias selectArea: selectArea
    property alias zoomIndicator: zoomIndicator
    property alias selectSizeTooltip: selectSizeTooltip

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
            if (!firstRelease) {
                firstRelease = true
            }

            if (firstRelease) {
                if (!firstEdit) {
                    selectArea.handleRelease()
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
        property int pressX: 0
        property int pressY: 0
        property bool hasPress: false
        property bool inCenter: false

        function handlePress(pos) {
            if (x <= pos.x && pos.x <= x + width && y <= pos.y && pos.y <= y + height) {
                hasPress = true
                if (x < pos.x && pos.x < x + width && y < pos.y && pos.y < y + height) {
                    inCenter = true
                    startX = x
                    startY = y
                    pressX = pos.x
                    pressY = pos.y
                }
            }
        }

        function handlePositionChange(pos) {
            if (hasPress) {
                if (inCenter) {
                    x = Math.max(Math.min(startX + pos.x - pressX, screenWidth - width), 0)
                    y = Math.max(Math.min(startY + pos.y - pressY, screenHeight - height), 0)
                }
            }
        }

        function handleRelease() {
            if (hasPress) {
                hasPress = false
                inCenter = false
                startX = 0
                startY = 0
                pressX = 0
                pressY = 0
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
        border.width: 2
        visible: firstMove
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
        width: 250
        height: 32
        color: "black"
        opacity: 0.7
        radius: 3
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

        onXChanged: {
            tryHideSizeTooltip()
        }

        onYChanged: {
            tryHideSizeTooltip()
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
                        x: -zoomIndicator.cursorX + zoomIndicator.width / (2 * zoomIndicatorClip.scaleValue)
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
                text: "[255, 255, 255]"
                color: "white"
            }

            Text {
                text: "拖动可自由选区"
                color: "white"
            }
        }
    }
}
