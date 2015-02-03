import QtQuick 2.1
import QtMultimedia 5.0
import QtQuick.Dialogs 1.0
Item {
    id: toolButton
    width: 40
    height: 28
    state: "off"
    property string imageName: ""
    property bool clicked: false
    property alias selectArea: selectArea

    signal saveIcon()
    signal listIcon()
    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 35
        height: 22
        radius: 4
        visible: false

        color: "white"
        opacity: 0.2
    }

    Row {
        id: pathList
        anchors.centerIn: parent
        Image {
            id: saveImage
            width: 24
            height: 24
            anchors.verticalCenter: parent.verticalCenter
            source: "../image/save/save.svg"
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
                    saveImage.source = "../image/save/save" + "_hover.svg"
                    listImage.source = "../image/save/list" + "_hover.svg"
                }
                onExited: {
                    selectArea.visible = false
                    saveImage.source = "../image/save/save" + ".svg"
                    listImage.source = "../image/save/list" + ".svg"
                }
                onPressed: {
                    toolButton.state = toolButton.state == "on" ? "off":"on"
                    saveImage.source = "../image/save/save" + "_press.svg"
                    count.running = true
                    cameraSound.play()
                }

            }
        }

        Image {
            id:listImage
            width: 10
            height: 10
            anchors.verticalCenter: parent.verticalCenter
            source: "../image/save/list.svg"
            MouseArea {
                anchors.fill: listImage
                hoverEnabled: true
                onEntered: {
                    selectArea.visible = true
                    saveImage.source = "../image/save/save" + "_hover.svg"
                    listImage.source = "../image/save/list" + "_hover.svg"
                }
                onExited: {
                    selectArea.visible = false
                    saveImage.source = "../image/save/save" + ".svg"
                    listImage.source = "../image/save/list" + ".svg"
                }
                onPressed : {
                    toolButton.listIcon()
                    listImage.source = "../image/save/list" + "_press.svg"
                }

            }
        }

    }

}
