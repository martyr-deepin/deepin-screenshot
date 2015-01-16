import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Widgets 1.0

Item {
    DDialog {
        id: dialog
        x: (Screen.desktopAvailableWidth - width) / 2
        y: (Screen.desktopAvailableHeight - height) / 2
        width: 480
        height: 360
        visible: true

        Item {
            id: mainItem
            anchors.top: parent.top
            width: parent.width
            height: 260

            ShareContent {
                id: shareContent
                anchors.fill: parent
                }
            }

        Item {
            width: parent.width
            height: 40
            anchors.top: mainItem.bottom
            anchors.topMargin: 25
            Row {
                id: row
                anchors.left: parent.left
                anchors.leftMargin: 5
                spacing: 10
                DImageCheckBox {
                    imageSource :"../images/sinaweibo_small.png"
                }
                DImageCheckBox {
                    imageSource :"../images/twitter_small.png"
                }
            }
            Text {
                id: light_to_select_label
                text: "点亮图标以选择"
                color: "#FDA825"
                font.pixelSize: 11
                anchors.left: row.right
                anchors.leftMargin: 5
            }
            Text {
                id: word_number_label
                property var show: (129 - shareContent.input_text.length)
                text: show
                color: "#FDA825"
                font.pixelSize: 11

                anchors.right: action_button.left
                anchors.rightMargin: 10
            }
            DTextButton {
                id: action_button
                text: "下一步"
                anchors.right: parent.right
                anchors.rightMargin: 5
            }
        }
    }
}
