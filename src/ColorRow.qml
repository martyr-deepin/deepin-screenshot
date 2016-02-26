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
    id:colorChange
    anchors.left: row.left
    anchors.leftMargin: 4
    anchors.top: row.bottom
    anchors.topMargin: 8
    visible: false
    spacing: 5
    property var colorOrder: 3
    property var colorStyle: screen.colorCard(colorOrder)
    onColorOrderChanged: {
        colorStyle = screen.colorCard(colorOrder)
    }
    function sponse(id) {
        colorChange.colorOrder = id.colorOrder
    }
    ColorButton{
        id: black
        colorOrder: 0
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(black)}
    }
    ColorButton{
        id: gray_dark
        colorOrder: 1
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(gray_dark) }
    }
    ColorButton{
        id: red
        colorOrder: 2
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(red) }
    }
    ColorButton{
        id: yellow_dark
        colorOrder: 3
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(yellow_dark) }
    }
    ColorButton{
        id: yellow
        colorOrder: 4
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(yellow) }
    }
    ColorButton{
        id: green
        colorOrder: 5
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(green) }
    }
    ColorButton{
        id: green_dark
        colorOrder: 6
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(green_dark) }
    }
    ColorButton{
        id: wathet_dark
        colorOrder: 7
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(wathet_dark) }
    }
    ColorButton{
        id: white
        colorOrder: 8
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(white) }
    }

    ColorButton{
        id: gray
        colorOrder: 9
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(gray) }
    }

    ColorButton{
        id: red_dark
        colorOrder: 10
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(red_dark) }
    }
    ColorButton{
        id: pink
        colorOrder: 11
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(pink) }
    }
    ColorButton{
        id: pink_dark
        colorOrder: 12
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(pink_dark) }
    }
    ColorButton{
        id: blue_dark
        colorOrder: 13
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(blue_dark) }
    }
    ColorButton{
        id: blue
        colorOrder: 14
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(blue) }
    }
    ColorButton{
        id: wathet
        colorOrder: 15
        colorStyle: screen.colorCard(colorOrder)
        onClicked: { sponse(wathet) }
    }
}
