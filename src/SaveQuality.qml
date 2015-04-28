/****************************************************************************
**
**  Copyright (C) 2014 ~ 2016 Deepin, Inc.
**                2014 ~ 2016 penghui
**
**  Author:     penghui<penghuilater@gmail.com>
**  Maintainer: penghui<penghuilater@gmail.com>
**
**  This program is free software: you can redistribute it and/or modify
**  it under the terms of the GNU General Public License as published by
**  the Free Software Foundation, either version 3 of the License, or
**  any later version.
**
**  This program is distributed in the hope that it will be useful,
**  but WITHOUT ANY WARRANTY; without even the implied warranty of
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**  GNU General Public License for more details.
**
**  You should have received a copy of the GNU General Public License
**  along with this program.  If not, see <http://www.gnu.org/licenses/>.
**
****************************************************************************/

import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import Deepin.Widgets 1.0

Item {
    id: saveSlider
    width: 130
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
            text: "低"
        }
        SaveSlider {
            id: save_picture_quality_slider
            min: saveMinIndex
            max: saveMaxIndex
            completeColorVisible: true
            init: saveQualityIndex
            height: 12
            onValueConfirmed:{
                saveSlider.savePictureQuality = save_picture_quality_slider.value
                saveQualityValueChanged()
            }
        }
        Text {
            id: rightLabel
            font.pixelSize: 12
            color: saveSlider.labelColor
            text: "高"
        }
    }
}
