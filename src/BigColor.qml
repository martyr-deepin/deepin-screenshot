import QtQuick 2.1

Item {
	id: bigColor
	width: 30
	height: 28

	property string colorStyle: "#FF1C49"
	signal pressed()

	Rectangle {
		id: selectArea
		anchors.centerIn: parent
		width: 24
		height: 22
		radius: 4
		visible: false
		opacity: 0.2
	}
	Rectangle {
		id: colorRect
		anchors.centerIn: parent
		width: 16
		height: 16
		radius: 4
		color: bigColor.colorStyle

		border.width: 1
        border.color: Qt.rgba(1,1,1,0.2)
	}
	MouseArea {
		anchors.fill: parent
		hoverEnabled: true

		onEntered: {
			selectArea.visible = true
			colorRect.border.color = Qt.rgba(1,1,1,0.6)
		}

		onExited: {
			selectArea.visible = false
			colorRect.border.color = Qt.rgba(1,1,1,0.2)
		}

		onPressed:{
			colorRect.border.color = Qt.rgba(1,1,1,1)
			bigColor.pressed()
		}
	}

}
