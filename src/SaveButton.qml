import QtQuick 2.1
import QtQuick.Dialogs 1.0
Item {
	id: toolButton
	width: 34
	height: 32

	property string imageName: ""
	property bool clicked: false
	property alias selectArea: selectArea

	Rectangle {
		id: selectArea
		anchors.centerIn: parent
		width: 35
		height: 20
		radius: 2
		visible: false

		color: "white"
		opacity: 0.2
	}

	Row {
		id: pathList
		anchors.centerIn: parent
		Image {
			anchors.verticalCenter: parent.verticalCenter
			source: "../image/action_menu/save_normal.png"
		}

		Image {
			anchors.verticalCenter: parent.verticalCenter
			source: "../image/action_menu/list_normal.png"
		}

	}

	Rectangle {
			id: pathSelect
			width: 150
			height: 88
			anchors.left: toolButton.right
			anchors.top: toolButton.bottom


			color: "white"
			visible: false
			radius: 3
			ListView {
				id: listView
				width: 200
				height: childrenRect.height

				clip: true
				model: listModel
				orientation: ListView.Vertical
				delegate: numberDelegate

				interactive: false
				highlight: highlightBar
				highlightFollowsCurrentItem: false

				focus: true

			}
			ListModel {
				id: listModel

				ListElement {
					eleId: "auto_save"
					name: "自动保存"
				}
				ListElement {
					eleId: "save_to_dir"
					name: "保存到指定目录"
				}
				ListElement {
					eleId: "save_to_ClipBoard"
					name: "复制到剪贴板"
				}
				ListElement {
					eleId: "auto_save&_ClipBoard"
					name: "自动保存并复制到剪贴板"
				}
			}

			Component {
				id: numberDelegate
				Item {
					id: wrapper
					width: 150
					height: 22
					property url directory: ""

					Rectangle {
						id: imageRect
						anchors.left: parent.left
						width: 22
						height:22
						visible: false
						Image {
							id: image
							width: 20
							height: 20
							anchors.left: parent.left
							source: "../image/select.png"
						}
					}

					Text {
						anchors.left: imageRect.right
						anchors.leftMargin: 2
						anchors.top: parent.top
						anchors.topMargin: 3
						font.pixelSize: 11
						text: name
					}


				MouseArea {
						anchors.fill: parent
						onClicked: {
							wrapper.ListView.view.currentIndex = index
							windowView.save_screenshot(eleId)
							windowView.close()
						}
					}

					states: State {
							name: "select"
							when: wrapper.ListView.isCurrentItem
							PropertyChanges {  target: imageRect; visible: true }
						}
				}
			}

			Component {
				id: highlightBar
				Rectangle {
					width: 150
					height: 22
					color: "steelblue"
					y: listView.currentItem.y;

				}
			}

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

		onPressed: {
			pathSelect.visible = true
		}
	}


}
