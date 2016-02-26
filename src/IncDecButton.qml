/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
import QtQuick 2.2

MouseArea {
    width: img.implicitWidth
    height: img.implicitHeight
    hoverEnabled: true
    state: "normal"

    property string type: "+"

    states: [
        State {
            name: "normal"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_normal.png".arg(type)
            }
        },
        State {
            name: "hover"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_hover.png".arg(type)
            }
        },
        State {
            name: "pressed"
            PropertyChanges {
                target: img
                source: "../image/widgets/%1_press.png".arg(type)
            }
        }
    ]

    onEntered: state = "hover"
    onExited: state = "normal"
    onPressed: state = "pressed"
    onReleased: state = "hover"

    Image { id: img }
}