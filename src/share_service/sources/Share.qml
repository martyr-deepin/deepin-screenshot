import QtQuick 2.1
import QtQuick.Window 2.1
import Deepin.Widgets 1.0

Item {
    DDialog {
        id: dialog
        x: (Screen.desktopAvailableWidth - width) / 2
        y: (Screen.desktopAvailableHeight - height) / 2
        width: 480
        height: 300
        visible: true

        Item {
            width: parent.width
            height: 300

            ShareContent { anchors.fill: parent }
        }

        Item {
            width: parent.width
            height: 38
            anchors.bottom: parent.bottom

            Row {
                id: row
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
            }

            Text {
                id: word_number_label
                text: "129"
                color: "#FDA825"
                font.pixelSize: 11

                anchors.right: action_button.left
            }

            DTextButton {
                id: action_button
                text: "下一步"
                anchors.right: parent.right
            }
        }
    }
}