/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
import QtQuick 2.1

Rectangle {
    id: colorButton
    width: 12
    height: 12
    color: colorButton.colorStyle
    property int colorOrder: 3
    property string colorStyle: "red"
    signal clicked()
    Rectangle {
        id: selectArea
        color: "transparent"
        border.width: 1
        border.color: Qt.rgba(1,1,1,0.3)

        anchors.fill: parent
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onEntered: {
            selectArea.border.color = Qt.rgba(1,1,1,0.7)
        }
        onExited: {
            selectArea.border.color = Qt.rgba(1,1,1,0.3)
        }

        onClicked:{
            selectArea.border.color = Qt.rgba(1,1,1,1)
            colorButton.clicked()
        }
    }
}
