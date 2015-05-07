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
    Row {
        anchors.fill: parent
        anchors.margins: 8
        Text {
            id: leftLabel
            font.pixelSize: 12
            color: saveSlider.labelColor
            text: dsTr("low")
        }
        SaveSlider {
            id: save_picture_quality_slider
            height: 12

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
            font.pixelSize: 12
            color: saveSlider.labelColor
            text: dsTr("high")
        }
    }
}
