import QtQuick 2.1

Item {
	id: bigColor
	width: 30
	height: 28

	property string colorStyle: "#FF1C49"
	signal pressed()
    signal entered()
    signal exited()
	Rectangle {
		id: colorRect
		anchors.centerIn: parent
		width: 16
		height: 16
		radius: 2
		color: bigColor.colorStyle

        border.width: 2
        border.color: "transparent"
    }
	Rectangle {
		id: selectArea
		anchors.centerIn: parent
		width: 14
		height: 14
        color: "transparent"
        radius: 2

        border.width: 1 
        border.color: Qt.rgba(1, 1, 1, 0.3)
    }

	MouseArea {
		anchors.fill: parent
        hoverEnabled: true 
        cursorShape: windowView.set_colorpen_cursor_shape("../image/mouse_style/color_pen/purple.png")

        onEntered: {
            colorRect.border.color = "#01bdff"
            selectArea.border.color = Qt.rgba(1,1,1,0.7)
            bigColor.entered()
		}

        onExited: {
            colorRect.border.color = "transparent"
			selectArea.border.color = Qt.rgba(1,1,1,0.3)
            bigColor.exited()
        }

		onPressed:{
			selectArea.border.color = Qt.rgba(1,1,1,1)
			bigColor.pressed()
		}
	}

}
