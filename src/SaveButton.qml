import QtQuick 2.1
import QtMultimedia 5.0
import QtQuick.Dialogs 1.0
Item {
	id: toolButton
	width: 40
	height: 28

	property string imageName: ""
	property bool clicked: false
	property alias selectArea: selectArea

	signal saveIcon()
	signal listIcon()
	Rectangle {
		id: selectArea
		anchors.centerIn: parent
		width: 35
		height: 24
		radius: 2
		visible: false

		color: "white"
		opacity: 0.2
	}

	Row {
		id: pathList
		anchors.centerIn: parent
		Image {
			id: saveImage
			width: 22
			height: 22
			anchors.verticalCenter: parent.verticalCenter
			source: "../image/action_menu/save_normal.png"
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

					toolButton.saveIcon()
				}
			}
			MouseArea {
				anchors.fill: saveImage
				hoverEnabled: true
				onEntered: {
					selectArea.visible = true
					saveImage.source = "../image/action_menu/save" + "_hover.png"
					listImage.source = "../image/action_menu/list" + "_hover.png"
				}
				onExited: {
					selectArea.visible = false
					saveImage.source = "../image/action_menu/save" + "_normal.png"
					listImage.source = "../image/action_menu/list" + "_normal.png"
				}
				onPressed: {
					saveImage.source = "../image/action_menu/save" + "_press.png"
					count.running = true
					cameraSound.play()
				}

			}
		}

		Image {
			id:listImage
			width: 11
			height: 22
			anchors.verticalCenter: parent.verticalCenter
			source: "../image/action_menu/list_normal.png"
			MouseArea {
				anchors.fill: listImage
				hoverEnabled: true
				onEntered: {
					selectArea.visible = true
					saveImage.source = "../image/action_menu/save" + "_hover.png"
					listImage.source = "../image/action_menu/list" + "_hover.png"
				}
				onExited: {
					selectArea.visible = false
					saveImage.source = "../image/action_menu/save" + "_normal.png"
					listImage.source = "../image/action_menu/list" + "_normal.png"
				}
				onPressed : {
					toolButton.listIcon()
					listImage.source = "../image/action_menu/list" + "_press.png"
				}

			}
		}

	}

}
