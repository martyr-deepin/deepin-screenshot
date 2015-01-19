import QtQuick 2.1
import QtQuick.Controls 1.2
import Deepin.Widgets 1.0

SlideInOutItem {
    id: root

    property alias wordCount: input_text.length
    property alias text: input_text.text
    property string screenshot

    function setScreenshot(source) {
        screenshot = source
    }

    TextEdit {
        id: input_text
        anchors.left: parent.left
        anchors.leftMargin: 5
        width: parent.width
        height: 50
        color: "#686868"
        wrapMode:TextEdit.Wrap
        onFocusChanged: { if (focus) { label.visible = false}}

        Label {
            id: label
            text: "在此输入想说的话．．．"
            color: "#686868"
            font.pixelSize: 11
            anchors.centerIn: parent
        }
    }

    DSeparatorHorizontal {
        id: separate_line
        width: parent.width - 5 * 2
        anchors.top: input_text.bottom
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Rectangle {
        width: 100
        height: 100
        color: "transparent"
        radius: 2
        border.width:2
        border.color: "white"

        anchors.top: separate_line.bottom
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter

        Image {
            id: image
            source: root.screenshot
            anchors.fill: parent
        }
    }

    DSeparatorHorizontal {
        id: base_line
        width: parent.width - 5 * 2

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
