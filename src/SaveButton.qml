import QtQuick 2.1

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
            anchors.left: toolButton.right
            anchors.top: toolButton.bottom
            width: 100
            height: 200
            visible: false
            color: "white"

            ListView {
                anchors.fill: parent
                anchors.margins: 2

                clip: true

                model: 4

                orientation: ListView.Vertical

                delegate: numberDelegate
                focus: true

            }

            Component {
                id: numberDelegate

                Rectangle {
                    width: 100
                    height: 50

                    color: ListView.isCurrentItem ? "Green" : "lightGreen"

                    Text {
                        anchors.centerIn: parent
                        font.pixelSize: 10
                        text: index
                    }
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
