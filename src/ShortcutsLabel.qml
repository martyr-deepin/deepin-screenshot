/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
import QtQuick 2.1

Row {
    width: 250
    height: 30

    property alias title: t_title.text
    property string shortcut: ""

    Text {
        id: t_title
        width: parent.width - t_shortcut.width
        color: "white"
        font.pixelSize: 14

        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: t_shortcut
        width: 80
        color: "white"
        text: parent.shortcut || dsTr("None")
        font.pixelSize: 14

        anchors.verticalCenter: parent.verticalCenter
    }
}