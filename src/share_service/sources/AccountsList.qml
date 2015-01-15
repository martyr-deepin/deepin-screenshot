import QtQuick 2.1
import QtGraphicalEffects 1.0

ListView {
	width: 400
	height: childrenRect.height

	highlight: Rectangle {
		clip: true

		RadialGradient {
			width: parent.width
			height: parent.height + 20
			verticalOffset: - height / 2

			gradient: Gradient {
				GradientStop { position: 0.0; color: Qt.rgba(0, 0, 0, 0.3) }
				GradientStop { position: 1.0; color: Qt.rgba(0, 0, 0, 0.0) }
			}
		}
	}
	delegate: Item {
		id: delegate_item
		width: ListView.view.width
		height: banner.implicitHeight

		Image {
			id: check_mark
			visible: itemSelected
			source: "../images/account_select_flag.png"
			anchors.verticalCenter: parent.verticalCenter
		}

		Image {
			id: banner
			source: imageSource
			anchors.horizontalCenter: parent.horizontalCenter
		}

		MouseArea {
			hoverEnabled: true
			anchors.fill: parent

			onEntered: delegate_item.ListView.view.currentIndex = index
			onExited: delegate_item.ListView.view.currentIndex = -1

			onClicked: itemSelected ? delegate_item.ListView.view.deselectItem(index) : delegate_item.ListView.view.selectItem(index)
		}
	}
	model: ListModel{
		ListElement {
			itemName: "sinaweibo"
			itemSelected: false
			imageSource: "../images/account_banner_sinaweibo.png"
		}
		ListElement {
			itemName: "twitter"
			itemSelected: false
			imageSource: "../images/account_banner_twitter.png"
		}
	}

	signal itemSelected(string name)
	signal itemDeselected(string name)

	function selectItem(idx) {
		for (var i = 0; i < count; i++) {
			if (i == idx) {
				model.setProperty(idx, "itemSelected", true)
				itemSelected(model.get(i).itemName)
			}
		}
	}

	function deselectItem(idx) {
		for (var i = 0; i < count; i++) {
			if (i == idx) {
				model.setProperty(idx, "itemSelected", false)
				itemDeselected(model.get(i).itemName)
			}
		}
	}
}