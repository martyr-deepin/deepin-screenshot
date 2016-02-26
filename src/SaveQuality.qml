/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
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

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 6
        font.pixelSize: 12
        color: saveSlider.labelColor
        text: dsTr("Low")
    }
    SaveSlider {
        id: save_picture_quality_slider
        height: 12

        anchors.fill: parent
        anchors.leftMargin: leftLabel.width
        anchors.rightMargin: rightLabel.width + 2
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

        height: parent.height
        anchors.right: parent.right
        anchors.rightMargin: 3
        anchors.top: parent.top
        anchors.topMargin: 6
        font.pixelSize: 12
        color: saveSlider.labelColor
        text: dsTr("High")
    }
}
