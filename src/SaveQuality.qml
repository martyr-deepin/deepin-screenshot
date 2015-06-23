import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import Deepin.Widgets 1.0

Item {
    id: saveSlider
    width: 145
    height: 30

    property int saveMaxIndex: 100
    property int saveMinIndex: 0
    property int saveQualityIndex: saveMaxIndex
    property int savePictureQuality: saveMaxIndex
    property color labelColor: "grey"
    signal saveQualityValueChanged

    Text {
        id: leftLabel
        width: 8
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 5
        font.pixelSize: 12
        color: saveSlider.labelColor
        text: dsTr("Low")
    }
    SaveSlider {
        id: save_picture_quality_slider
        height: 12

        anchors.fill: parent
        anchors.leftMargin: leftLabel.width + 3
        anchors.rightMargin: rightLabel.width + 10
        min: saveMinIndex
        max: saveMaxIndex
        completeColorVisible: true
        init: saveQualityIndex
        valueDisplayVisible: false
        onValueConfirmed:{
            saveSlider.savePictureQuality = save_picture_quality_slider.value
            saveQualityValueChanged()
        }
    }
    Text {
        id: rightLabel
        width: 8
        anchors.right: parent.right
        anchors.rightMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 5
        font.pixelSize: 12
        color: saveSlider.labelColor
        text: dsTr("High")
    }
}
