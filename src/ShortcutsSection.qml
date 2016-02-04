/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
import QtQuick 2.1

Column {
    id: column
    width: 300
    property alias title: t_title.text

    Text {
        id: t_title
        color: "white"
        text: column.title
        font.bold: true
        font.pixelSize: 18
    }

    Item { width: parent.width; height: 10 }
}