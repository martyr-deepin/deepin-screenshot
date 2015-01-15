import QtQuick 2.1
import Deepin.Widgets 1.0

DDialog {
    x: (screenWidth - width) / 2
    y: (screenHeight - height) / 2
    width: 480
    height: 300
    property bool isVisible: true 
    TextEdit {
        x: parent.x + 20
        y: 5
        width: parent.width - 20*2
        //height: 30
        text: "在此输入想说的话．．．"
        color: "grey"
        visible: isVisible
        wrapMode:TextEdit.Wrap 
    }


    Rectangle {
        x: parent.x + 20
        y: parent.y + 40
        width: parent.width - 20*2
        height: 1
        color: "transparent"
        visible: isVisible
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.1)
    }
    Rectangle {
        x: parent.x + 20
        y: parent.y + 45
        width: 100
        height: 100
        visible: isVisible
        border.width:2
        border.color: "white"
    }
    Rectangle {
        x: parent.x + 20
        y: parent.y + 180
        width: parent.width - 20*2
        height: 1
        color: "transparent"
        visible: isVisible
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.1)
    }
    Row {
        id: row
        x: 10
        y: 220
        spacing: 15
        visible: isVisible
        Row {
            spacing: 5
            Rectangle {
                width: 10
                height: 10
                color: "transparent"
                border.width: 1
                border.color: "grey"
            }
            Rectangle {
                width: 16
                height: 16
                color: "transparent"
                Image {
                    anchors.fill: parent
                    source: "../images/sinaweibo_small.png"
                }
            }
        }
        Row {
            spacing: 5
            Rectangle {
                width: 10
                height: 10
                color: "transparent"
                border.width: 1
                border.color: "grey"
           }
            Rectangle {
                width: 16
                height: 16
                color: "transparent"
                Image {
                    anchors.fill: parent
                    source: "../images/twitter_small.png"
                }
            }
       }
    }
    Rectangle {
        id: next
        x: 400
        y: 220
        width: 50
        height: 30
        color: "transparent"

        border.width: 1
        border.color: "grey"
        radius: 4
        Text {
            id: label
            anchors.centerIn: parent
            text: "下一步"
            font.pixelSize: 16
        }
        MouseArea {
            anchors.fill:parent
            onPressed: { 
                parent.border.color = "#01bdff"
            }
        }
    }

}
