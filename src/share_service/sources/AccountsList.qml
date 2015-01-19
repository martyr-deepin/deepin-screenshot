import QtQuick 2.1
import QtGraphicalEffects 1.0

SlideInOutItem {
	id: root

	function selectItem(idx) {
		for (var i = 0; i < list_view.count; i++) {
			if (i == idx) {
				list_view.model.setProperty(idx, "itemSelected", true)
			}
		}
	}

	function deselectItem(idx) {
		for (var i = 0; i < list_view.count; i++) {
			if (i == idx) {
				list_view.model.setProperty(idx, "itemSelected", false)
			}
		}
	}

	function getEnabledAccounts() {
		var result = []
		for (var i = 0; i < list_view.count; i++) {
			if (list_view.model.get(i).itemSelected) {
				result.push(list_view.model.get(i).itemName)
			}
		}
		return result
	}

	ListView {
		id: list_view
		width: parent.width
		height: parent.height

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

				onClicked: {
					if (itemSelected) {
						root.deselectItem(index)
					} else {
						var browser = Qt.createQmlObject("import QtQuick 2.2; Browser {}", root, "browser")
						browser.setUrl(_accounts_manager.getAuthorizeUrl(itemName))
						browser.urlChanged.connect(function (url) {
							var query = {};
							if (url.indexOf("?") != -1) {
								url = url.split("?")[1]
								url.split("&").forEach(function(part) {
									var item = part.split("=")
									query[item[0]] = item[1]
								})
							}
							if ("code" in query) {
								_accounts_manager.handleAuthorizeCode(itemName, query["code"])
								root.selectItem(index)
								browser.destroy()
							}
						})
						browser.show()
					}
				}
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
	}
}