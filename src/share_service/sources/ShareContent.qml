import QtQuick 2.1
import QtQuick.Controls 1.2
import Deepin.Widgets 1.0

Item {
    width: 300
    height: 260
    property alias input_text: input_text

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
        anchors.top: input_text.bottom
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: 5
        width: parent.width - 5 * 2
    }

    Rectangle {
        anchors.top: separate_line.bottom
        anchors.topMargin: 20
        anchors.left: parent.left
        anchors.leftMargin: (parent.width - width) / 2
        width: 100
        height: 100
        color: "transparent"
        radius: 2
        border.width:2
        border.color: "white"
    }

    DSeparatorHorizontal {
        id: base_line
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: 5
        width: parent.width - 5 * 2
    }
}
