import QtQuick 2.1

Item {
	id: bigColor
	width: 30
	height: 28

	property string colorStyle: "red"
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
		width: 20
		height: 20
		radius: 4
		color: bigColor.colorStyle

	}
	MouseArea {
		anchors.fill: parent
		hoverEnabled: true

		onEntered: {
			selectArea.visible = true
		}

		onExited: {
			selectArea.visible = false
		}

		onPressed:{
			bigColor.pressed()
		}
	}

}