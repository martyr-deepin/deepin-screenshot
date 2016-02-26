/**
 * Copyright (C) 2015 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/
import QtQuick 2.2
import QtQuick.Window 2.1
import Deepin.Locale 1.0

Window {
    id: osd_window
    x: (Screen.desktopAvailableWidth - width) / 2
    y: (Screen.desktopAvailableHeight - height) / 2
    width: 160
    height: 160
    color: "transparent"
    visible: false
    flags: Qt.X11BypassWindowManagerHint

    signal closed()

    DLocale { id: locale; domain: "deepin-screenshot" }

    function dsTr(src) { return locale.dsTr(src) }

    function showTips() { show_timer.restart() }

    Timer {
        id: show_timer
        interval: 500

        onTriggered: {
            osd_window.show()
            content.opacity = 1
            hide_timer.start()
        }
    }

    Timer {
        id: hide_timer
        interval: 2500

        onTriggered: {
            osd_window.close()
            content.opacity = 0
            osd_window.closed()
        }
    }

    Rectangle {
        id: content
        radius: 16
        color: Qt.rgba(0, 0, 0, 0.8)
        anchors.fill: parent

        Behavior on opacity {
            SmoothedAnimation {
                duration: 500
            }
        }

        Text {
            y: parent.height / 4
            text: dsTr("Tips")
            color: Qt.rgba(1, 1, 1, 0.8)
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            y: parent.height / 2
            width: parent.width - 2 * 10
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            color: Qt.rgba(1, 1, 1, 0.8)
            text: dsTr('You can use "Ctrl+Alt+A" to start the screenshot')
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
